import unittest
import os
import sys
import importlib
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        # Suppress stdout and stderr to hide error messages from student code
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

def cleanup_test_files(files_list):
    """Clean up test files safely."""
    for file in files_list:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception:
            pass

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestHydroponicException(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_comprehensive_exception_handling(self):
        """Test comprehensive exception handling including None inputs, invalid data types, file errors, corrupted data, and resource limits"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return

            test_files = []
            
            # ============ SECTION 1: NONE INPUT HANDLING ============
            
            # Test functions with None file paths and parameters
            none_tests = [
                ("read_sensor_data", [None]),
                ("save_daily_readings", [[], None]),
                ("save_daily_readings", [None, "test.txt"]),
                ("log_system_event", ["event", "message", None]),
                ("log_system_event", [None, "message", "log.txt"]),
                ("log_system_event", ["event", None, "log.txt"]),
                ("update_recipe", ["recipe", "instructions", None]),
                ("update_recipe", [None, "instructions", "recipes.txt"]),
                ("update_recipe", ["recipe", None, "recipes.txt"]),
                ("read_nutrient_levels", [None]),
                ("append_nutrient_reading", [None, "nutrients.csv"]),
                ("append_nutrient_reading", [{"date": "2023-06-01"}, None]),
                ("generate_weekly_report", [None, "report.txt"]),
                ("generate_weekly_report", ["data.txt", None]),
                ("search_logs", [None, "log.txt"]),
                ("search_logs", ["term", None]),
                ("backup_data_files", [None, "backup.txt"]),
                ("backup_data_files", ["source.txt", None])
            ]
            
            for func_name, args in none_tests:
                if check_function_exists(self.module_obj, func_name):
                    result = safely_call_function(self.module_obj, func_name, *args)
                    # Functions should handle None gracefully
                    if result is not None:
                        if func_name in ["read_sensor_data", "read_nutrient_levels", "search_logs"]:
                            if not isinstance(result, list):
                                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                                print("TestComprehensiveExceptionHandling = Failed")
                                return
                        elif func_name in ["save_daily_readings", "log_system_event", "update_recipe", 
                                         "append_nutrient_reading", "generate_weekly_report", "backup_data_files"]:
                            if not isinstance(result, bool):
                                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                                print("TestComprehensiveExceptionHandling = Failed")
                                return
                else:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            
            # ============ SECTION 2: INVALID DATA TYPES ============
            
            # Test with invalid data types
            invalid_type_tests = [
                ("read_sensor_data", [123]),
                ("read_sensor_data", [[]]),
                ("read_sensor_data", [{"not": "string"}]),
                ("save_daily_readings", ["not_a_list", "file.txt"]),
                ("save_daily_readings", [123, "file.txt"]),
                ("save_daily_readings", [[], 123]),
                ("log_system_event", [123, "message", "log.txt"]),
                ("log_system_event", ["event", 123, "log.txt"]),
                ("log_system_event", ["event", "message", 123]),
                ("update_recipe", [123, "instructions", "recipes.txt"]),
                ("update_recipe", ["recipe", 123, "recipes.txt"]),
                ("update_recipe", ["recipe", "instructions", 123]),
                ("read_nutrient_levels", [123]),
                ("read_nutrient_levels", [[]]),
                ("append_nutrient_reading", ["not_dict", "nutrients.csv"]),
                ("append_nutrient_reading", [123, "nutrients.csv"]),
                ("append_nutrient_reading", [{"date": "2023-06-01"}, 123]),
                ("generate_weekly_report", [123, "report.txt"]),
                ("generate_weekly_report", ["data.txt", 123]),
                ("search_logs", [123, "log.txt"]),
                ("search_logs", ["term", 123]),
                ("backup_data_files", [123, "backup.txt"]),
                ("backup_data_files", ["source.txt", 123])
            ]
            
            for func_name, args in invalid_type_tests:
                if check_function_exists(self.module_obj, func_name):
                    result = safely_call_function(self.module_obj, func_name, *args)
                    # Functions should handle invalid types gracefully without crashing
                    if result is not None:
                        if func_name in ["read_sensor_data", "read_nutrient_levels", "search_logs"]:
                            if not isinstance(result, list):
                                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                                print("TestComprehensiveExceptionHandling = Failed")
                                return
                        elif func_name in ["save_daily_readings", "log_system_event", "update_recipe", 
                                         "append_nutrient_reading", "generate_weekly_report", "backup_data_files"]:
                            if not isinstance(result, bool):
                                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                                print("TestComprehensiveExceptionHandling = Failed")
                                return
                else:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            
            # ============ SECTION 3: FILE NOT FOUND HANDLING ============
            
            # Test with non-existent files
            nonexistent_file = "definitely_does_not_exist_12345.txt"
            
            # Ensure file doesn't exist
            if os.path.exists(nonexistent_file):
                try:
                    os.remove(nonexistent_file)
                except Exception:
                    pass
            
            # Test reading non-existent files
            file_tests = [
                ("read_sensor_data", [nonexistent_file]),
                ("read_nutrient_levels", [nonexistent_file]),
                ("search_logs", ["test", nonexistent_file])
            ]
            
            for func_name, args in file_tests:
                if check_function_exists(self.module_obj, func_name):
                    result = safely_call_function(self.module_obj, func_name, *args)
                    if result is None or not isinstance(result, list) or len(result) != 0:
                        self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                        print("TestComprehensiveExceptionHandling = Failed")
                        return
                else:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            
            # Test operations that should return False for non-existent files
            false_tests = [
                ("update_recipe", ["TestRecipe", "Instructions", nonexistent_file]),
                ("generate_weekly_report", [nonexistent_file, "test_report.txt"]),
                ("backup_data_files", [nonexistent_file, "backup.txt"])
            ]
            
            for func_name, args in false_tests:
                if check_function_exists(self.module_obj, func_name):
                    result = safely_call_function(self.module_obj, func_name, *args)
                    if result is None or result is not False:
                        self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                        print("TestComprehensiveExceptionHandling = Failed")
                        return
                else:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            
            # ============ SECTION 4: CORRUPTED FILE HANDLING ============
            
            # Create corrupted files
            corrupted_files = ["corrupted_binary.txt", "corrupted_data.csv", "mixed_valid_invalid.txt"]
            test_files.extend(corrupted_files)
            
            try:
                # Create binary file that's not readable as text
                with open("corrupted_binary.txt", "wb") as f:
                    f.write(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f')
                
                # Create file with invalid CSV structure
                with open("corrupted_data.csv", "w") as f:
                    f.write("This is not CSV data at all\n")
                    f.write("Random text here\n")
                    f.write("More random content\n")
                
                # Create file with mixed valid/invalid lines
                with open("mixed_valid_invalid.txt", "w") as f:
                    f.write("2023-06-01,25.0,65.0,6.2,22000\n")  # Valid line
                    f.write("This is not sensor data\n")           # Invalid line
                    f.write("2023-06-02,invalid,data,here\n")      # Partially invalid
                    f.write("2023-06-03,26.0,70.0,6.1,23000\n")   # Valid line
            except Exception:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # Test reading corrupted files
            for test_file in corrupted_files:
                if check_function_exists(self.module_obj, "read_sensor_data"):
                    result = safely_call_function(self.module_obj, "read_sensor_data", test_file)
                    if result is None or not isinstance(result, list):
                        self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                        print("TestComprehensiveExceptionHandling = Failed")
                        return
                
                if check_function_exists(self.module_obj, "read_nutrient_levels"):
                    result = safely_call_function(self.module_obj, "read_nutrient_levels", test_file)
                    if result is None or not isinstance(result, list):
                        self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                        print("TestComprehensiveExceptionHandling = Failed")
                        return
            
            # ============ SECTION 5: INCOMPLETE DATA STRUCTURES ============
            
            incomplete_files = ["incomplete_test.txt", "incomplete_nutrients.csv"]
            test_files.extend(incomplete_files)
            
            # Test with incomplete sensor readings
            incomplete_readings = [
                {"date": "2023-06-01"},  # Missing most fields
                {"temperature": 25.0, "humidity": 65.0},  # Missing date and other fields
                {"date": "2023-06-03", "temperature": "invalid", "humidity": 70.0},  # Invalid data type
                {}  # Empty dictionary
            ]
            
            if check_function_exists(self.module_obj, "save_daily_readings"):
                result = safely_call_function(self.module_obj, "save_daily_readings", incomplete_readings, "incomplete_test.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # Test with incomplete nutrient readings
            incomplete_nutrients = [
                {"date": "2023-06-01"},  # Missing nutrient fields
                {"nitrogen": 180},  # Missing date and other fields
                {"date": "2023-06-03", "nitrogen": "invalid"},  # Invalid data type
                {}  # Empty dictionary
            ]
            
            for nutrient in incomplete_nutrients:
                if check_function_exists(self.module_obj, "append_nutrient_reading"):
                    result = safely_call_function(self.module_obj, "append_nutrient_reading", nutrient, "incomplete_nutrients.csv")
                    if result is None or not isinstance(result, bool):
                        self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                        print("TestComprehensiveExceptionHandling = Failed")
                        return
                else:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            
            # ============ SECTION 6: RESOURCE EXHAUSTION SCENARIOS ============
            
            large_files = ["large_readings.txt", "large_report.txt"]
            test_files.extend(large_files)
            
            # Test with very large data sets (but not too large to crash the test)
            large_readings = []
            for i in range(100):  # Create 100 readings
                reading = {
                    "date": f"2023-06-{i+1:02d}",
                    "temperature": 25.0 + (i % 10),
                    "humidity": 65.0 + (i % 20),
                    "ph_level": 6.0 + (i % 2),
                    "light_level": 22000 + (i % 1000)
                }
                large_readings.append(reading)
            
            if check_function_exists(self.module_obj, "save_daily_readings"):
                result = safely_call_function(self.module_obj, "save_daily_readings", large_readings, "large_readings.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # Test reading the large file back
            if check_function_exists(self.module_obj, "read_sensor_data"):
                result = safely_call_function(self.module_obj, "read_sensor_data", "large_readings.txt")
                if result is None or not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            
            # Test generating report from large dataset
            if check_function_exists(self.module_obj, "generate_weekly_report"):
                result = safely_call_function(self.module_obj, "generate_weekly_report", "large_readings.txt", "large_report.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # ============ CLEANUP AND FINAL ASSERTION ============
            
            # Clean up all test files
            cleanup_test_files(test_files)
            cleanup_test_files(["test_report.txt", "backup.txt"])  # Additional cleanup
            
            # All tests passed
            self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", True, "exception")
            print("TestComprehensiveExceptionHandling = Passed")

        except Exception:
            # Emergency cleanup
            if 'test_files' in locals():
                cleanup_test_files(test_files)
            cleanup_test_files(["test_report.txt", "backup.txt"])
            self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
            print("TestComprehensiveExceptionHandling = Failed")

if __name__ == '__main__':
    unittest.main()