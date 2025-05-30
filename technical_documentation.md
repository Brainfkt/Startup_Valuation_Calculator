# Technical Documentation - Startup Valuation Calculator

## Architecture Overview

### System Components

```
Startup Valuation Calculator
├── app.py                    # Main Streamlit application
├── valuation_calculator.py   # Core calculation engine
├── chart_generator.py        # Interactive chart generation
├── pdf_generator.py          # PDF report creation
├── data_models.py           # Data structures and constants
├── validation_schemas.py     # Input validation system
└── utils.py                 # Utility functions
```

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Charts**: Plotly (interactive visualizations)
- **PDF Generation**: ReportLab (professional reports)
- **Data Processing**: Pandas, NumPy
- **Validation**: Custom validation schemas

## Core Modules

### ValuationCalculator Class

**Location**: `valuation_calculator.py`

**Purpose**: Core calculation engine implementing six valuation methodologies

**Methods**:
- `dcf_valuation()`: Discounted Cash Flow calculations
- `market_multiples_valuation()`: Industry multiple-based valuation
- `scorecard_valuation()`: Criteria-based startup evaluation
- `berkus_valuation()`: Pre-revenue startup valuation
- `risk_factor_summation()`: Risk-adjusted valuations
- `venture_capital_method()`: VC investment analysis

**Input Validation**: Each method includes comprehensive input validation with detailed error messages.

**Return Format**: All methods return standardized dictionaries containing:
```python
{
    'success': bool,
    'valuation': float,
    'method': str,
    'details': dict,
    'error': str (if applicable)
}
```

### ChartGenerator Class

**Location**: `chart_generator.py`

**Purpose**: Creates interactive Plotly charts for each valuation method

**Chart Types**:
- DCF: Cash flow projections and value breakdown
- Market Multiples: Sector comparison charts
- Scorecard: Radar/spider charts for criteria analysis
- Berkus: Value component breakdown
- Risk Factors: Risk assessment visualization
- VC Method: Investment scenario analysis

**Features**:
- Interactive hover information
- Professional styling and colors
- Responsive design for different screen sizes
- Export capabilities for PDF inclusion

### PDFGenerator Class

**Location**: `pdf_generator.py`

**Purpose**: Creates comprehensive PDF reports with embedded charts and data tables

**Report Sections**:
1. **Title Page**: Professional cover with company information
2. **Executive Summary**: Key findings and recommendations
3. **Detailed Analysis**: Method-specific breakdowns
4. **Visual Charts**: ReportLab-generated charts
5. **Data Tables**: Comprehensive input and output tables
6. **Calculation History**: Comparison across methods
7. **Appendices**: Methodology explanations

**Chart Integration**: Uses ReportLab's native graphics engine to recreate charts without external dependencies.

## Data Models

### Core Data Structures

**Location**: `data_models.py`

```python
@dataclass
class ValuationResult:
    method: str
    valuation: float
    success: bool
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

@dataclass
class ValidationResult:
    is_valid: bool
    error_message: str = ""
```

### Industry Data

**Sector Multiples**: Comprehensive database of industry-specific valuation multiples
```python
SECTOR_MULTIPLES = {
    'Technology': {'Revenue': 6.5, 'EBITDA': 15.2},
    'Healthcare': {'Revenue': 4.2, 'EBITDA': 12.8},
    # ... additional sectors
}
```

**Scorecard Criteria**: Standardized evaluation criteria with descriptions and weightings

## Validation System

### ValidationManager Class

**Location**: `validation_schemas.py`

**Purpose**: Comprehensive input validation across all valuation methods

**Validation Types**:
- **Type Checking**: Ensures correct data types
- **Range Validation**: Checks realistic value ranges
- **Business Logic**: Validates relationships between inputs
- **Cross-Field Validation**: Ensures consistency across related fields

**Validation Levels**:
- **Errors**: Must be fixed before calculation
- **Warnings**: Suggestions for review
- **Info**: Additional context and tips

### Method-Specific Validators

Each valuation method has dedicated validation:

**DCFValidator**: 
- Cash flow projections validation
- Discount rate range checking
- Terminal growth rate validation
- Rate relationship verification

**MultiplesValidator**:
- Sector selection validation
- Metric type verification
- Multiple reasonableness checking
- Industry-specific warnings

**ScorecardValidator**:
- Criteria completeness checking
- Score range validation
- Weight sum verification
- Balanced scoring warnings

## Utility Functions

### Location: `utils.py`

**Key Functions**:

```python
def format_currency(amount: float) -> str:
    """Format currency with appropriate K/M/B suffixes"""

def validate_positive_number(value: Any, field_name: str) -> tuple:
    """Validate numeric inputs with detailed error messages"""

def save_calculation_history(method: str, inputs: Dict, result: Dict, chart_fig=None):
    """Store calculations with chart data for PDF generation"""

def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """Net Present Value calculation"""

def calculate_irr(cash_flows: List[float], initial_investment: float) -> float:
    """Internal Rate of Return using Newton-Raphson method"""
```

## Application Flow

### Main Application Structure

1. **Initialization**: Load default settings and initialize session state
2. **Method Selection**: Sidebar navigation between valuation methods
3. **Input Collection**: Dynamic forms based on selected method
4. **Validation**: Real-time input validation with user feedback
5. **Calculation**: Core valuation computation
6. **Results Display**: Charts, metrics, and detailed analysis
7. **History Management**: Store and display calculation history
8. **Report Generation**: PDF export with embedded visualizations

### Session State Management

```python
# Key session state variables
st.session_state.calculation_history: List[Dict]
st.session_state.current_results: Dict
st.session_state.selected_method: str
```

### Error Handling

**Validation Errors**: Displayed as colored messages with severity indicators
**Calculation Errors**: Graceful handling with detailed error messages
**PDF Generation Errors**: Fallback options with error reporting

## Configuration

### Chart Styling

Default color schemes and styling parameters:
```python
PRIMARY_COLOR = '#1f77b4'
SECONDARY_COLOR = '#ff7f0e'
SUCCESS_COLOR = '#2ca02c'
WARNING_COLOR = '#ff7f0e'
ERROR_COLOR = '#d62728'
```

### PDF Formatting

Professional report styling with:
- A4 page format
- Consistent margins and spacing
- Corporate color scheme
- Professional typography

### Validation Rules

Configurable validation parameters:
```python
DCF_DISCOUNT_RATE_RANGE = (0.01, 0.50)  # 1% to 50%
DCF_TERMINAL_GROWTH_RANGE = (0.0, 0.10)  # 0% to 10%
CASH_FLOW_MAX_YEARS = 15
BERKUS_MAX_VALUE_PER_CRITERION = 500000
```

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Charts generated only when needed
2. **Caching**: Streamlit caching for expensive calculations
3. **Efficient Data Structures**: Optimized data handling
4. **Memory Management**: Proper cleanup of temporary files

### Scalability Features

1. **Modular Architecture**: Easy to add new valuation methods
2. **Extensible Validation**: Pluggable validation system
3. **Configurable Parameters**: Easy adjustment of business rules
4. **Export Capabilities**: Multiple output formats supported

## Security Considerations

### Data Handling

- No persistent storage of sensitive data
- Session-based data management
- Secure PDF generation without external dependencies

### Input Sanitization

- Comprehensive input validation
- SQL injection prevention (not applicable - no database)
- XSS prevention through Streamlit's built-in protections

## Development Guidelines

### Adding New Valuation Methods

1. **Calculator Method**: Add method to `ValuationCalculator` class
2. **Chart Generation**: Implement chart creation in `ChartGenerator`
3. **PDF Integration**: Add PDF chart generation in `PDFGenerator`
4. **Validation**: Create validator class in `validation_schemas.py`
5. **UI Interface**: Add Streamlit interface in `app.py`

### Code Standards

- **Type Hints**: All functions include comprehensive type annotations
- **Documentation**: Docstrings for all classes and methods
- **Error Handling**: Graceful error handling with user-friendly messages
- **Testing**: Validation through comprehensive input testing

### Maintenance

- **Regular Updates**: Keep industry multiples current
- **Performance Monitoring**: Track calculation performance
- **User Feedback**: Incorporate user suggestions for improvements
- **Security Updates**: Regular dependency updates

## API Reference

### ValuationCalculator Methods

```python
def dcf_valuation(
    cash_flows: List[float], 
    growth_rate: float, 
    discount_rate: float, 
    terminal_growth: float = 0.02
) -> Dict:
    """
    DCF valuation calculation
    
    Args:
        cash_flows: List of projected cash flows
        growth_rate: Annual growth rate (legacy parameter)
        discount_rate: Discount rate (WACC)
        terminal_growth: Terminal growth rate
        
    Returns:
        Dictionary with valuation results and details
    """
```

### ChartGenerator Methods

```python
def create_dcf_chart(self, result: Dict, cash_flows: List[float]) -> go.Figure:
    """
    Create DCF analysis charts
    
    Args:
        result: DCF calculation results
        cash_flows: Input cash flow projections
        
    Returns:
        Plotly figure object
    """
```

### PDFGenerator Methods

```python
def create_report(
    self, 
    current_results: Dict, 
    calculation_history: List[Dict]
) -> BytesIO:
    """
    Create comprehensive PDF report
    
    Args:
        current_results: Current calculation results
        calculation_history: Historical calculations
        
    Returns:
        BytesIO buffer containing PDF data
    """
```

---

*This technical documentation serves as a comprehensive guide for developers working with the Startup Valuation Calculator codebase.*