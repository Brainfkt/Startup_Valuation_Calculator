"""
Valuation Calculator Module
Contains all valuation calculation methods with improved error handling and validation
"""

import numpy as np
from typing import Dict, List, Optional, Union
from data_models import ValidationResult

class ValuationCalculator:
    """Main calculator class for startup valuation methods"""
    
    def __init__(self):
        self.precision = 2  # Decimal places for calculations
    
    def dcf_valuation(
        self, 
        cash_flows: List[float], 
        growth_rate: float, 
        discount_rate: float, 
        terminal_growth: float = 0.02
    ) -> Dict:
        """
        DCF (Discounted Cash Flow) valuation with enhanced error handling
        
        Args:
            cash_flows: List of projected cash flows
            growth_rate: Annual growth rate (currently unused but kept for compatibility)
            discount_rate: Discount rate (WACC)
            terminal_growth: Terminal growth rate
        
        Returns:
            Dictionary containing valuation results or error message
        """
        try:
            # Input validation
            validation = self._validate_dcf_inputs(cash_flows, discount_rate, terminal_growth)
            if not validation.is_valid:
                return {"error": validation.error_message}
            
            # Convert to numpy arrays for better performance
            cash_flows_array = np.array(cash_flows)
            
            # Calculate discounted cash flows
            years = np.arange(1, len(cash_flows_array) + 1)
            discount_factors = (1 + discount_rate) ** years
            discounted_flows = cash_flows_array / discount_factors
            
            # Operating value (sum of discounted cash flows)
            operating_value = np.sum(discounted_flows)
            
            # Terminal value calculation
            if len(cash_flows) > 0:
                terminal_cf = cash_flows[-1] * (1 + terminal_growth)
                terminal_value = terminal_cf / (discount_rate - terminal_growth)
                terminal_pv = terminal_value / ((1 + discount_rate) ** len(cash_flows))
            else:
                terminal_pv = 0
            
            total_valuation = operating_value + terminal_pv
            
            return {
                "valuation": round(total_valuation, self.precision),
                "operating_value": round(operating_value, self.precision),
                "terminal_value": round(terminal_pv, self.precision),
                "terminal_pv": round(terminal_pv, self.precision),
                "discounted_flows": [round(cf, self.precision) for cf in discounted_flows.tolist()],
                "discount_rate": discount_rate,
                "terminal_growth": terminal_growth
            }
            
        except Exception as e:
            return {"error": f"DCF calculation failed: {str(e)}"}
    
    def market_multiples_valuation(
        self, 
        revenue_or_ebitda: float, 
        multiple: float, 
        metric_type: str = "Revenue"
    ) -> Dict:
        """
        Market multiples valuation with validation
        
        Args:
            revenue_or_ebitda: Financial metric value
            multiple: Industry multiple
            metric_type: Type of metric ("Revenue" or "EBITDA")
        
        Returns:
            Dictionary containing valuation results
        """
        try:
            # Input validation
            if revenue_or_ebitda < 0:
                return {"error": "Financial metric cannot be negative"}
            
            if multiple <= 0:
                return {"error": "Multiple must be positive"}
            
            valuation = revenue_or_ebitda * multiple
            
            return {
                "valuation": round(valuation, self.precision),
                "metric": round(revenue_or_ebitda, self.precision),
                "multiple": round(multiple, 2),
                "metric_type": metric_type
            }
            
        except Exception as e:
            return {"error": f"Market multiples calculation failed: {str(e)}"}
    
    def scorecard_valuation(
        self, 
        base_valuation: float, 
        criteria_scores: Dict[str, int], 
        criteria_weights: Optional[Dict[str, float]] = None
    ) -> Dict:
        """
        Scorecard method with improved score calculation
        
        Args:
            base_valuation: Base valuation amount
            criteria_scores: Dictionary of criterion scores (0-5)
            criteria_weights: Optional custom weights
        
        Returns:
            Dictionary containing adjusted valuation and analysis
        """
        try:
            # Input validation
            if base_valuation <= 0:
                return {"error": "Base valuation must be positive"}
            
            for criterion, score in criteria_scores.items():
                if not 0 <= score <= 5:
                    return {"error": f"Score for {criterion} must be between 0 and 5"}
            
            # Default weights
            if criteria_weights is None:
                criteria_weights = {
                    "team": 0.25,
                    "product": 0.20,
                    "market": 0.20,
                    "competition": 0.15,
                    "financial": 0.10,
                    "legal": 0.10
                }
            
            # Normalize weights to sum to 1
            total_weight = sum(criteria_weights.values())
            if total_weight != 1.0:
                criteria_weights = {k: v/total_weight for k, v in criteria_weights.items()}
            
            # Calculate weighted adjustment factor
            # Score 3 = neutral (1.0x), Score 0 = 0.5x, Score 5 = 1.5x
            weighted_factor = 0
            criteria_analysis = {}
            
            for criterion, score in criteria_scores.items():
                weight = criteria_weights.get(criterion, 0)
                factor = 0.5 + (score / 5.0)  # Convert 0-5 to 0.5-1.5
                contribution = weight * factor
                weighted_factor += contribution
                
                criteria_analysis[criterion] = {
                    "score": score,
                    "weight": weight,
                    "factor": factor,
                    "contribution": contribution
                }
            
            adjusted_valuation = base_valuation * weighted_factor
            
            return {
                "valuation": round(adjusted_valuation, self.precision),
                "base_valuation": round(base_valuation, self.precision),
                "adjustment_factor": round(weighted_factor, 3),
                "criteria_analysis": criteria_analysis
            }
            
        except Exception as e:
            return {"error": f"Scorecard calculation failed: {str(e)}"}
    
    def berkus_valuation(self, criteria_scores: Dict[str, int]) -> Dict:
        """
        Berkus method for pre-revenue startups
        
        Args:
            criteria_scores: Dictionary of Berkus criteria scores (0-5)
        
        Returns:
            Dictionary containing valuation breakdown
        """
        try:
            # Validate inputs
            required_criteria = ["concept", "prototype", "team", "strategic_relationships", "product_rollout"]
            
            for criterion in required_criteria:
                if criterion not in criteria_scores:
                    return {"error": f"Missing required criterion: {criterion}"}
                
                score = criteria_scores[criterion]
                if not 0 <= score <= 5:
                    return {"error": f"Score for {criterion} must be between 0 and 5"}
            
            max_value_per_criterion = 500000  # €500k max per criterion
            
            criteria_mapping = {
                "concept": "Sound Idea (Basic Value)",
                "prototype": "Prototype (Reduces Technology Risk)",
                "team": "Quality Management Team (Reduces Execution Risk)",
                "strategic_relationships": "Strategic Relationships (Reduces Market Risk)",
                "product_rollout": "Product Rollout or Sales (Reduces Financial Risk)"
            }
            
            valuation_breakdown = {}
            total_valuation = 0
            
            for criterion, score in criteria_scores.items():
                if criterion in criteria_mapping:
                    criterion_value = (score / 5.0) * max_value_per_criterion
                    valuation_breakdown[criterion] = {
                        "name": criteria_mapping[criterion],
                        "score": score,
                        "value": round(criterion_value, self.precision)
                    }
                    total_valuation += criterion_value
            
            return {
                "valuation": round(total_valuation, self.precision),
                "breakdown": valuation_breakdown,
                "max_possible": len(required_criteria) * max_value_per_criterion
            }
            
        except Exception as e:
            return {"error": f"Berkus calculation failed: {str(e)}"}
    
    def risk_factor_summation(
        self, 
        base_valuation: float, 
        risk_factors: Dict[str, int]
    ) -> Dict:
        """
        Risk Factor Summation method with capped adjustments
        
        Args:
            base_valuation: Base valuation amount
            risk_factors: Dictionary of risk ratings (-2 to +2)
        
        Returns:
            Dictionary containing risk-adjusted valuation
        """
        try:
            # Input validation
            if base_valuation <= 0:
                return {"error": "Base valuation must be positive"}
            
            for factor, rating in risk_factors.items():
                if not -2 <= rating <= 2:
                    return {"error": f"Risk rating for {factor} must be between -2 and 2"}
            
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
            
            # Calculate total risk adjustment
            total_adjustment = 0
            risk_analysis = {}
            
            for factor, rating in risk_factors.items():
                # Each factor can adjust by ±12.5% (rating * 6.25%)
                adjustment_pct = rating * 0.0625  # 12.5% / 2
                total_adjustment += adjustment_pct
                
                risk_analysis[factor] = {
                    "name": risk_categories.get(factor, factor),
                    "rating": rating,
                    "adjustment": adjustment_pct
                }
            
            # Cap total adjustment at ±50%
            total_adjustment = max(-0.5, min(0.5, total_adjustment))
            
            adjusted_valuation = base_valuation * (1 + total_adjustment)
            
            return {
                "valuation": round(adjusted_valuation, self.precision),
                "base_valuation": round(base_valuation, self.precision),
                "total_adjustment": round(total_adjustment, 4),
                "risk_analysis": risk_analysis
            }
            
        except Exception as e:
            return {"error": f"Risk factor calculation failed: {str(e)}"}
    
    def venture_capital_method(
        self,
        expected_revenue: float,
        exit_multiple: float,
        required_return: float,
        years_to_exit: int = 5,
        investment_needed: Optional[float] = None
    ) -> Dict:
        """
        Venture Capital method with optional investment calculation
        
        Args:
            expected_revenue: Expected revenue at exit
            exit_multiple: Revenue multiple at exit
            required_return: Required annual return rate
            years_to_exit: Number of years to exit
            investment_needed: Optional investment amount
        
        Returns:
            Dictionary containing VC method results
        """
        try:
            # Input validation
            if expected_revenue <= 0:
                return {"error": "Expected revenue must be positive"}
            
            if exit_multiple <= 0:
                return {"error": "Exit multiple must be positive"}
            
            if required_return <= 0:
                return {"error": "Required return must be positive"}
            
            if years_to_exit <= 0:
                return {"error": "Years to exit must be positive"}
            
            # Calculate exit value
            exit_value = expected_revenue * exit_multiple
            
            # Calculate present value
            present_value = exit_value / ((1 + required_return) ** years_to_exit)
            
            # Calculate returns
            if present_value > 0:
                return_multiple = exit_value / present_value
                annualized_return = (return_multiple ** (1/years_to_exit)) - 1
            else:
                return_multiple = 0
                annualized_return = 0
            
            result = {
                "exit_value": round(exit_value, self.precision),
                "present_value": round(present_value, self.precision),
                "expected_return_multiple": round(return_multiple, 2),
                "annualized_return": round(annualized_return, 4)
            }
            
            # Add investment calculations if provided
            if investment_needed is not None:
                if investment_needed < 0:
                    return {"error": "Investment amount cannot be negative"}
                
                if present_value > 0:
                    ownership_percentage = investment_needed / present_value
                    pre_money_valuation = present_value - investment_needed
                    post_money_valuation = present_value
                    
                    result.update({
                        "ownership_percentage": round(ownership_percentage, 4),
                        "pre_money_valuation": round(pre_money_valuation, self.precision),
                        "post_money_valuation": round(post_money_valuation, self.precision),
                        "investment_needed": round(investment_needed, self.precision)
                    })
            
            return result
            
        except Exception as e:
            return {"error": f"VC method calculation failed: {str(e)}"}
    
    def _validate_dcf_inputs(
        self, 
        cash_flows: List[float], 
        discount_rate: float, 
        terminal_growth: float
    ) -> ValidationResult:
        """Validate DCF input parameters"""
        
        if not cash_flows or len(cash_flows) == 0:
            return ValidationResult(False, "Cash flows are required")
        
        if any(cf < 0 for cf in cash_flows):
            return ValidationResult(False, "Cash flows cannot be negative")
        
        if discount_rate <= 0:
            return ValidationResult(False, "Discount rate must be positive")
        
        if discount_rate <= terminal_growth:
            return ValidationResult(False, "Discount rate must be higher than terminal growth rate")
        
        if terminal_growth < 0:
            return ValidationResult(False, "Terminal growth rate cannot be negative")
        
        if terminal_growth > 0.1:  # 10% seems reasonable as max
            return ValidationResult(False, "Terminal growth rate seems unrealistically high (>10%)")
        
        return ValidationResult(True, "")
