# API Reference - Startup Valuation Calculator

## Core Classes and Methods

### ValuationCalculator

The main calculation engine for all valuation methods.

#### Constructor
```python
calculator = ValuationCalculator()
```

#### Methods

##### dcf_valuation()
```python
def dcf_valuation(
    cash_flows: List[float], 
    growth_rate: float, 
    discount_rate: float, 
    terminal_growth: float = 0.02
) -> Dict[str, Any]
```

**Parameters:**
- `cash_flows` (List[float]): Projected cash flows for each year
- `growth_rate` (float): Legacy parameter, not used in calculation
- `discount_rate` (float): Discount rate (WACC) as decimal (e.g., 0.12 for 12%)
- `terminal_growth` (float): Terminal growth rate as decimal (default: 0.02)

**Returns:**
```python
{
    'success': True,
    'valuation': 5000000.0,
    'operating_value': 3000000.0,
    'terminal_value': 4000000.0,
    'terminal_pv': 2000000.0,
    'method': 'DCF',
    'cash_flows': [100000, 150000, 200000, 250000, 300000],
    'pv_cash_flows': [89285.71, 119642.86, 142045.45, 158945.91, 170535.71]
}
```

##### market_multiples_valuation()
```python
def market_multiples_valuation(
    revenue_or_ebitda: float, 
    multiple: float, 
    metric_type: str = "Revenue"
) -> Dict[str, Any]
```

**Parameters:**
- `revenue_or_ebitda` (float): Financial metric value
- `multiple` (float): Industry multiple
- `metric_type` (str): Type of metric ("Revenue", "EBITDA", "EBIT", "Net Income")

**Returns:**
```python
{
    'success': True,
    'valuation': 10000000.0,
    'metric': 2000000.0,
    'multiple': 5.0,
    'metric_type': 'Revenue',
    'method': 'Market Multiples'
}
```

##### scorecard_valuation()
```python
def scorecard_valuation(
    base_valuation: float, 
    criteria_scores: Dict[str, int], 
    criteria_weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `base_valuation` (float): Base valuation amount
- `criteria_scores` (Dict[str, int]): Scores for each criterion (0-5)
- `criteria_weights` (Optional[Dict[str, float]]): Custom weights (sum must equal 1.0)

**Returns:**
```python
{
    'success': True,
    'valuation': 2200000.0,
    'base_valuation': 2000000.0,
    'adjustment_factor': 1.1,
    'total_adjustment': 0.1,
    'criteria_analysis': {
        'management': {'score': 4, 'weight': 0.25, 'adjustment': 0.05},
        # ... other criteria
    },
    'method': 'Scorecard'
}
```

##### berkus_valuation()
```python
def berkus_valuation(criteria_scores: Dict[str, int]) -> Dict[str, Any]
```

**Parameters:**
- `criteria_scores` (Dict[str, int]): Berkus criteria scores (0-5)

**Returns:**
```python
{
    'success': True,
    'valuation': 1500000.0,
    'breakdown': {
        'basic_value': {'score': 4, 'value': 400000, 'name': 'Basic Value'},
        'technology': {'score': 3, 'value': 300000, 'name': 'Technology Risk'},
        # ... other criteria
    },
    'method': 'Berkus'
}
```

##### risk_factor_summation()
```python
def risk_factor_summation(
    base_valuation: float, 
    risk_factors: Dict[str, int]
) -> Dict[str, Any]
```

**Parameters:**
- `base_valuation` (float): Starting valuation amount
- `risk_factors` (Dict[str, int]): Risk ratings (-2 to +2)

**Returns:**
```python
{
    'success': True,
    'valuation': 1800000.0,
    'base_valuation': 2000000.0,
    'total_adjustment': -0.1,
    'risk_analysis': {
        'management': {'rating': 1, 'adjustment': 0.05, 'name': 'Management'},
        # ... other risk factors
    },
    'method': 'Risk Factor Summation'
}
```

##### venture_capital_method()
```python
def venture_capital_method(
    expected_revenue: float,
    exit_multiple: float,
    required_return: float,
    years_to_exit: int = 5,
    investment_needed: Optional[float] = None
) -> Dict[str, Any]
```

**Parameters:**
- `expected_revenue` (float): Expected revenue at exit
- `exit_multiple` (float): Revenue multiple at exit
- `required_return` (float): Required annual return as decimal
- `years_to_exit` (int): Years until exit (default: 5)
- `investment_needed` (Optional[float]): Investment amount

**Returns:**
```python
{
    'success': True,
    'valuation': 8000000.0,
    'exit_value': 50000000.0,
    'present_value': 8000000.0,
    'required_return': 0.25,
    'years_to_exit': 5,
    'investment_analysis': {
        'ownership_required': 0.125,
        'pre_money': 7000000.0,
        'post_money': 8000000.0
    },
    'method': 'Venture Capital'
}
```

### ChartGenerator

Creates interactive Plotly charts for visualization.

#### Constructor
```python
chart_gen = ChartGenerator()
```

#### Methods

##### create_dcf_chart()
```python
def create_dcf_chart(result: Dict, cash_flows: List[float]) -> go.Figure
```

**Parameters:**
- `result` (Dict): DCF calculation results
- `cash_flows` (List[float]): Input cash flow projections

**Returns:** Plotly Figure object with DCF visualization

##### create_multiples_chart()
```python
def create_multiples_chart(result: Dict, sector: str) -> go.Figure
```

**Parameters:**
- `result` (Dict): Market multiples results
- `sector` (str): Industry sector

**Returns:** Plotly Figure object with sector comparison

##### create_scorecard_chart()
```python
def create_scorecard_chart(result: Dict) -> go.Figure
```

**Parameters:**
- `result` (Dict): Scorecard calculation results

**Returns:** Plotly Figure object with radar chart

##### create_berkus_chart()
```python
def create_berkus_chart(result: Dict) -> go.Figure
```

**Parameters:**
- `result` (Dict): Berkus method results

**Returns:** Plotly Figure object with value breakdown

##### create_risk_factor_chart()
```python
def create_risk_factor_chart(result: Dict) -> go.Figure
```

**Parameters:**
- `result` (Dict): Risk factor analysis results

**Returns:** Plotly Figure object with risk visualization

##### create_vc_method_chart()
```python
def create_vc_method_chart(result: Dict, include_investment: bool) -> go.Figure
```

**Parameters:**
- `result` (Dict): VC method results
- `include_investment` (bool): Whether to include investment analysis

**Returns:** Plotly Figure object with VC analysis

### PDFGenerator

Generates comprehensive PDF reports.

#### Constructor
```python
pdf_gen = PDFGenerator()
```

#### Methods

##### create_report()
```python
def create_report(
    current_results: Dict, 
    calculation_history: List[Dict]
) -> BytesIO
```

**Parameters:**
- `current_results` (Dict): Current calculation results
- `calculation_history` (List[Dict]): Historical calculations

**Returns:** BytesIO buffer containing PDF data

### ValidationManager

Handles input validation across all methods.

#### Constructor
```python
validator = ValidationManager()
```

#### Methods

##### validate_method_inputs()
```python
def validate_method_inputs(method: str, data: Dict[str, Any]) -> ValidationResult
```

**Parameters:**
- `method` (str): Valuation method name
- `data` (Dict): Input data to validate

**Returns:**
```python
ValidationResult(
    is_valid=True,
    messages=[],
    sanitized_data={'cash_flows': [100000, 150000], 'discount_rate': 0.12}
)
```

##### get_method_requirements()
```python
def get_method_requirements(method: str) -> Dict[str, Any]
```

**Parameters:**
- `method` (str): Valuation method name

**Returns:** Dictionary with field requirements and types

## Utility Functions

### Currency Formatting
```python
def format_currency(amount: Union[float, int], precision: int = 0) -> str
```

**Example:**
```python
format_currency(1500000)  # Returns "€1.5M"
format_currency(750000)   # Returns "€750K"
```

### Percentage Formatting
```python
def format_percentage(value: Union[float, int], precision: int = 1) -> str
```

**Example:**
```python
format_percentage(0.15)  # Returns "15.0%"
```

### Validation Functions
```python
def validate_positive_number(value: Any, field_name: str) -> tuple[bool, str]
def validate_range(value: Any, min_val: float, max_val: float, field_name: str) -> tuple[bool, str]
```

### Financial Calculations
```python
def calculate_npv(cash_flows: List[float], discount_rate: float, initial_investment: float = 0) -> float
def calculate_irr(cash_flows: List[float], initial_investment: float, max_iterations: int = 100) -> Optional[float]
```

## Error Handling

### Standard Error Response
All calculation methods return errors in a consistent format:

```python
{
    'success': False,
    'error': 'Detailed error message',
    'method': 'Method Name',
    'valuation': 0
}
```

### Validation Error Response
```python
ValidationResult(
    is_valid=False,
    messages=[
        ValidationMessage(
            field='discount_rate',
            message='Discount rate must be higher than terminal growth rate',
            severity=ValidationSeverity.ERROR,
            code='RATE_RELATIONSHIP_ERROR'
        )
    ],
    sanitized_data=None
)
```

## Constants and Enums

### Sector Multiples
```python
SECTOR_MULTIPLES = {
    'Technology': {'Revenue': 6.5, 'EBITDA': 15.2},
    'Healthcare': {'Revenue': 4.2, 'EBITDA': 12.8},
    # ... additional sectors
}
```

### Scorecard Criteria
```python
SCORECARD_CRITERIA = {
    'management': {'name': 'Management Team', 'weight': 0.25},
    'opportunity': {'name': 'Market Opportunity', 'weight': 0.25},
    # ... additional criteria
}
```

### Berkus Criteria
```python
BERKUS_CRITERIA = {
    'basic_value': {'name': 'Basic Value', 'max_value': 500000},
    'technology': {'name': 'Technology Risk', 'max_value': 500000},
    # ... additional criteria
}
```

### Risk Factors
```python
RISK_FACTORS = {
    'management': {'name': 'Management', 'description': 'Quality and experience of management team'},
    'stage': {'name': 'Stage of Business', 'description': 'Development and operational stage'},
    # ... additional factors
}
```

## Usage Examples

### Basic DCF Calculation
```python
from valuation_calculator import ValuationCalculator

calculator = ValuationCalculator()
cash_flows = [100000, 150000, 200000, 250000, 300000]
result = calculator.dcf_valuation(
    cash_flows=cash_flows,
    growth_rate=0,  # Legacy parameter
    discount_rate=0.12,
    terminal_growth=0.03
)

if result['success']:
    print(f"Valuation: {result['valuation']:,.0f}")
```

### Validation Example
```python
from validation_schemas import ValidationManager

validator = ValidationManager()
data = {
    'cash_flows': [100000, 150000, 200000],
    'discount_rate': 0.12,
    'terminal_growth': 0.03
}

validation_result = validator.validate_method_inputs('DCF', data)
if validation_result.is_valid:
    print("Validation passed")
else:
    for error in validation_result.get_errors():
        print(f"Error: {error.message}")
```

### Chart Generation Example
```python
from chart_generator import ChartGenerator

chart_gen = ChartGenerator()
fig = chart_gen.create_dcf_chart(result, cash_flows)
fig.show()  # Display in Jupyter/browser
```

### PDF Generation Example
```python
from pdf_generator import PDFGenerator

pdf_gen = PDFGenerator()
current_results = {'method': 'DCF', 'result': result}
calculation_history = [current_results]

pdf_buffer = pdf_gen.create_report(current_results, calculation_history)
with open('valuation_report.pdf', 'wb') as f:
    f.write(pdf_buffer.getvalue())
```

---

*This API reference provides comprehensive documentation for developers integrating with or extending the Startup Valuation Calculator.*