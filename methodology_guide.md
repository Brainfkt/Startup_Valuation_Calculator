# Valuation Methodology Guide

## Introduction

This guide provides detailed explanations of the six valuation methodologies implemented in the Startup Valuation Calculator. Each method serves different purposes and is appropriate for different stages of company development and types of analysis.

## 1. Discounted Cash Flow (DCF) Method

### Overview
The DCF method calculates the intrinsic value of a company based on projected future cash flows, discounted back to present value using an appropriate discount rate.

### Mathematical Foundation
```
PV = Σ(CFt / (1 + r)^t) + TV / (1 + r)^n

Where:
- PV = Present Value
- CFt = Cash Flow in period t
- r = Discount rate (WACC)
- TV = Terminal Value
- n = Number of projection periods
```

### Terminal Value Calculation
```
TV = CF(n+1) / (r - g)

Where:
- CF(n+1) = Cash flow in first year beyond projection period
- g = Terminal growth rate
```

### When to Use
- Companies with predictable cash flows
- Established business models
- Sufficient historical data for projections
- Long-term investment decisions

### Key Assumptions
- **Cash Flow Projections**: Based on realistic business fundamentals
- **Discount Rate**: Reflects company's risk profile and cost of capital
- **Terminal Growth**: Conservative long-term growth assumption
- **Perpetuity**: Company continues operating indefinitely

### Advantages
- Based on fundamental business value
- Considers time value of money
- Flexible for scenario analysis
- Widely accepted in financial markets

### Limitations
- Highly sensitive to assumptions
- Requires detailed financial projections
- Difficult for early-stage companies
- Terminal value often dominates total value

### Best Practices
- Use multiple scenarios (conservative, base, optimistic)
- Sensitivity analysis on key variables
- Regular assumption updates
- Cross-validation with other methods

## 2. Market Multiples Method

### Overview
Values companies based on multiples derived from comparable public companies or recent transactions in the same industry.

### Mathematical Foundation
```
Valuation = Company Metric × Industry Multiple

Common Multiples:
- Revenue Multiple = Enterprise Value / Revenue
- EBITDA Multiple = Enterprise Value / EBITDA
- P/E Ratio = Market Cap / Net Income
```

### When to Use
- Sufficient comparable companies exist
- Active M&A market in the sector
- Established companies with standard metrics
- Quick valuation estimates needed

### Key Considerations
- **Comparability**: Companies must be truly similar
- **Market Conditions**: Multiples reflect current market sentiment
- **Size Differences**: May require adjustments for scale
- **Growth Differences**: High-growth companies command premiums

### Advantages
- Market-based and current
- Quick and straightforward
- Reflects investor sentiment
- Useful for reality checks

### Limitations
- Assumes market efficiency
- Limited comparable companies
- Market timing effects
- May not reflect intrinsic value

### Implementation Steps
1. Identify comparable companies
2. Calculate relevant multiples
3. Select appropriate multiple range
4. Apply to company metrics
5. Adjust for differences

## 3. Scorecard Method

### Overview
Evaluates startups by comparing key success factors against typical companies in the region, adjusting a base valuation based on relative strengths and weaknesses.

### Mathematical Foundation
```
Adjusted Valuation = Base Valuation × Σ(Factor Weight × Score Adjustment)

Score Adjustment = (Company Score / Average Score) - 1
```

### Evaluation Criteria
1. **Management Team** (0-30%): Experience, track record, completeness
2. **Market Opportunity** (0-25%): Size, growth, timing
3. **Product/Technology** (0-15%): Uniqueness, IP, development stage
4. **Competitive Environment** (0-10%): Barriers, differentiation
5. **Marketing/Sales** (0-10%): Strategy, channels, traction
6. **Funding Requirements** (0-5%): Capital efficiency, funding path
7. **Exit Potential** (0-5%): Strategic value, market size

### When to Use
- Early-stage startups
- Limited financial history
- Angel investment decisions
- Pre-seed through Series A

### Scoring Guidelines
- **5 (Excellent)**: Top 10% in region
- **4 (Good)**: Top 25% in region
- **3 (Average)**: Typical for region
- **2 (Below Average)**: Bottom 25% in region
- **1 (Poor)**: Bottom 10% in region

### Advantages
- Appropriate for early-stage companies
- Considers qualitative factors
- Regional market adjustment
- Systematic evaluation process

### Limitations
- Subjective scoring
- Requires accurate base valuation
- Regional variations
- May miss unique factors

## 4. Berkus Method

### Overview
Designed specifically for pre-revenue startups, the Berkus Method assigns monetary values to key risk mitigation factors.

### Value Components
Each component can contribute up to $500,000 to total valuation:

1. **Basic Value** ($0-$500K): Strength of business concept
2. **Technology** ($0-$500K): Technology risk mitigation
3. **Execution** ($0-$500K): Quality of management team
4. **Core Relationships** ($0-$500K): Key partnerships and customers
5. **Production** ($0-$500K): Market and scalability risk mitigation

### Mathematical Foundation
```
Total Valuation = Σ(Component Score × $100,000)

Maximum Valuation = $2,500,000
```

### When to Use
- Pre-revenue startups
- Technology-focused companies
- Seed-stage investments
- Risk assessment needed

### Scoring Criteria
- **5**: Excellent risk mitigation, minimal concerns
- **4**: Good progress, minor risks remain
- **3**: Average development, moderate risks
- **2**: Below average, significant risks
- **1**: Poor development, major risks
- **0**: No progress, extreme risks

### Advantages
- Designed for pre-revenue stage
- Focus on risk mitigation
- Simple and fast
- Conservative valuations

### Limitations
- Capped maximum valuation
- May undervalue high-potential companies
- Subjective assessments
- Limited to early-stage only

## 5. Risk Factor Summation Method

### Overview
Adjusts a base valuation by systematically evaluating specific risk factors that could impact company value.

### Risk Categories
Each factor rated from -2 (high risk) to +2 (low risk):

1. **Management** (-2 to +2): Team quality and experience
2. **Stage of Business** (-2 to +2): Development progress
3. **Legislation/Political Risk** (-2 to +2): Regulatory environment
4. **Manufacturing Risk** (-2 to +2): Production complexities
5. **Sales/Marketing Risk** (-2 to +2): Market penetration ability
6. **Funding/Capital Risk** (-2 to +2): Access to future funding
7. **Competition Risk** (-2 to +2): Competitive threats
8. **Technology Risk** (-2 to +2): Technical feasibility
9. **Litigation Risk** (-2 to +2): Legal exposures
10. **International Risk** (-2 to +2): Global expansion risks
11. **Reputation Risk** (-2 to +2): Brand and reputation factors
12. **Potential Lucrative Exit** (-2 to +2): Exit opportunity quality

### Mathematical Foundation
```
Risk Adjustment = Σ(Risk Factor Rating × 5%)
Adjusted Valuation = Base Valuation × (1 + Risk Adjustment)

Maximum adjustment: ±30% of base valuation
```

### When to Use
- Secondary validation method
- Risk-focused analysis
- Due diligence process
- Scenario planning

### Rating Guidelines
- **+2**: Significantly below average risk
- **+1**: Below average risk
- **0**: Average risk for sector/stage
- **-1**: Above average risk
- **-2**: Significantly above average risk

### Advantages
- Systematic risk assessment
- Flexible adjustment mechanism
- Comprehensive risk coverage
- Useful for sensitivity analysis

### Limitations
- Subjective risk assessments
- Requires accurate base valuation
- May double-count some risks
- Limited by ±30% adjustment range

## 6. Venture Capital Method

### Overview
Calculates the present value of a company based on projected exit value and required investor returns.

### Mathematical Foundation
```
Exit Value = Expected Revenue × Exit Multiple
Present Value = Exit Value / (1 + Required Return)^Years

If investment amount provided:
Post-Money Valuation = Present Value
Ownership Required = Investment / Post-Money Valuation
Pre-Money Valuation = Post-Money - Investment
```

### When to Use
- VC investment analysis
- Growth-stage companies
- Clear exit strategy exists
- Performance milestones defined

### Key Variables
- **Expected Revenue**: Revenue projection at exit
- **Exit Multiple**: Industry-appropriate revenue multiple
- **Required Return**: Annual return expectation (typically 25-50%)
- **Time to Exit**: Years until liquidity event (typically 3-7 years)

### Advantages
- Investor perspective
- Clear return expectations
- Market-based exit assumptions
- Accounts for time value

### Limitations
- Requires exit scenario planning
- Sensitive to assumptions
- May not reflect intrinsic value
- Ignores intermediate value creation

## Comparative Analysis

### Method Selection Framework

| Company Stage | Primary Methods | Secondary Methods |
|---------------|----------------|-------------------|
| Pre-Revenue | Berkus, Scorecard | Risk Factor |
| Early Revenue | Scorecard, DCF | Market Multiples |
| Growth Stage | DCF, VC Method | Market Multiples |
| Established | DCF, Market Multiples | Risk Factor |

### Validation Approach
1. **Primary Method**: Most appropriate for company stage
2. **Secondary Method**: Validation and comparison
3. **Sensitivity Analysis**: Test key assumptions
4. **Range Estimation**: Present results as ranges, not point estimates

### Common Pitfalls
- Over-reliance on single method
- Unrealistic growth assumptions
- Ignoring market conditions
- Insufficient comparable data
- Subjective bias in scoring

## Industry-Specific Considerations

### Technology Startups
- Higher growth expectations
- Platform effects and scalability
- Intellectual property value
- Network effects
- Rapid obsolescence risk

### Healthcare/Biotech
- Regulatory approval risks
- Long development timelines
- High capital requirements
- Patent protection
- Reimbursement considerations

### Consumer Products
- Brand value importance
- Market penetration rates
- Distribution channel access
- Seasonal variations
- Competitive dynamics

### B2B Services
- Customer concentration risk
- Recurring revenue models
- Scalability limitations
- Key personnel dependency
- Contract terms and duration

## Conclusion

Effective startup valuation requires:
- Appropriate method selection based on company stage
- Realistic and well-researched assumptions
- Multiple method validation
- Regular updates as conditions change
- Professional judgment and experience

Remember that all valuations are estimates based on assumptions about future performance. Use these methods as starting points for analysis and decision-making, not as definitive statements of value.

---

*This methodology guide provides the theoretical foundation for the valuation methods. Practical application should always consider specific company circumstances and current market conditions.*