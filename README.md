# Startup Valuation Calculator

A comprehensive Streamlit-based application for calculating startup valuations using multiple professional methodologies. This tool provides detailed financial analysis, interactive charts, and professional PDF reporting capabilities.

## 🚀 Features

### Valuation Methods
- **DCF (Discounted Cash Flow)**: Calculate intrinsic value based on projected cash flows
- **Market Multiples**: Compare valuation using industry benchmarks
- **Scorecard Method**: Evaluate startups against key criteria
- **Berkus Method**: Pre-revenue startup valuation approach
- **Risk Factor Summation**: Adjust valuations based on risk assessment
- **Venture Capital Method**: Calculate present value from projected exit scenarios

### Key Capabilities
- **Interactive Charts**: Real-time visualization using Plotly
- **PDF Reports**: Professional reports with embedded charts and data tables
- **Calculation History**: Track and compare multiple valuations
- **Data Validation**: Comprehensive input validation with helpful error messages
- **Export Functionality**: Download detailed PDF reports

## 📋 Prerequisites

- Python 3.11 or higher
- Streamlit
- Required Python packages (see requirements below)

## 🛠️ Installation

1. Clone or download the project files
2. Install required packages:
   ```bash
   pip install streamlit pandas numpy plotly reportlab pillow
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📖 User Guide

### Getting Started

1. **Launch the Application**: Run `streamlit run app.py` in your terminal
2. **Select Valuation Method**: Choose from the sidebar menu
3. **Enter Data**: Fill in the required fields for your chosen method
4. **Calculate**: Click the calculation button to generate results
5. **Review Results**: Examine charts, metrics, and analysis
6. **Generate Reports**: Use the calculation history to create PDF reports

### Valuation Methods Guide

#### DCF (Discounted Cash Flow)
**Best for**: Companies with predictable cash flows
**Inputs**:
- Cash flow projections (3-10 years)
- Discount rate (WACC) - typically 8-25%
- Terminal growth rate - typically 0-5%

**Tips**:
- Ensure discount rate > terminal growth rate
- Use conservative growth assumptions
- Consider multiple scenarios

#### Market Multiples
**Best for**: Companies with comparable public companies
**Inputs**:
- Industry sector selection
- Financial metric (Revenue/EBITDA)
- Metric value
- Industry multiple

**Tips**:
- Research current market conditions
- Use recent transaction data
- Consider company stage and growth

#### Scorecard Method
**Best for**: Early-stage startups with limited financial history
**Inputs**:
- Base valuation (comparable company)
- Criteria scores (0-5 scale):
  - Management team quality
  - Market opportunity size
  - Product/technology
  - Competitive environment
  - Marketing/sales channels
  - Funding requirements
  - Exit potential

**Tips**:
- Be realistic in scoring
- Compare against similar stage companies
- Weight criteria based on importance

#### Berkus Method
**Best for**: Pre-revenue startups
**Inputs**:
- Criteria scores (0-5 scale):
  - Basic value (concept quality)
  - Technology risk
  - Execution risk
  - Core relationships
  - Production/market risk

**Maximum Values**:
- Each criterion: $500K maximum
- Total valuation: $2.5M maximum

#### Risk Factor Summation
**Best for**: Adjusting valuations based on specific risks
**Inputs**:
- Base valuation
- Risk factor ratings (-2 to +2):
  - Management quality
  - Development stage
  - Legislative/political risk
  - Manufacturing risk
  - Sales/marketing risk
  - Funding/capital risk
  - Competition risk
  - Technology risk
  - Litigation risk
  - International risk
  - Reputation risk
  - Exit potential

#### Venture Capital Method
**Best for**: VC investment scenarios
**Inputs**:
- Expected revenue at exit
- Exit multiple (revenue multiple)
- Required annual return rate
- Years to exit (typically 3-7 years)
- Investment amount (optional)

## 🔍 Understanding Results

### Metrics Displayed
- **Valuation**: Primary output value
- **Supporting Metrics**: Method-specific calculations
- **Charts**: Visual representation of data and results

### PDF Reports
Generated reports include:
- Executive summary
- Detailed methodology explanation
- Visual charts and data tables
- Calculation history comparison
- Professional formatting for sharing

## ⚠️ Important Considerations

### Data Quality
- Ensure all inputs are realistic and well-researched
- Use current market data when available
- Consider multiple scenarios and methods

### Limitations
- Valuations are estimates based on assumptions
- Market conditions change rapidly
- Multiple methods should be used for validation
- Professional advice recommended for significant decisions

### Best Practices
- **Use Multiple Methods**: Compare results across different approaches
- **Document Assumptions**: Keep records of your input rationale
- **Regular Updates**: Refresh valuations as data changes
- **Sensitivity Analysis**: Test how changes affect valuations

## 🔧 Technical Features

### Data Validation
- Comprehensive input validation
- Range checking and business logic validation
- Warning messages for unusual values
- Suggested corrections for invalid inputs

### Calculation History
- Automatic saving of all calculations
- Comparison across different methods
- Chart visualization in history
- Bulk PDF report generation

### Export Capabilities
- Professional PDF reports
- Embedded charts and visualizations
- Detailed data tables
- Company-ready formatting

## 📊 Example Workflows

### Technology Startup Valuation
1. Start with **Scorecard Method** for initial assessment
2. Use **Berkus Method** if pre-revenue
3. Apply **DCF Method** once projections are available
4. Validate with **Market Multiples** using tech sector data
5. Generate comprehensive PDF report

### Investment Decision Analysis
1. Use **Venture Capital Method** for target returns
2. Apply **Risk Factor Summation** for risk adjustment
3. Compare with **Market Multiples** for reality check
4. Document all assumptions and scenarios

## 🚨 Troubleshooting

### Common Issues
- **Calculation Errors**: Check that discount rate > terminal growth rate
- **Large Values**: Verify input units (thousands vs millions)
- **PDF Generation**: Ensure all calculations are completed first
- **Missing Charts**: Refresh the page and recalculate

### Validation Messages
- **Red (Errors)**: Must be fixed before calculation
- **Yellow (Warnings)**: Review but calculation can proceed
- **Blue (Info)**: Additional context or suggestions

## 📈 Advanced Usage

### Custom Weightings
- Scorecard method supports custom criteria weights
- Ensure weights sum to 100%
- Adjust based on company-specific factors

### Scenario Analysis
- Run multiple calculations with different assumptions
- Use calculation history to compare scenarios
- Generate reports showing sensitivity to key variables

### Integration Tips
- Export data for further analysis
- Use results as input to financial models
- Combine with other due diligence processes

## 🤝 Support

For questions or issues:
- Review input validation messages
- Check calculation assumptions
- Ensure all required fields are completed
- Verify data ranges and formats

## 📝 Version History

### Current Version
- Six valuation methods implemented
- Interactive Plotly charts
- Professional PDF reporting
- Comprehensive data validation
- Calculation history tracking

---

*This tool is designed for educational and analytical purposes. Professional financial advice should be sought for investment decisions.*