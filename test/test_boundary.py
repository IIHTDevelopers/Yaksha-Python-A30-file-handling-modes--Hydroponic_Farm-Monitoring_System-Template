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

class TestHydroponicBoundary(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_comprehensive_boundary_cases(self):
        """Test comprehensive boundary scenarios including empty files, malformed data, extreme values, and edge cases"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return

            test_files = []
            
            # ============ SECTION 1: EMPTY FILE HANDLING ============
            
            # Create empty test files
            empty_files = ["empty_sensor.txt", "empty_nutrients.csv", "empty_log.txt", "empty_recipes.txt"]
            test_files.extend(empty_files)
            
            for file in empty_files:
                try:
                    with open(file, "w") as f:
                        pass  # Create empty file
                except Exception:
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # Test reading empty sensor data file
            if check_function_exists(self.module_obj, "read_sensor_data"):
                result = safely_call_function(self.module_obj, "read_sensor_data", "empty_sensor.txt")
                if result is None or not isinstance(result, list) or len(result) != 0:
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # Test reading empty nutrient levels file
            if check_function_exists(self.module_obj, "read_nutrient_levels"):
                result = safely_call_function(self.module_obj, "read_nutrient_levels", "empty_nutrients.csv")
                if result is None or not isinstance(result, list) or len(result) != 0:
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # Test searching empty log file
            if check_function_exists(self.module_obj, "search_logs"):
                result = safely_call_function(self.module_obj, "search_logs", "test", "empty_log.txt")
                if result is None or not isinstance(result, list) or len(result) != 0:
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # Test updating recipe in empty file
            if check_function_exists(self.module_obj, "update_recipe"):
                result = safely_call_function(self.module_obj, "update_recipe", "TestRecipe", "Instructions", "empty_recipes.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # ============ SECTION 2: MALFORMED DATA HANDLING ============
            
            # Create files with malformed data
            malformed_files = ["malformed_sensor.txt", "malformed_nutrients.csv"]
            test_files.extend(malformed_files)
            
            try:
                # Malformed sensor data
                with open("malformed_sensor.txt", "w") as f:
                    f.write("incomplete,line\n")
                    f.write("2023-06-01,not_a_number,60.0,6.0\n")
                    f.write("2023-06-02\n")  # Missing data
                    f.write("2023-06-03,25.0,65.0,6.2,22000,extra_field\n")  # Extra field
                
                # Malformed CSV header
                with open("malformed_nutrients.csv", "w") as f:
                    f.write("wrong,header,format\n")
                    f.write("2023-06-01,180,45,210,1.8\n")
                    f.write("invalid,data,here,too,much\n")
            except Exception:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # Test reading malformed sensor data
            if check_function_exists(self.module_obj, "read_sensor_data"):
                result = safely_call_function(self.module_obj, "read_sensor_data", "malformed_sensor.txt")
                if result is None or not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # Test reading malformed nutrient data
            if check_function_exists(self.module_obj, "read_nutrient_levels"):
                result = safely_call_function(self.module_obj, "read_nutrient_levels", "malformed_nutrients.csv")
                if result is None or not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # ============ SECTION 3: EXTREME VALUES HANDLING ============
            
            extreme_files = ["extreme_sensor.txt", "extreme_nutrients.csv", "long_log.txt"]
            test_files.extend(extreme_files)
            
            # Test with extreme values in data
            extreme_readings = [
                {
                    "date": "2023-06-01",
                    "temperature": -50.0,  # Very low temperature
                    "humidity": 0.0,       # Minimum humidity
                    "ph_level": 0.0,       # Minimum pH
                    "light_level": 0        # No light
                },
                {
                    "date": "2023-06-02",
                    "temperature": 100.0,  # Very high temperature
                    "humidity": 100.0,     # Maximum humidity
                    "ph_level": 14.0,      # Maximum pH
                    "light_level": 100000  # Very high light
                }
            ]
            
            # Test saving extreme readings
            if check_function_exists(self.module_obj, "save_daily_readings"):
                result = safely_call_function(self.module_obj, "save_daily_readings", extreme_readings, "extreme_sensor.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # Test with extreme nutrient values
            extreme_nutrient = {
                "date": "2023-06-01",
                "nitrogen": 0,         # Minimum nitrogen
                "phosphorus": 1000,    # Very high phosphorus
                "potassium": 0,        # Minimum potassium
                "ec_level": 10.0       # Very high EC
            }
            
            if check_function_exists(self.module_obj, "append_nutrient_reading"):
                result = safely_call_function(self.module_obj, "append_nutrient_reading", extreme_nutrient, "extreme_nutrients.csv")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # Test with very long strings
            if check_function_exists(self.module_obj, "log_system_event"):
                very_long_message = "A" * 1000  # 1000 character message
                result = safely_call_function(self.module_obj, "log_system_event", "LongMessage", very_long_message, "long_log.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # ============ SECTION 4: BOUNDARY DATA RANGES ============
            
            boundary_files = ["boundary_sensor.txt", "boundary_nutrients.csv"]
            test_files.extend(boundary_files)
            
            # Test boundary pH values
            boundary_readings = [
                {
                    "date": "2023-06-01",
                    "temperature": 0.0,    # Freezing point
                    "humidity": 0.0,       # No humidity
                    "ph_level": 1.0,       # Very acidic
                    "light_level": 1       # Minimal light
                },
                {
                    "date": "2023-06-02",
                    "temperature": 50.0,   # High temperature
                    "humidity": 99.9,      # Near maximum humidity
                    "ph_level": 13.0,      # Very basic
                    "light_level": 50000   # High light
                }
            ]
            
            # Test saving boundary readings
            if check_function_exists(self.module_obj, "save_daily_readings"):
                result = safely_call_function(self.module_obj, "save_daily_readings", boundary_readings, "boundary_sensor.txt")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # Test with zero nutrient values
            zero_nutrient = {
                "date": "2023-06-01",
                "nitrogen": 0,
                "phosphorus": 0,
                "potassium": 0,
                "ec_level": 0.0
            }
            
            if check_function_exists(self.module_obj, "append_nutrient_reading"):
                result = safely_call_function(self.module_obj, "append_nutrient_reading", zero_nutrient, "boundary_nutrients.csv")
                if result is None or not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # ============ SECTION 5: EDGE CASE SEARCH SCENARIOS ============
            
            # Test with empty search term
            if check_function_exists(self.module_obj, "search_logs"):
                result = safely_call_function(self.module_obj, "search_logs", "", "system_log.txt")
                if result is None or not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # Test with single character search
            if check_function_exists(self.module_obj, "search_logs"):
                result = safely_call_function(self.module_obj, "search_logs", "a", "system_log.txt")
                if result is None or not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # ============ SECTION 6: FILE PERMISSION ISSUES ============
            
            # Test with directory instead of file (should fail gracefully)
            if not os.path.exists("test_directory"):
                try:
                    os.mkdir("test_directory")
                    test_files.append("test_directory")
                except Exception:
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # Test reading a directory as a file
            if check_function_exists(self.module_obj, "read_sensor_data"):
                result = safely_call_function(self.module_obj, "read_sensor_data", "test_directory")
                if result is not None and not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            
            # Test backup to a directory that doesn't exist
            if check_function_exists(self.module_obj, "backup_data_files"):
                result = safely_call_function(self.module_obj, "backup_data_files", "nonexistent_source.txt", "nonexistent_dir/backup.txt")
                if result is not None and not isinstance(result, bool):
                    self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                    print("TestComprehensiveBoundaryCases = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
                print("TestComprehensiveBoundaryCases = Failed")
                return
            
            # ============ CLEANUP AND FINAL ASSERTION ============
            
            # Clean up all test files
            cleanup_test_files(test_files)
            
            # Clean up test directory
            try:
                if os.path.exists("test_directory"):
                    os.rmdir("test_directory")
            except Exception:
                pass
            
            # All tests passed
            self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", True, "boundary")
            print("TestComprehensiveBoundaryCases = Passed")

        except Exception:
            # Emergency cleanup
            if 'test_files' in locals():
                cleanup_test_files(test_files)
            try:
                if os.path.exists("test_directory"):
                    os.rmdir("test_directory")
            except Exception:
                pass
            self.test_obj.yakshaAssert("TestComprehensiveBoundaryCases", False, "boundary")
            print("TestComprehensiveBoundaryCases = Failed")

if __name__ == '__main__':
    unittest.main()