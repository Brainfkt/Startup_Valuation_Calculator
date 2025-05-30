"""
Export Manager Module - Simplified Version
Handles export functionality for multiple formats with reliable implementation
"""

import pandas as pd
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any, Optional
from io import BytesIO, StringIO
import csv

class ExportManager:
    """Manages export functionality for valuation data in multiple formats"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'excel', 'json', 'xml', 'txt']
    
    def export_calculation_data(
        self, 
        calculation_history: List[Dict[str, Any]], 
        format_type: str,
        include_charts: bool = False
    ) -> BytesIO:
        """Export calculation data in specified format"""
        if format_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format_type}")
        
        if format_type == 'csv':
            return self._export_csv(calculation_history, include_charts)
        elif format_type == 'excel':
            return self._export_excel(calculation_history, include_charts)
        elif format_type == 'json':
            return self._export_json(calculation_history, include_charts)
        elif format_type == 'xml':
            return self._export_xml(calculation_history, include_charts)
        elif format_type == 'txt':
            return self._export_txt(calculation_history, include_charts)
        else:
            return self._export_json(calculation_history, include_charts)
    
    def _export_csv(self, calculation_history: List[Dict], include_charts: bool) -> BytesIO:
        """Export data as CSV format"""
        buffer = BytesIO()
        
        # Prepare data for CSV export
        csv_data = []
        
        for calc in calculation_history:
            row = {
                'Timestamp': calc.get('timestamp', ''),
                'Method': calc.get('method', ''),
                'Valuation': calc.get('valuation', 0),
                'Success': calc.get('result', {}).get('success', False)
            }
            
            # Add method-specific data
            self._add_method_specific_csv_data(row, calc)
            csv_data.append(row)
        
        if csv_data:
            df = pd.DataFrame(csv_data)
            csv_string = df.to_csv(index=False)
            buffer.write(csv_string.encode('utf-8'))
        
        buffer.seek(0)
        return buffer
    
    def _export_excel(self, calculation_history: List[Dict], include_charts: bool) -> BytesIO:
        """Export data as Excel format"""
        # Convert to CSV data first
        csv_data = []
        for calc in calculation_history:
            row = {
                'Timestamp': calc.get('timestamp', ''),
                'Method': calc.get('method', ''),
                'Valuation': calc.get('valuation', 0),
                'Success': calc.get('result', {}).get('success', False)
            }
            self._add_method_specific_csv_data(row, calc)
            csv_data.append(row)
        
        # Create Excel file in memory
        buffer = BytesIO()
        if csv_data:
            df = pd.DataFrame(csv_data)
            # Use xlsxwriter engine for better compatibility
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Valuations', index=False)
        
        buffer.seek(0)
        return buffer
    
    def _export_json(self, calculation_history: List[Dict], include_charts: bool) -> BytesIO:
        """Export data as JSON format"""
        buffer = BytesIO()
        
        export_data = {
            'export_metadata': {
                'timestamp': datetime.now().isoformat(),
                'format': 'json',
                'version': '1.0',
                'total_calculations': len(calculation_history),
                'include_charts': include_charts
            },
            'calculations': []
        }
        
        for calc in calculation_history:
            calc_data = {
                'timestamp': calc.get('timestamp', ''),
                'method': calc.get('method', ''),
                'valuation': calc.get('valuation', 0),
                'inputs': calc.get('inputs', {}),
                'result': calc.get('result', {}),
                'success': calc.get('result', {}).get('success', False)
            }
            
            # Include chart data if requested and available
            if include_charts and 'chart_data' in calc:
                calc_data['chart_data'] = calc['chart_data']
            
            export_data['calculations'].append(calc_data)
        
        json_string = json.dumps(export_data, indent=2, default=str)
        buffer.write(json_string.encode('utf-8'))
        buffer.seek(0)
        return buffer
    
    def _export_xml(self, calculation_history: List[Dict], include_charts: bool) -> BytesIO:
        """Export data as XML format"""
        buffer = BytesIO()
        
        # Create root element
        root = ET.Element('ValuationExport')
        
        # Add metadata
        metadata = ET.SubElement(root, 'Metadata')
        ET.SubElement(metadata, 'Timestamp').text = datetime.now().isoformat()
        ET.SubElement(metadata, 'Format').text = 'xml'
        ET.SubElement(metadata, 'Version').text = '1.0'
        ET.SubElement(metadata, 'TotalCalculations').text = str(len(calculation_history))
        ET.SubElement(metadata, 'IncludeCharts').text = str(include_charts)
        
        # Add calculations
        calculations = ET.SubElement(root, 'Calculations')
        
        for calc in calculation_history:
            calc_elem = ET.SubElement(calculations, 'Calculation')
            
            ET.SubElement(calc_elem, 'Timestamp').text = calc.get('timestamp', '')
            ET.SubElement(calc_elem, 'Method').text = calc.get('method', '')
            ET.SubElement(calc_elem, 'Valuation').text = str(calc.get('valuation', 0))
            ET.SubElement(calc_elem, 'Success').text = str(calc.get('result', {}).get('success', False))
            
            # Add inputs
            inputs_elem = ET.SubElement(calc_elem, 'Inputs')
            self._dict_to_xml(calc.get('inputs', {}), inputs_elem)
            
            # Add result details
            result_elem = ET.SubElement(calc_elem, 'Result')
            self._dict_to_xml(calc.get('result', {}), result_elem)
        
        # Convert to string and write to buffer
        xml_string = ET.tostring(root, encoding='unicode')
        buffer.write(xml_string.encode('utf-8'))
        buffer.seek(0)
        return buffer
    
    def _export_txt(self, calculation_history: List[Dict], include_charts: bool) -> BytesIO:
        """Export data as plain text format"""
        buffer = BytesIO()
        
        lines = []
        lines.append("STARTUP VALUATION CALCULATOR - EXPORT REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Calculations: {len(calculation_history)}")
        lines.append("")
        
        for i, calc in enumerate(calculation_history, 1):
            lines.append(f"CALCULATION #{i}")
            lines.append("-" * 30)
            lines.append(f"Timestamp: {calc.get('timestamp', 'N/A')}")
            lines.append(f"Method: {calc.get('method', 'N/A')}")
            lines.append(f"Valuation: ${calc.get('valuation', 0):,.2f}")
            lines.append(f"Success: {calc.get('result', {}).get('success', False)}")
            
            # Add method-specific details
            self._add_method_specific_txt_data(lines, calc)
            lines.append("")
        
        # Add summary statistics
        lines.append("SUMMARY STATISTICS")
        lines.append("-" * 30)
        valuations = [calc.get('valuation', 0) for calc in calculation_history if calc.get('result', {}).get('success', False)]
        if valuations:
            lines.append(f"Average Valuation: ${sum(valuations) / len(valuations):,.2f}")
            lines.append(f"Median Valuation: ${sorted(valuations)[len(valuations)//2]:,.2f}")
            lines.append(f"Min Valuation: ${min(valuations):,.2f}")
            lines.append(f"Max Valuation: ${max(valuations):,.2f}")
        
        text_content = "\n".join(lines)
        buffer.write(text_content.encode('utf-8'))
        buffer.seek(0)
        return buffer
    
    def _add_method_specific_csv_data(self, row: Dict, calc: Dict):
        """Add method-specific data to CSV row"""
        method = calc.get('method', '')
        result = calc.get('result', {})
        inputs = calc.get('inputs', {})
        
        if method == 'DCF':
            row['Operating_Value'] = result.get('operating_value', 0)
            row['Terminal_Value'] = result.get('terminal_pv', 0)
            row['Discount_Rate'] = inputs.get('discount_rate', 0)
            row['Terminal_Growth'] = inputs.get('terminal_growth', 0)
        elif method == 'Market Multiples':
            row['Sector'] = inputs.get('sector', '')
            row['Metric_Type'] = inputs.get('metric_type', '')
            row['Metric_Value'] = inputs.get('metric_value', 0)
            row['Multiple'] = inputs.get('multiple', 0)
        elif method == 'Scorecard':
            row['Base_Valuation'] = inputs.get('base_valuation', 0)
            row['Adjustment_Factor'] = result.get('adjustment_factor', 1.0)
        elif method == 'Berkus':
            breakdown = result.get('breakdown', {})
            for criteria, details in breakdown.items():
                row[f'Berkus_{criteria}'] = details.get('value', 0)
        elif method == 'Risk Factor Summation':
            row['Base_Valuation'] = inputs.get('base_valuation', 0)
            row['Total_Adjustment'] = result.get('total_adjustment', 0)
        elif method == 'Venture Capital':
            row['Exit_Value'] = result.get('exit_value', 0)
            row['Present_Value'] = result.get('present_value', 0)
            row['Required_Return'] = inputs.get('required_return', 0)
            row['Years_to_Exit'] = inputs.get('years_to_exit', 0)
    
    def _dict_to_xml(self, data: Dict, parent: ET.Element):
        """Convert dictionary to XML elements"""
        for key, value in data.items():
            element = ET.SubElement(parent, str(key).replace(' ', '_'))
            if isinstance(value, dict):
                self._dict_to_xml(value, element)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    item_elem = ET.SubElement(element, f'Item_{i}')
                    if isinstance(item, dict):
                        self._dict_to_xml(item, item_elem)
                    else:
                        item_elem.text = str(item)
            else:
                element.text = str(value)
    
    def _add_method_specific_txt_data(self, lines: List[str], calc: Dict):
        """Add method-specific details to text export"""
        method = calc.get('method', '')
        result = calc.get('result', {})
        inputs = calc.get('inputs', {})
        
        lines.append("\nInputs:")
        for key, value in inputs.items():
            lines.append(f"  {key}: {value}")
        
        lines.append("\nResults:")
        for key, value in result.items():
            if key not in ['success', 'method']:
                if isinstance(value, (int, float)):
                    if 'value' in key.lower() or 'valuation' in key.lower():
                        lines.append(f"  {key}: ${value:,.2f}")
                    else:
                        lines.append(f"  {key}: {value}")
                else:
                    lines.append(f"  {key}: {value}")
    
    def export_single_calculation(
        self, 
        calculation: Dict[str, Any], 
        format_type: str,
        include_charts: bool = False
    ) -> BytesIO:
        """Export a single calculation in specified format"""
        return self.export_calculation_data([calculation], format_type, include_charts)
    
    def export_comparison_report(
        self, 
        calculations: List[Dict[str, Any]], 
        format_type: str = 'excel'
    ) -> BytesIO:
        """Export comparison report across multiple calculations"""
        return self.export_calculation_data(calculations, format_type, False)
    
    def get_export_metadata(self, calculation_history: List[Dict]) -> Dict[str, Any]:
        """Get metadata about exportable data"""
        methods = set(calc.get('method', '') for calc in calculation_history)
        successful_calcs = sum(1 for calc in calculation_history if calc.get('result', {}).get('success', False))
        
        return {
            'total_calculations': len(calculation_history),
            'successful_calculations': successful_calcs,
            'failed_calculations': len(calculation_history) - successful_calcs,
            'methods_used': list(methods),
            'date_range': {
                'earliest': min(calc.get('timestamp', '') for calc in calculation_history) if calculation_history else '',
                'latest': max(calc.get('timestamp', '') for calc in calculation_history) if calculation_history else ''
            },
            'supported_formats': self.supported_formats
        }