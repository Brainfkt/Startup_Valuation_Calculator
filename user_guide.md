# Startup Valuation Calculator - User Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Valuation Methods](#valuation-methods)
3. [Step-by-Step Tutorials](#step-by-step-tutorials)
4. [Understanding Results](#understanding-results)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### First Time Setup
1. Open your web browser and navigate to the application
2. The application loads with the DCF method selected by default
3. Use the sidebar to switch between different valuation methods
4. Each method has specific input requirements - follow the on-screen guidance

### Basic Workflow
1. **Choose Method**: Select the most appropriate valuation method for your startup
2. **Enter Data**: Fill in all required fields with accurate information
3. **Validate**: Check that all inputs pass validation (green checkmarks)
4. **Calculate**: Click the calculation button to generate results
5. **Analyze**: Review charts, metrics, and detailed breakdowns
6. **Export**: Generate PDF reports for documentation and sharing

## Valuation Methods

### 1. DCF (Discounted Cash Flow)
**When to use**: For startups with reliable revenue projections and established business models

**Required Inputs**:
- **Cash Flow Projections**: Enter expected cash flows for 3-10 years
- **Discount Rate (WACC)**: The weighted average cost of capital (typically 8-25%)
- **Terminal Growth Rate**: Long-term growth assumption (typically 0-5%)

**Key Rules**:
- Discount rate must be higher than terminal growth rate
- Cash flows can be negative in early years
- Consider multiple scenarios (conservative, optimistic, pessimistic)

**Example Use Case**:
A SaaS startup with 2 years of revenue history and clear subscription metrics.

### 2. Market Multiples
**When to use**: When comparable companies exist in your industry

**Required Inputs**:
- **Sector**: Choose your industry from the dropdown
- **Metric Type**: Revenue, EBITDA, EBIT, or Net Income
- **Metric Value**: Your company's actual metric value
- **Multiple**: Industry multiple (research current market rates)

**Key Rules**:
- Use recent transaction data for multiples
- Ensure comparability with selected companies
- Consider company stage and growth differences

**Example Use Case**:
A fintech startup comparing against recent acquisitions in the financial services sector.

### 3. Scorecard Method
**When to use**: For early-stage startups without extensive financial history

**Required Inputs**:
- **Base Valuation**: Typical valuation for similar companies in your region
- **Criteria Scores**: Rate your company (0-5) on:
  - Management team quality
  - Market opportunity size
  - Product/technology strength
  - Competitive environment
  - Marketing/sales capability
  - Funding requirements
  - Exit potential

**Key Rules**:
- Be honest and realistic in scoring
- Use local market data for base valuation
- Consider getting external validation of scores

**Example Use Case**:
A pre-seed biotech startup seeking angel investment.

### 4. Berkus Method
**When to use**: Specifically for pre-revenue startups

**Required Inputs**:
- **Criteria Scores**: Rate your company (0-5) on:
  - Basic value (strength of business concept)
  - Technology risk mitigation
  - Execution risk mitigation
  - Core relationships in place
  - Production and market risk mitigation

**Key Rules**:
- Maximum $500K value per criterion
- Total valuation capped at $2.5M
- Focus on risk mitigation rather than potential

**Example Use Case**:
A tech startup with a prototype but no revenue yet.

### 5. Risk Factor Summation
**When to use**: To adjust existing valuations based on specific risk factors

**Required Inputs**:
- **Base Valuation**: Starting valuation from another method
- **Risk Factor Ratings**: Rate each factor from -2 (high risk) to +2 (low risk):
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

**Key Rules**:
- Use as a secondary validation method
- Focus on company-specific risks
- Be conservative in positive ratings

**Example Use Case**:
Adjusting a DCF valuation for a startup in a highly regulated industry.

### 6. Venture Capital Method
**When to use**: When evaluating investment opportunities with clear exit strategies

**Required Inputs**:
- **Expected Revenue at Exit**: Projected revenue in exit year
- **Exit Multiple**: Revenue multiple at exit (research industry standards)
- **Required Return Rate**: Annual return expectation (typically 25-50%)
- **Years to Exit**: Time horizon for exit (typically 3-7 years)
- **Investment Amount**: (Optional) Amount being invested

**Key Rules**:
- Use realistic exit scenarios
- Consider current market conditions
- Factor in dilution from future rounds

**Example Use Case**:
A VC firm evaluating a Series A investment opportunity.

## Step-by-Step Tutorials

### Tutorial 1: DCF Valuation for SaaS Startup

**Scenario**: 3-year-old SaaS company with $2M ARR growing 50% annually

**Step 1**: Prepare Your Data
- Gather historical financial statements
- Create realistic growth projections
- Research industry discount rates

**Step 2**: Enter Cash Flow Projections
```
Year 1: $800,000 (40% of revenue as cash flow)
Year 2: $1,200,000
Year 3: $1,600,000
Year 4: $2,000,000
Year 5: $2,400,000
```

**Step 3**: Set Parameters
- Discount Rate: 15% (based on industry standards)
- Terminal Growth: 3% (conservative long-term growth)

**Step 4**: Calculate and Analyze
- Review the operating vs terminal value split
- Check sensitivity to key assumptions
- Compare against industry benchmarks

### Tutorial 2: Scorecard Method for Early-Stage Startup

**Scenario**: Pre-seed healthcare startup with experienced team

**Step 1**: Research Base Valuation
- Look up typical pre-seed valuations in your region
- Consider recent angel round data
- Use $2M as base valuation

**Step 2**: Score Each Criterion (0-5 scale)
- Management: 4 (experienced healthcare professionals)
- Opportunity: 4 (large addressable market)
- Product: 3 (prototype developed, needs refinement)
- Competition: 3 (moderate competitive landscape)
- Marketing: 2 (limited marketing experience)
- Funding: 3 (clear funding path)
- Valuation: 3 (reasonable exit potential)

**Step 3**: Calculate and Review
- Total adjustment factor calculated
- Final valuation derived
- Compare with similar companies

### Tutorial 3: Market Multiples for Tech Acquisition

**Scenario**: Established tech company being acquired

**Step 1**: Identify Comparable Companies
- Research recent acquisitions in your sector
- Find companies of similar size and growth
- Collect multiple data points

**Step 2**: Choose Appropriate Metric
- Use Revenue multiples for high-growth companies
- Use EBITDA for profitable companies
- Consider industry standards

**Step 3**: Apply Multiple
- Current Revenue: $10M
- Industry Multiple: 4.5x
- Valuation: $45M

**Step 4**: Validate Results
- Compare with other valuation methods
- Consider premium/discount factors
- Adjust for market conditions

## Understanding Results

### Key Metrics Explained

**DCF Results**:
- **Total Valuation**: Sum of operating value and terminal value
- **Operating Value**: Present value of projected cash flows
- **Terminal Value**: Present value of cash flows beyond projection period
- **Value Split**: Shows relative importance of near-term vs long-term value

**Market Multiples Results**:
- **Valuation**: Metric value × Multiple
- **Implied Multiple**: Reverse calculation for validation
- **Sector Comparison**: How your multiple compares to industry

**Scorecard Results**:
- **Adjusted Valuation**: Base valuation × Adjustment factor
- **Factor Breakdown**: Impact of each criterion
- **Score Analysis**: Strengths and weaknesses identified

### Chart Interpretations

**DCF Pie Chart**:
- Shows proportion of value from operations vs terminal value
- Higher terminal value % indicates longer payback period
- Balanced split suggests stable business model

**Bar Charts**:
- Compare different metrics or time periods
- Color coding indicates performance levels
- Height represents relative values

**Risk Factor Charts**:
- Positive bars = risk mitigation factors
- Negative bars = risk enhancement factors
- Length indicates impact magnitude

## Best Practices

### Data Quality
1. **Use Recent Data**: Financial projections should be current
2. **Validate Assumptions**: Cross-check with industry data
3. **Document Sources**: Keep records of where data came from
4. **Multiple Scenarios**: Run optimistic, realistic, and pessimistic cases

### Method Selection
1. **Company Stage**: Use appropriate method for development stage
2. **Data Availability**: Choose methods that match available information
3. **Industry Standards**: Follow common practices in your sector
4. **Multiple Methods**: Use 2-3 methods for validation

### Result Interpretation
1. **Range of Values**: Present results as ranges, not single points
2. **Sensitivity Analysis**: Test how changes affect valuation
3. **Market Context**: Consider current market conditions
4. **Qualitative Factors**: Include non-quantifiable elements

### Documentation
1. **Assumption Records**: Document all key assumptions
2. **Source Citations**: Reference data sources
3. **Methodology Notes**: Explain why methods were chosen
4. **Update Schedule**: Plan for regular valuation updates

## Troubleshooting

### Common Validation Errors

**"Discount rate must be higher than terminal growth rate"**
- Solution: Increase discount rate or decrease terminal growth
- Explanation: Prevents mathematical inconsistencies

**"Value must be a valid number"**
- Solution: Check for text characters or formatting issues
- Tip: Use numbers only, no currency symbols

**"Very large value detected"**
- Solution: Verify input units (thousands vs millions)
- Check: Ensure realistic order of magnitude

### Calculation Issues

**Results seem too high/low**:
1. Double-check input units
2. Verify industry benchmarks
3. Review assumption reasonableness
4. Compare with other methods

**Charts not displaying**:
1. Refresh the page
2. Complete all required fields
3. Check browser compatibility
4. Clear browser cache

**PDF generation fails**:
1. Ensure calculations are completed
2. Check that charts loaded properly
3. Wait for all data to process
4. Try generating again

### Data Input Tips

**Cash Flow Projections**:
- Start with revenue projections
- Apply realistic margin assumptions
- Consider working capital changes
- Include capital expenditures

**Growth Rates**:
- Research industry averages
- Consider company lifecycle stage
- Factor in market saturation
- Use conservative long-term rates

**Multiples**:
- Use recent transaction data
- Adjust for company differences
- Consider market conditions
- Validate with multiple sources

### Getting Help

**Input Validation**:
- Red messages: Must fix before proceeding
- Yellow messages: Warnings to review
- Blue messages: Helpful information

**Result Review**:
- Compare across multiple methods
- Check against industry benchmarks
- Validate key assumptions
- Consider qualitative factors

**Professional Guidance**:
- Complex valuations may require expert advice
- Consider hiring valuation professionals
- Use results as starting point for discussions
- Regular updates recommended as business evolves

---

*Remember: Valuations are estimates based on assumptions. Use multiple methods and seek professional advice for important decisions.*