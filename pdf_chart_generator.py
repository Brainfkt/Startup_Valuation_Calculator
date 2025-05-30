"""
PDF Chart Generator Module
Creates matplotlib charts for PDF reports with proper sizing and formatting
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from io import BytesIO
import tempfile
import os
from typing import Dict, List, Any, Optional, Tuple
from reportlab.lib.units import inch
from reportlab.platypus import Image, Spacer
from reportlab.lib import colors


class PDFChartGenerator:
    """Generate matplotlib charts optimized for PDF integration"""
    
    def __init__(self):
        # Set matplotlib to use non-interactive backend
        plt.switch_backend('Agg')
        
        # PDF-optimized chart settings
        self.chart_width = 6.5  # inches, fits within PDF margins
        self.chart_height = 4.0  # inches, good aspect ratio
        self.dpi = 300  # High resolution for PDF
        self.temp_files = []  # Track temporary files for cleanup
        
        # Color palette for consistent styling
        self.colors = [
            '#2E86AB', '#A23B72', '#F18F01', '#C73E1D',
            '#8BB174', '#6A994E', '#BC4749', '#386641'
        ]
        
        # Chart style settings
        plt.style.use('default')
        self.setup_chart_style()
    
    def setup_chart_style(self):
        """Configure matplotlib style for PDF charts"""
        plt.rcParams.update({
            'font.size': 10,
            'font.family': 'sans-serif',
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.titlesize': 14,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'grid.alpha': 0.3,
            'axes.grid': True,
            'grid.linewidth': 0.5
        })
    
    def create_dcf_chart(self, calc_data: Dict) -> Optional[str]:
        """Create DCF analysis chart showing cash flows and valuation breakdown"""
        try:
            result = calc_data.get('result', {})
            inputs = calc_data.get('inputs', {})
            
            # Extract data
            cash_flows = result.get('discounted_flows', [])
            operating_value = result.get('operating_value', 0)
            terminal_value = result.get('terminal_pv', 0)
            
            if not cash_flows:
                return None
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.chart_width, self.chart_height))
            
            # Chart 1: Cash Flow Analysis
            years = list(range(1, len(cash_flows) + 1))
            ax1.bar(years, cash_flows, color=self.colors[0], alpha=0.7, label='Discounted Cash Flows')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Cash Flow (€)')
            ax1.set_title('DCF Cash Flow Analysis')
            ax1.grid(True, alpha=0.3)
            
            # Format y-axis as currency
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000:.0f}K'))
            
            # Chart 2: Valuation Breakdown
            values = [operating_value, terminal_value]
            labels = ['Operating Value', 'Terminal Value']
            colors_pie = [self.colors[0], self.colors[1]]
            
            wedges, texts, autotexts = ax2.pie(values, labels=labels, colors=colors_pie, 
                                              autopct='%1.1f%%', startangle=90)
            ax2.set_title('Valuation Breakdown')
            
            # Enhance pie chart text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            # Save to temporary file
            temp_file = self._save_chart_to_temp(fig)
            plt.close(fig)
            
            return temp_file
            
        except Exception as e:
            print(f"Error creating DCF chart: {e}")
            return None
    
    def create_multiples_chart(self, calc_data: Dict) -> Optional[str]:
        """Create market multiples comparison chart"""
        try:
            result = calc_data.get('result', {})
            inputs = calc_data.get('inputs', {})
            
            sector = inputs.get('sector', 'Unknown')
            metric_type = inputs.get('metric_type', 'Revenue')
            metric_value = inputs.get('metric_value', 0)
            multiple = inputs.get('multiple', 0)
            valuation = result.get('valuation', 0)
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.chart_width, self.chart_height))
            
            # Chart 1: Multiple Analysis
            categories = ['Base Metric', 'Applied Multiple', 'Resulting Valuation']
            values = [metric_value, multiple, valuation]
            colors_bar = [self.colors[0], self.colors[1], self.colors[2]]
            
            # Normalize values for visualization (different scales)
            normalized_values = [metric_value, metric_value * multiple / 100, valuation]
            
            bars = ax1.bar(categories, normalized_values, color=colors_bar, alpha=0.7)
            ax1.set_ylabel('Value (€)')
            ax1.set_title(f'{sector} - {metric_type} Multiple Analysis')
            ax1.tick_params(axis='x', rotation=15)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                if value >= 1000000:
                    label = f'€{value/1000000:.1f}M'
                elif value >= 1000:
                    label = f'€{value/1000:.0f}K'
                else:
                    label = f'€{value:.0f}'
                
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        label, ha='center', va='bottom', fontweight='bold')
            
            # Chart 2: Sector Comparison (illustrative)
            sector_multiples = self._get_sector_multiples_data(sector, metric_type)
            sectors = list(sector_multiples.keys())
            multiples = list(sector_multiples.values())
            
            # Highlight current sector
            colors_comparison = [self.colors[0] if s == sector else self.colors[3] for s in sectors]
            
            bars2 = ax2.bar(sectors, multiples, color=colors_comparison, alpha=0.7)
            ax2.set_ylabel('Multiple (x)')
            ax2.set_title(f'{metric_type} Multiples by Sector')
            ax2.tick_params(axis='x', rotation=45)
            
            # Highlight the selected sector
            for bar, sect in zip(bars2, sectors):
                if sect == sector:
                    bar.set_edgecolor('red')
                    bar.set_linewidth(2)
            
            plt.tight_layout()
            
            temp_file = self._save_chart_to_temp(fig)
            plt.close(fig)
            
            return temp_file
            
        except Exception as e:
            print(f"Error creating multiples chart: {e}")
            return None
    
    def create_scorecard_chart(self, calc_data: Dict) -> Optional[str]:
        """Create scorecard method visualization"""
        try:
            result = calc_data.get('result', {})
            inputs = calc_data.get('inputs', {})
            
            criteria_scores = inputs.get('criteria_scores', {})
            criteria_analysis = result.get('criteria_analysis', {})
            adjustment_factor = result.get('adjustment_factor', 1.0)
            
            if not criteria_scores:
                return None
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.chart_width, self.chart_height))
            
            # Chart 1: Criteria Scores
            criteria = list(criteria_scores.keys())
            scores = list(criteria_scores.values())
            
            bars = ax1.barh(criteria, scores, color=self.colors[0], alpha=0.7)
            ax1.set_xlabel('Score (0-5)')
            ax1.set_title('Scorecard Criteria Evaluation')
            ax1.set_xlim(0, 5)
            
            # Add score labels
            for bar, score in zip(bars, scores):
                width = bar.get_width()
                ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                        f'{score}', ha='left', va='center', fontweight='bold')
            
            # Add reference lines
            ax1.axvline(x=3, color='orange', linestyle='--', alpha=0.7, label='Average (3)')
            ax1.axvline(x=4, color='green', linestyle='--', alpha=0.7, label='Good (4)')
            ax1.legend()
            
            # Chart 2: Impact Analysis
            if criteria_analysis:
                criteria_names = list(criteria_analysis.keys())
                contributions = [criteria_analysis[c].get('contribution', 0) for c in criteria_names]
                
                # Create pie chart of contributions
                wedges, texts, autotexts = ax2.pie(contributions, labels=criteria_names, 
                                                  colors=self.colors[:len(criteria_names)],
                                                  autopct='%1.1f%%', startangle=90)
                ax2.set_title('Criteria Impact on Valuation')
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(8)
            else:
                # Fallback: simple adjustment visualization
                ax2.bar(['Base', 'Adjusted'], [1.0, adjustment_factor], 
                       color=[self.colors[1], self.colors[0]], alpha=0.7)
                ax2.set_ylabel('Valuation Factor')
                ax2.set_title('Adjustment Factor Impact')
                ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Baseline')
                ax2.legend()
            
            plt.tight_layout()
            
            temp_file = self._save_chart_to_temp(fig)
            plt.close(fig)
            
            return temp_file
            
        except Exception as e:
            print(f"Error creating scorecard chart: {e}")
            return None
    
    def create_berkus_chart(self, calc_data: Dict) -> Optional[str]:
        """Create Berkus method visualization"""
        try:
            result = calc_data.get('result', {})
            inputs = calc_data.get('inputs', {})
            
            breakdown = result.get('breakdown', {})
            max_possible = result.get('max_possible', 2500000)
            
            if not breakdown:
                return None
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.chart_width, self.chart_height))
            
            # Chart 1: Criteria Values
            criteria_names = []
            values = []
            scores = []
            
            for criterion, data in breakdown.items():
                criteria_names.append(criterion.replace('_', ' ').title())
                values.append(data.get('value', 0))
                scores.append(data.get('score', 0))
            
            bars = ax1.bar(range(len(criteria_names)), values, color=self.colors[0], alpha=0.7)
            ax1.set_xlabel('Berkus Criteria')
            ax1.set_ylabel('Value (€)')
            ax1.set_title('Berkus Method - Value by Criteria')
            ax1.set_xticks(range(len(criteria_names)))
            ax1.set_xticklabels(criteria_names, rotation=45, ha='right')
            
            # Format y-axis
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000:.0f}K'))
            
            # Add value labels
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'€{value/1000:.0f}K', ha='center', va='bottom', fontsize=8)
            
            # Chart 2: Achievement vs Potential
            total_value = sum(values)
            achievement_pct = (total_value / max_possible) * 100
            
            # Create a gauge-like visualization
            angles = np.linspace(0, np.pi, 100)
            radius = 1
            
            # Background arc (potential)
            ax2.plot(radius * np.cos(angles), radius * np.sin(angles), 
                    color='lightgray', linewidth=10, alpha=0.3)
            
            # Achievement arc
            achievement_angles = angles[:int(achievement_pct)]
            ax2.plot(radius * np.cos(achievement_angles), radius * np.sin(achievement_angles), 
                    color=self.colors[0], linewidth=10)
            
            # Add percentage text
            ax2.text(0, -0.3, f'{achievement_pct:.1f}%', ha='center', va='center', 
                    fontsize=16, fontweight='bold')
            ax2.text(0, -0.5, 'of Maximum Potential', ha='center', va='center', fontsize=10)
            
            ax2.set_xlim(-1.2, 1.2)
            ax2.set_ylim(-0.6, 1.2)
            ax2.set_aspect('equal')
            ax2.axis('off')
            ax2.set_title('Achievement Level')
            
            plt.tight_layout()
            
            temp_file = self._save_chart_to_temp(fig)
            plt.close(fig)
            
            return temp_file
            
        except Exception as e:
            print(f"Error creating Berkus chart: {e}")
            return None
    
    def create_comparison_chart(self, calculations: List[Dict]) -> Optional[str]:
        """Create comparison chart across multiple calculations"""
        try:
            if len(calculations) < 2:
                return None
            
            methods = []
            valuations = []
            timestamps = []
            
            for calc in calculations[-6:]:  # Show last 6 calculations
                methods.append(calc.get('method', 'Unknown'))
                valuations.append(calc.get('valuation', 0))
                timestamps.append(calc.get('timestamp', '')[:10])  # Date only
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.chart_width, self.chart_height))
            
            # Chart 1: Valuation by Method
            method_colors = [self.colors[i % len(self.colors)] for i in range(len(methods))]
            bars = ax1.bar(range(len(methods)), valuations, color=method_colors, alpha=0.7)
            
            ax1.set_xlabel('Calculation Method')
            ax1.set_ylabel('Valuation (€)')
            ax1.set_title('Valuation Comparison by Method')
            ax1.set_xticks(range(len(methods)))
            ax1.set_xticklabels(methods, rotation=45, ha='right')
            
            # Format y-axis
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000000:.1f}M'))
            
            # Add value labels
            for bar, value in zip(bars, valuations):
                height = bar.get_height()
                if value >= 1000000:
                    label = f'€{value/1000000:.1f}M'
                else:
                    label = f'€{value/1000:.0f}K'
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        label, ha='center', va='bottom', fontsize=8)
            
            # Chart 2: Valuation Trend
            ax2.plot(range(len(valuations)), valuations, marker='o', linewidth=2, 
                    markersize=6, color=self.colors[0])
            ax2.fill_between(range(len(valuations)), valuations, alpha=0.3, color=self.colors[0])
            
            ax2.set_xlabel('Calculation Sequence')
            ax2.set_ylabel('Valuation (€)')
            ax2.set_title('Valuation Trend Over Time')
            ax2.grid(True, alpha=0.3)
            
            # Format y-axis
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000000:.1f}M'))
            
            plt.tight_layout()
            
            temp_file = self._save_chart_to_temp(fig)
            plt.close(fig)
            
            return temp_file
            
        except Exception as e:
            print(f"Error creating comparison chart: {e}")
            return None
    
    def _get_sector_multiples_data(self, current_sector: str, metric_type: str) -> Dict[str, float]:
        """Get representative sector multiples for comparison"""
        # This would typically come from a database or API
        # Using representative data based on common industry multiples
        
        multiples_data = {
            'Technology': {'Revenue': 6.5, 'EBITDA': 15.2},
            'Healthcare': {'Revenue': 4.8, 'EBITDA': 12.8},
            'Financial Services': {'Revenue': 3.2, 'EBITDA': 9.5},
            'Manufacturing': {'Revenue': 2.1, 'EBITDA': 8.3},
            'Retail': {'Revenue': 1.8, 'EBITDA': 7.2},
            'Energy': {'Revenue': 2.5, 'EBITDA': 6.8}
        }
        
        result = {}
        for sector, data in multiples_data.items():
            result[sector] = data.get(metric_type, 5.0)
        
        return result
    
    def _save_chart_to_temp(self, fig) -> str:
        """Save matplotlib figure to temporary file and return path"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.close()
        
        # Save with high DPI for PDF quality
        fig.savefig(temp_file.name, dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        
        self.temp_files.append(temp_file.name)
        return temp_file.name
    
    def create_reportlab_image(self, chart_path: str, width: float = None, height: float = None) -> Image:
        """Create ReportLab Image object from chart file"""
        if width is None:
            width = self.chart_width * inch
        if height is None:
            height = self.chart_height * inch
            
        return Image(chart_path, width=width, height=height)
    
    def cleanup_temp_files(self):
        """Clean up temporary chart files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                print(f"Error cleaning up temp file {temp_file}: {e}")
        
        self.temp_files.clear()
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.cleanup_temp_files()