"""
Data Models Module
Contains data structures, constants, and validation models
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

# Sector multiples data for market comparison
SECTOR_MULTIPLES = {
    "Technology": {"Revenue": 6.5, "EBITDA": 15.2},
    "SaaS": {"Revenue": 8.2, "EBITDA": 18.5},
    "E-commerce": {"Revenue": 3.1, "EBITDA": 12.8},
    "Fintech": {"Revenue": 7.8, "EBITDA": 16.9},
    "Biotech": {"Revenue": 12.4, "EBITDA": 25.6},
    "Cleantech": {"Revenue": 4.7, "EBITDA": 13.1},
    "Marketplace": {"Revenue": 5.3, "EBITDA": 14.7},
    "Media": {"Revenue": 2.8, "EBITDA": 9.4},
    "Manufacturing": {"Revenue": 1.9, "EBITDA": 8.2},
    "Retail": {"Revenue": 1.4, "EBITDA": 6.8},
    "Healthcare": {"Revenue": 4.2, "EBITDA": 12.1},
    "Education": {"Revenue": 3.8, "EBITDA": 10.5},
    "Gaming": {"Revenue": 7.1, "EBITDA": 16.3},
    "Food & Beverage": {"Revenue": 2.1, "EBITDA": 7.8},
    "Real Estate": {"Revenue": 3.4, "EBITDA": 9.7}
}

@dataclass
class ValidationResult:
    """Result of input validation"""
    is_valid: bool
    error_message: str = ""

@dataclass
class ValuationInput:
    """Base class for valuation inputs"""
    method: str
    timestamp: str
    user_inputs: Dict[str, Any]

@dataclass
class DCFInputs(ValuationInput):
    """DCF method specific inputs"""
    cash_flows: list
    discount_rate: float
    terminal_growth: float
    growth_rate: Optional[float] = None

@dataclass
class MultiplesInputs(ValuationInput):
    """Market multiples method inputs"""
    sector: str
    metric_type: str
    metric_value: float
    multiple: float

@dataclass
class ScorecardInputs(ValuationInput):
    """Scorecard method inputs"""
    base_valuation: float
    criteria_scores: Dict[str, int]
    criteria_weights: Optional[Dict[str, float]] = None

@dataclass
class BerkusInputs(ValuationInput):
    """Berkus method inputs"""
    criteria_scores: Dict[str, int]

@dataclass
class RiskFactorInputs(ValuationInput):
    """Risk factor summation inputs"""
    base_valuation: float
    risk_factors: Dict[str, int]

@dataclass
class VCMethodInputs(ValuationInput):
    """Venture capital method inputs"""
    expected_revenue: float
    exit_multiple: float
    required_return: float
    years_to_exit: int
    investment_needed: Optional[float] = None

@dataclass
class ValuationResult:
    """Base valuation result"""
    method: str
    valuation: float
    success: bool
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# Validation constants
MIN_CASH_FLOW = 0
MAX_CASH_FLOW = 1000000000  # 1B
MIN_DISCOUNT_RATE = 0.01  # 1%
MAX_DISCOUNT_RATE = 0.50  # 50%
MIN_TERMINAL_GROWTH = 0.00  # 0%
MAX_TERMINAL_GROWTH = 0.10  # 10%

MIN_VALUATION = 0
MAX_VALUATION = 100000000000  # 100B

MIN_SCORE = 0
MAX_SCORE = 5

MIN_RISK_RATING = -2
MAX_RISK_RATING = 2

# Default criteria weights for scorecard method
DEFAULT_SCORECARD_WEIGHTS = {
    "team": 0.25,
    "product": 0.20,
    "market": 0.20,
    "competition": 0.15,
    "financial": 0.10,
    "legal": 0.10
}

# Berkus criteria definitions
BERKUS_CRITERIA = {
    "concept": {
        "name": "Sound Idea (Basic Value)",
        "description": "Quality and market potential of the core business concept",
        "max_value": 500000
    },
    "prototype": {
        "name": "Prototype (Reduces Technology Risk)",
        "description": "Functional prototype or MVP that demonstrates technical feasibility",
        "max_value": 500000
    },
    "team": {
        "name": "Quality Management Team (Reduces Execution Risk)",
        "description": "Experience and capabilities of the founding and management team",
        "max_value": 500000
    },
    "strategic_relationships": {
        "name": "Strategic Relationships (Reduces Market Risk)",
        "description": "Key partnerships, advisors, and market connections",
        "max_value": 500000
    },
    "product_rollout": {
        "name": "Product Rollout or Sales (Reduces Financial Risk)",
        "description": "Evidence of product-market fit through sales or user adoption",
        "max_value": 500000
    }
}

# Risk factor categories for risk factor summation
RISK_FACTOR_CATEGORIES = {
    "management": {
        "name": "Management Team Risk",
        "description": "Risk related to management experience and capabilities"
    },
    "stage": {
        "name": "Development Stage Risk",
        "description": "Risk based on company's current development stage"
    },
    "legislation": {
        "name": "Legislative/Political Risk",
        "description": "Risk from regulatory changes or political factors"
    },
    "manufacturing": {
        "name": "Manufacturing Risk",
        "description": "Risk related to production and operational scalability"
    },
    "sales": {
        "name": "Sales/Marketing Risk",
        "description": "Risk in market penetration and customer acquisition"
    },
    "funding": {
        "name": "Funding/Capital Risk",
        "description": "Risk of securing adequate funding for growth"
    },
    "competition": {
        "name": "Competition Risk",
        "description": "Risk from existing and potential competitors"
    },
    "technology": {
        "name": "Technology Risk",
        "description": "Risk of technical execution and innovation"
    },
    "litigation": {
        "name": "Litigation Risk",
        "description": "Risk from legal disputes and intellectual property issues"
    },
    "international": {
        "name": "International Risk",
        "description": "Risk from international expansion and operations"
    },
    "reputation": {
        "name": "Reputation Risk",
        "description": "Risk to brand and company reputation"
    },
    "exit": {
        "name": "Exit Strategy Risk",
        "description": "Risk related to potential exit opportunities and liquidity"
    }
}

# Scorecard criteria definitions
SCORECARD_CRITERIA = {
    "team": {
        "name": "Management Team Quality",
        "description": "Experience, track record, and capabilities of the team",
        "weight": 0.25
    },
    "product": {
        "name": "Product/Technology",
        "description": "Innovation, differentiation, and technical merit",
        "weight": 0.20
    },
    "market": {
        "name": "Market Opportunity",
        "description": "Market size, growth potential, and timing",
        "weight": 0.20
    },
    "competition": {
        "name": "Competitive Advantage",
        "description": "Barriers to entry, moats, and competitive positioning",
        "weight": 0.15
    },
    "financial": {
        "name": "Financial Performance",
        "description": "Revenue growth, unit economics, and financial metrics",
        "weight": 0.10
    },
    "legal": {
        "name": "Legal/IP Protection",
        "description": "Intellectual property, legal structure, and compliance",
        "weight": 0.10
    }
}

# Application constants
APP_TITLE = "Startup Valuation Calculator"
APP_VERSION = "2.0.0"
REPORT_TEMPLATE_VERSION = "1.0"

# Chart color schemes
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff6b35',
    'info': '#9467bd',
    'light': '#bcbd22',
    'dark': '#17becf'
}

# PDF report settings
PDF_SETTINGS = {
    'page_size': 'A4',
    'margin_top': 72,
    'margin_bottom': 18,
    'margin_left': 72,
    'margin_right': 72,
    'font_size_title': 24,
    'font_size_header': 16,
    'font_size_normal': 12,
    'font_size_small': 10
}

# Error messages
ERROR_MESSAGES = {
    'invalid_cash_flows': "Cash flows must be positive numbers",
    'invalid_discount_rate': f"Discount rate must be between {MIN_DISCOUNT_RATE*100:.0f}% and {MAX_DISCOUNT_RATE*100:.0f}%",
    'invalid_terminal_growth': f"Terminal growth must be between {MIN_TERMINAL_GROWTH*100:.0f}% and {MAX_TERMINAL_GROWTH*100:.0f}%",
    'discount_vs_terminal': "Discount rate must be higher than terminal growth rate",
    'invalid_valuation': f"Valuation must be between €{MIN_VALUATION:,} and €{MAX_VALUATION:,}",
    'invalid_score': f"Scores must be between {MIN_SCORE} and {MAX_SCORE}",
    'invalid_risk_rating': f"Risk ratings must be between {MIN_RISK_RATING} and {MAX_RISK_RATING}",
    'calculation_failed': "Calculation failed due to invalid inputs",
    'pdf_generation_failed': "PDF report generation failed",
    'chart_generation_failed': "Chart generation failed"
}
