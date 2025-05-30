"""
Chart Generator Module
Creates interactive Plotly charts for different valuation methods
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any

class ChartGenerator:
    """Generate interactive charts for valuation results"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#bcbd22'
        }
    
    def create_dcf_chart(self, result: Dict, cash_flows: List[float]) -> go.Figure:
        """Create DCF analysis charts"""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Cash Flow Projections',
                    'Present Values',
                    'Valuation Breakdown',
                    'Cumulative Present Value'
                ),
                specs=[
                    [{"type": "bar"}, {"type": "bar"}],
                    [{"type": "pie"}, {"type": "scatter"}]
                ]
            )
            
            years = [f"Year {i+1}" for i in range(len(cash_flows))]
            
            # Chart 1: Cash Flow Projections
            fig.add_trace(
                go.Bar(
                    x=years,
                    y=cash_flows,
                    name="Cash Flows",
                    marker_color=self.color_palette['primary'],
                    text=[f"€{cf:,.0f}" for cf in cash_flows],
                    textposition='outside'
                ),
                row=1, col=1
            )
            
            # Chart 2: Present Values
            discounted_flows = result.get('discounted_flows', [])
            fig.add_trace(
                go.Bar(
                    x=years,
                    y=discounted_flows,
                    name="Present Values",
                    marker_color=self.color_palette['secondary'],
                    text=[f"€{pv:,.0f}" for pv in discounted_flows],
                    textposition='outside'
                ),
                row=1, col=2
            )
            
            # Chart 3: Valuation Breakdown
            operating_value = result.get('operating_value', 0)
            terminal_value = result.get('terminal_pv', 0)
            
            fig.add_trace(
                go.Pie(
                    labels=['Operating Value', 'Terminal Value'],
                    values=[operating_value, terminal_value],
                    hole=0.3,
                    marker_colors=[self.color_palette['success'], self.color_palette['info']],
                    textinfo='label+percent+value',
                    texttemplate='%{label}<br>%{percent}<br>€%{value:,.0f}'
                ),
                row=2, col=1
            )
            
            # Chart 4: Cumulative Present Value
            cumulative_pv = np.cumsum([0] + discounted_flows)
            fig.add_trace(
                go.Scatter(
                    x=['Start'] + years,
                    y=cumulative_pv,
                    mode='lines+markers',
                    name="Cumulative PV",
                    line=dict(color=self.color_palette['primary'], width=3),
                    marker=dict(size=8)
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title_text="DCF Valuation Analysis",
                showlegend=False,
                height=600
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"DCF chart generation failed: {str(e)}")
    
    def create_multiples_chart(self, result: Dict, sector: str) -> go.Figure:
        """Create market multiples comparison chart"""
        try:
            # Import here to avoid circular import
            from data_models import SECTOR_MULTIPLES
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Valuation Calculation', 'Industry Comparison'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Chart 1: Valuation breakdown
            metric_value = result.get('metric', 0)
            multiple = result.get('multiple', 0)
            valuation = result.get('valuation', 0)
            
            fig.add_trace(
                go.Bar(
                    x=['Base Metric', 'Applied Multiple', 'Valuation'],
                    y=[metric_value, multiple, valuation],
                    name="Calculation",
                    marker_color=[
                        self.color_palette['primary'],
                        self.color_palette['secondary'],
                        self.color_palette['success']
                    ],
                    text=[
                        f"€{metric_value:,.0f}",
                        f"{multiple:.1f}x",
                        f"€{valuation:,.0f}"
                    ],
                    textposition='outside'
                ),
                row=1, col=1
            )
            
            # Chart 2: Industry comparison
            metric_type = result.get('metric_type', 'Revenue')
            sectors = list(SECTOR_MULTIPLES.keys())
            multiples = [SECTOR_MULTIPLES[s][metric_type] for s in sectors]
            
            colors = [
                self.color_palette['warning'] if s == sector else self.color_palette['light']
                for s in sectors
            ]
            
            fig.add_trace(
                go.Bar(
                    x=sectors,
                    y=multiples,
                    name=f"{metric_type} Multiples",
                    marker_color=colors,
                    text=[f"{m:.1f}x" for m in multiples],
                    textposition='outside'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title_text=f"Market Multiples Analysis - {sector}",
                showlegend=False,
                height=400
            )
            
            # Rotate x-axis labels for better readability
            fig.update_xaxes(tickangle=45, row=1, col=2)
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Multiples chart generation failed: {str(e)}")
    
    def create_scorecard_chart(self, result: Dict) -> go.Figure:
        """Create scorecard method visualization"""
        try:
            criteria_analysis = result.get('criteria_analysis', {})
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Criteria Scores', 'Weight Contributions'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            criteria_names = []
            scores = []
            weights = []
            contributions = []
            
            for criterion, data in criteria_analysis.items():
                criteria_names.append(criterion.title())
                scores.append(data['score'])
                weights.append(data['weight'] * 100)  # Convert to percentage
                contributions.append(data['contribution'])
            
            # Chart 1: Criteria scores
            fig.add_trace(
                go.Bar(
                    x=criteria_names,
                    y=scores,
                    name="Scores",
                    marker_color=self.color_palette['primary'],
                    text=[f"{s}/5" for s in scores],
                    textposition='outside'
                ),
                row=1, col=1
            )
            
            # Chart 2: Weight contributions
            fig.add_trace(
                go.Bar(
                    x=criteria_names,
                    y=contributions,
                    name="Weighted Contributions",
                    marker_color=self.color_palette['secondary'],
                    text=[f"{c:.3f}" for c in contributions],
                    textposition='outside'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title_text="Scorecard Method Analysis",
                showlegend=False,
                height=400
            )
            
            # Set y-axis ranges
            fig.update_yaxes(range=[0, 5.5], row=1, col=1, title_text="Score (0-5)")
            fig.update_yaxes(title_text="Contribution Factor", row=1, col=2)
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Scorecard chart generation failed: {str(e)}")
    
    def create_berkus_chart(self, result: Dict) -> go.Figure:
        """Create Berkus method visualization"""
        try:
            breakdown = result.get('breakdown', {})
            
            criteria_names = []
            scores = []
            values = []
            max_values = []
            
            for criterion, data in breakdown.items():
                criteria_names.append(data['name'])
                scores.append(data['score'])
                values.append(data['value'])
                max_values.append(500000)  # Max per criterion
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Value by Criterion', 'Completion Percentage'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Chart 1: Values by criterion
            fig.add_trace(
                go.Bar(
                    x=criteria_names,
                    y=values,
                    name="Criterion Values",
                    marker_color=self.color_palette['success'],
                    text=[f"€{v:,.0f}" for v in values],
                    textposition='outside'
                ),
                row=1, col=1
            )
            
            # Chart 2: Completion percentages
            percentages = [(v/500000)*100 for v in values]
            fig.add_trace(
                go.Bar(
                    x=criteria_names,
                    y=percentages,
                    name="Completion %",
                    marker_color=self.color_palette['info'],
                    text=[f"{p:.1f}%" for p in percentages],
                    textposition='outside'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title_text="Berkus Method Analysis",
                showlegend=False,
                height=400
            )
            
            # Update axes
            fig.update_xaxes(tickangle=45)
            fig.update_yaxes(title_text="Value (€)", row=1, col=1)
            fig.update_yaxes(title_text="Completion (%)", range=[0, 105], row=1, col=2)
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Berkus chart generation failed: {str(e)}")
    
    def create_risk_factor_chart(self, result: Dict) -> go.Figure:
        """Create risk factor summation visualization"""
        try:
            risk_analysis = result.get('risk_analysis', {})
            
            risk_names = []
            ratings = []
            adjustments = []
            
            for factor, data in risk_analysis.items():
                risk_names.append(data['name'])
                ratings.append(data['rating'])
                adjustments.append(data['adjustment'] * 100)  # Convert to percentage
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Risk Ratings', 'Valuation Adjustments'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Chart 1: Risk ratings
            colors_ratings = [
                self.color_palette['warning'] if r < 0 else 
                self.color_palette['success'] if r > 0 else 
                self.color_palette['light']
                for r in ratings
            ]
            
            fig.add_trace(
                go.Bar(
                    x=risk_names,
                    y=ratings,
                    name="Risk Ratings",
                    marker_color=colors_ratings,
                    text=[f"{r:+d}" for r in ratings],
                    textposition='outside'
                ),
                row=1, col=1
            )
            
            # Chart 2: Adjustments
            colors_adj = [
                self.color_palette['warning'] if a < 0 else 
                self.color_palette['success'] if a > 0 else 
                self.color_palette['light']
                for a in adjustments
            ]
            
            fig.add_trace(
                go.Bar(
                    x=risk_names,
                    y=adjustments,
                    name="Adjustments",
                    marker_color=colors_adj,
                    text=[f"{a:+.1f}%" for a in adjustments],
                    textposition='outside'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title_text="Risk Factor Analysis",
                showlegend=False,
                height=400
            )
            
            # Update axes
            fig.update_xaxes(tickangle=45)
            fig.update_yaxes(title_text="Rating (-2 to +2)", range=[-2.5, 2.5], row=1, col=1)
            fig.update_yaxes(title_text="Adjustment (%)", row=1, col=2)
            
            # Add horizontal line at zero
            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=2)
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Risk factor chart generation failed: {str(e)}")
    
    def create_vc_method_chart(self, result: Dict, include_investment: bool) -> go.Figure:
        """Create venture capital method visualization"""
        try:
            if include_investment and 'pre_money_valuation' in result:
                return self._create_vc_investment_chart(result)
            else:
                return self._create_vc_returns_chart(result)
                
        except Exception as e:
            return self._create_error_chart(f"VC method chart generation failed: {str(e)}")
    
    def _create_vc_investment_chart(self, result: Dict) -> go.Figure:
        """Create VC investment structure chart"""
        pre_money = result.get('pre_money_valuation', 0)
        investment = result.get('investment_needed', 0)
        post_money = result.get('post_money_valuation', 0)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Investment Structure', 'Ownership Split'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Chart 1: Investment structure
        fig.add_trace(
            go.Bar(
                x=['Pre-Money', 'Investment', 'Post-Money'],
                y=[pre_money, investment, post_money],
                name="Valuation",
                marker_color=[
                    self.color_palette['primary'],
                    self.color_palette['secondary'],
                    self.color_palette['success']
                ],
                text=[
                    f"€{pre_money:,.0f}",
                    f"€{investment:,.0f}",
                    f"€{post_money:,.0f}"
                ],
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Chart 2: Ownership split
        ownership_pct = result.get('ownership_percentage', 0) * 100
        founder_pct = 100 - ownership_pct
        
        fig.add_trace(
            go.Pie(
                labels=['Founders', 'Investors'],
                values=[founder_pct, ownership_pct],
                hole=0.3,
                marker_colors=[self.color_palette['primary'], self.color_palette['secondary']],
                textinfo='label+percent',
                texttemplate='%{label}<br>%{percent}'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="VC Investment Analysis",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def _create_vc_returns_chart(self, result: Dict) -> go.Figure:
        """Create VC returns analysis chart"""
        present_value = result.get('present_value', 0)
        exit_value = result.get('exit_value', 0)
        return_multiple = result.get('expected_return_multiple', 0)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Value Comparison', 'Return Analysis'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Chart 1: Value comparison
        fig.add_trace(
            go.Bar(
                x=['Present Value', 'Exit Value'],
                y=[present_value, exit_value],
                name="Values",
                marker_color=[self.color_palette['primary'], self.color_palette['success']],
                text=[f"€{present_value:,.0f}", f"€{exit_value:,.0f}"],
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Chart 2: Return metrics
        annualized_return = result.get('annualized_return', 0) * 100
        
        fig.add_trace(
            go.Bar(
                x=['Return Multiple', 'Annualized Return %'],
                y=[return_multiple, annualized_return],
                name="Returns",
                marker_color=[self.color_palette['info'], self.color_palette['warning']],
                text=[f"{return_multiple:.1f}x", f"{annualized_return:.1f}%"],
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="VC Returns Analysis",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def _create_error_chart(self, error_message: str) -> go.Figure:
        """Create error message chart"""
        fig = go.Figure()
        
        fig.add_annotation(
            text=f"Chart Generation Error:<br>{error_message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="red")
        )
        
        fig.update_layout(
            title_text="Chart Error",
            showlegend=False,
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        return fig
