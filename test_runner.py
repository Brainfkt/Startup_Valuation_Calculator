"""
Test Runner Module
Provides interface for running automated tests within the Streamlit application
"""

import unittest
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, List, Tuple, Any
from datetime import datetime
import traceback

from test_valuation_methods import (
    TestDCFMethod, TestMarketMultiplesMethod, TestScorecardMethod,
    TestBerkusMethod, TestRiskFactorMethod, TestVCMethod,
    TestValidationSchemas, TestUtilityFunctions, TestIntegration
)


class TestRunner:
    """Manages test execution and reporting for the valuation calculator"""
    
    def __init__(self):
        self.test_classes = {
            "DCF Method": TestDCFMethod,
            "Market Multiples": TestMarketMultiplesMethod,
            "Scorecard Method": TestScorecardMethod,
            "Berkus Method": TestBerkusMethod,
            "Risk Factor Method": TestRiskFactorMethod,
            "Venture Capital Method": TestVCMethod,
            "Input Validation": TestValidationSchemas,
            "Utility Functions": TestUtilityFunctions,
            "Integration Tests": TestIntegration
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and return comprehensive results"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'total_failures': 0,
            'total_errors': 0,
            'success_rate': 0,
            'test_results': {},
            'summary': {},
            'execution_time': 0
        }
        
        start_time = datetime.now()
        
        for test_name, test_class in self.test_classes.items():
            test_result = self._run_single_test_class(test_class, test_name)
            results['test_results'][test_name] = test_result
            
            results['total_tests'] += test_result['tests_run']
            results['total_failures'] += test_result['failures']
            results['total_errors'] += test_result['errors']
        
        end_time = datetime.now()
        results['execution_time'] = (end_time - start_time).total_seconds()
        
        if results['total_tests'] > 0:
            success_count = results['total_tests'] - results['total_failures'] - results['total_errors']
            results['success_rate'] = (success_count / results['total_tests']) * 100
        
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def run_specific_tests(self, test_categories: List[str]) -> Dict[str, Any]:
        """Run specific test categories"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'total_failures': 0,
            'total_errors': 0,
            'success_rate': 0,
            'test_results': {},
            'summary': {},
            'execution_time': 0
        }
        
        start_time = datetime.now()
        
        for test_name in test_categories:
            if test_name in self.test_classes:
                test_class = self.test_classes[test_name]
                test_result = self._run_single_test_class(test_class, test_name)
                results['test_results'][test_name] = test_result
                
                results['total_tests'] += test_result['tests_run']
                results['total_failures'] += test_result['failures']
                results['total_errors'] += test_result['errors']
        
        end_time = datetime.now()
        results['execution_time'] = (end_time - start_time).total_seconds()
        
        if results['total_tests'] > 0:
            success_count = results['total_tests'] - results['total_failures'] - results['total_errors']
            results['success_rate'] = (success_count / results['total_tests']) * 100
        
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _run_single_test_class(self, test_class, test_name: str) -> Dict[str, Any]:
        """Run a single test class and capture results"""
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        test_result = {
            'name': test_name,
            'tests_run': 0,
            'failures': 0,
            'errors': 0,
            'success_rate': 0,
            'individual_tests': [],
            'output': '',
            'error_output': '',
            'status': 'unknown'
        }
        
        try:
            # Create test suite for this class
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            
            # Run tests with captured output
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                runner = unittest.TextTestRunner(
                    stream=stdout_capture, 
                    verbosity=2, 
                    buffer=True
                )
                result = runner.run(suite)
            
            # Extract results
            test_result['tests_run'] = result.testsRun
            test_result['failures'] = len(result.failures)
            test_result['errors'] = len(result.errors)
            test_result['output'] = stdout_capture.getvalue()
            test_result['error_output'] = stderr_capture.getvalue()
            
            if test_result['tests_run'] > 0:
                success_count = test_result['tests_run'] - test_result['failures'] - test_result['errors']
                test_result['success_rate'] = (success_count / test_result['tests_run']) * 100
            
            # Process individual test results
            test_result['individual_tests'] = self._process_individual_results(result)
            
            # Determine overall status
            if result.wasSuccessful():
                test_result['status'] = 'passed'
            elif test_result['errors'] > 0:
                test_result['status'] = 'error'
            else:
                test_result['status'] = 'failed'
                
        except Exception as e:
            test_result['status'] = 'error'
            test_result['error_output'] = f"Test execution failed: {str(e)}\n{traceback.format_exc()}"
        
        return test_result
    
    def _process_individual_results(self, unittest_result) -> List[Dict[str, Any]]:
        """Process individual test results from unittest output"""
        individual_tests = []
        
        # Add successful tests
        for test in unittest_result._testMethodName if hasattr(unittest_result, '_testMethodName') else []:
            individual_tests.append({
                'name': str(test),
                'status': 'passed',
                'message': ''
            })
        
        # Add failed tests
        for test, traceback_str in unittest_result.failures:
            individual_tests.append({
                'name': str(test),
                'status': 'failed',
                'message': traceback_str.split('\n')[-2] if traceback_str else 'Test failed'
            })
        
        # Add error tests
        for test, traceback_str in unittest_result.errors:
            individual_tests.append({
                'name': str(test),
                'status': 'error',
                'message': traceback_str.split('\n')[-2] if traceback_str else 'Test error'
            })
        
        return individual_tests
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics and insights"""
        summary = {
            'overall_status': 'unknown',
            'critical_issues': [],
            'recommendations': [],
            'method_performance': {},
            'coverage_analysis': {}
        }
        
        # Determine overall status
        if results['success_rate'] >= 95:
            summary['overall_status'] = 'excellent'
        elif results['success_rate'] >= 85:
            summary['overall_status'] = 'good'
        elif results['success_rate'] >= 70:
            summary['overall_status'] = 'acceptable'
        else:
            summary['overall_status'] = 'needs_attention'
        
        # Identify critical issues
        for test_name, test_result in results['test_results'].items():
            if test_result['status'] == 'error':
                summary['critical_issues'].append(f"{test_name}: Critical error detected")
            elif test_result['failures'] > test_result['tests_run'] * 0.3:  # >30% failure rate
                summary['critical_issues'].append(f"{test_name}: High failure rate ({test_result['failures']}/{test_result['tests_run']})")
        
        # Generate recommendations
        if results['total_errors'] > 0:
            summary['recommendations'].append("Review and fix critical errors before deployment")
        
        if results['success_rate'] < 90:
            summary['recommendations'].append("Improve test coverage and fix failing tests")
        
        if not summary['critical_issues']:
            summary['recommendations'].append("All tests passing - system ready for production")
        
        # Method performance analysis
        for test_name, test_result in results['test_results'].items():
            if 'Method' in test_name:
                summary['method_performance'][test_name] = {
                    'status': test_result['status'],
                    'success_rate': test_result['success_rate'],
                    'reliability': 'high' if test_result['success_rate'] >= 90 else 'medium' if test_result['success_rate'] >= 70 else 'low'
                }
        
        # Coverage analysis
        total_methods = len([name for name in results['test_results'].keys() if 'Method' in name])
        passing_methods = len([result for name, result in results['test_results'].items() 
                             if 'Method' in name and result['status'] == 'passed'])
        
        summary['coverage_analysis'] = {
            'total_methods_tested': total_methods,
            'methods_passing': passing_methods,
            'method_coverage': (passing_methods / total_methods * 100) if total_methods > 0 else 0,
            'validation_tested': 'Input Validation' in results['test_results'],
            'integration_tested': 'Integration Tests' in results['test_results']
        }
        
        return summary
    
    def get_test_categories(self) -> List[str]:
        """Get list of available test categories"""
        return list(self.test_classes.keys())
    
    def run_quick_validation(self) -> Dict[str, Any]:
        """Run a quick validation test for core functionality"""
        quick_tests = ["DCF Method", "Market Multiples", "Input Validation"]
        return self.run_specific_tests(quick_tests)
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive validation including all methods"""
        return self.run_all_tests()
    
    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """Generate a formatted text report of test results"""
        report_lines = []
        
        report_lines.append("STARTUP VALUATION CALCULATOR - TEST REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {results['timestamp']}")
        report_lines.append(f"Execution Time: {results['execution_time']:.2f} seconds")
        report_lines.append("")
        
        # Overall Summary
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 30)
        report_lines.append(f"Total Tests: {results['total_tests']}")
        report_lines.append(f"Passed: {results['total_tests'] - results['total_failures'] - results['total_errors']}")
        report_lines.append(f"Failed: {results['total_failures']}")
        report_lines.append(f"Errors: {results['total_errors']}")
        report_lines.append(f"Success Rate: {results['success_rate']:.1f}%")
        report_lines.append(f"Overall Status: {results['summary']['overall_status'].upper()}")
        report_lines.append("")
        
        # Method Performance
        if results['summary']['method_performance']:
            report_lines.append("VALUATION METHOD PERFORMANCE")
            report_lines.append("-" * 30)
            for method, performance in results['summary']['method_performance'].items():
                report_lines.append(f"{method}: {performance['status'].upper()} ({performance['success_rate']:.1f}%)")
            report_lines.append("")
        
        # Critical Issues
        if results['summary']['critical_issues']:
            report_lines.append("CRITICAL ISSUES")
            report_lines.append("-" * 30)
            for issue in results['summary']['critical_issues']:
                report_lines.append(f"• {issue}")
            report_lines.append("")
        
        # Recommendations
        if results['summary']['recommendations']:
            report_lines.append("RECOMMENDATIONS")
            report_lines.append("-" * 30)
            for rec in results['summary']['recommendations']:
                report_lines.append(f"• {rec}")
            report_lines.append("")
        
        # Detailed Results
        report_lines.append("DETAILED TEST RESULTS")
        report_lines.append("-" * 30)
        for test_name, test_result in results['test_results'].items():
            report_lines.append(f"\n{test_name}:")
            report_lines.append(f"  Status: {test_result['status'].upper()}")
            report_lines.append(f"  Tests Run: {test_result['tests_run']}")
            if test_result['failures'] > 0:
                report_lines.append(f"  Failures: {test_result['failures']}")
            if test_result['errors'] > 0:
                report_lines.append(f"  Errors: {test_result['errors']}")
            report_lines.append(f"  Success Rate: {test_result['success_rate']:.1f}%")
        
        return "\n".join(report_lines)