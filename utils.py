"""
Utility Functions Module
Common utility functions used across the application
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Union, List, Dict, Any, Optional
import json
import re

def format_currency(amount: Union[float, int], precision: int = 0) -> str:
    """
    Format currency values with appropriate units (K, M, B)
    
    Args:
        amount: The amount to format
        precision: Number of decimal places
    
    Returns:
        Formatted currency string
    """
    try:
        if pd.isna(amount) or amount is None:
            return "€0"
        
        amount = float(amount)
        
        if abs(amount) >= 1_000_000_000:
            return f"€{amount/1_000_000_000:.{precision}f}B"
        elif abs(amount) >= 1_000_000:
            return f"€{amount/1_000_000:.{precision}f}M"
        elif abs(amount) >= 1_000:
            return f"€{amount/1_000:.{precision}f}K"
        else:
            return f"€{amount:,.{precision}f}"
            
    except (ValueError, TypeError):
        return "€0"

def format_percentage(value: Union[float, int], precision: int = 1) -> str:
    """
    Format percentage values
    
    Args:
        value: The value to format (as decimal, e.g., 0.15 for 15%)
        precision: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    try:
        if pd.isna(value) or value is None:
            return "0.0%"
        
        return f"{float(value) * 100:.{precision}f}%"
        
    except (ValueError, TypeError):
        return "0.0%"

def validate_positive_number(value: Any, field_name: str = "Value") -> tuple[bool, str]:
    """
    Validate that a value is a positive number
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if value is None or value == "":
            return False, f"{field_name} is required"
        
        num_value = float(value)
        
        if num_value < 0:
            return False, f"{field_name} must be positive"
        
        if not np.isfinite(num_value):
            return False, f"{field_name} must be a finite number"
        
        return True, ""
        
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"

def validate_range(value: Any, min_val: float, max_val: float, field_name: str = "Value") -> tuple[bool, str]:
    """
    Validate that a value is within a specified range
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if value is None or value == "":
            return False, f"{field_name} is required"
        
        num_value = float(value)
        
        if num_value < min_val or num_value > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}"
        
        return True, ""
        
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, handling division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Value to return if division by zero
    
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0 or not np.isfinite(denominator):
            return default
        
        result = numerator / denominator
        
        if not np.isfinite(result):
            return default
        
        return result
        
    except (TypeError, ValueError):
        return default

def calculate_growth_rate(initial_value: float, final_value: float, periods: int) -> float:
    """
    Calculate compound annual growth rate (CAGR)
    
    Args:
        initial_value: Starting value
        final_value: Ending value
        periods: Number of periods
    
    Returns:
        Growth rate as decimal (e.g., 0.15 for 15%)
    """
    try:
        if initial_value <= 0 or final_value <= 0 or periods <= 0:
            return 0.0
        
        growth_rate = (final_value / initial_value) ** (1 / periods) - 1
        
        if not np.isfinite(growth_rate):
            return 0.0
        
        return growth_rate
        
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0

def save_calculation_history(method: str, inputs: Dict[str, Any], result: Dict[str, Any]) -> None:
    """
    Save calculation to session state history
    
    Args:
        method: Valuation method used
        inputs: Input parameters
        result: Calculation results
    """
    try:
        if 'calculation_history' not in st.session_state:
            st.session_state.calculation_history = []
        
        # Extract valuation from result
        valuation = result.get('valuation', 0)
        
        # Create history entry
        history_entry = {
            'method': method,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'valuation': valuation,
            'inputs': inputs,
            'result': result
        }
        
        # Add to history (keep last 50 entries)
        st.session_state.calculation_history.append(history_entry)
        if len(st.session_state.calculation_history) > 50:
            st.session_state.calculation_history = st.session_state.calculation_history[-50:]
            
    except Exception as e:
        st.error(f"Failed to save calculation history: {str(e)}")

def export_calculation_data(calculation_history: List[Dict]) -> Dict[str, Any]:
    """
    Export calculation data for external use
    
    Args:
        calculation_history: List of calculation entries
    
    Returns:
        Dictionary with exportable data
    """
    try:
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'total_calculations': len(calculation_history),
            'calculations': calculation_history,
            'summary': {
                'methods_used': list(set(calc['method'] for calc in calculation_history)),
                'date_range': {
                    'earliest': min(calc['timestamp'] for calc in calculation_history) if calculation_history else None,
                    'latest': max(calc['timestamp'] for calc in calculation_history) if calculation_history else None
                },
                'valuation_range': {
                    'min': min(calc['valuation'] for calc in calculation_history) if calculation_history else 0,
                    'max': max(calc['valuation'] for calc in calculation_history) if calculation_history else 0,
                    'average': np.mean([calc['valuation'] for calc in calculation_history]) if calculation_history else 0
                }
            }
        }
        
        return export_data
        
    except Exception as e:
        return {'error': f"Export failed: {str(e)}"}

def clean_numeric_input(value: str) -> Optional[float]:
    """
    Clean and parse numeric input from user
    
    Args:
        value: String input from user
    
    Returns:
        Parsed float value or None if invalid
    """
    try:
        if not value or value.strip() == "":
            return None
        
        # Remove common formatting characters
        cleaned = re.sub(r'[€$,\s]', '', str(value))
        
        # Handle percentage
        if '%' in cleaned:
            cleaned = cleaned.replace('%', '')
            return float(cleaned) / 100
        
        # Handle K, M, B suffixes
        if cleaned.upper().endswith('K'):
            return float(cleaned[:-1]) * 1_000
        elif cleaned.upper().endswith('M'):
            return float(cleaned[:-1]) * 1_000_000
        elif cleaned.upper().endswith('B'):
            return float(cleaned[:-1]) * 1_000_000_000
        
        return float(cleaned)
        
    except (ValueError, TypeError):
        return None

def generate_summary_stats(valuations: List[float]) -> Dict[str, float]:
    """
    Generate summary statistics for a list of valuations
    
    Args:
        valuations: List of valuation amounts
    
    Returns:
        Dictionary with summary statistics
    """
    try:
        if not valuations:
            return {
                'count': 0,
                'mean': 0,
                'median': 0,
                'std': 0,
                'min': 0,
                'max': 0,
                'range': 0
            }
        
        valuations_array = np.array(valuations)
        
        return {
            'count': len(valuations),
            'mean': float(np.mean(valuations_array)),
            'median': float(np.median(valuations_array)),
            'std': float(np.std(valuations_array)),
            'min': float(np.min(valuations_array)),
            'max': float(np.max(valuations_array)),
            'range': float(np.max(valuations_array) - np.min(valuations_array))
        }
        
    except Exception:
        return {
            'count': 0,
            'mean': 0,
            'median': 0,
            'std': 0,
            'min': 0,
            'max': 0,
            'range': 0
        }

def create_comparison_table(calculations: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Create a comparison table from multiple calculations
    
    Args:
        calculations: List of calculation results
    
    Returns:
        Pandas DataFrame with comparison data
    """
    try:
        if not calculations:
            return pd.DataFrame()
        
        comparison_data = []
        
        for calc in calculations:
            comparison_data.append({
                'Method': calc.get('method', 'Unknown'),
                'Date': calc.get('timestamp', 'Unknown'),
                'Valuation': calc.get('valuation', 0),
                'Valuation (Formatted)': format_currency(calc.get('valuation', 0))
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Sort by valuation descending
        if 'Valuation' in df.columns:
            df = df.sort_values('Valuation', ascending=False)
        
        return df
        
    except Exception:
        return pd.DataFrame()

def validate_cash_flow_inputs(cash_flows: List[Any]) -> tuple[bool, str, List[float]]:
    """
    Validate and clean cash flow inputs
    
    Args:
        cash_flows: List of cash flow values
    
    Returns:
        Tuple of (is_valid, error_message, cleaned_cash_flows)
    """
    try:
        if not cash_flows:
            return False, "At least one cash flow is required", []
        
        cleaned_flows = []
        
        for i, cf in enumerate(cash_flows):
            if cf is None or cf == "":
                return False, f"Cash flow for year {i+1} is required", []
            
            try:
                cf_value = float(cf)
                if cf_value < 0:
                    return False, f"Cash flow for year {i+1} cannot be negative", []
                
                if not np.isfinite(cf_value):
                    return False, f"Cash flow for year {i+1} must be a finite number", []
                
                cleaned_flows.append(cf_value)
                
            except (ValueError, TypeError):
                return False, f"Cash flow for year {i+1} must be a valid number", []
        
        return True, "", cleaned_flows
        
    except Exception as e:
        return False, f"Cash flow validation failed: {str(e)}", []

def calculate_npv(cash_flows: List[float], discount_rate: float, initial_investment: float = 0) -> float:
    """
    Calculate Net Present Value
    
    Args:
        cash_flows: List of cash flows
        discount_rate: Discount rate as decimal
        initial_investment: Initial investment (negative cash flow at t=0)
    
    Returns:
        Net Present Value
    """
    try:
        if not cash_flows or discount_rate < 0:
            return 0.0
        
        npv = -initial_investment  # Initial investment as negative cash flow
        
        for i, cf in enumerate(cash_flows):
            year = i + 1
            present_value = cf / ((1 + discount_rate) ** year)
            npv += present_value
        
        return npv if np.isfinite(npv) else 0.0
        
    except Exception:
        return 0.0

def calculate_irr(cash_flows: List[float], initial_investment: float, max_iterations: int = 100) -> Optional[float]:
    """
    Calculate Internal Rate of Return using Newton-Raphson method
    
    Args:
        cash_flows: List of cash flows
        initial_investment: Initial investment
        max_iterations: Maximum iterations for convergence
    
    Returns:
        IRR as decimal or None if no solution found
    """
    try:
        if not cash_flows or initial_investment <= 0:
            return None
        
        # Combine initial investment with cash flows
        all_flows = [-initial_investment] + cash_flows
        
        # Initial guess
        irr = 0.1  # 10%
        
        for _ in range(max_iterations):
            npv = sum(cf / ((1 + irr) ** i) for i, cf in enumerate(all_flows))
            
            if abs(npv) < 1e-6:  # Convergence threshold
                return irr
            
            # Derivative of NPV
            dnpv = sum(-i * cf / ((1 + irr) ** (i + 1)) for i, cf in enumerate(all_flows))
            
            if abs(dnpv) < 1e-12:  # Avoid division by zero
                break
            
            # Newton-Raphson step
            irr = irr - npv / dnpv
            
            # Keep IRR in reasonable bounds
            if irr < -0.99 or irr > 10:  # -99% to 1000%
                break
        
        # Verify solution
        npv_check = sum(cf / ((1 + irr) ** i) for i, cf in enumerate(all_flows))
        if abs(npv_check) < 1e-3:  # Solution tolerance
            return irr
        
        return None
        
    except Exception:
        return None

def get_sector_benchmark(sector: str, metric_type: str) -> Optional[float]:
    """
    Get benchmark multiple for a sector and metric
    
    Args:
        sector: Industry sector
        metric_type: Revenue or EBITDA
    
    Returns:
        Benchmark multiple or None if not found
    """
    try:
        from data_models import SECTOR_MULTIPLES
        
        if sector in SECTOR_MULTIPLES and metric_type in SECTOR_MULTIPLES[sector]:
            return SECTOR_MULTIPLES[sector][metric_type]
        
        return None
        
    except Exception:
        return None
