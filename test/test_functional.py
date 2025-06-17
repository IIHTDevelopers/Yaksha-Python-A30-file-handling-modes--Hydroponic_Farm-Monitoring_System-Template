import unittest
import os
import sys
import importlib
import inspect
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

class TestHydroponicFunctional(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_function_existence_and_signatures(self):
        """Test that all required functions exist with correct signatures"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
                print("TestFunctionExistenceAndSignatures = Failed")
                return

            # Required functions with their expected parameter counts (minimum)
            required_functions = {
                "read_sensor_data": 0,  # file_path has default
                "save_daily_readings": 1,  # data required, file_path has default
                "log_system_event": 2,  # event_type and message required, file_path has default
                "update_recipe": 2,  # recipe_name and new_instructions required, file_path has default
                "read_nutrient_levels": 0,  # file_path has default
                "append_nutrient_reading": 1,  # reading required, file_path has default
                "generate_weekly_report": 1,  # data_file_path required, output_file_path has default
                "search_logs": 1,  # search_term required, file_path has default
                "backup_data_files": 2,  # source_path and backup_path required
                "create_sample_data": 0,  # no required parameters
                "main": 0  # no required parameters
            }
            
            # Check each required function exists
            for func_name, min_params in required_functions.items():
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
                    print("TestFunctionExistenceAndSignatures = Failed")
                    return
                else:
                    # Check function signature
                    try:
                        func = getattr(self.module_obj, func_name)
                        sig = inspect.signature(func)
                        params = list(sig.parameters.values())
                        
                        # Count required parameters (those without defaults)
                        required_params = sum(1 for p in params if p.default == inspect.Parameter.empty)
                        
                        if required_params > min_params:
                            self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
                            print("TestFunctionExistenceAndSignatures = Failed")
                            return
                    except Exception:
                        self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
                        print("TestFunctionExistenceAndSignatures = Failed")
                        return
            
            # Check for docstrings
            for func_name in required_functions.keys():
                if check_function_exists(self.module_obj, func_name):
                    try:
                        func = getattr(self.module_obj, func_name)
                        if not func.__doc__ or len(func.__doc__.strip()) < 10:
                            self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
                            print("TestFunctionExistenceAndSignatures = Failed")
                            return
                    except Exception:
                        self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
                        print("TestFunctionExistenceAndSignatures = Failed")
                        return
            
            # All tests passed
            self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", True, "functional")
            print("TestFunctionExistenceAndSignatures = Passed")

        except Exception:
            self.test_obj.yakshaAssert("TestFunctionExistenceAndSignatures", False, "functional")
            print("TestFunctionExistenceAndSignatures = Failed")

    def test_file_operations_functionality(self):
        """Test basic file operations work correctly"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                print("TestFileOperationsFunctionality = Failed")
                return

            # Test basic file creation and reading cycle
            test_readings = [
                {
                    "date": "2023-06-01",
                    "temperature": 24.5,
                    "humidity": 65.2,
                    "ph_level": 6.2,
                    "light_level": 22000
                },
                {
                    "date": "2023-06-02",
                    "temperature": 25.1,
                    "humidity": 63.7,
                    "ph_level": 6.3,
                    "light_level": 21800
                }
            ]
            
            # Test saving readings
            if check_function_exists(self.module_obj, "save_daily_readings"):
                result = safely_call_function(self.module_obj, "save_daily_readings", test_readings, "test_sensor_data.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                    print("TestFileOperationsFunctionality = Failed")
                    return
                else:
                    # Verify file was created
                    if not os.path.exists("test_sensor_data.txt"):
                        self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                        print("TestFileOperationsFunctionality = Failed")
                        return
            else:
                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                print("TestFileOperationsFunctionality = Failed")
                return
            
            # Test reading the saved data back
            if check_function_exists(self.module_obj, "read_sensor_data"):
                result = safely_call_function(self.module_obj, "read_sensor_data", "test_sensor_data.txt")
                if result is None or not isinstance(result, list) or len(result) != 2:
                    self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                    print("TestFileOperationsFunctionality = Failed")
                    return
                else:
                    # Verify data integrity
                    for i, reading in enumerate(result):
                        if not isinstance(reading, dict):
                            self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                            print("TestFileOperationsFunctionality = Failed")
                            return
                        
                        expected = test_readings[i]
                        for key in ["date", "temperature", "humidity", "ph_level", "light_level"]:
                            if key not in reading:
                                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                                print("TestFileOperationsFunctionality = Failed")
                                return
                            elif key == "date":
                                # String comparison for date
                                if str(reading[key]) != str(expected[key]):
                                    self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                                    print("TestFileOperationsFunctionality = Failed")
                                    return
                            else:
                                # Numeric comparison for other fields
                                try:
                                    if abs(float(reading[key]) - float(expected[key])) > 0.001:
                                        self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                                        print("TestFileOperationsFunctionality = Failed")
                                        return
                                except (ValueError, TypeError):
                                    if str(reading[key]) != str(expected[key]):
                                        self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                                        print("TestFileOperationsFunctionality = Failed")
                                        return
            else:
                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                print("TestFileOperationsFunctionality = Failed")
                return
            
            # Test logging functionality
            if check_function_exists(self.module_obj, "log_system_event"):
                result = safely_call_function(self.module_obj, "log_system_event", "Test", "Test log message", "test_log.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                    print("TestFileOperationsFunctionality = Failed")
                    return
                else:
                    # Verify log file was created
                    if not os.path.exists("test_log.txt"):
                        self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                        print("TestFileOperationsFunctionality = Failed")
                        return
                    else:
                        # Verify log content
                        try:
                            with open("test_log.txt", "r") as f:
                                content = f.read()
                                if "Test" not in content or "Test log message" not in content:
                                    self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                                    print("TestFileOperationsFunctionality = Failed")
                                    return
                        except Exception:
                            self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                            print("TestFileOperationsFunctionality = Failed")
                            return
            else:
                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                print("TestFileOperationsFunctionality = Failed")
                return
            
            # Test search functionality
            if check_function_exists(self.module_obj, "search_logs"):
                result = safely_call_function(self.module_obj, "search_logs", "Test", "test_log.txt")
                if result is None or not isinstance(result, list) or len(result) == 0:
                    self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                    print("TestFileOperationsFunctionality = Failed")
                    return
                else:
                    # Verify search result structure
                    first_result = result[0]
                    if not isinstance(first_result, dict):
                        self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                        print("TestFileOperationsFunctionality = Failed")
                        return
                    else:
                        required_fields = ["timestamp", "event_type", "message"]
                        for field in required_fields:
                            if field not in first_result:
                                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                                print("TestFileOperationsFunctionality = Failed")
                                return
            else:
                self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
                print("TestFileOperationsFunctionality = Failed")
                return
            
            # Clean up test files
            cleanup_test_files(["test_sensor_data.txt", "test_log.txt"])
            
            # All tests passed
            self.test_obj.yakshaAssert("TestFileOperationsFunctionality", True, "functional")
            print("TestFileOperationsFunctionality = Passed")

        except Exception:
            cleanup_test_files(["test_sensor_data.txt", "test_log.txt"])
            self.test_obj.yakshaAssert("TestFileOperationsFunctionality", False, "functional")
            print("TestFileOperationsFunctionality = Failed")

    def test_csv_operations_functionality(self):
        """Test CSV file operations work correctly"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                print("TestCsvOperationsFunctionality = Failed")
                return

            # Test CSV nutrient operations
            test_nutrient = {
                "date": "2023-06-01",
                "nitrogen": 180,
                "phosphorus": 45,
                "potassium": 210,
                "ec_level": 1.8
            }
            
            # Test appending nutrient reading (should create file with header)
            if check_function_exists(self.module_obj, "append_nutrient_reading"):
                result = safely_call_function(self.module_obj, "append_nutrient_reading", test_nutrient, "test_nutrients.csv")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                    print("TestCsvOperationsFunctionality = Failed")
                    return
                else:
                    # Verify file was created
                    if not os.path.exists("test_nutrients.csv"):
                        self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                        print("TestCsvOperationsFunctionality = Failed")
                        return
                    else:
                        # Verify CSV structure
                        try:
                            with open("test_nutrients.csv", "r") as f:
                                lines = f.readlines()
                                if len(lines) < 2:
                                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                    print("TestCsvOperationsFunctionality = Failed")
                                    return
                                elif "date,nitrogen,phosphorus,potassium,ec_level" not in lines[0]:
                                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                    print("TestCsvOperationsFunctionality = Failed")
                                    return
                                elif "2023-06-01,180,45,210,1.8" not in lines[1]:
                                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                    print("TestCsvOperationsFunctionality = Failed")
                                    return
                        except Exception:
                            self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                            print("TestCsvOperationsFunctionality = Failed")
                            return
            else:
                self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                print("TestCsvOperationsFunctionality = Failed")
                return
            
            # Test reading nutrient levels
            if check_function_exists(self.module_obj, "read_nutrient_levels"):
                result = safely_call_function(self.module_obj, "read_nutrient_levels", "test_nutrients.csv")
                if result is None or not isinstance(result, list) or len(result) != 1:
                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                    print("TestCsvOperationsFunctionality = Failed")
                    return
                else:
                    # Verify data integrity
                    reading = result[0]
                    if not isinstance(reading, dict):
                        self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                        print("TestCsvOperationsFunctionality = Failed")
                        return
                    else:
                        for key in ["date", "nitrogen", "phosphorus", "potassium", "ec_level"]:
                            if key not in reading:
                                self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                print("TestCsvOperationsFunctionality = Failed")
                                return
                            elif key == "date":
                                # String comparison for date
                                if str(reading[key]) != str(test_nutrient[key]):
                                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                    print("TestCsvOperationsFunctionality = Failed")
                                    return
                            else:
                                # Numeric comparison for other fields
                                try:
                                    if abs(float(reading[key]) - float(test_nutrient[key])) > 0.001:
                                        self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                        print("TestCsvOperationsFunctionality = Failed")
                                        return
                                except (ValueError, TypeError):
                                    if str(reading[key]) != str(test_nutrient[key]):
                                        self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                                        print("TestCsvOperationsFunctionality = Failed")
                                        return
            else:
                self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                print("TestCsvOperationsFunctionality = Failed")
                return
            
            # Test appending another reading
            if check_function_exists(self.module_obj, "append_nutrient_reading"):
                test_nutrient2 = {
                    "date": "2023-06-02",
                    "nitrogen": 175,
                    "phosphorus": 42,
                    "potassium": 205,
                    "ec_level": 1.7
                }
                
                result = safely_call_function(self.module_obj, "append_nutrient_reading", test_nutrient2, "test_nutrients.csv")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                    print("TestCsvOperationsFunctionality = Failed")
                    return
                else:
                    # Verify both readings are now present
                    if check_function_exists(self.module_obj, "read_nutrient_levels"):
                        result = safely_call_function(self.module_obj, "read_nutrient_levels", "test_nutrients.csv")
                        if result is None or len(result) != 2:
                            self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
                            print("TestCsvOperationsFunctionality = Failed")
                            return
            
            # Clean up test files
            cleanup_test_files(["test_nutrients.csv"])
            
            # All tests passed
            self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", True, "functional")
            print("TestCsvOperationsFunctionality = Passed")

        except Exception:
            cleanup_test_files(["test_nutrients.csv"])
            self.test_obj.yakshaAssert("TestCsvOperationsFunctionality", False, "functional")
            print("TestCsvOperationsFunctionality = Failed")

    def test_recipe_update_functionality(self):
        """Test recipe update functionality using r+ mode"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                print("TestRecipeUpdateFunctionality = Failed")
                return

            # Create initial recipes file
            initial_recipes = """Recipe: Leafy Greens
Nitrogen: 180 ppm
Phosphorus: 50 ppm
Potassium: 210 ppm
EC Range: 1.6-2.0
pH Range: 5.8-6.2

Recipe: Tomatoes
Nitrogen: 160 ppm
Phosphorus: 60 ppm
Potassium: 190 ppm
EC Range: 2.0-3.5
pH Range: 5.5-6.5"""
            
            try:
                with open("test_recipes.txt", "w") as f:
                    f.write(initial_recipes)
            except Exception:
                self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                print("TestRecipeUpdateFunctionality = Failed")
                return
            
            # Test updating an existing recipe
            if check_function_exists(self.module_obj, "update_recipe"):
                new_instructions = """Nitrogen: 185 ppm
Phosphorus: 55 ppm
Potassium: 215 ppm
EC Range: 1.7-2.1
pH Range: 5.9-6.3"""
                
                result = safely_call_function(self.module_obj, "update_recipe", "Leafy Greens", new_instructions, "test_recipes.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                    print("TestRecipeUpdateFunctionality = Failed")
                    return
                else:
                    # Verify the recipe was updated
                    try:
                        with open("test_recipes.txt", "r") as f:
                            content = f.read()
                            if ("Nitrogen: 185 ppm" not in content or 
                                "Phosphorus: 55 ppm" not in content or 
                                "Recipe: Tomatoes" not in content or 
                                "Nitrogen: 160 ppm" not in content):
                                self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                                print("TestRecipeUpdateFunctionality = Failed")
                                return
                    except Exception:
                        self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                        print("TestRecipeUpdateFunctionality = Failed")
                        return
            else:
                self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                print("TestRecipeUpdateFunctionality = Failed")
                return
            
            # Test updating non-existent recipe
            if check_function_exists(self.module_obj, "update_recipe"):
                result = safely_call_function(self.module_obj, "update_recipe", "NonExistent Recipe", "Some instructions", "test_recipes.txt")
                if result is None or result is not False:
                    self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
                    print("TestRecipeUpdateFunctionality = Failed")
                    return
            
            # Clean up test files
            cleanup_test_files(["test_recipes.txt"])
            
            # All tests passed
            self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", True, "functional")
            print("TestRecipeUpdateFunctionality = Passed")

        except Exception:
            cleanup_test_files(["test_recipes.txt"])
            self.test_obj.yakshaAssert("TestRecipeUpdateFunctionality", False, "functional")
            print("TestRecipeUpdateFunctionality = Failed")

    def test_report_generation_functionality(self):
        """Test report generation with calculations"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                print("TestReportGenerationFunctionality = Failed")
                return

            # Create test sensor data with known values for calculation verification
            test_data = [
                {
                    "date": "2023-06-01",
                    "temperature": 24.0,
                    "humidity": 60.0,
                    "ph_level": 6.0,
                    "light_level": 20000
                },
                {
                    "date": "2023-06-02",
                    "temperature": 26.0,
                    "humidity": 70.0,
                    "ph_level": 6.2,
                    "light_level": 22000
                },
                {
                    "date": "2023-06-03",
                    "temperature": 25.0,
                    "humidity": 65.0,
                    "ph_level": 6.1,
                    "light_level": 21000
                }
            ]
            
            # Calculate expected averages
            expected_avg_temp = (24.0 + 26.0 + 25.0) / 3  # 25.0
            expected_avg_humidity = (60.0 + 70.0 + 65.0) / 3  # 65.0
            expected_avg_ph = (6.0 + 6.2 + 6.1) / 3  # 6.1
            expected_avg_light = (20000 + 22000 + 21000) / 3  # 21000.0
            
            # Save test data
            if check_function_exists(self.module_obj, "save_daily_readings"):
                result = safely_call_function(self.module_obj, "save_daily_readings", test_data, "test_report_data.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                    print("TestReportGenerationFunctionality = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                print("TestReportGenerationFunctionality = Failed")
                return
            
            # Generate report
            if check_function_exists(self.module_obj, "generate_weekly_report"):
                result = safely_call_function(self.module_obj, "generate_weekly_report", "test_report_data.txt", "test_report.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                    print("TestReportGenerationFunctionality = Failed")
                    return
                else:
                    # Verify report was created and contains correct information
                    if not os.path.exists("test_report.txt"):
                        self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                        print("TestReportGenerationFunctionality = Failed")
                        return
                    else:
                        try:
                            with open("test_report.txt", "r") as f:
                                content = f.read()
                                
                                # Check for required sections
                                if ("WEEKLY HYDROPONIC MONITORING REPORT" not in content or
                                    "AVERAGES:" not in content or
                                    "DAILY READINGS:" not in content):
                                    self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                                    print("TestReportGenerationFunctionality = Failed")
                                    return
                                
                                # Check calculations (allow small rounding differences)
                                import re
                                temp_match = re.search(r"Temperature:\s*([\d.]+)", content)
                                humidity_match = re.search(r"Humidity:\s*([\d.]+)", content)
                                ph_match = re.search(r"pH Level:\s*([\d.]+)", content)
                                light_match = re.search(r"Light Level:\s*([\d.]+)", content)
                                
                                if temp_match:
                                    reported_temp = float(temp_match.group(1))
                                    if abs(reported_temp - expected_avg_temp) > 0.1:
                                        self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                                        print("TestReportGenerationFunctionality = Failed")
                                        return
                                
                                if humidity_match:
                                    reported_humidity = float(humidity_match.group(1))
                                    if abs(reported_humidity - expected_avg_humidity) > 0.1:
                                        self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                                        print("TestReportGenerationFunctionality = Failed")
                                        return
                                
                                if ph_match:
                                    reported_ph = float(ph_match.group(1))
                                    if abs(reported_ph - expected_avg_ph) > 0.1:
                                        self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                                        print("TestReportGenerationFunctionality = Failed")
                                        return
                                
                                if light_match:
                                    reported_light = float(light_match.group(1))
                                    if abs(reported_light - expected_avg_light) > 1:
                                        self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                                        print("TestReportGenerationFunctionality = Failed")
                                        return
                                
                                # Check that all daily readings are included
                                for reading in test_data:
                                    if reading["date"] not in content:
                                        self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                                        print("TestReportGenerationFunctionality = Failed")
                                        return
                        except Exception:
                            self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                            print("TestReportGenerationFunctionality = Failed")
                            return
            else:
                self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
                print("TestReportGenerationFunctionality = Failed")
                return
            
            # Clean up test files
            cleanup_test_files(["test_report_data.txt", "test_report.txt"])
            
            # All tests passed
            self.test_obj.yakshaAssert("TestReportGenerationFunctionality", True, "functional")
            print("TestReportGenerationFunctionality = Passed")

        except Exception:
            cleanup_test_files(["test_report_data.txt", "test_report.txt"])
            self.test_obj.yakshaAssert("TestReportGenerationFunctionality", False, "functional")
            print("TestReportGenerationFunctionality = Failed")

    def test_backup_functionality(self):
        """Test backup file functionality"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                print("TestBackupFunctionality = Failed")
                return

            # Create a test source file
            test_content = """2023-06-01,24.5,65.2,6.2,22000
2023-06-02,25.1,63.7,6.3,21800
2023-06-03,24.8,67.5,6.1,22500"""
            
            try:
                with open("test_source.txt", "w") as f:
                    f.write(test_content)
            except Exception:
                self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                print("TestBackupFunctionality = Failed")
                return
            
            # Test backup functionality
            if check_function_exists(self.module_obj, "backup_data_files"):
                result = safely_call_function(self.module_obj, "backup_data_files", "test_source.txt", "test_backup.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                    print("TestBackupFunctionality = Failed")
                    return
                else:
                    # Verify backup file was created
                    if not os.path.exists("test_backup.txt"):
                        self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                        print("TestBackupFunctionality = Failed")
                        return
                    else:
                        # Verify backup content matches source
                        try:
                            with open("test_backup.txt", "r") as f:
                                backup_content = f.read()
                                if backup_content != test_content:
                                    self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                                    print("TestBackupFunctionality = Failed")
                                    return
                        except Exception:
                            self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                            print("TestBackupFunctionality = Failed")
                            return
            else:
                self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                print("TestBackupFunctionality = Failed")
                return
            
            # Test backup of non-existent file
            if check_function_exists(self.module_obj, "backup_data_files"):
                result = safely_call_function(self.module_obj, "backup_data_files", "nonexistent.txt", "backup_nonexistent.txt")
                if result is None or result is not False:
                    self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
                    print("TestBackupFunctionality = Failed")
                    return
            
            # Clean up test files
            cleanup_test_files(["test_source.txt", "test_backup.txt", "backup_nonexistent.txt"])
            
            # All tests passed
            self.test_obj.yakshaAssert("TestBackupFunctionality", True, "functional")
            print("TestBackupFunctionality = Passed")

        except Exception:
            cleanup_test_files(["test_source.txt", "test_backup.txt", "backup_nonexistent.txt"])
            self.test_obj.yakshaAssert("TestBackupFunctionality", False, "functional")
            print("TestBackupFunctionality = Failed")

    def test_sample_data_creation(self):
        """Test sample data creation functionality"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                print("TestSampleDataCreation = Failed")
                return

            # Clean up any existing sample files first
            sample_files = ["sensor_readings.txt", "nutrient_levels.csv", "recipes.txt", "system_log.txt"]
            cleanup_test_files(sample_files)
            
            # Test sample data creation
            if check_function_exists(self.module_obj, "create_sample_data"):
                result = safely_call_function(self.module_obj, "create_sample_data")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                    print("TestSampleDataCreation = Failed")
                    return
                else:
                    # Verify expected files were created
                    expected_files = ["sensor_readings.txt", "nutrient_levels.csv", "recipes.txt"]
                    for file in expected_files:
                        if not os.path.exists(file):
                            self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                            print("TestSampleDataCreation = Failed")
                            return
                        else:
                            # Verify files are not empty
                            try:
                                with open(file, "r") as f:
                                    content = f.read().strip()
                                    if not content:
                                        self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                        print("TestSampleDataCreation = Failed")
                                        return
                            except Exception:
                                self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                print("TestSampleDataCreation = Failed")
                                return
                    
                    # Verify sensor readings format
                    if os.path.exists("sensor_readings.txt"):
                        try:
                            with open("sensor_readings.txt", "r") as f:
                                lines = f.readlines()
                                if len(lines) < 1:
                                    self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                    print("TestSampleDataCreation = Failed")
                                    return
                                else:
                                    # Check first line format
                                    parts = lines[0].strip().split(",")
                                    if len(parts) != 5:
                                        self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                        print("TestSampleDataCreation = Failed")
                                        return
                        except Exception:
                            self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                            print("TestSampleDataCreation = Failed")
                            return
                    
                    # Verify nutrient levels CSV format
                    if os.path.exists("nutrient_levels.csv"):
                        try:
                            with open("nutrient_levels.csv", "r") as f:
                                lines = f.readlines()
                                if len(lines) < 2:
                                    self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                    print("TestSampleDataCreation = Failed")
                                    return
                                elif "date,nitrogen,phosphorus,potassium,ec_level" not in lines[0]:
                                    self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                    print("TestSampleDataCreation = Failed")
                                    return
                        except Exception:
                            self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                            print("TestSampleDataCreation = Failed")
                            return
                    
                    # Verify recipes format
                    if os.path.exists("recipes.txt"):
                        try:
                            with open("recipes.txt", "r") as f:
                                content = f.read()
                                if "Recipe:" not in content:
                                    self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                                    print("TestSampleDataCreation = Failed")
                                    return
                        except Exception:
                            self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                            print("TestSampleDataCreation = Failed")
                            return
            else:
                self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
                print("TestSampleDataCreation = Failed")
                return
            
            # Don't clean up sample files here - they might be needed for other tests
            
            # All tests passed
            self.test_obj.yakshaAssert("TestSampleDataCreation", True, "functional")
            print("TestSampleDataCreation = Passed")

        except Exception:
            self.test_obj.yakshaAssert("TestSampleDataCreation", False, "functional")
            print("TestSampleDataCreation = Failed")

    def test_integration_workflow(self):
        """Test complete workflow integration"""
        try:
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                print("TestIntegrationWorkflow = Failed")
                return

            # Test complete workflow: create data -> read data -> generate report -> search logs
            
            # Step 1: Create sample data
            if check_function_exists(self.module_obj, "create_sample_data"):
                result = safely_call_function(self.module_obj, "create_sample_data")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
            else:
                self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                print("TestIntegrationWorkflow = Failed")
                return
            
            # Step 2: Add new sensor reading
            if check_function_exists(self.module_obj, "read_sensor_data") and check_function_exists(self.module_obj, "save_daily_readings"):
                existing_data = safely_call_function(self.module_obj, "read_sensor_data")
                if existing_data is None:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
                else:
                    new_reading = {
                        "date": "2023-06-10",
                        "temperature": 27.0,
                        "humidity": 68.0,
                        "ph_level": 6.3,
                        "light_level": 23000
                    }
                    existing_data.append(new_reading)
                    
                    result = safely_call_function(self.module_obj, "save_daily_readings", existing_data)
                    if result is None or result is not True:
                        self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                        print("TestIntegrationWorkflow = Failed")
                        return
            
            # Step 3: Add nutrient reading
            if check_function_exists(self.module_obj, "append_nutrient_reading"):
                new_nutrient = {
                    "date": "2023-06-10",
                    "nitrogen": 185,
                    "phosphorus": 50,
                    "potassium": 220,
                    "ec_level": 1.9
                }
                
                result = safely_call_function(self.module_obj, "append_nutrient_reading", new_nutrient)
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
            
            # Step 4: Generate report
            if check_function_exists(self.module_obj, "generate_weekly_report"):
                result = safely_call_function(self.module_obj, "generate_weekly_report", "sensor_readings.txt", "workflow_report.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
                elif not os.path.exists("workflow_report.txt"):
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
            
            # Step 5: Search logs for our activities
            if check_function_exists(self.module_obj, "search_logs"):
                result = safely_call_function(self.module_obj, "search_logs", "saved")
                if result is None or not isinstance(result, list):
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
                # Note: We don't require specific log entries as implementation may vary
            
            # Step 6: Create backup
            if check_function_exists(self.module_obj, "backup_data_files"):
                result = safely_call_function(self.module_obj, "backup_data_files", "sensor_readings.txt", "workflow_backup.txt")
                if result is None or result is not True:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
                elif not os.path.exists("workflow_backup.txt"):
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
            
            # Verify final state
            if check_function_exists(self.module_obj, "read_sensor_data"):
                final_data = safely_call_function(self.module_obj, "read_sensor_data")
                if final_data is None:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
                elif not any(reading.get("date") == "2023-06-10" for reading in final_data):
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
            
            if check_function_exists(self.module_obj, "read_nutrient_levels"):
                final_nutrients = safely_call_function(self.module_obj, "read_nutrient_levels")
                if final_nutrients is None:
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
                elif not any(nutrient.get("date") == "2023-06-10" for nutrient in final_nutrients):
                    self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
                    print("TestIntegrationWorkflow = Failed")
                    return
            
            # Clean up workflow test files
            cleanup_test_files(["workflow_report.txt", "workflow_backup.txt"])
            
            # All tests passed
            self.test_obj.yakshaAssert("TestIntegrationWorkflow", True, "functional")
            print("TestIntegrationWorkflow = Passed")

        except Exception:
            cleanup_test_files(["workflow_report.txt", "workflow_backup.txt"])
            self.test_obj.yakshaAssert("TestIntegrationWorkflow", False, "functional")
            print("TestIntegrationWorkflow = Failed")

if __name__ == '__main__':
    unittest.main()