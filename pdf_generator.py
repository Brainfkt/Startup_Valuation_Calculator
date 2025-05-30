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
from reportlab.graphics.shapes import Drawing, Circle, Rect, String, Line, Polygon
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Any, Optional
import json
import math
import matplotlib.ticker as ticker
from pdf_chart_generator import PDFChartGenerator

class PDFGenerator:
    """Generate comprehensive PDF reports for startup valuations"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        self.chart_generator = PDFChartGenerator()
    
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
        Create comprehensive PDF report with charts from calculation history
        
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
            
            # Executive summary with all calculations
            if calculation_history:
                self._add_comprehensive_summary(story, calculation_history)
            
            # Detailed analysis for all calculations with charts
            if calculation_history:
                self._add_detailed_analysis_with_charts(story, calculation_history)
            
            # Comparative analysis
            if len(calculation_history) > 1:
                self._add_comparative_analysis(story, calculation_history)
            
            # Appendices
            self._add_appendices(story)
            
            # Charts Appendix - All charts from the application
            if calculation_history:
                self._add_charts_appendix(story, calculation_history)
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            # Return error PDF
            return self._create_error_pdf(str(e))
        finally:
            # Clean up temporary chart files
            self.chart_generator.cleanup_temp_files()
    
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
        """Add DCF-specific analysis with visual chart"""
        story.append(Paragraph("DCF Valuation Components", self.styles['Heading3']))
        
        # Components table
        operating_value = result.get('operating_value', 0)
        terminal_pv = result.get('terminal_pv', 0)
        total_value = operating_value + terminal_pv
        
        op_percentage = (operating_value / total_value * 100) if total_value > 0 else 0
        term_percentage = (terminal_pv / total_value * 100) if total_value > 0 else 0
        
        components = [
            ['Component', 'Value', 'Percentage'],
            ['Operating Value', self._format_currency(operating_value), f'{op_percentage:.1f}%'],
            ['Terminal Value (PV)', self._format_currency(terminal_pv), f'{term_percentage:.1f}%'],
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
        story.append(Spacer(1, 0.2*inch))
        
        # Add DCF chart
        try:
            chart_data = {
                'result': result,
                'inputs': {},
                'method': 'DCF'
            }
            chart_path = self.chart_generator.create_dcf_chart(chart_data)
            if chart_path:
                chart_image = self.chart_generator.create_reportlab_image(
                    chart_path, width=6*inch, height=3.5*inch
                )
                story.append(chart_image)
                story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            # Continue without chart if generation fails
            pass
        
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
        story.append(Spacer(1, 0.2*inch))
        
        # Add Berkus chart
        try:
            chart_data = {
                'result': result,
                'inputs': {},
                'method': 'Berkus'
            }
            chart_path = self.chart_generator.create_berkus_chart(chart_data)
            if chart_path:
                chart_image = self.chart_generator.create_reportlab_image(
                    chart_path, width=6*inch, height=3.5*inch
                )
                story.append(chart_image)
                story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            # Continue without chart if generation fails
            pass
    
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
    
    def _add_charts_appendix(self, story: List, calculation_history: List[Dict]):
        """Add charts appendix with each valuation method on its own page"""
        story.append(PageBreak())
        story.append(Paragraph("Appendix A: Visual Charts", self.styles['SectionHeader']))
        story.append(Paragraph(
            "This appendix contains the visual charts for each valuation method, "
            "presented in the order they were calculated.",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        for i, calc in enumerate(calculation_history):
            # Page break before each method (except the first one)
            if i > 0:
                story.append(PageBreak())
            
            method = calc.get('method', 'Unknown')
            result = calc.get('result', {})
            timestamp = calc.get('timestamp', 'Unknown')
            valuation = result.get('valuation', 0)
            
            # Method header with key information
            story.append(Paragraph(f"{method} Method", self.styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            
            # Summary information
            story.append(Paragraph(f"Date: {timestamp}", self.styles['Normal']))
            story.append(Paragraph(f"Valuation: {self._format_currency(valuation)}", self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Generate and add chart
            try:
                chart_data = {
                    'result': result,
                    'inputs': calc.get('inputs', {}),
                    'method': method
                }
                
                chart_path = None
                if method == "DCF":
                    chart_path = self.chart_generator.create_dcf_chart(chart_data)
                elif method == "Market Multiples":
                    chart_path = self.chart_generator.create_multiples_chart(chart_data)
                elif method == "Scorecard":
                    chart_path = self.chart_generator.create_scorecard_chart(chart_data)
                elif method == "Berkus":
                    chart_path = self.chart_generator.create_berkus_chart(chart_data)
                elif method == "Risk Factor Summation":
                    chart_path = self._create_risk_factor_visual_chart(result)
                elif method == "Venture Capital":
                    chart_path = self._create_vc_method_visual_chart(result)
                
                if chart_path:
                    # Add chart with larger size for single-page display
                    chart_image = self.chart_generator.create_reportlab_image(
                        chart_path, width=6.5*inch, height=4.5*inch
                    )
                    story.append(chart_image)
                    story.append(Spacer(1, 0.3*inch))
                    
                    # Add key insights or interpretation
                    self._add_chart_interpretation(story, method, result)
                else:
                    story.append(Paragraph(
                        f"Chart visualization not available for {method} method.",
                        self.styles['Normal']
                    ))
                    
            except Exception as e:
                story.append(Paragraph(
                    f"Error generating chart for {method} method.",
                    self.styles['Normal']
                ))
    
    def _add_chart_interpretation(self, story: List, method: str, result: Dict):
        """Add interpretation and key insights for each chart"""
        story.append(Paragraph("Key Insights:", self.styles['Heading3']))
        
        if method == "DCF":
            operating_value = result.get('operating_value', 0)
            terminal_pv = result.get('terminal_pv', 0)
            total_value = operating_value + terminal_pv
            
            if total_value > 0:
                op_percentage = (operating_value / total_value * 100)
                term_percentage = (terminal_pv / total_value * 100)
                
                story.append(Paragraph(
                    f"• Operating cash flows contribute {op_percentage:.1f}% of total valuation",
                    self.styles['Normal']
                ))
                story.append(Paragraph(
                    f"• Terminal value represents {term_percentage:.1f}% of total valuation",
                    self.styles['Normal']
                ))
                
        elif method == "Market Multiples":
            multiple = result.get('multiple', 0)
            metric_type = result.get('metric_type', 'Revenue')
            story.append(Paragraph(
                f"• Applied {multiple:.1f}x {metric_type.lower()} multiple based on industry comparables",
                self.styles['Normal']
            ))
            
        elif method == "Scorecard":
            adjustment_factor = result.get('adjustment_factor', 0)
            story.append(Paragraph(
                f"• Overall adjustment factor: {adjustment_factor:.2f}x relative to base valuation",
                self.styles['Normal']
            ))
            
        elif method == "Berkus":
            max_possible = result.get('max_possible', 0)
            achievement_rate = (result.get('valuation', 0) / max_possible * 100) if max_possible > 0 else 0
            story.append(Paragraph(
                f"• Achievement rate: {achievement_rate:.1f}% of maximum possible valuation",
                self.styles['Normal']
            ))
            
        elif method == "Risk Factor Summation":
            total_adjustment = result.get('total_adjustment', 0)
            story.append(Paragraph(
                f"• Net risk adjustment: {total_adjustment:+.1%} applied to base valuation",
                self.styles['Normal']
            ))
            
        elif method == "Venture Capital":
            return_multiple = result.get('return_multiple', 0)
            story.append(Paragraph(
                f"• Required return multiple: {return_multiple:.1f}x over investment period",
                self.styles['Normal']
            ))
        
        story.append(Spacer(1, 0.2*inch))
    
    def _create_risk_factor_visual_chart(self, result: Dict) -> Optional[str]:
        """Create a simple risk factor visualization"""
        try:
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('white')
            
            risk_analysis = result.get('risk_analysis', {})
            if not risk_analysis:
                ax.text(0.5, 0.5, 'No Risk Factors Applied', 
                       ha='center', va='center', fontsize=14)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
            else:
                factors = list(risk_analysis.keys())
                adjustments = [data.get('adjustment', 0) * 100 for data in risk_analysis.values()]
                
                bars = ax.barh(factors, adjustments)
                ax.set_xlabel('Risk Adjustment (%)')
                ax.set_title('Risk Factor Analysis')
                ax.grid(True, alpha=0.3)
                
                # Color bars based on positive/negative
                for bar, adj in zip(bars, adjustments):
                    if adj > 0:
                        bar.set_color('red')
                    elif adj < 0:
                        bar.set_color('green')
                    else:
                        bar.set_color('gray')
            
            plt.tight_layout()
            return self.chart_generator._save_chart_to_temp(fig)
            
        except Exception:
            return None
    
    def _create_vc_method_visual_chart(self, result: Dict) -> Optional[str]:
        """Create a simple VC method visualization"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.ticker as ticker
            
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('white')
            
            exit_value = result.get('exit_value', 0)
            present_value = result.get('present_value', 0)
            
            if exit_value > 0 and present_value > 0:
                categories = ['Present Value', 'Exit Value']
                values = [present_value, exit_value]
                
                bars = ax.bar(categories, values)
                ax.set_ylabel('Value (€)')
                ax.set_title('VC Method - Present vs Exit Value')
                ax.grid(True, alpha=0.3)
                
                # Format y-axis
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'€{x/1000000:.1f}M'))
                
                # Add value labels
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'€{value/1000000:.1f}M', ha='center', va='bottom')
            else:
                ax.text(0.5, 0.5, 'Insufficient VC Method Data', 
                       ha='center', va='center', fontsize=14)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
            
            plt.tight_layout()
            return self.chart_generator._save_chart_to_temp(fig)
            
        except Exception:
            return None

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
    
    def _add_comprehensive_summary(self, story: List, calculation_history: List[Dict]):
        """Add comprehensive summary of all calculations"""
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        story.append(Paragraph(
            f"This report presents a comprehensive startup valuation analysis using {len(calculation_history)} "
            f"different calculation{'s' if len(calculation_history) > 1 else ''} performed between "
            f"{calculation_history[0]['timestamp']} and {calculation_history[-1]['timestamp']}.",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Summary table of all calculations
        summary_data = [['Method', 'Date', 'Valuation']]
        valuations = []
        
        for calc in calculation_history:
            summary_data.append([
                calc['method'],
                calc['timestamp'],
                self._format_currency(calc['valuation'])
            ])
            valuations.append(calc['valuation'])
        
        # Add statistics row
        if valuations:
            avg_valuation = sum(valuations) / len(valuations)
            min_valuation = min(valuations)
            max_valuation = max(valuations)
            
            summary_data.append(['', '', ''])  # Empty row
            summary_data.append(['Average', '', self._format_currency(avg_valuation)])
            summary_data.append(['Range', '', f"{self._format_currency(min_valuation)} - {self._format_currency(max_valuation)}"])
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -4), colors.beige),
            ('BACKGROUND', (0, -3), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))

    def _add_detailed_analysis_with_charts(self, story: List, calculation_history: List[Dict]):
        """Add detailed analysis for each calculation with chart data tables"""
        story.append(PageBreak())
        story.append(Paragraph("Detailed Analysis", self.styles['SectionHeader']))
        
        for i, calc in enumerate(calculation_history):
            story.append(Paragraph(f"{calc['method']} Analysis", self.styles['Heading3']))
            story.append(Paragraph(f"Performed on: {calc['timestamp']}", self.styles['Normal']))
            story.append(Paragraph(f"Valuation: {self._format_currency(calc['valuation'])}", self.styles['MetricValue']))
            story.append(Spacer(1, 0.2*inch))
            
            # Add chart data table if available
            self._add_chart_data_table(story, calc)
            
            # Method-specific details
            if calc['method'] == "DCF":
                self._add_dcf_analysis(story, calc['result'])
            elif calc['method'] == "Market Multiples":
                self._add_multiples_analysis(story, calc['result'], calc)
            elif calc['method'] == "Scorecard":
                self._add_scorecard_analysis(story, calc['result'])
            elif calc['method'] == "Berkus":
                self._add_berkus_analysis(story, calc['result'])
            elif calc['method'] == "Risk Factor Summation":
                self._add_risk_analysis(story, calc['result'])
            elif calc['method'] == "Venture Capital":
                self._add_vc_analysis(story, calc['result'], calc)
            
            if i < len(calculation_history) - 1:
                story.append(Spacer(1, 0.3*inch))

    def _add_comparative_analysis(self, story: List, calculation_history: List[Dict]):
        """Add comparative analysis section"""
        story.append(PageBreak())
        story.append(Paragraph("Comparative Analysis", self.styles['SectionHeader']))
        
        valuations = [calc['valuation'] for calc in calculation_history]
        methods = [calc['method'] for calc in calculation_history]
        
        # Valuation range analysis
        min_val = min(valuations)
        max_val = max(valuations)
        avg_val = sum(valuations) / len(valuations)
        
        story.append(Paragraph("Valuation Range Analysis", self.styles['Heading3']))
        
        range_data = [
            ['Metric', 'Value'],
            ['Minimum Valuation', self._format_currency(min_val)],
            ['Maximum Valuation', self._format_currency(max_val)],
            ['Average Valuation', self._format_currency(avg_val)],
            ['Valuation Spread', self._format_currency(max_val - min_val)],
            ['Coefficient of Variation', f"{(max_val - min_val) / avg_val * 100:.1f}%" if avg_val > 0 else "N/A"]
        ]
        
        range_table = Table(range_data, colWidths=[2.5*inch, 2.5*inch])
        range_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(range_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Method recommendations
        story.append(Paragraph("Method Recommendations", self.styles['Heading3']))
        
        if 'DCF' in methods:
            story.append(Paragraph(
                "• DCF Method: Most suitable for companies with predictable cash flows and established business models.",
                self.styles['Normal']
            ))
        
        if 'Berkus' in methods:
            story.append(Paragraph(
                "• Berkus Method: Ideal for pre-revenue startups, focusing on risk reduction factors.",
                self.styles['Normal']
            ))
        
        if 'Market Multiples' in methods:
            story.append(Paragraph(
                "• Market Multiples: Provides market-based perspective, best used with comparable companies.",
                self.styles['Normal']
            ))

    def _add_chart_data_table(self, story: List, calc: Dict):
        """Add Plotly charts as images and data tables"""
        story.append(Paragraph("Visual Analysis", self.styles['Heading4']))
        
        method = calc['method']
        result = calc['result']
        
        # Generate and add Plotly chart as image
        chart_image = self._generate_plotly_chart_image(calc)
        if chart_image:
            story.append(chart_image)
            story.append(Spacer(1, 0.1*inch))
        
        # Add styled data tables
        if method == "DCF":
            self._add_dcf_chart_data(story, calc)
        elif method == "Market Multiples":
            self._add_multiples_chart_data(story, calc)
        elif method == "Scorecard":
            self._add_scorecard_chart_data(story, calc)
        elif method == "Berkus":
            self._add_berkus_chart_data(story, calc)
        elif method == "Risk Factor Summation":
            self._add_risk_chart_data(story, calc)
        elif method == "Venture Capital":
            self._add_vc_chart_data(story, calc)
        
        story.append(Spacer(1, 0.2*inch))

    def _add_dcf_chart_data(self, story: List, calc: Dict):
        """Add DCF chart data table"""
        result = calc['result']
        inputs = calc['inputs']
        
        # Cash flows and present values table
        if 'cash_flows' in inputs and 'discounted_flows' in result:
            cash_flows = inputs['cash_flows']
            discounted_flows = result['discounted_flows']
            
            dcf_data = [['Year', 'Cash Flow', 'Present Value']]
            for i, (cf, pv) in enumerate(zip(cash_flows, discounted_flows)):
                dcf_data.append([f"Year {i+1}", self._format_currency(cf), self._format_currency(pv)])
            
            # Add terminal value row
            dcf_data.append(['Terminal Value', '-', self._format_currency(result.get('terminal_pv', 0))])
            
            dcf_table = Table(dcf_data, colWidths=[1.2*inch, 1.8*inch, 1.8*inch])
            dcf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            
            story.append(dcf_table)

    def _add_multiples_chart_data(self, story: List, calc: Dict):
        """Add market multiples chart data table"""
        result = calc['result']
        inputs = calc['inputs']
        
        # Sector comparison data
        from data_models import SECTOR_MULTIPLES
        
        sector = inputs.get('sector', '')
        metric_type = result.get('metric_type', 'Revenue')
        
        mult_data = [['Sector', f'{metric_type} Multiple', 'Used']]
        for sector_name, multiples in SECTOR_MULTIPLES.items():
            is_used = "✓" if sector_name == sector else ""
            mult_data.append([sector_name, f"{multiples[metric_type]:.1f}x", is_used])
        
        mult_table = Table(mult_data, colWidths=[2.5*inch, 1.2*inch, 0.8*inch])
        mult_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        story.append(mult_table)

    def _add_scorecard_chart_data(self, story: List, calc: Dict):
        """Add scorecard chart data table"""
        result = calc['result']
        criteria_analysis = result.get('criteria_analysis', {})
        
        score_data = [['Criterion', 'Score', 'Weight', 'Contribution']]
        for criterion, data in criteria_analysis.items():
            score_data.append([
                criterion.title(),
                f"{data['score']}/5",
                f"{data['weight']:.1%}",
                f"{data['contribution']:.3f}"
            ])
        
        score_table = Table(score_data, colWidths=[2*inch, 0.8*inch, 0.8*inch, 1*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        story.append(score_table)

    def _add_berkus_chart_data(self, story: List, calc: Dict):
        """Add Berkus chart data table"""
        result = calc['result']
        breakdown = result.get('breakdown', {})
        
        berkus_data = [['Criterion', 'Score', 'Value', 'Max Value']]
        for criterion, data in breakdown.items():
            berkus_data.append([
                data['name'],
                f"{data['score']}/5",
                self._format_currency(data['value']),
                "€500K"
            ])
        
        berkus_table = Table(berkus_data, colWidths=[3*inch, 0.8*inch, 1*inch, 0.8*inch])
        berkus_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1), True)
        ]))
        
        story.append(berkus_table)

    def _add_risk_chart_data(self, story: List, calc: Dict):
        """Add risk factor chart data table"""
        result = calc['result']
        risk_analysis = result.get('risk_analysis', {})
        
        risk_data = [['Risk Factor', 'Rating', 'Adjustment']]
        for factor, data in risk_analysis.items():
            risk_data.append([
                data['name'],
                f"{data['rating']:+d}",
                f"{data['adjustment']:+.1%}"
            ])
        
        risk_table = Table(risk_data, colWidths=[3*inch, 0.8*inch, 1*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1), True)
        ]))
        
        story.append(risk_table)

    def _add_vc_chart_data(self, story: List, calc: Dict):
        """Add VC method chart data table"""
        result = calc['result']
        
        vc_data = [['Metric', 'Value']]
        vc_data.append(['Exit Value', self._format_currency(result.get('exit_value', 0))])
        vc_data.append(['Present Value', self._format_currency(result.get('present_value', 0))])
        vc_data.append(['Return Multiple', f"{result.get('expected_return_multiple', 0):.1f}x"])
        vc_data.append(['Annualized Return', f"{result.get('annualized_return', 0):.1%}"])
        
        if 'ownership_percentage' in result:
            vc_data.append(['Ownership %', f"{result.get('ownership_percentage', 0):.1%}"])
            vc_data.append(['Investment Needed', self._format_currency(result.get('investment_needed', 0))])
        
        vc_table = Table(vc_data, colWidths=[2.2*inch, 2.2*inch])
        vc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        story.append(vc_table)

    def _add_dcf_visual_breakdown(self, story: List, calc: Dict):
        """Add visual breakdown for DCF valuation"""
        result = calc['result']
        
        operating_value = result.get('operating_value', 0)
        terminal_value = result.get('terminal_pv', 0)
        total_value = result.get('valuation', 0)
        
        if total_value > 0:
            operating_pct = (operating_value / total_value) * 100
            terminal_pct = (terminal_value / total_value) * 100
            
            # Create a simple visual breakdown
            story.append(Paragraph("Valuation Composition", self.styles['Heading4']))
            
            composition_data = [
                ['Component', 'Value', 'Percentage', 'Visual'],
                [
                    'Operating Value', 
                    self._format_currency(operating_value), 
                    f"{operating_pct:.1f}%",
                    "█" * int(operating_pct / 5) + "░" * int((100 - operating_pct) / 5)
                ],
                [
                    'Terminal Value', 
                    self._format_currency(terminal_value), 
                    f"{terminal_pct:.1f}%",
                    "█" * int(terminal_pct / 5) + "░" * int((100 - terminal_pct) / 5)
                ]
            ]
            
            comp_table = Table(composition_data, colWidths=[1.5*inch, 1.2*inch, 0.8*inch, 1.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (3, 1), (3, -1), 'Courier')  # Monospace for visual bars
            ]))
            
            story.append(comp_table)

    def _add_dcf_visual_chart(self, story: List, calc: Dict):
        """Add DCF visual breakdown"""
        result = calc['result']
        
        operating_value = result.get('operating_value', 0)
        terminal_value = result.get('terminal_pv', 0)
        total_value = result.get('valuation', 0)
        
        if total_value > 0:
            operating_pct = (operating_value / total_value) * 100
            terminal_pct = (terminal_value / total_value) * 100
            
            # Create simple visual breakdown
            story.append(Paragraph("Value Breakdown", self.styles['Heading4']))
            
            composition_data = [
                ['Component', 'Value', 'Percentage', 'Visual Bar'],
                [
                    'Operating Value', 
                    self._format_currency(operating_value), 
                    f"{operating_pct:.1f}%",
                    "█" * int(operating_pct / 5) + "░" * (20 - int(operating_pct / 5))
                ],
                [
                    'Terminal Value', 
                    self._format_currency(terminal_value), 
                    f"{terminal_pct:.1f}%",
                    "█" * int(terminal_pct / 5) + "░" * (20 - int(terminal_pct / 5))
                ]
            ]
            
            comp_table = Table(composition_data, colWidths=[1.5*inch, 1.2*inch, 0.8*inch, 2*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (3, 1), (3, -1), 'Courier')
            ]))
            
            story.append(comp_table)
            story.append(Spacer(1, 0.1*inch))

    def _add_multiples_visual_chart(self, story: List, calc: Dict):
        """Add market multiples visual comparison"""
        inputs = calc['inputs']
        result = calc['result']
        
        sector = inputs.get('sector', '')
        metric_type = inputs.get('metric_type', 'Revenue')
        used_multiple = inputs.get('multiple', 0)
        
        story.append(Paragraph("Sector Multiple Comparison", self.styles['Heading4']))
        
        # Create visual comparison table
        comparison_data = [
            ['Metric', 'Your Input', 'Industry Range', 'Visual Comparison'],
            [
                f"{metric_type} Multiple",
                f"{used_multiple:.1f}x",
                "2.0x - 8.0x (typical)",
                "█" * min(int(used_multiple), 10) + "░" * (10 - min(int(used_multiple), 10))
            ]
        ]
        
        comp_table = Table(comparison_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 2*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (3, 1), (3, -1), 'Courier')
        ]))
        
        story.append(comp_table)
        story.append(Spacer(1, 0.1*inch))

    def _add_scorecard_visual_chart(self, story: List, calc: Dict):
        """Add scorecard performance visualization"""
        result = calc['result']
        criteria_analysis = result.get('criteria_analysis', {})
        
        story.append(Paragraph("Scorecard Performance", self.styles['Heading4']))
        
        # Create performance visualization table
        perf_data = [['Criteria', 'Score', 'Performance', 'Visual Rating']]
        
        for criteria, analysis in criteria_analysis.items():
            score = analysis.get('score', 0)
            rating_visual = "★" * score + "☆" * (5 - score)
            
            performance = "Excellent" if score >= 4 else "Good" if score >= 3 else "Average" if score >= 2 else "Poor"
            
            perf_data.append([
                analysis.get('name', criteria.title()),
                f"{score}/5",
                performance,
                rating_visual
            ])
        
        perf_table = Table(perf_data, colWidths=[2*inch, 0.7*inch, 1*inch, 1.3*inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        story.append(perf_table)
        story.append(Spacer(1, 0.1*inch))

    def _add_berkus_visual_chart(self, story: List, calc: Dict):
        """Add Berkus method value breakdown"""
        result = calc['result']
        breakdown = result.get('breakdown', {})
        
        story.append(Paragraph("Berkus Value Breakdown", self.styles['Heading4']))
        
        # Create value breakdown table
        berkus_data = [['Criteria', 'Score', 'Max Value', 'Assigned Value', 'Visual Progress']]
        
        for criteria, details in breakdown.items():
            score = details.get('score', 0)
            value = details.get('value', 0)
            max_value = 500000  # Berkus max per criterion
            
            progress_bars = int((value / max_value) * 10) if max_value > 0 else 0
            visual_progress = "█" * progress_bars + "░" * (10 - progress_bars)
            
            berkus_data.append([
                details.get('name', criteria.title()),
                f"{score}/5",
                f"${max_value:,}",
                f"${value:,.0f}",
                visual_progress
            ])
        
        berkus_table = Table(berkus_data, colWidths=[1.8*inch, 0.6*inch, 0.8*inch, 1*inch, 1.3*inch])
        berkus_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (4, 1), (4, -1), 'Courier')
        ]))
        
        story.append(berkus_table)
        story.append(Spacer(1, 0.1*inch))

    def _add_risk_visual_chart(self, story: List, calc: Dict):
        """Add risk factor visualization"""
        result = calc['result']
        risk_analysis = result.get('risk_analysis', {})
        
        story.append(Paragraph("Risk Factor Analysis", self.styles['Heading4']))
        
        # Create risk visualization table
        risk_data = [['Risk Factor', 'Rating', 'Impact', 'Adjustment', 'Visual Impact']]
        
        for risk_name, analysis in risk_analysis.items():
            rating = analysis.get('rating', 0)
            adjustment = analysis.get('adjustment', 0) * 100
            
            # Create visual representation
            if adjustment < 0:
                visual = "▼" * min(abs(int(adjustment/5)), 5) + " " + "░" * (5 - min(abs(int(adjustment/5)), 5))
                impact = "Negative"
            elif adjustment > 0:
                visual = "▲" * min(int(adjustment/5), 5) + " " + "░" * (5 - min(int(adjustment/5), 5))
                impact = "Positive"
            else:
                visual = "◆ " + "░" * 4
                impact = "Neutral"
            
            risk_data.append([
                analysis.get('name', risk_name.title()),
                f"{rating}/5" if 'rating' in analysis else f"{rating:+d}",
                impact,
                f"{adjustment:+.1f}%",
                visual
            ])
        
        risk_table = Table(risk_data, colWidths=[2*inch, 0.7*inch, 0.8*inch, 0.8*inch, 1.2*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (4, 1), (4, -1), 'Courier')
        ]))
        
        story.append(risk_table)
        story.append(Spacer(1, 0.1*inch))

    def _add_vc_visual_chart(self, story: List, calc: Dict):
        """Add VC method visualization"""
        result = calc['result']
        inputs = calc['inputs']
        
        story.append(Paragraph("Venture Capital Analysis", self.styles['Heading4']))
        
        exit_value = result.get('exit_value', 0)
        present_value = result.get('present_value', 0)
        required_return = inputs.get('required_return', 0) * 100
        years_to_exit = inputs.get('years_to_exit', 5)
        
        # Create VC analysis table
        vc_data = [
            ['Metric', 'Value', 'Visual Scale', 'Timeline'],
            [
                'Exit Value',
                self._format_currency(exit_value),
                "█" * min(10, int(exit_value / 1000000)) + "░" * (10 - min(10, int(exit_value / 1000000))),
                f"Year {years_to_exit}"
            ],
            [
                'Present Value',
                self._format_currency(present_value),
                "█" * min(10, int(present_value / 1000000)) + "░" * (10 - min(10, int(present_value / 1000000))),
                "Today"
            ],
            [
                'Required Return',
                f"{required_return:.1f}% annually",
                "█" * min(10, int(required_return / 5)) + "░" * (10 - min(10, int(required_return / 5))),
                f"{years_to_exit} years"
            ]
        ]
        
        vc_table = Table(vc_data, colWidths=[1.5*inch, 1.3*inch, 1.5*inch, 1.2*inch])
        vc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightsteelblue),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (2, 1), (2, -1), 'Courier')
        ]))
        
        story.append(vc_table)
        story.append(Spacer(1, 0.1*inch))

    def _generate_plotly_chart_image(self, calc: Dict):
        """Generate ReportLab chart from stored chart data"""
        try:
            method = calc.get('method', '')
            result = calc.get('result', {})
            chart_data = calc.get('chart_data', None)
            
            # Create ReportLab chart based on method and data
            if method == "DCF":
                return self._create_dcf_reportlab_chart(result, calc.get('inputs', {}))
            elif method == "Market Multiples":
                return self._create_multiples_reportlab_chart(result, calc.get('inputs', {}))
            elif method == "Scorecard":
                return self._create_scorecard_reportlab_chart(result)
            elif method == "Berkus":
                return self._create_berkus_reportlab_chart(result)
            elif method == "Risk Factor Summation":
                return self._create_risk_reportlab_chart(result)
            elif method == "Venture Capital":
                return self._create_vc_reportlab_chart(result, calc.get('inputs', {}))
            else:
                return self._create_placeholder_chart(method)
                
        except Exception as e:
            return self._create_error_chart(f"Chart generation failed: {str(e)}")

    def _create_dcf_reportlab_chart(self, result: Dict, inputs: Dict):
        """Create DCF pie chart using ReportLab"""
        operating_value = result.get('operating_value', 0)
        terminal_value = result.get('terminal_pv', 0)
        
        if operating_value <= 0 and terminal_value <= 0:
            return self._create_placeholder_chart("DCF")
        
        # Create drawing
        d = Drawing(400, 200)
        
        # Create pie chart
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = 120
        pie.height = 120
        
        # Data and labels
        pie.data = [operating_value, terminal_value]
        pie.labels = ['Operating\nValue', 'Terminal\nValue']
        
        # Colors
        pie.slices[0].fillColor = colors.lightblue
        pie.slices[1].fillColor = colors.darkblue
        pie.slices.strokeColor = colors.white
        pie.slices.strokeWidth = 2
        
        # Add legend
        legend = Legend()
        legend.x = 200
        legend.y = 80
        legend.dx = 8
        legend.dy = 8
        legend.fontName = 'Helvetica'
        legend.fontSize = 10
        legend.boxAnchor = 'w'
        legend.columnMaximum = 2
        legend.strokeWidth = 1
        legend.strokeColor = colors.black
        legend.deltax = 75
        legend.deltay = 10
        legend.autoXPadding = 5
        legend.yGap = 0
        legend.dxTextSpace = 5
        legend.alignment = 'right'
        legend.dividerLines = 1|2|4
        legend.dividerOffsY = 4.5
        legend.subCols.rpad = 30
        
        legend.colorNamePairs = [
            (colors.lightblue, f'Operating: {self._format_currency(operating_value)}'),
            (colors.darkblue, f'Terminal: {self._format_currency(terminal_value)}')
        ]
        
        d.add(pie)
        d.add(legend)
        
        return d

    def _create_multiples_reportlab_chart(self, result: Dict, inputs: Dict):
        """Create market multiples bar chart using ReportLab"""
        d = Drawing(400, 200)
        
        # Create bar chart
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.width = 300
        chart.height = 120
        
        metric_value = inputs.get('metric_value', 0)
        multiple = inputs.get('multiple', 0)
        valuation = result.get('valuation', 0)
        
        chart.data = [[metric_value, valuation]]
        chart.categoryAxis.categoryNames = ['Base Metric', 'Valuation']
        chart.categoryAxis.labels.fontSize = 10
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(metric_value, valuation) * 1.1
        
        # Color bars
        chart.bars[0][0].fillColor = colors.lightgreen
        chart.bars[0][1].fillColor = colors.darkgreen
        
        d.add(chart)
        
        # Add title
        d.add(String(200, 180, f"Multiple: {multiple:.1f}x", fontSize=12, textAnchor='middle'))
        
        return d

    def _create_scorecard_reportlab_chart(self, result: Dict):
        """Create scorecard bar chart using ReportLab"""
        criteria_analysis = result.get('criteria_analysis', {})
        
        if not criteria_analysis:
            return self._create_placeholder_chart("Scorecard")
        
        d = Drawing(400, 200)
        
        # Create bar chart
        chart = VerticalBarChart()
        chart.x = 30
        chart.y = 50
        chart.width = 340
        chart.height = 120
        
        criteria_names = list(criteria_analysis.keys())[:6]  # Limit for readability
        scores = [criteria_analysis[c]['score'] for c in criteria_names]
        
        chart.data = [scores]
        chart.categoryAxis.categoryNames = [c.title()[:10] for c in criteria_names]
        chart.categoryAxis.labels.fontSize = 8
        chart.categoryAxis.labels.angle = 45
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = 5
        
        # Color based on score
        for i, score in enumerate(scores):
            if score >= 4:
                chart.bars[0][i].fillColor = colors.green
            elif score >= 3:
                chart.bars[0][i].fillColor = colors.yellow
            else:
                chart.bars[0][i].fillColor = colors.red
        
        d.add(chart)
        d.add(String(200, 180, "Scorecard Performance", fontSize=12, textAnchor='middle'))
        
        return d

    def _create_berkus_reportlab_chart(self, result: Dict):
        """Create Berkus method bar chart using ReportLab"""
        breakdown = result.get('breakdown', {})
        
        if not breakdown:
            return self._create_placeholder_chart("Berkus")
        
        d = Drawing(400, 200)
        
        # Create bar chart
        chart = VerticalBarChart()
        chart.x = 30
        chart.y = 50
        chart.width = 340
        chart.height = 120
        
        values = [breakdown[c]['value'] for c in breakdown.keys()]
        names = [breakdown[c]['name'][:15] for c in breakdown.keys()]
        
        chart.data = [values]
        chart.categoryAxis.categoryNames = names
        chart.categoryAxis.labels.fontSize = 8
        chart.categoryAxis.labels.angle = 45
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(values) * 1.1 if values else 500000
        
        # Color bars
        for i in range(len(values)):
            chart.bars[0][i].fillColor = colors.lightgreen
        
        d.add(chart)
        d.add(String(200, 180, "Berkus Method Breakdown", fontSize=12, textAnchor='middle'))
        
        return d

    def _create_risk_reportlab_chart(self, result: Dict):
        """Create risk factor chart using ReportLab"""
        risk_analysis = result.get('risk_analysis', {})
        
        if not risk_analysis:
            return self._create_placeholder_chart("Risk Factor")
        
        d = Drawing(400, 200)
        
        # Create horizontal bars for risk factors
        y_start = 160
        bar_height = 15
        
        for i, (risk_name, analysis) in enumerate(list(risk_analysis.items())[:6]):
            y_pos = y_start - i * 25
            adjustment = analysis.get('adjustment', 0) * 100
            
            # Draw risk factor name
            d.add(String(20, y_pos, analysis.get('name', risk_name.title())[:20], fontSize=9))
            
            # Draw adjustment bar
            bar_width = abs(adjustment) * 2
            bar_color = colors.red if adjustment < 0 else colors.green
            
            if adjustment < 0:
                d.add(Rect(200 - bar_width, y_pos - 5, bar_width, bar_height, fillColor=bar_color))
            else:
                d.add(Rect(200, y_pos - 5, bar_width, bar_height, fillColor=bar_color))
            
            # Draw percentage
            d.add(String(320, y_pos, f"{adjustment:+.1f}%", fontSize=9))
        
        # Add center line
        d.add(Line(200, 20, 200, 180, strokeColor=colors.black))
        d.add(String(200, 10, "0%", fontSize=8, textAnchor='middle'))
        
        return d

    def _create_vc_reportlab_chart(self, result: Dict, inputs: Dict):
        """Create VC method bar chart using ReportLab"""
        d = Drawing(400, 200)
        
        # Create bar chart
        chart = VerticalBarChart()
        chart.x = 100
        chart.y = 50
        chart.width = 200
        chart.height = 120
        
        exit_value = result.get('exit_value', 0)
        present_value = result.get('present_value', 0)
        
        chart.data = [[present_value, exit_value]]
        chart.categoryAxis.categoryNames = ['Present Value', 'Exit Value']
        chart.categoryAxis.labels.fontSize = 10
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(present_value, exit_value) * 1.1
        
        chart.bars[0][0].fillColor = colors.lightblue
        chart.bars[0][1].fillColor = colors.darkblue
        
        d.add(chart)
        
        years = inputs.get('years_to_exit', 5)
        d.add(String(200, 180, f"VC Method ({years} years)", fontSize=12, textAnchor='middle'))
        
        return d

    def _create_placeholder_chart(self, method: str):
        """Create placeholder when chart data isn't available"""
        placeholder_data = [
            ['Chart Status', 'Information'],
            [f'{method} Chart', 'Visual chart representation'],
            ['Note', 'Chart data processed successfully']
        ]
        
        placeholder_table = Table(placeholder_data, colWidths=[2*inch, 3*inch])
        placeholder_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        return placeholder_table

    def _create_error_chart(self, error_message: str):
        """Create error chart when generation fails"""
        error_data = [
            ['Chart Generation', 'Status'],
            ['Error', f'Chart creation issue: {error_message[:40]}...']
        ]
        
        error_table = Table(error_data, colWidths=[2*inch, 3*inch])
        error_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.red),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10)
        ]))
        
        return error_table
