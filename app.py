"""
Startup Valuation Calculator
Comprehensive Streamlit application for calculating startup valuations using multiple methods
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
from io import BytesIO

from valuation_calculator import ValuationCalculator
from chart_generator import ChartGenerator
from pdf_generator import PDFGenerator
from data_models import SECTOR_MULTIPLES, ValidationResult
from utils import format_currency, validate_positive_number, save_calculation_history
from export_manager_simple import ExportManager
from test_suite import run_test_suite

# Page configuration
st.set_page_config(
    page_title="Startup Valuation Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []

if 'current_results' not in st.session_state:
    st.session_state.current_results = {}

def main():
    """Main application function"""
    st.title("📊 Startup Valuation Calculator")
    st.markdown("---")
    
    # Sidebar for method selection
    st.sidebar.title("Valuation Methods")
    method = st.sidebar.selectbox(
        "Choose a valuation method:",
        [
            "DCF (Discounted Cash Flow)",
            "Market Multiples",
            "Scorecard Method",
            "Berkus Method",
            "Risk Factor Summation",
            "Venture Capital Method"
        ]
    )
    
    # Add test suite section
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧪 Testing")
    if st.sidebar.button("Run Test Suite"):
        st.session_state.show_tests = True
    

    
    # Method-specific interfaces
    if method == "DCF (Discounted Cash Flow)":
        dcf_interface()
    elif method == "Market Multiples":
        market_multiples_interface()
    elif method == "Scorecard Method":
        scorecard_interface()
    elif method == "Berkus Method":
        berkus_interface()
    elif method == "Risk Factor Summation":
        risk_factor_interface()
    elif method == "Venture Capital Method":
        vc_method_interface()
    
    # Display calculation history
    display_calculation_history()
    
    # Export and PDF sections at bottom of page
    st.markdown("---")
    
    # Export Data Section
    st.subheader("📤 Export Data")
    display_export_options()
    
    st.markdown("---")
    
    # PDF Report Section
    st.subheader("📄 Generate PDF Report")
    generate_pdf_report()

def dcf_interface():
    """DCF method interface"""
    st.header("💰 DCF (Discounted Cash Flow) Method")
    st.markdown("Calculate valuation based on projected cash flows")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cash Flow Projections")
        num_years = st.slider("Number of projection years", 3, 10, 5)
        
        cash_flows = []
        for i in range(num_years):
            cf = st.number_input(
                f"Year {i+1} Cash Flow (€)",
                min_value=0.0,
                value=100000.0 * (i + 1),
                step=10000.0,
                key=f"cf_{i}"
            )
            cash_flows.append(cf)
    
    with col2:
        st.subheader("Valuation Parameters")
        discount_rate = st.slider("Discount Rate (WACC) %", 5.0, 25.0, 12.0) / 100
        terminal_growth = st.slider("Terminal Growth Rate %", 0.0, 5.0, 2.0) / 100
        
        # Validation
        if discount_rate <= terminal_growth:
            st.error("⚠️ Discount rate must be higher than terminal growth rate")
            return
    
    if st.button("Calculate DCF Valuation", type="primary"):
        try:
            calculator = ValuationCalculator()
            result = calculator.dcf_valuation(cash_flows, 0, discount_rate, terminal_growth)
            
            if "error" in result:
                st.error(f"Calculation Error: {result['error']}")
                return
            
            # Display results and get chart
            chart_fig = display_dcf_results(result, cash_flows)
            
            # Save to history with chart
            save_calculation_history(
                method="DCF",
                inputs={
                    "cash_flows": cash_flows,
                    "discount_rate": discount_rate,
                    "terminal_growth": terminal_growth
                },
                result=result,
                chart_fig=chart_fig
            )
            
        except Exception as e:
            st.error(f"Calculation failed: {str(e)}")

def display_dcf_results(result, cash_flows):
    """Display DCF calculation results and return chart figure"""
    st.success("✅ DCF Calculation Complete")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Valuation",
            format_currency(result['valuation']),
            delta=None
        )
    
    with col2:
        st.metric(
            "Operating Value",
            format_currency(result['operating_value']),
            delta=None
        )
    
    with col3:
        st.metric(
            "Terminal Value (PV)",
            format_currency(result['terminal_pv']),
            delta=None
        )
    
    # Chart
    chart_gen = ChartGenerator()
    fig = chart_gen.create_dcf_chart(result, cash_flows)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store results for PDF generation
    st.session_state.current_results = {
        "method": "DCF",
        "result": result,
        "chart_data": {"cash_flows": cash_flows},
        "chart": fig
    }
    
    return fig

def market_multiples_interface():
    """Market multiples method interface"""
    st.header("📈 Market Multiples Method")
    st.markdown("Valuation based on industry multiples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sector = st.selectbox("Industry Sector", list(SECTOR_MULTIPLES.keys()))
        metric_type = st.selectbox("Metric Type", ["Revenue", "EBITDA"])
        
        metric_value = st.number_input(
            f"Current {metric_type} (€)",
            min_value=0.0,
            value=1000000.0,
            step=50000.0
        )
    
    with col2:
        st.subheader("Sector Multiples")
        sector_data = SECTOR_MULTIPLES[sector]
        
        st.info(f"**{sector}** Industry Averages:")
        st.write(f"• Revenue Multiple: {sector_data['Revenue']}x")
        st.write(f"• EBITDA Multiple: {sector_data['EBITDA']}x")
        
        # Allow custom multiple
        use_custom = st.checkbox("Use custom multiple")
        if use_custom:
            custom_multiple = st.number_input(
                f"Custom {metric_type} Multiple",
                min_value=0.1,
                value=sector_data[metric_type],
                step=0.1
            )
            multiple = custom_multiple
        else:
            multiple = sector_data[metric_type]
    
    if st.button("Calculate Market Multiple Valuation", type="primary"):
        try:
            calculator = ValuationCalculator()
            result = calculator.market_multiples_valuation(metric_value, multiple, metric_type)
            
            # Display results
            display_market_multiples_results(result, sector)
            
            # Save to history
            save_calculation_history(
                method="Market Multiples",
                inputs={
                    "sector": sector,
                    "metric_type": metric_type,
                    "metric_value": metric_value,
                    "multiple": multiple
                },
                result=result
            )
            
        except Exception as e:
            st.error(f"Calculation failed: {str(e)}")

def display_market_multiples_results(result, sector):
    """Display market multiples results"""
    st.success("✅ Market Multiples Calculation Complete")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Valuation",
            format_currency(result['valuation']),
            delta=None
        )
    
    with col2:
        st.metric(
            f"{result['metric_type']}",
            format_currency(result['metric']),
            delta=None
        )
    
    with col3:
        st.metric(
            "Multiple Applied",
            f"{result['multiple']:.1f}x",
            delta=None
        )
    
    # Chart
    chart_gen = ChartGenerator()
    fig = chart_gen.create_multiples_chart(result, sector)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store results
    st.session_state.current_results = {
        "method": "Market Multiples",
        "result": result,
        "sector": sector,
        "chart": fig
    }

def scorecard_interface():
    """Scorecard method interface"""
    st.header("📋 Scorecard Method")
    st.markdown("Adjust base valuation using weighted criteria scores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Base Valuation")
        base_valuation = st.number_input(
            "Base Valuation (€)",
            min_value=0.0,
            value=2000000.0,
            step=100000.0
        )
        
        st.info("💡 Use a comparable company valuation or average industry valuation as base")
    
    with col2:
        st.subheader("Scoring Criteria (0-5 scale)")
        
        criteria_scores = {}
        criteria_labels = {
            "team": "Management Team Quality",
            "product": "Product/Technology",
            "market": "Market Opportunity",
            "competition": "Competitive Advantage",
            "financial": "Financial Performance",
            "legal": "Legal/IP Protection"
        }
        
        for key, label in criteria_labels.items():
            score = st.slider(
                label,
                min_value=0,
                max_value=5,
                value=3,
                key=f"scorecard_{key}"
            )
            criteria_scores[key] = score
    
    if st.button("Calculate Scorecard Valuation", type="primary"):
        try:
            calculator = ValuationCalculator()
            result = calculator.scorecard_valuation(base_valuation, criteria_scores)
            
            # Display results
            display_scorecard_results(result)
            
            # Save to history
            save_calculation_history(
                method="Scorecard",
                inputs={
                    "base_valuation": base_valuation,
                    "criteria_scores": criteria_scores
                },
                result=result
            )
            
        except Exception as e:
            st.error(f"Calculation failed: {str(e)}")

def display_scorecard_results(result):
    """Display scorecard method results"""
    st.success("✅ Scorecard Calculation Complete")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Adjusted Valuation",
            format_currency(result['valuation']),
            delta=format_currency(result['valuation'] - result['base_valuation'])
        )
    
    with col2:
        st.metric(
            "Base Valuation",
            format_currency(result['base_valuation']),
            delta=None
        )
    
    with col3:
        st.metric(
            "Adjustment Factor",
            f"{result['adjustment_factor']:.2f}x",
            delta=None
        )
    
    # Detailed breakdown
    st.subheader("Criteria Analysis")
    criteria_df = pd.DataFrame([
        {
            "Criterion": details["score"],
            "Score": details["score"],
            "Weight": f"{details['weight']:.1%}",
            "Contribution": f"{details['contribution']:.3f}"
        }
        for criterion, details in result['criteria_analysis'].items()
    ])
    
    st.dataframe(criteria_df, use_container_width=True)
    
    # Chart
    chart_gen = ChartGenerator()
    fig = chart_gen.create_scorecard_chart(result)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store results
    st.session_state.current_results = {
        "method": "Scorecard",
        "result": result,
        "chart": fig
    }

def berkus_interface():
    """Berkus method interface"""
    st.header("🎯 Berkus Method")
    st.markdown("Pre-revenue startup valuation (max €2.5M)")
    
    st.info("💡 Rate each criterion from 0-5 (5 = excellent, 0 = poor/missing)")
    
    criteria_scores = {}
    criteria_descriptions = {
        "concept": "Sound Idea (Basic Value)",
        "prototype": "Prototype (Reduces Technology Risk)",
        "team": "Quality Management Team (Reduces Execution Risk)",
        "strategic_relationships": "Strategic Relationships (Reduces Market Risk)",
        "product_rollout": "Product Rollout or Sales (Reduces Financial Risk)"
    }
    
    col1, col2 = st.columns(2)
    
    criteria_items = list(criteria_descriptions.items())
    mid_point = len(criteria_items) // 2
    
    with col1:
        for key, description in criteria_items[:mid_point + 1]:
            score = st.slider(
                description,
                min_value=0,
                max_value=5,
                value=3,
                key=f"berkus_{key}"
            )
            criteria_scores[key] = score
    
    with col2:
        for key, description in criteria_items[mid_point + 1:]:
            score = st.slider(
                description,
                min_value=0,
                max_value=5,
                value=3,
                key=f"berkus_{key}"
            )
            criteria_scores[key] = score
    
    if st.button("Calculate Berkus Valuation", type="primary"):
        try:
            calculator = ValuationCalculator()
            result = calculator.berkus_valuation(criteria_scores)
            
            # Display results
            display_berkus_results(result)
            
            # Save to history
            save_calculation_history(
                method="Berkus",
                inputs={"criteria_scores": criteria_scores},
                result=result
            )
            
        except Exception as e:
            st.error(f"Calculation failed: {str(e)}")

def display_berkus_results(result):
    """Display Berkus method results"""
    st.success("✅ Berkus Calculation Complete")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Valuation",
            format_currency(result['valuation']),
            delta=None
        )
    
    with col2:
        st.metric(
            "Achievement Rate",
            f"{(result['valuation'] / result['max_possible']) * 100:.1f}%",
            delta=None
        )
    
    with col3:
        st.metric(
            "Max Possible",
            format_currency(result['max_possible']),
            delta=None
        )
    
    # Breakdown table
    st.subheader("Valuation Breakdown")
    breakdown_df = pd.DataFrame([
        {
            "Criterion": details["name"],
            "Score": f"{details['score']}/5",
            "Value": format_currency(details["value"])
        }
        for criterion, details in result['breakdown'].items()
    ])
    
    st.dataframe(breakdown_df, use_container_width=True)
    
    # Chart
    chart_gen = ChartGenerator()
    fig = chart_gen.create_berkus_chart(result)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store results
    st.session_state.current_results = {
        "method": "Berkus",
        "result": result,
        "chart": fig
    }

def risk_factor_interface():
    """Risk factor summation interface"""
    st.header("⚖️ Risk Factor Summation Method")
    st.markdown("Adjust base valuation based on risk assessment")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Base Valuation")
        base_valuation = st.number_input(
            "Base Valuation (€)",
            min_value=0.0,
            value=2000000.0,
            step=100000.0
        )
        
        st.info("💡 Each factor can adjust valuation by ±12.5% (total max ±50%)")
    
    with col2:
        st.subheader("Risk Factors (-2 to +2)")
        st.caption("-2: Very High Risk, -1: High Risk, 0: Average, +1: Low Risk, +2: Very Low Risk")
        
        risk_factors = {}
        risk_categories = {
            "management": "Management Team Risk",
            "stage": "Development Stage Risk",
            "legislation": "Legislative/Political Risk",
            "manufacturing": "Manufacturing Risk",
            "sales": "Sales/Marketing Risk",
            "funding": "Funding/Capital Risk",
            "competition": "Competition Risk",
            "technology": "Technology Risk",
            "litigation": "Litigation Risk",
            "international": "International Risk",
            "reputation": "Reputation Risk",
            "exit": "Exit Strategy Risk"
        }
        
        # Display in two columns
        risk_items = list(risk_categories.items())
        mid_point = len(risk_items) // 2
        
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            for key, label in risk_items[:mid_point]:
                rating = st.slider(
                    label,
                    min_value=-2,
                    max_value=2,
                    value=0,
                    key=f"risk_{key}"
                )
                risk_factors[key] = rating
        
        with subcol2:
            for key, label in risk_items[mid_point:]:
                rating = st.slider(
                    label,
                    min_value=-2,
                    max_value=2,
                    value=0,
                    key=f"risk_{key}"
                )
                risk_factors[key] = rating
    
    if st.button("Calculate Risk-Adjusted Valuation", type="primary"):
        try:
            calculator = ValuationCalculator()
            result = calculator.risk_factor_summation(base_valuation, risk_factors)
            
            # Display results
            display_risk_factor_results(result)
            
            # Save to history
            save_calculation_history(
                method="Risk Factor Summation",
                inputs={
                    "base_valuation": base_valuation,
                    "risk_factors": risk_factors
                },
                result=result
            )
            
        except Exception as e:
            st.error(f"Calculation failed: {str(e)}")

def display_risk_factor_results(result):
    """Display risk factor summation results"""
    st.success("✅ Risk Factor Calculation Complete")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Risk-Adjusted Valuation",
            format_currency(result['valuation']),
            delta=format_currency(result['valuation'] - result['base_valuation'])
        )
    
    with col2:
        st.metric(
            "Base Valuation",
            format_currency(result['base_valuation']),
            delta=None
        )
    
    with col3:
        st.metric(
            "Total Risk Adjustment",
            f"{result['total_adjustment']:+.1%}",
            delta=None
        )
    
    # Risk analysis table
    st.subheader("Risk Factor Analysis")
    risk_df = pd.DataFrame([
        {
            "Risk Factor": details["name"],
            "Rating": details["rating"],
            "Adjustment": f"{details['adjustment']:+.1%}"
        }
        for factor, details in result['risk_analysis'].items()
    ])
    
    st.dataframe(risk_df, use_container_width=True)
    
    # Chart
    chart_gen = ChartGenerator()
    fig = chart_gen.create_risk_factor_chart(result)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store results
    st.session_state.current_results = {
        "method": "Risk Factor Summation",
        "result": result,
        "chart": fig
    }

def vc_method_interface():
    """Venture Capital method interface"""
    st.header("💼 Venture Capital Method")
    st.markdown("Calculate valuation based on expected exit scenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exit Projections")
        expected_revenue = st.number_input(
            "Expected Revenue at Exit (€)",
            min_value=0.0,
            value=10000000.0,
            step=500000.0
        )
        
        exit_multiple = st.slider(
            "Exit Multiple (Revenue)",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.5
        )
        
        years_to_exit = st.slider(
            "Years to Exit",
            min_value=3,
            max_value=10,
            value=5
        )
    
    with col2:
        st.subheader("Investment Parameters")
        required_return = st.slider(
            "Required Annual Return %",
            min_value=10.0,
            max_value=50.0,
            value=25.0
        ) / 100
        
        include_investment = st.checkbox("Include investment calculation")
        
        investment_needed = 0
        if include_investment:
            investment_needed = st.number_input(
                "Investment Needed (€)",
                min_value=0.0,
                value=1000000.0,
                step=50000.0
            )
    
    if st.button("Calculate VC Method Valuation", type="primary"):
        try:
            calculator = ValuationCalculator()
            result = calculator.venture_capital_method(
                expected_revenue, 
                exit_multiple, 
                required_return, 
                years_to_exit,
                investment_needed if include_investment else None
            )
            
            # Display results
            display_vc_method_results(result, include_investment)
            
            # Save to history
            save_calculation_history(
                method="Venture Capital",
                inputs={
                    "expected_revenue": expected_revenue,
                    "exit_multiple": exit_multiple,
                    "required_return": required_return,
                    "years_to_exit": years_to_exit,
                    "investment_needed": investment_needed if include_investment else None
                },
                result=result
            )
            
        except Exception as e:
            st.error(f"Calculation failed: {str(e)}")

def display_vc_method_results(result, include_investment):
    """Display VC method results"""
    st.success("✅ VC Method Calculation Complete")
    
    if include_investment and 'pre_money_valuation' in result:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Pre-Money Valuation",
                format_currency(result['pre_money_valuation']),
                delta=None
            )
        
        with col2:
            st.metric(
                "Post-Money Valuation",
                format_currency(result['post_money_valuation']),
                delta=None
            )
        
        with col3:
            st.metric(
                "Ownership %",
                f"{result['ownership_percentage']:.1%}",
                delta=None
            )
        
        with col4:
            st.metric(
                "Investment",
                format_currency(result['investment_needed']),
                delta=None
            )
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Valuation",
                format_currency(result['present_value']),
                delta=None
            )
        
        with col2:
            st.metric(
                "Exit Value",
                format_currency(result['exit_value']),
                delta=None
            )
        
        with col3:
            st.metric(
                "Annualized Return",
                f"{result['annualized_return']:.1%}",
                delta=None
            )
    
    # Chart
    chart_gen = ChartGenerator()
    fig = chart_gen.create_vc_method_chart(result, include_investment)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store results
    st.session_state.current_results = {
        "method": "Venture Capital",
        "result": result,
        "include_investment": include_investment,
        "chart": fig
    }

def display_calculation_history():
    """Display calculation history and PDF generation"""
    if st.session_state.calculation_history:
        st.markdown("---")
        st.subheader("📊 Calculation History")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Display all calculations with charts and delete options
            for i, calc in enumerate(reversed(st.session_state.calculation_history)):
                with st.expander(f"{calc['method']} - {calc['timestamp']} - {format_currency(calc['valuation'])}"):
                    col_info, col_delete = st.columns([4, 1])
                    
                    with col_info:
                        st.write(f"**Valuation:** {format_currency(calc['valuation'])}")
                        
                        # Display chart if available
                        if calc.get('chart') is not None:
                            st.plotly_chart(calc['chart'], use_container_width=True, key=f"chart_{calc.get('id', i)}")
                        
                        # Show key inputs summary
                        if calc['method'] == "DCF":
                            inputs = calc['inputs']
                            st.write(f"**Discount Rate:** {inputs.get('discount_rate', 0)*100:.1f}%")
                            st.write(f"**Terminal Growth:** {inputs.get('terminal_growth', 0)*100:.1f}%")
                        elif calc['method'] == "Market Multiples":
                            inputs = calc['inputs']
                            st.write(f"**Sector:** {inputs.get('sector', 'N/A')}")
                            st.write(f"**Multiple:** {inputs.get('multiple', 0):.1f}x")
                        elif calc['method'] == "Berkus":
                            result = calc['result']
                            achievement = (result.get('valuation', 0) / result.get('max_possible', 1)) * 100
                            st.write(f"**Achievement Rate:** {achievement:.1f}%")
                        elif calc['method'] == "Scorecard":
                            result = calc['result']
                            st.write(f"**Base Valuation:** {format_currency(result.get('base_valuation', 0))}")
                            st.write(f"**Adjustment Factor:** {result.get('adjustment_factor', 0):.2f}x")
                        elif calc['method'] == "Risk Factor Summation":
                            result = calc['result']
                            st.write(f"**Base Valuation:** {format_currency(result.get('base_valuation', 0))}")
                            st.write(f"**Risk Adjustment:** {result.get('total_adjustment', 0):+.1%}")
                        elif calc['method'] == "Venture Capital":
                            result = calc['result']
                            st.write(f"**Exit Value:** {format_currency(result.get('exit_value', 0))}")
                            st.write(f"**Present Value:** {format_currency(result.get('present_value', 0))}")
                    
                    with col_delete:
                        if st.button("🗑️", key=f"delete_{calc.get('id', i)}", help="Delete this calculation"):
                            # Remove this calculation from history
                            original_index = len(st.session_state.calculation_history) - 1 - i
                            del st.session_state.calculation_history[original_index]
                            st.rerun()
        
        with col2:
            if st.button("🗑️ Clear All History"):
                st.session_state.calculation_history = []
                st.session_state.current_results = {}
                st.rerun()

def generate_pdf_report():
    """Generate and download PDF report"""
    try:
        if not st.session_state.calculation_history:
            st.warning("No calculations available to generate report for. Please perform at least one valuation calculation.")
            return
        
        pdf_gen = PDFGenerator()
        pdf_buffer = pdf_gen.create_report(
            st.session_state.current_results,
            st.session_state.calculation_history
        )
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name=f"valuation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
        
        st.success(f"✅ PDF report generated with {len(st.session_state.calculation_history)} calculation(s)")
        
    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")

def display_export_options():
    """Display export options for multiple formats"""
    if not st.session_state.calculation_history:
        st.info("No calculations available for export. Please perform calculations first.")
        return
    
    export_manager = ExportManager()
    
    # Export format selection
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox(
            "Select Export Format",
            options=['csv', 'excel', 'json', 'xml', 'txt'],
            format_func=lambda x: {
                'csv': 'CSV (Comma Separated Values)',
                'excel': 'Excel Spreadsheet (.xlsx)',
                'json': 'JSON (JavaScript Object Notation)',
                'xml': 'XML (Extensible Markup Language)',
                'txt': 'Plain Text Report'
            }[x]
        )
    
    with col2:
        include_charts = st.checkbox("Include Chart Data", value=False)
    
    # Export options
    st.write("**Export Options:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export All Calculations"):
            try:
                export_buffer = export_manager.export_calculation_data(
                    st.session_state.calculation_history,
                    export_format,
                    include_charts
                )
                
                file_extensions = {
                    'csv': 'csv',
                    'excel': 'xlsx',
                    'json': 'json',
                    'xml': 'xml',
                    'txt': 'txt'
                }
                
                mime_types = {
                    'csv': 'text/csv',
                    'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'json': 'application/json',
                    'xml': 'application/xml',
                    'txt': 'text/plain'
                }
                
                st.download_button(
                    label=f"💾 Download {export_format.upper()} File",
                    data=export_buffer.getvalue(),
                    file_name=f"valuation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extensions[export_format]}",
                    mime=mime_types[export_format]
                )
                
                st.success(f"✅ {export_format.upper()} export prepared with {len(st.session_state.calculation_history)} calculations")
                
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    with col2:
        if st.button("📈 Export Current Results"):
            if st.session_state.current_results:
                try:
                    export_buffer = export_manager.export_single_calculation(
                        st.session_state.current_results,
                        export_format,
                        include_charts
                    )
                    
                    file_extensions = {
                        'csv': 'csv',
                        'excel': 'xlsx', 
                        'json': 'json',
                        'xml': 'xml',
                        'txt': 'txt'
                    }
                    
                    mime_types = {
                        'csv': 'text/csv',
                        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'json': 'application/json',
                        'xml': 'application/xml',
                        'txt': 'text/plain'
                    }
                    
                    st.download_button(
                        label=f"💾 Download Current {export_format.upper()}",
                        data=export_buffer.getvalue(),
                        file_name=f"current_valuation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extensions[export_format]}",
                        mime=mime_types[export_format]
                    )
                    
                    st.success(f"✅ Current calculation exported as {export_format.upper()}")
                    
                except Exception as e:
                    st.error(f"Export failed: {str(e)}")
            else:
                st.warning("No current calculation to export. Please perform a calculation first.")
    
    with col3:
        if st.button("🔍 Export Comparison Report"):
            if len(st.session_state.calculation_history) >= 2:
                try:
                    export_buffer = export_manager.export_comparison_report(
                        st.session_state.calculation_history,
                        'excel'  # Comparison reports work best in Excel
                    )
                    
                    st.download_button(
                        label="💾 Download Comparison Report",
                        data=export_buffer.getvalue(),
                        file_name=f"valuation_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    st.success("✅ Comparison report prepared with statistical analysis")
                    
                except Exception as e:
                    st.error(f"Comparison export failed: {str(e)}")
            else:
                st.warning("Need at least 2 calculations for comparison report.")
    
    # Export metadata
    with st.expander("📋 Export Information"):
        metadata = export_manager.get_export_metadata(st.session_state.calculation_history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Calculations", metadata['total_calculations'])
            st.metric("Successful Calculations", metadata['successful_calculations'])
            
        with col2:
            st.metric("Failed Calculations", metadata['failed_calculations'])
            st.write("**Methods Used:**", ", ".join(metadata['methods_used']))
        
        if metadata['date_range']['earliest']:
            st.write("**Date Range:**")
            st.write(f"From: {metadata['date_range']['earliest']}")
            st.write(f"To: {metadata['date_range']['latest']}")

if __name__ == "__main__":
    main()
