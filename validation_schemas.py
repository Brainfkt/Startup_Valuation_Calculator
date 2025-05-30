"""
Data Validation Schemas Module
Comprehensive validation schemas for all valuation inputs and outputs
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import re

class ValidationSeverity(Enum):
    """Validation message severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationMessage:
    """Individual validation message"""
    field: str
    message: str
    severity: ValidationSeverity
    code: str
    suggested_value: Optional[Any] = None

@dataclass
class ValidationResult:
    """Complete validation result"""
    is_valid: bool
    messages: List[ValidationMessage]
    sanitized_data: Optional[Dict[str, Any]] = None
    
    def get_errors(self) -> List[ValidationMessage]:
        """Get only error messages"""
        return [msg for msg in self.messages if msg.severity == ValidationSeverity.ERROR]
    
    def get_warnings(self) -> List[ValidationMessage]:
        """Get only warning messages"""
        return [msg for msg in self.messages if msg.severity == ValidationSeverity.WARNING]

class BaseValidator:
    """Base validator class with common validation methods"""
    
    def __init__(self):
        self.messages: List[ValidationMessage] = []
    
    def add_error(self, field: str, message: str, code: str, suggested_value: Any = None):
        """Add error message"""
        self.messages.append(ValidationMessage(
            field=field,
            message=message,
            severity=ValidationSeverity.ERROR,
            code=code,
            suggested_value=suggested_value
        ))
    
    def add_warning(self, field: str, message: str, code: str, suggested_value: Any = None):
        """Add warning message"""
        self.messages.append(ValidationMessage(
            field=field,
            message=message,
            severity=ValidationSeverity.WARNING,
            code=code,
            suggested_value=suggested_value
        ))
    
    def add_info(self, field: str, message: str, code: str):
        """Add info message"""
        self.messages.append(ValidationMessage(
            field=field,
            message=message,
            severity=ValidationSeverity.INFO,
            code=code
        ))
    
    def validate_positive_number(self, value: Any, field_name: str, min_value: float = 0.0, 
                                max_value: Optional[float] = None) -> Optional[float]:
        """Validate positive number with optional range"""
        try:
            if value is None:
                self.add_error(field_name, "Value cannot be empty", "REQUIRED_FIELD")
                return None
            
            # Convert to float
            num_value = float(value)
            
            # Check if finite
            if not (num_value == num_value and num_value != float('inf') and num_value != float('-inf')):
                self.add_error(field_name, "Value must be a valid finite number", "INVALID_NUMBER")
                return None
            
            # Check minimum
            if num_value < min_value:
                self.add_error(
                    field_name, 
                    f"Value must be at least {min_value:,.2f}", 
                    "VALUE_TOO_LOW",
                    suggested_value=min_value
                )
                return None
            
            # Check maximum
            if max_value is not None and num_value > max_value:
                self.add_error(
                    field_name, 
                    f"Value must not exceed {max_value:,.2f}", 
                    "VALUE_TOO_HIGH",
                    suggested_value=max_value
                )
                return None
            
            # Warnings for unusual values
            if num_value == 0 and min_value == 0:
                self.add_warning(field_name, "Zero value may affect calculation accuracy", "ZERO_VALUE")
            
            if num_value > 1_000_000_000:  # 1 billion
                self.add_warning(field_name, "Very large value - please verify", "LARGE_VALUE")
            
            return num_value
            
        except (ValueError, TypeError):
            self.add_error(field_name, "Value must be a valid number", "INVALID_FORMAT")
            return None
    
    def validate_percentage(self, value: Any, field_name: str, min_percent: float = 0.0, 
                           max_percent: float = 100.0, as_decimal: bool = False) -> Optional[float]:
        """Validate percentage value"""
        validated_value = self.validate_positive_number(value, field_name, min_percent, max_percent)
        
        if validated_value is not None:
            if as_decimal:
                return validated_value / 100.0
            return validated_value
        return None
    
    def validate_cash_flows(self, cash_flows: List[Any], field_name: str = "cash_flows") -> Optional[List[float]]:
        """Validate cash flow projections"""
        if not cash_flows:
            self.add_error(field_name, "At least one cash flow projection is required", "EMPTY_LIST")
            return None
        
        if len(cash_flows) > 15:
            self.add_warning(field_name, "More than 15 years may reduce accuracy", "TOO_MANY_PERIODS")
        
        validated_flows = []
        for i, cf in enumerate(cash_flows):
            validated_cf = self.validate_positive_number(
                cf, 
                f"{field_name}[{i+1}]", 
                min_value=-1_000_000_000,  # Allow negative cash flows
                max_value=1_000_000_000_000  # 1 trillion max
            )
            if validated_cf is not None:
                validated_flows.append(validated_cf)
            else:
                return None
        
        # Business logic validations
        negative_count = sum(1 for cf in validated_flows if cf < 0)
        if negative_count > len(validated_flows) * 0.6:  # More than 60% negative
            self.add_warning(field_name, "High proportion of negative cash flows detected", "HIGH_NEGATIVE_FLOWS")
        
        # Check for growth patterns
        if len(validated_flows) >= 3:
            growth_rates = []
            for i in range(1, len(validated_flows)):
                if validated_flows[i-1] > 0:
                    growth_rate = (validated_flows[i] / validated_flows[i-1]) - 1
                    growth_rates.append(growth_rate)
            
            if growth_rates and max(growth_rates) > 5.0:  # 500% growth
                self.add_warning(field_name, "Extremely high growth rates detected", "HIGH_GROWTH")
        
        return validated_flows

class DCFValidator(BaseValidator):
    """Validator for DCF method inputs"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate DCF inputs"""
        self.messages = []
        sanitized_data = {}
        
        # Validate cash flows
        cash_flows = self.validate_cash_flows(data.get('cash_flows', []))
        if cash_flows:
            sanitized_data['cash_flows'] = cash_flows
        
        # Validate discount rate
        discount_rate = self.validate_percentage(
            data.get('discount_rate'), 
            'discount_rate', 
            min_percent=1.0, 
            max_percent=50.0, 
            as_decimal=True
        )
        if discount_rate:
            sanitized_data['discount_rate'] = discount_rate
        
        # Validate terminal growth rate
        terminal_growth = self.validate_percentage(
            data.get('terminal_growth'), 
            'terminal_growth', 
            min_percent=0.0, 
            max_percent=10.0, 
            as_decimal=True
        )
        if terminal_growth:
            sanitized_data['terminal_growth'] = terminal_growth
        
        # Cross-field validation
        if discount_rate and terminal_growth:
            if discount_rate <= terminal_growth:
                self.add_error(
                    'discount_rate', 
                    'Discount rate must be higher than terminal growth rate', 
                    'RATE_RELATIONSHIP_ERROR'
                )
            elif discount_rate - terminal_growth < 0.02:  # Less than 2% spread
                self.add_warning(
                    'discount_rate', 
                    'Small spread between discount and terminal growth rates', 
                    'LOW_RATE_SPREAD'
                )
        
        is_valid = len(self.get_errors()) == 0
        return ValidationResult(is_valid, self.messages, sanitized_data if is_valid else None)

class MultiplesValidator(BaseValidator):
    """Validator for Market Multiples method inputs"""
    
    VALID_SECTORS = [
        'Technology', 'Healthcare', 'Financial Services', 'Consumer Goods',
        'Industrial', 'Energy', 'Real Estate', 'Telecommunications',
        'Media & Entertainment', 'Retail', 'Automotive', 'Aerospace'
    ]
    
    VALID_METRICS = ['Revenue', 'EBITDA', 'EBIT', 'Net Income']
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate market multiples inputs"""
        self.messages = []
        sanitized_data = {}
        
        # Validate sector
        sector = data.get('sector', '').strip()
        if not sector:
            self.add_error('sector', 'Sector selection is required', 'REQUIRED_FIELD')
        elif sector not in self.VALID_SECTORS:
            self.add_error(
                'sector', 
                f'Invalid sector. Must be one of: {", ".join(self.VALID_SECTORS)}', 
                'INVALID_SECTOR',
                suggested_value=self.VALID_SECTORS[0]
            )
        else:
            sanitized_data['sector'] = sector
        
        # Validate metric type
        metric_type = data.get('metric_type', '').strip()
        if not metric_type:
            self.add_error('metric_type', 'Metric type is required', 'REQUIRED_FIELD')
        elif metric_type not in self.VALID_METRICS:
            self.add_error(
                'metric_type', 
                f'Invalid metric. Must be one of: {", ".join(self.VALID_METRICS)}', 
                'INVALID_METRIC',
                suggested_value='Revenue'
            )
        else:
            sanitized_data['metric_type'] = metric_type
        
        # Validate metric value
        metric_value = self.validate_positive_number(
            data.get('metric_value'), 
            'metric_value', 
            min_value=1000,  # Minimum $1K
            max_value=100_000_000_000  # $100B max
        )
        if metric_value:
            sanitized_data['metric_value'] = metric_value
        
        # Validate multiple
        multiple = self.validate_positive_number(
            data.get('multiple'), 
            'multiple', 
            min_value=0.1, 
            max_value=50.0
        )
        if multiple:
            sanitized_data['multiple'] = multiple
            
            # Industry-specific multiple validation
            if sector == 'Technology' and multiple > 20:
                self.add_warning('multiple', 'High multiple for technology sector', 'HIGH_TECH_MULTIPLE')
            elif sector == 'Industrial' and multiple > 8:
                self.add_warning('multiple', 'High multiple for industrial sector', 'HIGH_INDUSTRIAL_MULTIPLE')
        
        is_valid = len(self.get_errors()) == 0
        return ValidationResult(is_valid, self.messages, sanitized_data if is_valid else None)

class ScorecardValidator(BaseValidator):
    """Validator for Scorecard method inputs"""
    
    REQUIRED_CRITERIA = [
        'management', 'opportunity', 'product', 'competition', 
        'marketing', 'funding', 'valuation'
    ]
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate scorecard inputs"""
        self.messages = []
        sanitized_data = {}
        
        # Validate base valuation
        base_valuation = self.validate_positive_number(
            data.get('base_valuation'), 
            'base_valuation', 
            min_value=10000,  # $10K minimum
            max_value=1_000_000_000  # $1B maximum
        )
        if base_valuation:
            sanitized_data['base_valuation'] = base_valuation
        
        # Validate criteria scores
        criteria_scores = data.get('criteria_scores', {})
        if not criteria_scores:
            self.add_error('criteria_scores', 'Criteria scores are required', 'REQUIRED_FIELD')
        else:
            validated_scores = {}
            for criterion in self.REQUIRED_CRITERIA:
                score = criteria_scores.get(criterion)
                validated_score = self.validate_positive_number(
                    score, 
                    f'criteria_scores.{criterion}', 
                    min_value=0, 
                    max_value=5
                )
                if validated_score is not None:
                    validated_scores[criterion] = int(validated_score)
            
            if len(validated_scores) == len(self.REQUIRED_CRITERIA):
                sanitized_data['criteria_scores'] = validated_scores
                
                # Check for balanced scoring
                avg_score = sum(validated_scores.values()) / len(validated_scores)
                if avg_score < 1.5:
                    self.add_warning('criteria_scores', 'Overall low scores may indicate high risk', 'LOW_SCORES')
                elif avg_score > 4.5:
                    self.add_warning('criteria_scores', 'Very high scores - ensure realistic assessment', 'HIGH_SCORES')
        
        # Validate optional weights
        criteria_weights = data.get('criteria_weights')
        if criteria_weights:
            validated_weights = {}
            total_weight = 0
            
            for criterion, weight in criteria_weights.items():
                validated_weight = self.validate_percentage(
                    weight, 
                    f'criteria_weights.{criterion}', 
                    min_percent=0, 
                    max_percent=100,
                    as_decimal=True
                )
                if validated_weight is not None:
                    validated_weights[criterion] = validated_weight
                    total_weight += validated_weight
            
            if abs(total_weight - 1.0) > 0.01:  # Allow 1% tolerance
                self.add_error('criteria_weights', 'Weights must sum to 100%', 'WEIGHT_SUM_ERROR')
            else:
                sanitized_data['criteria_weights'] = validated_weights
        
        is_valid = len(self.get_errors()) == 0
        return ValidationResult(is_valid, self.messages, sanitized_data if is_valid else None)

class BerkusValidator(BaseValidator):
    """Validator for Berkus method inputs"""
    
    BERKUS_CRITERIA = [
        'basic_value', 'technology', 'execution', 'core_relationships', 'production'
    ]
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate Berkus method inputs"""
        self.messages = []
        sanitized_data = {}
        
        # Validate criteria scores
        criteria_scores = data.get('criteria_scores', {})
        if not criteria_scores:
            self.add_error('criteria_scores', 'Berkus criteria scores are required', 'REQUIRED_FIELD')
        else:
            validated_scores = {}
            for criterion in self.BERKUS_CRITERIA:
                score = criteria_scores.get(criterion)
                validated_score = self.validate_positive_number(
                    score, 
                    f'criteria_scores.{criterion}', 
                    min_value=0, 
                    max_value=5
                )
                if validated_score is not None:
                    validated_scores[criterion] = int(validated_score)
            
            if len(validated_scores) == len(self.BERKUS_CRITERIA):
                sanitized_data['criteria_scores'] = validated_scores
                
                # Berkus-specific validations
                total_value = sum(validated_scores.values()) * 500000  # $500K per criterion max
                if total_value > 2_500_000:  # $2.5M total max
                    self.add_info('criteria_scores', f'Estimated total value: ${total_value:,.0f}', 'VALUE_ESTIMATE')
                
                # Check for pre-revenue appropriate scoring
                if validated_scores.get('production', 0) > 3:
                    self.add_warning(
                        'criteria_scores.production', 
                        'High production score - ensure appropriate for pre-revenue stage', 
                        'HIGH_PRODUCTION_SCORE'
                    )
        
        is_valid = len(self.get_errors()) == 0
        return ValidationResult(is_valid, self.messages, sanitized_data if is_valid else None)

class RiskFactorValidator(BaseValidator):
    """Validator for Risk Factor Summation method inputs"""
    
    RISK_FACTORS = [
        'management', 'stage', 'legislation', 'manufacturing', 'sales', 
        'funding', 'competition', 'technology', 'litigation', 'international', 
        'reputation', 'potential_lucrative_exit'
    ]
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate risk factor inputs"""
        self.messages = []
        sanitized_data = {}
        
        # Validate base valuation
        base_valuation = self.validate_positive_number(
            data.get('base_valuation'), 
            'base_valuation', 
            min_value=10000,  # $10K minimum
            max_value=1_000_000_000  # $1B maximum
        )
        if base_valuation:
            sanitized_data['base_valuation'] = base_valuation
        
        # Validate risk factors
        risk_factors = data.get('risk_factors', {})
        if not risk_factors:
            self.add_error('risk_factors', 'Risk factor ratings are required', 'REQUIRED_FIELD')
        else:
            validated_factors = {}
            for factor in self.RISK_FACTORS:
                rating = risk_factors.get(factor)
                validated_rating = self.validate_positive_number(
                    rating, 
                    f'risk_factors.{factor}', 
                    min_value=-2, 
                    max_value=2
                )
                if validated_rating is not None:
                    validated_factors[factor] = int(validated_rating)
            
            if len(validated_factors) >= len(self.RISK_FACTORS) * 0.7:  # At least 70% of factors
                sanitized_data['risk_factors'] = validated_factors
                
                # Risk analysis
                avg_risk = sum(validated_factors.values()) / len(validated_factors)
                if avg_risk < -1:
                    self.add_warning('risk_factors', 'High overall risk profile detected', 'HIGH_RISK')
                elif avg_risk > 1:
                    self.add_warning('risk_factors', 'Very positive risk profile - verify assessments', 'LOW_RISK')
        
        is_valid = len(self.get_errors()) == 0
        return ValidationResult(is_valid, self.messages, sanitized_data if is_valid else None)

class VCMethodValidator(BaseValidator):
    """Validator for Venture Capital method inputs"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate VC method inputs"""
        self.messages = []
        sanitized_data = {}
        
        # Validate expected revenue
        expected_revenue = self.validate_positive_number(
            data.get('expected_revenue'), 
            'expected_revenue', 
            min_value=100000,  # $100K minimum
            max_value=10_000_000_000  # $10B maximum
        )
        if expected_revenue:
            sanitized_data['expected_revenue'] = expected_revenue
        
        # Validate exit multiple
        exit_multiple = self.validate_positive_number(
            data.get('exit_multiple'), 
            'exit_multiple', 
            min_value=0.5, 
            max_value=20.0
        )
        if exit_multiple:
            sanitized_data['exit_multiple'] = exit_multiple
        
        # Validate required return
        required_return = self.validate_percentage(
            data.get('required_return'), 
            'required_return', 
            min_percent=10.0, 
            max_percent=100.0, 
            as_decimal=True
        )
        if required_return:
            sanitized_data['required_return'] = required_return
        
        # Validate years to exit
        years_to_exit = self.validate_positive_number(
            data.get('years_to_exit'), 
            'years_to_exit', 
            min_value=1, 
            max_value=15
        )
        if years_to_exit:
            sanitized_data['years_to_exit'] = int(years_to_exit)
        
        # Validate optional investment needed
        investment_needed = data.get('investment_needed')
        if investment_needed is not None:
            validated_investment = self.validate_positive_number(
                investment_needed, 
                'investment_needed', 
                min_value=10000,  # $10K minimum
                max_value=1_000_000_000  # $1B maximum
            )
            if validated_investment:
                sanitized_data['investment_needed'] = validated_investment
        
        # Cross-field validations
        if required_return and years_to_exit:
            total_return_multiple = (1 + required_return) ** years_to_exit
            if total_return_multiple > 50:  # 50x return
                self.add_warning(
                    'required_return', 
                    'Very high return expectations may be unrealistic', 
                    'HIGH_RETURN_EXPECTATION'
                )
        
        if exit_multiple and exit_multiple > 10:
            self.add_warning('exit_multiple', 'High exit multiple - verify market conditions', 'HIGH_EXIT_MULTIPLE')
        
        is_valid = len(self.get_errors()) == 0
        return ValidationResult(is_valid, self.messages, sanitized_data if is_valid else None)

class ValidationManager:
    """Central validation manager for all methods"""
    
    def __init__(self):
        self.validators = {
            'DCF': DCFValidator(),
            'Market Multiples': MultiplesValidator(),
            'Scorecard': ScorecardValidator(),
            'Berkus': BerkusValidator(),
            'Risk Factor Summation': RiskFactorValidator(),
            'Venture Capital': VCMethodValidator()
        }
    
    def validate_method_inputs(self, method: str, data: Dict[str, Any]) -> ValidationResult:
        """Validate inputs for a specific valuation method"""
        if method not in self.validators:
            return ValidationResult(
                is_valid=False,
                messages=[ValidationMessage(
                    field='method',
                    message=f'Unknown valuation method: {method}',
                    severity=ValidationSeverity.ERROR,
                    code='UNKNOWN_METHOD'
                )]
            )
        
        validator = self.validators[method]
        return validator.validate(data)
    
    def get_method_requirements(self, method: str) -> Dict[str, Any]:
        """Get validation requirements for a method"""
        requirements = {
            'DCF': {
                'required_fields': ['cash_flows', 'discount_rate', 'terminal_growth'],
                'field_types': {
                    'cash_flows': 'list[float]',
                    'discount_rate': 'float (0.01-0.50)',
                    'terminal_growth': 'float (0.00-0.10)'
                }
            },
            'Market Multiples': {
                'required_fields': ['sector', 'metric_type', 'metric_value', 'multiple'],
                'field_types': {
                    'sector': 'string (from predefined list)',
                    'metric_type': 'string (Revenue/EBITDA/EBIT/Net Income)',
                    'metric_value': 'float (1000-100B)',
                    'multiple': 'float (0.1-50.0)'
                }
            },
            'Scorecard': {
                'required_fields': ['base_valuation', 'criteria_scores'],
                'field_types': {
                    'base_valuation': 'float (10K-1B)',
                    'criteria_scores': 'dict[string, int] (0-5)',
                    'criteria_weights': 'dict[string, float] (optional, sum=1.0)'
                }
            },
            'Berkus': {
                'required_fields': ['criteria_scores'],
                'field_types': {
                    'criteria_scores': 'dict[string, int] (0-5)'
                }
            },
            'Risk Factor Summation': {
                'required_fields': ['base_valuation', 'risk_factors'],
                'field_types': {
                    'base_valuation': 'float (10K-1B)',
                    'risk_factors': 'dict[string, int] (-2 to +2)'
                }
            },
            'Venture Capital': {
                'required_fields': ['expected_revenue', 'exit_multiple', 'required_return', 'years_to_exit'],
                'field_types': {
                    'expected_revenue': 'float (100K-10B)',
                    'exit_multiple': 'float (0.5-20.0)',
                    'required_return': 'float (0.10-1.00)',
                    'years_to_exit': 'int (1-15)',
                    'investment_needed': 'float (optional, 10K-1B)'
                }
            }
        }
        
        return requirements.get(method, {'required_fields': [], 'field_types': {}})