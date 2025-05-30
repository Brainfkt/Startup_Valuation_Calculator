"""
PDF Generator Module
Creates comprehensive PDF reports for valuation calculations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Any
import json
import tempfile
import os

class PDFGenerator:
    """Generate comprehensive PDF reports for startup valuations"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.darkgreen,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            leftIndent=20,
            fontName='Helvetica-Oblique'
        ))
    
    def create_report(self, current_results: Dict, calculation_history: List[Dict]) -> BytesIO:
        """
        Create comprehensive PDF report
        
        Args:
            current_results: Current calculation results
            calculation_history: List of previous calculations
        
        Returns:
            BytesIO buffer containing PDF data
        """
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Title page
            self._add_title_page(story)
            
            # Executive summary
            if current_results:
                self._add_executive_summary(story, current_results)
            
            # Detailed analysis
            if current_results:
                self._add_detailed_analysis(story, current_results)
            
            # Calculation history
            if calculation_history:
                self._add_calculation_history(story, calculation_history)
            
            # Appendices
            self._add_appendices(story)
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            # Return error PDF
            return self._create_error_pdf(str(e))
    
    def _add_title_page(self, story: List):
        """Add title page to the report"""
        story.append(Spacer(1, 2*inch))
        
        story.append(Paragraph("Startup Valuation Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        story.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 1*inch))
        
        # Company placeholder
        story.append(Paragraph("Company: _________________________", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("Prepared by: _____________________", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("Date: ____________________________", self.styles['Normal']))
        
        story.append(PageBreak())
    
    def _add_executive_summary(self, story: List, current_results: Dict):
        """Add executive summary section"""
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        method = current_results.get('method', 'Unknown')
        result = current_results.get('result', {})
        valuation = result.get('valuation', 0)
        
        story.append(Paragraph(
            f"This report presents a startup valuation analysis using the <b>{method}</b> method.",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Key findings table
        key_data = [
            ['Valuation Method', method],
            ['Calculated Valuation', self._format_currency(valuation)],
            ['Analysis Date', datetime.now().strftime('%B %d, %Y')],
            ['Report Status', 'Final']
        ]
        
        key_table = Table(key_data, colWidths=[2.5*inch, 3*inch])
        key_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(key_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Method-specific summary
        self._add_method_summary(story, method, result)
        
    def _add_method_summary(self, story: List, method: str, result: Dict):
        """Add method-specific summary"""
        if method == "DCF":
            operating_value = result.get('operating_value', 0)
            terminal_value = result.get('terminal_pv', 0)
            
            story.append(Paragraph(
                f"The DCF analysis shows an operating value of <b>{self._format_currency(operating_value)}</b> "
                f"and a terminal value of <b>{self._format_currency(terminal_value)}</b>.",
                self.styles['Normal']
            ))
            
        elif method == "Market Multiples":
            multiple = result.get('multiple', 0)
            metric_type = result.get('metric_type', 'Revenue')
            
            story.append(Paragraph(
                f"The market multiples analysis applies a <b>{multiple:.1f}x</b> {metric_type.lower()} "
                f"multiple based on industry comparables.",
                self.styles['Normal']
            ))
            
        elif method == "Berkus":
            max_possible = result.get('max_possible', 0)
            achievement_rate = (result.get('valuation', 0) / max_possible * 100) if max_possible > 0 else 0
            
            story.append(Paragraph(
                f"The Berkus method evaluation shows an achievement rate of <b>{achievement_rate:.1f}%</b> "
                f"of the maximum possible valuation.",
                self.styles['Normal']
            ))
    
    def _add_detailed_analysis(self, story: List, current_results: Dict):
        """Add detailed analysis section"""
        story.append(PageBreak())
        story.append(Paragraph("Detailed Analysis", self.styles['SectionHeader']))
        
        method = current_results.get('method', 'Unknown')
        result = current_results.get('result', {})
        
        if method == "DCF":
            self._add_dcf_analysis(story, result)
        elif method == "Market Multiples":
            self._add_multiples_analysis(story, result, current_results)
        elif method == "Scorecard":
            self._add_scorecard_analysis(story, result)
        elif method == "Berkus":
            self._add_berkus_analysis(story, result)
        elif method == "Risk Factor Summation":
            self._add_risk_analysis(story, result)
        elif method == "Venture Capital":
            self._add_vc_analysis(story, result, current_results)
    
    def _add_dcf_analysis(self, story: List, result: Dict):
        """Add DCF-specific analysis"""
        story.append(Paragraph("DCF Valuation Components", self.styles['Heading3']))
        
        # Components table
        components = [
            ['Component', 'Value', 'Percentage'],
            ['Operating Value', self._format_currency(result.get('operating_value', 0)), ''],
            ['Terminal Value (PV)', self._format_currency(result.get('terminal_pv', 0)), ''],
            ['Total Valuation', self._format_currency(result.get('valuation', 0)), '100%']
        ]
        
        # Calculate percentages
        total_val = result.get('valuation', 0)
        if total_val > 0:
            components[1][2] = f"{(result.get('operating_value', 0) / total_val * 100):.1f}%"
            components[2][2] = f"{(result.get('terminal_pv', 0) / total_val * 100):.1f}%"
        
        comp_table = Table(components, colWidths=[2*inch, 2*inch, 1.5*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(comp_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Assumptions
        story.append(Paragraph("Key Assumptions", self.styles['Heading3']))
        story.append(Paragraph(
            f"• Discount Rate: {result.get('discount_rate', 0)*100:.1f}%",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            f"• Terminal Growth Rate: {result.get('terminal_growth', 0)*100:.1f}%",
            self.styles['Normal']
        ))
    
    def _add_multiples_analysis(self, story: List, result: Dict, current_results: Dict):
        """Add market multiples analysis"""
        story.append(Paragraph("Market Multiples Analysis", self.styles['Heading3']))
        
        sector = current_results.get('sector', 'Unknown')
        
        story.append(Paragraph(f"Industry Sector: <b>{sector}</b>", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        calc_data = [
            ['Metric', 'Value'],
            [f"{result.get('metric_type', 'Revenue')}", self._format_currency(result.get('metric', 0))],
            ['Multiple Applied', f"{result.get('multiple', 0):.1f}x"],
            ['Calculated Valuation', self._format_currency(result.get('valuation', 0))]
        ]
        
        calc_table = Table(calc_data, colWidths=[2.5*inch, 2.5*inch])
        calc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(calc_table)
    
    def _add_scorecard_analysis(self, story: List, result: Dict):
        """Add scorecard method analysis"""
        story.append(Paragraph("Scorecard Method Analysis", self.styles['Heading3']))
        
        # Criteria analysis table
        criteria_data = [['Criterion', 'Score', 'Weight', 'Contribution']]
        
        criteria_analysis = result.get('criteria_analysis', {})
        for criterion, data in criteria_analysis.items():
            criteria_data.append([
                criterion.title(),
                f"{data['score']}/5",
                f"{data['weight']:.1%}",
                f"{data['contribution']:.3f}"
            ])
        
        criteria_table = Table(criteria_data, colWidths=[2*inch, 1*inch, 1*inch, 1.5*inch])
        criteria_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(criteria_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        story.append(Paragraph(
            f"Base Valuation: <b>{self._format_currency(result.get('base_valuation', 0))}</b>",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            f"Adjustment Factor: <b>{result.get('adjustment_factor', 0):.2f}x</b>",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            f"Adjusted Valuation: <b>{self._format_currency(result.get('valuation', 0))}</b>",
            self.styles['Normal']
        ))
    
    def _add_berkus_analysis(self, story: List, result: Dict):
        """Add Berkus method analysis"""
        story.append(Paragraph("Berkus Method Analysis", self.styles['Heading3']))
        
        # Breakdown table
        breakdown_data = [['Criterion', 'Score', 'Value Assigned']]
        
        breakdown = result.get('breakdown', {})
        for criterion, data in breakdown.items():
            breakdown_data.append([
                data['name'],
                f"{data['score']}/5",
                self._format_currency(data['value'])
            ])
        
        breakdown_table = Table(breakdown_data, colWidths=[3*inch, 1*inch, 1.5*inch])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(breakdown_table)
    
    def _add_risk_analysis(self, story: List, result: Dict):
        """Add risk factor analysis"""
        story.append(Paragraph("Risk Factor Analysis", self.styles['Heading3']))
        
        # Risk factors table
        risk_data = [['Risk Factor', 'Rating', 'Adjustment']]
        
        risk_analysis = result.get('risk_analysis', {})
        for factor, data in risk_analysis.items():
            risk_data.append([
                data['name'],
                f"{data['rating']:+d}",
                f"{data['adjustment']:+.1%}"
            ])
        
        risk_table = Table(risk_data, colWidths=[3*inch, 1*inch, 1.5*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(risk_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        story.append(Paragraph(
            f"Total Risk Adjustment: <b>{result.get('total_adjustment', 0):+.1%}</b>",
            self.styles['Normal']
        ))
    
    def _add_vc_analysis(self, story: List, result: Dict, current_results: Dict):
        """Add VC method analysis"""
        story.append(Paragraph("Venture Capital Method Analysis", self.styles['Heading3']))
        
        include_investment = current_results.get('include_investment', False)
        
        if include_investment and 'pre_money_valuation' in result:
            # Investment structure
            invest_data = [
                ['Component', 'Value'],
                ['Pre-Money Valuation', self._format_currency(result.get('pre_money_valuation', 0))],
                ['Investment Amount', self._format_currency(result.get('investment_needed', 0))],
                ['Post-Money Valuation', self._format_currency(result.get('post_money_valuation', 0))],
                ['Investor Ownership', f"{result.get('ownership_percentage', 0):.1%}"]
            ]
        else:
            # Returns analysis
            invest_data = [
                ['Component', 'Value'],
                ['Current Valuation', self._format_currency(result.get('present_value', 0))],
                ['Exit Value', self._format_currency(result.get('exit_value', 0))],
                ['Return Multiple', f"{result.get('expected_return_multiple', 0):.1f}x"],
                ['Annualized Return', f"{result.get('annualized_return', 0):.1%}"]
            ]
        
        invest_table = Table(invest_data, colWidths=[2.5*inch, 2.5*inch])
        invest_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(invest_table)
    
    def _add_calculation_history(self, story: List, calculation_history: List[Dict]):
        """Add calculation history section"""
        story.append(PageBreak())
        story.append(Paragraph("Calculation History", self.styles['SectionHeader']))
        
        if not calculation_history:
            story.append(Paragraph("No previous calculations available.", self.styles['Normal']))
            return
        
        # History table
        history_data = [['Date', 'Method', 'Valuation']]
        
        for calc in calculation_history[-10:]:  # Last 10 calculations
            history_data.append([
                calc.get('timestamp', 'Unknown'),
                calc.get('method', 'Unknown'),
                self._format_currency(calc.get('valuation', 0))
            ])
        
        history_table = Table(history_data, colWidths=[2*inch, 2*inch, 2*inch])
        history_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(history_table)
    
    def _add_appendices(self, story: List):
        """Add appendices section"""
        story.append(PageBreak())
        story.append(Paragraph("Appendices", self.styles['SectionHeader']))
        
        # Disclaimer
        story.append(Paragraph("Important Disclaimers", self.styles['Heading3']))
        story.append(Paragraph(
            "This valuation report is for informational purposes only and should not be considered "
            "as investment advice. The calculations are based on assumptions and inputs provided "
            "and may not reflect actual market conditions or future performance.",
            self.styles['Warning']
        ))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Methodology notes
        story.append(Paragraph("Methodology Notes", self.styles['Heading3']))
        story.append(Paragraph(
            "• DCF valuations are sensitive to discount rate and growth assumptions\n"
            "• Market multiples depend on the availability of comparable companies\n"
            "• Scorecard and Berkus methods involve subjective scoring\n"
            "• Risk assessments should be regularly updated\n"
            "• VC method assumes specific exit scenarios",
            self.styles['Normal']
        ))
    
    def _format_currency(self, amount: float) -> str:
        """Format currency values"""
        if amount >= 1000000:
            return f"€{amount/1000000:.1f}M"
        elif amount >= 1000:
            return f"€{amount/1000:.0f}K"
        else:
            return f"€{amount:,.0f}"
    
    def _create_error_pdf(self, error_message: str) -> BytesIO:
        """Create error PDF when report generation fails"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        story.append(Paragraph("PDF Generation Error", self.styles['Title']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Error: {error_message}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            "Please try again or contact support if the problem persists.",
            self.styles['Normal']
        ))
        
        doc.build(story)
        buffer.seek(0)
        
        return buffer
