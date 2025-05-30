"""
Automated Testing Suite for Startup Valuation Calculator
Comprehensive tests for all valuation methods and core functionality
"""

import unittest
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add the project root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from valuation_calculator import ValuationCalculator
from utils import format_currency


class TestDCFMethod(unittest.TestCase):
    """Test cases for DCF valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_dcf_basic_calculation(self):
        """Test basic DCF calculation with simple inputs"""
        inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[100000, 120000, 144000, 172800, 207360],
            discount_rate=0.12,
            terminal_growth=0.03
        )
        
        result = self.calculator.calculate_dcf(inputs)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.valuation, (int, float))
        self.assertGreater(result.valuation, 0)
        self.assertIn('operating_value', result.details)
        self.assertIn('terminal_pv', result.details)
    
    def test_dcf_with_growth_rate(self):
        """Test DCF calculation with growth rate projection"""
        inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[100000],
            discount_rate=0.15,
            terminal_growth=0.025,
            growth_rate=0.20
        )
        
        result = self.calculator.calculate_dcf(inputs)
        
        self.assertTrue(result.success)
        self.assertGreater(result.valuation, 0)
        self.assertEqual(len(result.details['projected_cash_flows']), 5)
    
    def test_dcf_edge_cases(self):
        """Test DCF method with edge cases"""
        # Test with zero cash flows
        inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[0, 0, 0],
            discount_rate=0.10,
            terminal_growth=0.02
        )
        
        result = self.calculator.calculate_dcf(inputs)
        self.assertTrue(result.success)
        self.assertEqual(result.valuation, 0)
        
        # Test with high discount rate
        inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[1000000, 1200000, 1400000],
            discount_rate=0.50,
            terminal_growth=0.03
        )
        
        result = self.calculator.calculate_dcf(inputs)
        self.assertTrue(result.success)
        self.assertGreater(result.valuation, 0)
    
    def test_dcf_invalid_inputs(self):
        """Test DCF method with invalid inputs"""
        # Test with negative discount rate
        inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[100000, 120000],
            discount_rate=-0.05,
            terminal_growth=0.03
        )
        
        result = self.calculator.calculate_dcf(inputs)
        self.assertFalse(result.success)
        
        # Test with terminal growth > discount rate
        inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[100000, 120000],
            discount_rate=0.05,
            terminal_growth=0.10
        )
        
        result = self.calculator.calculate_dcf(inputs)
        self.assertFalse(result.success)


class TestMarketMultiplesMethod(unittest.TestCase):
    """Test cases for Market Multiples valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_multiples_basic_calculation(self):
        """Test basic market multiples calculation"""
        inputs = MultiplesInputs(
            method="Market Multiples",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            sector="Technology",
            metric_type="Revenue",
            metric_value=1000000,
            multiple=5.0
        )
        
        result = self.calculator.calculate_market_multiples(inputs)
        
        self.assertTrue(result.success)
        self.assertEqual(result.valuation, 5000000)
        self.assertIn('multiple_applied', result.details)
        self.assertIn('sector_context', result.details)
    
    def test_multiples_different_sectors(self):
        """Test market multiples across different sectors"""
        sectors = ["Technology", "Healthcare", "Financial Services", "Manufacturing"]
        
        for sector in sectors:
            inputs = MultiplesInputs(
                method="Market Multiples",
                timestamp=datetime.now().isoformat(),
                user_inputs={},
                sector=sector,
                metric_type="Revenue",
                metric_value=2000000,
                multiple=3.5
            )
            
            result = self.calculator.calculate_market_multiples(inputs)
            self.assertTrue(result.success)
            self.assertEqual(result.valuation, 7000000)
    
    def test_multiples_different_metrics(self):
        """Test market multiples with different metric types"""
        metrics = ["Revenue", "EBITDA", "Users", "ARR"]
        
        for metric in metrics:
            inputs = MultiplesInputs(
                method="Market Multiples",
                timestamp=datetime.now().isoformat(),
                user_inputs={},
                sector="Technology",
                metric_type=metric,
                metric_value=500000,
                multiple=4.0
            )
            
            result = self.calculator.calculate_market_multiples(inputs)
            self.assertTrue(result.success)
            self.assertEqual(result.valuation, 2000000)
    
    def test_multiples_edge_cases(self):
        """Test market multiples edge cases"""
        # Test with zero metric value
        inputs = MultiplesInputs(
            method="Market Multiples",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            sector="Technology",
            metric_type="Revenue",
            metric_value=0,
            multiple=5.0
        )
        
        result = self.calculator.calculate_market_multiples(inputs)
        self.assertTrue(result.success)
        self.assertEqual(result.valuation, 0)
        
        # Test with very high multiple
        inputs = MultiplesInputs(
            method="Market Multiples",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            sector="Technology",
            metric_type="Revenue",
            metric_value=1000000,
            multiple=100.0
        )
        
        result = self.calculator.calculate_market_multiples(inputs)
        self.assertTrue(result.success)
        self.assertEqual(result.valuation, 100000000)


class TestScorecardMethod(unittest.TestCase):
    """Test cases for Scorecard valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_scorecard_basic_calculation(self):
        """Test basic scorecard calculation"""
        inputs = ScorecardInputs(
            method="Scorecard",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            base_valuation=2000000,
            criteria_scores={
                "Management Team": 4,
                "Market Opportunity": 3,
                "Product/Technology": 5,
                "Competitive Environment": 3,
                "Marketing/Sales": 4,
                "Need for Investment": 2,
                "Other": 3
            }
        )
        
        result = self.calculator.calculate_scorecard(inputs)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.valuation, (int, float))
        self.assertGreater(result.valuation, 0)
        self.assertIn('adjustment_factor', result.details)
        self.assertIn('criteria_breakdown', result.details)
    
    def test_scorecard_perfect_scores(self):
        """Test scorecard with perfect scores"""
        inputs = ScorecardInputs(
            method="Scorecard",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            base_valuation=1000000,
            criteria_scores={
                "Management Team": 5,
                "Market Opportunity": 5,
                "Product/Technology": 5,
                "Competitive Environment": 5,
                "Marketing/Sales": 5,
                "Need for Investment": 5,
                "Other": 5
            }
        )
        
        result = self.calculator.calculate_scorecard(inputs)
        
        self.assertTrue(result.success)
        # Perfect scores should result in higher valuation than base
        self.assertGreater(result.valuation, inputs.base_valuation)
        self.assertAlmostEqual(result.details['adjustment_factor'], 1.25, places=2)
    
    def test_scorecard_poor_scores(self):
        """Test scorecard with poor scores"""
        inputs = ScorecardInputs(
            method="Scorecard",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            base_valuation=1000000,
            criteria_scores={
                "Management Team": 1,
                "Market Opportunity": 1,
                "Product/Technology": 1,
                "Competitive Environment": 1,
                "Marketing/Sales": 1,
                "Need for Investment": 1,
                "Other": 1
            }
        )
        
        result = self.calculator.calculate_scorecard(inputs)
        
        self.assertTrue(result.success)
        # Poor scores should result in lower valuation than base
        self.assertLess(result.valuation, inputs.base_valuation)
        self.assertLess(result.details['adjustment_factor'], 1.0)


class TestBerkusMethod(unittest.TestCase):
    """Test cases for Berkus valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_berkus_basic_calculation(self):
        """Test basic Berkus calculation"""
        inputs = BerkusInputs(
            method="Berkus",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            criteria_scores={
                "Sound Idea": 3,
                "Prototype": 4,
                "Quality Management": 3,
                "Strategic Relationships": 2,
                "Product Rollout": 1
            }
        )
        
        result = self.calculator.calculate_berkus(inputs)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.valuation, (int, float))
        self.assertGreater(result.valuation, 0)
        self.assertIn('breakdown', result.details)
        self.assertIn('max_possible', result.details)
    
    def test_berkus_maximum_scores(self):
        """Test Berkus with maximum scores"""
        inputs = BerkusInputs(
            method="Berkus",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            criteria_scores={
                "Sound Idea": 5,
                "Prototype": 5,
                "Quality Management": 5,
                "Strategic Relationships": 5,
                "Product Rollout": 5
            }
        )
        
        result = self.calculator.calculate_berkus(inputs)
        
        self.assertTrue(result.success)
        self.assertEqual(result.valuation, 2500000)  # 5 * 500k each
        self.assertEqual(result.details['max_possible'], 2500000)
    
    def test_berkus_minimum_scores(self):
        """Test Berkus with minimum scores"""
        inputs = BerkusInputs(
            method="Berkus",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            criteria_scores={
                "Sound Idea": 0,
                "Prototype": 0,
                "Quality Management": 0,
                "Strategic Relationships": 0,
                "Product Rollout": 0
            }
        )
        
        result = self.calculator.calculate_berkus(inputs)
        
        self.assertTrue(result.success)
        self.assertEqual(result.valuation, 0)
    
    def test_berkus_partial_scores(self):
        """Test Berkus with partial implementation"""
        inputs = BerkusInputs(
            method="Berkus",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            criteria_scores={
                "Sound Idea": 5,
                "Prototype": 3,
                "Quality Management": 0,
                "Strategic Relationships": 0,
                "Product Rollout": 0
            }
        )
        
        result = self.calculator.calculate_berkus(inputs)
        
        self.assertTrue(result.success)
        expected_value = (5 * 500000) + (3 * 500000)  # 4,000,000
        self.assertEqual(result.valuation, expected_value)


class TestRiskFactorMethod(unittest.TestCase):
    """Test cases for Risk Factor Summation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_risk_factor_basic_calculation(self):
        """Test basic risk factor calculation"""
        inputs = RiskFactorInputs(
            method="Risk Factor Summation",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            base_valuation=3000000,
            risk_factors={
                "Management": 1,
                "Stage of Business": 0,
                "Political/Legislation Risk": -1,
                "Manufacturing Risk": 0,
                "Sales/Marketing Risk": 2,
                "Funding/Capital Risk": -2,
                "Competition Risk": 1,
                "Technology Risk": 0,
                "Litigation Risk": 0,
                "International Risk": -1,
                "Reputation Risk": 0,
                "Potential Lucrative Exit": 2
            }
        )
        
        result = self.calculator.calculate_risk_factor_summation(inputs)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.valuation, (int, float))
        self.assertGreater(result.valuation, 0)
        self.assertIn('total_adjustment', result.details)
        self.assertIn('risk_breakdown', result.details)
    
    def test_risk_factor_all_positive(self):
        """Test risk factor with all positive adjustments"""
        inputs = RiskFactorInputs(
            method="Risk Factor Summation",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            base_valuation=1000000,
            risk_factors={
                "Management": 2,
                "Stage of Business": 2,
                "Political/Legislation Risk": 1,
                "Manufacturing Risk": 1,
                "Sales/Marketing Risk": 2,
                "Funding/Capital Risk": 2,
                "Competition Risk": 1,
                "Technology Risk": 2,
                "Litigation Risk": 1,
                "International Risk": 1,
                "Reputation Risk": 1,
                "Potential Lucrative Exit": 2
            }
        )
        
        result = self.calculator.calculate_risk_factor_summation(inputs)
        
        self.assertTrue(result.success)
        # All positive should increase valuation significantly
        self.assertGreater(result.valuation, inputs.base_valuation * 1.5)
    
    def test_risk_factor_all_negative(self):
        """Test risk factor with all negative adjustments"""
        inputs = RiskFactorInputs(
            method="Risk Factor Summation",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            base_valuation=1000000,
            risk_factors={
                "Management": -2,
                "Stage of Business": -1,
                "Political/Legislation Risk": -2,
                "Manufacturing Risk": -1,
                "Sales/Marketing Risk": -2,
                "Funding/Capital Risk": -2,
                "Competition Risk": -2,
                "Technology Risk": -1,
                "Litigation Risk": -2,
                "International Risk": -1,
                "Reputation Risk": -1,
                "Potential Lucrative Exit": -2
            }
        )
        
        result = self.calculator.calculate_risk_factor_summation(inputs)
        
        self.assertTrue(result.success)
        # All negative should decrease valuation significantly
        self.assertLess(result.valuation, inputs.base_valuation * 0.5)


class TestVCMethod(unittest.TestCase):
    """Test cases for Venture Capital method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_vc_method_basic_calculation(self):
        """Test basic VC method calculation"""
        inputs = VCMethodInputs(
            method="Venture Capital",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            expected_revenue=10000000,
            exit_multiple=5.0,
            required_return=0.30,
            years_to_exit=5
        )
        
        result = self.calculator.calculate_vc_method(inputs)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.valuation, (int, float))
        self.assertGreater(result.valuation, 0)
        self.assertIn('exit_value', result.details)
        self.assertIn('present_value', result.details)
    
    def test_vc_method_with_investment(self):
        """Test VC method with investment requirements"""
        inputs = VCMethodInputs(
            method="Venture Capital",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            expected_revenue=5000000,
            exit_multiple=4.0,
            required_return=0.25,
            years_to_exit=4,
            investment_needed=2000000
        )
        
        result = self.calculator.calculate_vc_method(inputs)
        
        self.assertTrue(result.success)
        self.assertIn('investment_needed', result.details)
        self.assertIn('ownership_percentage', result.details)
        self.assertIn('post_money_valuation', result.details)
    
    def test_vc_method_different_scenarios(self):
        """Test VC method with different time horizons and returns"""
        scenarios = [
            (3, 0.40, 8.0),  # High return, short term, high multiple
            (7, 0.20, 3.0),  # Low return, long term, low multiple
            (5, 0.30, 5.0),  # Medium scenario
        ]
        
        for years, return_rate, multiple in scenarios:
            inputs = VCMethodInputs(
                method="Venture Capital",
                timestamp=datetime.now().isoformat(),
                user_inputs={},
                expected_revenue=8000000,
                exit_multiple=multiple,
                required_return=return_rate,
                years_to_exit=years
            )
            
            result = self.calculator.calculate_vc_method(inputs)
            self.assertTrue(result.success)
            self.assertGreater(result.valuation, 0)


class TestValidationSchemas(unittest.TestCase):
    """Test cases for input validation"""
    
    def setUp(self):
        self.validator = ValidationSchemas()
    
    def test_dcf_validation(self):
        """Test DCF input validation"""
        # Valid inputs
        valid_result = self.validator.validate_dcf_inputs(
            cash_flows=[100000, 120000, 144000],
            discount_rate=0.12,
            terminal_growth=0.03
        )
        self.assertTrue(valid_result.is_valid)
        
        # Invalid inputs - negative discount rate
        invalid_result = self.validator.validate_dcf_inputs(
            cash_flows=[100000, 120000],
            discount_rate=-0.05,
            terminal_growth=0.03
        )
        self.assertFalse(invalid_result.is_valid)
    
    def test_multiples_validation(self):
        """Test market multiples validation"""
        # Valid inputs
        valid_result = self.validator.validate_multiples_inputs(
            sector="Technology",
            metric_type="Revenue",
            metric_value=1000000,
            multiple=5.0
        )
        self.assertTrue(valid_result.is_valid)
        
        # Invalid inputs - negative multiple
        invalid_result = self.validator.validate_multiples_inputs(
            sector="Technology",
            metric_type="Revenue",
            metric_value=1000000,
            multiple=-2.0
        )
        self.assertFalse(invalid_result.is_valid)
    
    def test_scorecard_validation(self):
        """Test scorecard validation"""
        # Valid inputs
        valid_result = self.validator.validate_scorecard_inputs(
            base_valuation=2000000,
            criteria_scores={
                "Management Team": 4,
                "Market Opportunity": 3,
                "Product/Technology": 5
            }
        )
        self.assertTrue(valid_result.is_valid)
        
        # Invalid inputs - score out of range
        invalid_result = self.validator.validate_scorecard_inputs(
            base_valuation=2000000,
            criteria_scores={
                "Management Team": 6,  # Invalid score > 5
                "Market Opportunity": 3
            }
        )
        self.assertFalse(invalid_result.is_valid)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_format_currency(self):
        """Test currency formatting function"""
        self.assertEqual(format_currency(1000000), "$1,000,000")
        self.assertEqual(format_currency(1234.56), "$1,234.56")
        self.assertEqual(format_currency(0), "$0")
        self.assertEqual(format_currency(-500), "-$500")
    
    def test_validate_positive_number(self):
        """Test positive number validation"""
        self.assertTrue(validate_positive_number(100))
        self.assertTrue(validate_positive_number(0.1))
        self.assertFalse(validate_positive_number(-10))
        self.assertFalse(validate_positive_number(0))
        self.assertTrue(validate_positive_number(0, allow_zero=True))


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_complete_valuation_workflow(self):
        """Test complete valuation workflow with multiple methods"""
        results = []
        
        # DCF Method
        dcf_inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[200000, 250000, 300000, 350000, 400000],
            discount_rate=0.15,
            terminal_growth=0.03
        )
        dcf_result = self.calculator.calculate_dcf(dcf_inputs)
        self.assertTrue(dcf_result.success)
        results.append(dcf_result.valuation)
        
        # Market Multiples Method
        multiples_inputs = MultiplesInputs(
            method="Market Multiples",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            sector="Technology",
            metric_type="Revenue",
            metric_value=1500000,
            multiple=4.0
        )
        multiples_result = self.calculator.calculate_market_multiples(multiples_inputs)
        self.assertTrue(multiples_result.success)
        results.append(multiples_result.valuation)
        
        # Berkus Method
        berkus_inputs = BerkusInputs(
            method="Berkus",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            criteria_scores={
                "Sound Idea": 4,
                "Prototype": 3,
                "Quality Management": 4,
                "Strategic Relationships": 2,
                "Product Rollout": 1
            }
        )
        berkus_result = self.calculator.calculate_berkus(berkus_inputs)
        self.assertTrue(berkus_result.success)
        results.append(berkus_result.valuation)
        
        # Verify all methods produced positive valuations
        for valuation in results:
            self.assertGreater(valuation, 0)
        
        # Calculate average valuation
        average_valuation = sum(results) / len(results)
        self.assertGreater(average_valuation, 0)
    
    def test_error_handling_integration(self):
        """Test error handling across different methods"""
        # Test DCF with invalid inputs
        dcf_inputs = DCFInputs(
            method="DCF",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            cash_flows=[],  # Empty cash flows
            discount_rate=0.10,
            terminal_growth=0.15  # Greater than discount rate
        )
        dcf_result = self.calculator.calculate_dcf(dcf_inputs)
        self.assertFalse(dcf_result.success)
        self.assertIsNotNone(dcf_result.error_message)
        
        # Test multiples with negative values
        multiples_inputs = MultiplesInputs(
            method="Market Multiples",
            timestamp=datetime.now().isoformat(),
            user_inputs={},
            sector="Technology",
            metric_type="Revenue",
            metric_value=-1000000,  # Negative value
            multiple=3.0
        )
        multiples_result = self.calculator.calculate_market_multiples(multiples_inputs)
        self.assertFalse(multiples_result.success)


def run_test_suite():
    """Run the complete test suite and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestDCFMethod,
        TestMarketMultiplesMethod,
        TestScorecardMethod,
        TestBerkusMethod,
        TestRiskFactorMethod,
        TestVCMethod,
        TestValidationSchemas,
        TestUtilityFunctions,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    return result


if __name__ == "__main__":
    print("Starting Automated Test Suite for Startup Valuation Calculator")
    print("=" * 70)
    
    result = run_test_suite()
    
    print("\n" + "=" * 70)
    print("TEST SUITE SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\nAll tests passed successfully! ✅")
    else:
        print(f"\nSome tests failed. Please review the issues above. ❌")