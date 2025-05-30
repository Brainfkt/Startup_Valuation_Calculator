"""
Automated Testing Suite for Startup Valuation Calculator
Tests for all valuation methods with correct method signatures
"""

import unittest
import sys
import os
from datetime import datetime

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
        cash_flows = [100000, 120000, 144000, 172800, 207360]
        growth_rate = 0.20
        discount_rate = 0.12
        terminal_growth = 0.03
        
        result = self.calculator.dcf_valuation(cash_flows, growth_rate, discount_rate, terminal_growth)
        
        self.assertNotIn('error', result)
        self.assertIn('valuation', result)
        self.assertGreater(result['valuation'], 0)
        self.assertIn('operating_value', result)
        self.assertIn('terminal_pv', result)
    
    def test_dcf_with_empty_cash_flows(self):
        """Test DCF with empty cash flows"""
        cash_flows = []
        growth_rate = 0.15
        discount_rate = 0.10
        terminal_growth = 0.02
        
        result = self.calculator.dcf_valuation(cash_flows, growth_rate, discount_rate, terminal_growth)
        
        # Should either handle gracefully or return error
        if 'error' in result:
            self.assertIsInstance(result['error'], str)
        else:
            self.assertEqual(result['valuation'], 0)
    
    def test_dcf_edge_cases(self):
        """Test DCF method with edge cases"""
        # Test with zero cash flows
        cash_flows = [0, 0, 0]
        growth_rate = 0.20
        discount_rate = 0.10
        terminal_growth = 0.02
        
        result = self.calculator.dcf_valuation(cash_flows, growth_rate, discount_rate, terminal_growth)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['valuation'], 0)
        
        # Test with high discount rate
        cash_flows = [1000000, 1200000, 1400000]
        growth_rate = 0.15
        discount_rate = 0.50
        terminal_growth = 0.03
        
        result = self.calculator.dcf_valuation(cash_flows, growth_rate, discount_rate, terminal_growth)
        
        self.assertNotIn('error', result)
        self.assertGreater(result['valuation'], 0)
    
    def test_dcf_invalid_inputs(self):
        """Test DCF method with invalid inputs"""
        # Test with negative discount rate
        cash_flows = [100000, 120000]
        growth_rate = 0.20
        discount_rate = -0.05
        terminal_growth = 0.03
        
        result = self.calculator.dcf_valuation(cash_flows, growth_rate, discount_rate, terminal_growth)
        
        self.assertIn('error', result)
        
        # Test with terminal growth > discount rate
        cash_flows = [100000, 120000]
        growth_rate = 0.20
        discount_rate = 0.05
        terminal_growth = 0.10
        
        result = self.calculator.dcf_valuation(cash_flows, growth_rate, discount_rate, terminal_growth)
        
        self.assertIn('error', result)


class TestMarketMultiplesMethod(unittest.TestCase):
    """Test cases for Market Multiples valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_multiples_basic_calculation(self):
        """Test basic market multiples calculation"""
        revenue = 1000000
        multiple = 5.0
        metric_type = "Revenue"
        
        result = self.calculator.market_multiples_valuation(revenue, multiple, metric_type)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['valuation'], 5000000)
        self.assertIn('metric', result)
        self.assertIn('multiple', result)
    
    def test_multiples_different_metrics(self):
        """Test market multiples with different metric types"""
        metrics = ["Revenue", "EBITDA"]
        
        for metric in metrics:
            revenue = 500000
            multiple = 4.0
            
            result = self.calculator.market_multiples_valuation(revenue, multiple, metric)
            
            self.assertNotIn('error', result)
            self.assertEqual(result['valuation'], 2000000)
            self.assertEqual(result['metric_type'], metric)
    
    def test_multiples_edge_cases(self):
        """Test market multiples edge cases"""
        # Test with zero metric value
        revenue = 0
        multiple = 5.0
        
        result = self.calculator.market_multiples_valuation(revenue, multiple)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['valuation'], 0)
        
        # Test with very high multiple
        revenue = 1000000
        multiple = 100.0
        
        result = self.calculator.market_multiples_valuation(revenue, multiple)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['valuation'], 100000000)
    
    def test_multiples_invalid_inputs(self):
        """Test market multiples with invalid inputs"""
        # Test with negative revenue
        revenue = -1000000
        multiple = 3.0
        
        result = self.calculator.market_multiples_valuation(revenue, multiple)
        
        self.assertIn('error', result)
        
        # Test with negative multiple
        revenue = 1000000
        multiple = -2.0
        
        result = self.calculator.market_multiples_valuation(revenue, multiple)
        
        self.assertIn('error', result)


class TestScorecardMethod(unittest.TestCase):
    """Test cases for Scorecard valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_scorecard_basic_calculation(self):
        """Test basic scorecard calculation"""
        base_valuation = 2000000
        criteria_scores = {
            "team": 4,
            "product": 3,
            "market": 5,
            "competition": 3,
            "financial": 4,
            "legal": 2
        }
        
        result = self.calculator.scorecard_valuation(base_valuation, criteria_scores)
        
        self.assertNotIn('error', result)
        self.assertIn('valuation', result)
        self.assertGreater(result['valuation'], 0)
        self.assertIn('adjustment_factor', result)
        self.assertIn('criteria_analysis', result)
    
    def test_scorecard_perfect_scores(self):
        """Test scorecard with perfect scores"""
        base_valuation = 1000000
        criteria_scores = {
            "team": 5,
            "product": 5,
            "market": 5,
            "competition": 5,
            "financial": 5,
            "legal": 5
        }
        
        result = self.calculator.scorecard_valuation(base_valuation, criteria_scores)
        
        self.assertNotIn('error', result)
        # Perfect scores should result in higher valuation than base
        self.assertGreater(result['valuation'], base_valuation)
    
    def test_scorecard_poor_scores(self):
        """Test scorecard with poor scores"""
        base_valuation = 1000000
        criteria_scores = {
            "team": 1,
            "product": 1,
            "market": 1,
            "competition": 1,
            "financial": 1,
            "legal": 1
        }
        
        result = self.calculator.scorecard_valuation(base_valuation, criteria_scores)
        
        self.assertNotIn('error', result)
        # Poor scores should result in lower valuation than base
        self.assertLess(result['valuation'], base_valuation)
    
    def test_scorecard_invalid_inputs(self):
        """Test scorecard with invalid inputs"""
        # Test with invalid score
        base_valuation = 1000000
        criteria_scores = {
            "team": 6  # Invalid score > 5
        }
        
        result = self.calculator.scorecard_valuation(base_valuation, criteria_scores)
        
        self.assertIn('error', result)
        
        # Test with negative base valuation
        base_valuation = -1000000
        criteria_scores = {"team": 3}
        
        result = self.calculator.scorecard_valuation(base_valuation, criteria_scores)
        
        self.assertIn('error', result)


class TestBerkusMethod(unittest.TestCase):
    """Test cases for Berkus valuation method"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_berkus_basic_calculation(self):
        """Test basic Berkus calculation"""
        criteria_scores = {
            "concept": 3,
            "prototype": 4,
            "team": 3,
            "strategic_relationships": 2,
            "product_rollout": 1
        }
        
        result = self.calculator.berkus_valuation(criteria_scores)
        
        self.assertNotIn('error', result)
        self.assertIn('valuation', result)
        self.assertGreater(result['valuation'], 0)
        self.assertIn('breakdown', result)
        self.assertIn('max_possible', result)
    
    def test_berkus_maximum_scores(self):
        """Test Berkus with maximum scores"""
        criteria_scores = {
            "concept": 5,
            "prototype": 5,
            "team": 5,
            "strategic_relationships": 5,
            "product_rollout": 5
        }
        
        result = self.calculator.berkus_valuation(criteria_scores)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['valuation'], 2500000)  # 5 * 500k each
        self.assertEqual(result['max_possible'], 2500000)
    
    def test_berkus_minimum_scores(self):
        """Test Berkus with minimum scores"""
        criteria_scores = {
            "concept": 0,
            "prototype": 0,
            "team": 0,
            "strategic_relationships": 0,
            "product_rollout": 0
        }
        
        result = self.calculator.berkus_valuation(criteria_scores)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['valuation'], 0)
    
    def test_berkus_invalid_inputs(self):
        """Test Berkus with invalid inputs"""
        # Test with missing criteria
        criteria_scores = {
            "concept": 5,
            "prototype": 3
            # Missing other criteria
        }
        
        result = self.calculator.berkus_valuation(criteria_scores)
        
        self.assertIn('error', result)
        
        # Test with invalid score
        criteria_scores = {
            "concept": 6,  # Invalid score > 5
            "prototype": 3,
            "team": 4,
            "strategic_relationships": 2,
            "product_rollout": 1
        }
        
        result = self.calculator.berkus_valuation(criteria_scores)
        
        self.assertIn('error', result)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_format_currency(self):
        """Test currency formatting function"""
        # Test that format_currency returns a string with proper formatting
        result = format_currency(1000000)
        self.assertIsInstance(result, str)
        self.assertIn("1", result)  # Should contain the number
        
        # Test zero
        result = format_currency(0)
        self.assertIsInstance(result, str)
        
        # Test negative
        result = format_currency(-500)
        self.assertIsInstance(result, str)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        self.calculator = ValuationCalculator()
    
    def test_complete_valuation_workflow(self):
        """Test complete valuation workflow with multiple methods"""
        results = []
        
        # DCF Method
        dcf_result = self.calculator.dcf_valuation(
            [200000, 250000, 300000, 350000, 400000],
            0.20,
            0.15,
            0.03
        )
        self.assertNotIn('error', dcf_result)
        results.append(dcf_result['valuation'])
        
        # Market Multiples Method
        multiples_result = self.calculator.market_multiples_valuation(1500000, 4.0, "Revenue")
        self.assertNotIn('error', multiples_result)
        results.append(multiples_result['valuation'])
        
        # Berkus Method
        berkus_result = self.calculator.berkus_valuation({
            "concept": 4,
            "prototype": 3,
            "team": 4,
            "strategic_relationships": 2,
            "product_rollout": 1
        })
        self.assertNotIn('error', berkus_result)
        results.append(berkus_result['valuation'])
        
        # Verify all methods produced positive valuations
        for valuation in results:
            self.assertGreater(valuation, 0)
        
        # Calculate average valuation
        average_valuation = sum(results) / len(results)
        self.assertGreater(average_valuation, 0)
    
    def test_error_handling_integration(self):
        """Test error handling across different methods"""
        # Test DCF with invalid inputs
        dcf_result = self.calculator.dcf_valuation([], 0.20, 0.10, 0.15)
        # Should handle gracefully
        
        # Test multiples with negative values
        multiples_result = self.calculator.market_multiples_valuation(-1000000, 3.0)
        self.assertIn('error', multiples_result)


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