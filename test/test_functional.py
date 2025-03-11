import pytest
import inspect
from test.TestUtils import TestUtils
from hydroponic_farm_monitoring_system import (
    read_sensor_data,
    save_daily_readings,
    log_system_event,
    update_recipe,
    read_nutrient_levels,
    append_nutrient_reading,
    generate_weekly_report,
    search_logs,
    backup_data_files,
    create_sample_data,
    main
)

class TestFunctional:
    """Test class for functional tests of the Hydroponic Farm Monitoring System."""
    
    def test_implementation_requirements(self):
        """Test function existence and implementation requirements"""
        try:
            # List of required function names
            required_functions = [
                "read_sensor_data", "save_daily_readings", "log_system_event",
                "update_recipe", "read_nutrient_levels", "append_nutrient_reading",
                "generate_weekly_report", "search_logs", "backup_data_files",
                "create_sample_data", "main"
            ]
            
            # Get all function names from the imported module
            module_functions = [name for name, obj in globals().items() 
                               if callable(obj) and not name.startswith('__') and not name.startswith('Test')]
            
            # Check each required function exists
            for func_name in required_functions:
                assert func_name in module_functions, f"Required function '{func_name}' is missing"
            
            # Check docstrings for all functions
            for func_name in required_functions:
                func = globals()[func_name]
                assert func.__doc__, f"Function '{func_name}' is missing a docstring"
            
            # Ensure create_sample_data creates required files
            create_sample_data()
            
            # Check if files were created
            import os
            assert os.path.exists("sensor_readings.txt"), "sensor_readings.txt was not created"
            assert os.path.exists("nutrient_levels.csv"), "nutrient_levels.csv was not created"
            assert os.path.exists("recipes.txt"), "recipes.txt was not created"
            
            # Check if a log entry was created (tests if create_sample_data logs its actions)
            log_results = search_logs("created sample data", "system_log.txt")
            assert len(log_results) > 0, "Sample data creation should be logged"
            
            TestUtils.yakshaAssert("TestImplementationRequirements", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestImplementationRequirements", False, "functional")
            pytest.fail(f"Implementation requirements test failed: {str(e)}")
    
    def test_file_reading_operations(self):
        """Test reading operations from data files"""
        try:
            # Create sample data for testing
            create_sample_data()
            
            # Test reading sensor data
            readings = read_sensor_data()
            assert isinstance(readings, list) and len(readings) > 0, "read_sensor_data should return a non-empty list"
            
            # Verify sample readings data structure
            first_reading = readings[0]
            required_fields = ["date", "temperature", "humidity", "ph_level", "light_level"]
            for field in required_fields:
                assert field in first_reading, f"Sensor reading missing required field: {field}"
            
            # Test reading nutrient levels
            nutrients = read_nutrient_levels()
            assert isinstance(nutrients, list) and len(nutrients) > 0, "read_nutrient_levels should return a non-empty list"
            
            # Verify sample nutrient data structure
            first_nutrient = nutrients[0]
            required_fields = ["date", "nitrogen", "phosphorus", "potassium", "ec_level"]
            for field in required_fields:
                assert field in first_nutrient, f"Nutrient reading missing required field: {field}"
            
            # Test searching logs - create a log entry first
            log_system_event("test_event", "Test log entry")
            log_results = search_logs("test")
            assert isinstance(log_results, list), "search_logs should return a list"
            assert len(log_results) > 0, "Should find logs containing test term"
            
            # Test searching for non-existent term
            nonexistent_logs = search_logs("nonexistent_term")
            assert isinstance(nonexistent_logs, list), "search_logs should return a list"
            assert len(nonexistent_logs) == 0, "Should return empty list for non-existent term"
            
            TestUtils.yakshaAssert("TestFileReadingOperations", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestFileReadingOperations", False, "functional")
            pytest.fail(f"File reading operations test failed: {str(e)}")
    
    def test_file_writing_operations(self):
        """Test writing operations to data files"""
        try:
            # Create sample data for testing
            create_sample_data()
            
            # Test saving sensor readings
            new_reading = {
                "date": "2023-06-15",
                "temperature": 26.2,
                "humidity": 70.5,
                "ph_level": 6.4,
                "light_level": 23000
            }
            
            # Read existing data
            existing_readings = read_sensor_data()
            initial_count = len(existing_readings)
            
            # Add new reading and save
            existing_readings.append(new_reading)
            save_result = save_daily_readings(existing_readings)
            assert save_result is True, "Should successfully save readings"
            
            # Verify reading was added
            updated_readings = read_sensor_data()
            assert len(updated_readings) == initial_count + 1, "Should have one more reading"
            
            found_reading = False
            for reading in updated_readings:
                if (reading["date"] == "2023-06-15" and
                    reading["temperature"] == 26.2 and
                    reading["humidity"] == 70.5):
                    found_reading = True
                    break
            
            assert found_reading, "Should find newly added reading"
            
            # Check if save operation was logged
            log_results = search_logs("saved", "system_log.txt")
            assert len(log_results) > 0, "Save operation should be logged"
            
            # Test appending nutrient reading
            new_nutrient = {
                "date": "2023-06-15",
                "nitrogen": 190,
                "phosphorus": 50,
                "potassium": 220,
                "ec_level": 2.0
            }
            
            append_result = append_nutrient_reading(new_nutrient)
            assert append_result is True, "Should successfully append nutrient reading"
            
            # Verify nutrient reading was added
            updated_nutrients = read_nutrient_levels()
            
            found_nutrient = False
            for nutrient in updated_nutrients:
                if (nutrient["date"] == "2023-06-15" and
                    nutrient["nitrogen"] == 190 and
                    nutrient["phosphorus"] == 50):
                    found_nutrient = True
                    break
            
            assert found_nutrient, "Should find newly added nutrient reading"
            
            # Test updating recipe
            recipe_name = "Leafy Greens"
            new_instructions = "Updated Nitrogen: 200 ppm\nUpdated Phosphorus: 55 ppm\nUpdated Potassium: 220 ppm"
            
            update_result = update_recipe(recipe_name, new_instructions)
            assert update_result is True, "Should successfully update recipe"
            
            # Verify recipe was updated
            with open("recipes.txt", "r") as file:
                content = file.read()
                assert "Updated Nitrogen: 200 ppm" in content, "Recipe should contain updated content"
                assert "Updated Phosphorus: 55 ppm" in content, "Recipe should contain updated content"
            
            # Test creating backup
            backup_result = backup_data_files("sensor_readings.txt", "sensor_backup.txt")
            assert backup_result is True, "Should successfully create backup"
            
            # Verify backup was created
            import os
            assert os.path.exists("sensor_backup.txt"), "Backup file should exist"
            
            # Verify backup content
            with open("sensor_backup.txt", "r") as file:
                content = file.read()
                assert "2023-06-15,26.2,70.5,6.4,23000" in content, "Backup should contain data"
            
            # Clean up backup file
            if os.path.exists("sensor_backup.txt"):
                os.remove("sensor_backup.txt")
            
            TestUtils.yakshaAssert("TestFileWritingOperations", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestFileWritingOperations", False, "functional")
            pytest.fail(f"File writing operations test failed: {str(e)}")
    
    def test_analysis_operations(self):
        """Test analysis and reporting operations with calculation verification"""
        try:
            # Create sample data for testing
            create_sample_data()
            
            # Get original sensor readings to verify calculations later
            original_readings = read_sensor_data()
            
            # Calculate expected averages manually
            expected_temp_sum = sum(reading["temperature"] for reading in original_readings)
            expected_humidity_sum = sum(reading["humidity"] for reading in original_readings)
            expected_ph_sum = sum(reading["ph_level"] for reading in original_readings)
            expected_light_sum = sum(reading["light_level"] for reading in original_readings)
            
            count = len(original_readings)
            expected_avg_temp = expected_temp_sum / count
            expected_avg_humidity = expected_humidity_sum / count
            expected_avg_ph = expected_ph_sum / count
            expected_avg_light = expected_light_sum / count
            
            # Test generating weekly report
            report_result = generate_weekly_report("sensor_readings.txt", "test_report.txt")
            assert report_result is True, "Should successfully generate report"
            
            # Verify report was created
            import os
            assert os.path.exists("test_report.txt"), "Report file should exist"
            
            # Verify report content
            with open("test_report.txt", "r") as file:
                content = file.read()
                assert "WEEKLY HYDROPONIC MONITORING REPORT" in content, "Report should have title"
                assert "AVERAGES:" in content, "Report should include averages"
                
                # Verify calculations are correct
                temp_line = next((line for line in content.split('\n') if line.startswith("Temperature:")), "")
                humidity_line = next((line for line in content.split('\n') if line.startswith("Humidity:")), "")
                ph_line = next((line for line in content.split('\n') if line.startswith("pH Level:")), "")
                
                # Extract calculated values from the report (handle different formatting)
                import re
                temp_match = re.search(r"Temperature:\s*([\d.]+)", temp_line)
                humidity_match = re.search(r"Humidity:\s*([\d.]+)", humidity_line)
                ph_match = re.search(r"pH Level:\s*([\d.]+)", ph_line)
                
                if temp_match and humidity_match and ph_match:
                    reported_temp = float(temp_match.group(1))
                    reported_humidity = float(humidity_match.group(1))
                    reported_ph = float(ph_match.group(1))
                    
                    # Allow small rounding differences (0.1)
                    assert abs(reported_temp - expected_avg_temp) < 0.2, "Temperature average calculation should be correct"
                    assert abs(reported_humidity - expected_avg_humidity) < 0.2, "Humidity average calculation should be correct"
                    assert abs(reported_ph - expected_avg_ph) < 0.2, "pH average calculation should be correct"
                else:
                    assert False, "Report should include properly formatted averages"
            
            # Clean up report file
            if os.path.exists("test_report.txt"):
                os.remove("test_report.txt")
            
            TestUtils.yakshaAssert("TestAnalysisOperations", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestAnalysisOperations", False, "functional")
            pytest.fail(f"Analysis operations test failed: {str(e)}")
    
    def test_logging_operations(self):
        """Test logging operations and file handling modes"""
        try:
            # Create empty log file
            import os
            if os.path.exists("test_system_log.txt"):
                os.remove("test_system_log.txt")
            
            # Test logging operations
            log_result = log_system_event("TestEvent", "Test event details", "test_system_log.txt")
            assert log_result is True, "Should successfully log event"
            
            # Verify log was written
            assert os.path.exists("test_system_log.txt"), "Log file should exist"
            
            # Read the first log content
            with open("test_system_log.txt", "r") as file:
                first_log_content = file.read()
                assert "TestEvent" in first_log_content, "Log should contain event type"
                assert "Test event details" in first_log_content, "Log should contain message"
            
            # Test logging multiple events - this tests if append mode is working correctly
            log_system_event("Add", "Added test data", "test_system_log.txt")
            log_system_event("Update", "Updated test data", "test_system_log.txt")
            
            # Read the log again to verify append mode is working (previous log wasn't overwritten)
            with open("test_system_log.txt", "r") as file:
                updated_log_content = file.read()
                assert first_log_content in updated_log_content, "First log should still exist (append mode test)"
                assert "Added test data" in updated_log_content, "Second log should be added"
                assert "Updated test data" in updated_log_content, "Third log should be added"
            
            # Test case-insensitive search
            results_lower = search_logs("test", "test_system_log.txt")
            results_upper = search_logs("TEST", "test_system_log.txt")
            assert len(results_lower) > 0, "Should find logs with lowercase search"
            assert len(results_upper) > 0, "Should find logs with uppercase search (case-insensitive)"
            assert len(results_lower) == len(results_upper), "Case-insensitive search should return same results"
            
            # Verify search results structure
            first_result = results_lower[0]
            required_fields = ["timestamp", "event_type", "message"]
            for field in required_fields:
                assert field in first_result, f"Log entry missing required field: {field}"
            
            # Clean up log file
            if os.path.exists("test_system_log.txt"):
                os.remove("test_system_log.txt")
            
            TestUtils.yakshaAssert("TestLoggingOperations", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestLoggingOperations", False, "functional")
            pytest.fail(f"Logging operations test failed: {str(e)}")
    
    def test_file_handling_modes(self):
        """Test specific file handling modes and context manager usage"""
        try:
            import os
            
            # Create sample binary file for testing
            with open("test_binary.dat", "wb") as f:
                f.write(b'\x00\x01\x02\x03\x04\x05')
            
            # Test r+ mode (read/write) by creating a recipe file and updating it
            with open("test_r_plus.txt", "w") as f:
                f.write("Recipe: TestRecipe\nOriginal line 1\nOriginal line 2\n")
            
            # Update using r+ mode (should not use separate read/write operations)
            result = update_recipe("TestRecipe", "Updated line 1\nUpdated line 2", "test_r_plus.txt")
            assert result is True, "Should successfully update recipe using r+ mode"
            
            # Test backup function with binary content
            backup_result = backup_data_files("test_binary.dat", "test_binary_backup.dat")
            assert backup_result is True, "Should successfully backup binary file"
            
            # Binary files should be identical
            with open("test_binary.dat", "rb") as original:
                original_content = original.read()
            
            with open("test_binary_backup.dat", "rb") as backup:
                backup_content = backup.read()
            
            assert original_content == backup_content, "Binary backup should match original exactly"
            
            # Test context manager usage by injecting a temporary file error
            # Create a class to monitor file opens
            class FileOpenMonitor:
                def __init__(self):
                    self.files_opened = 0
                    self.files_closed = 0
                    self.original_open = open
                
                def custom_open(self, *args, **kwargs):
                    file = self.original_open(*args, **kwargs)
                    self.files_opened += 1
                    original_close = file.close
                    
                    def counting_close():
                        self.files_closed += 1
                        return original_close()
                    
                    file.close = counting_close
                    return file
                
                def install(self):
                    import builtins
                    builtins.open = self.custom_open
                
                def uninstall(self):
                    import builtins
                    builtins.open = self.original_open
            
            # Install monitor, run a test function, then check if all files were closed
            monitor = FileOpenMonitor()
            try:
                monitor.install()
                
                # Call a function that should use context manager
                read_sensor_data("sensor_readings.txt")
                
                # Check if all opened files were closed
                assert monitor.files_opened > 0, "Function should open files"
                assert monitor.files_opened == monitor.files_closed, "All opened files should be closed (use context managers)"
            finally:
                monitor.uninstall()
            
            # Clean up test files
            for file in ["test_binary.dat", "test_binary_backup.dat", "test_r_plus.txt"]:
                if os.path.exists(file):
                    os.remove(file)
            
            TestUtils.yakshaAssert("TestFileHandlingModes", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestFileHandlingModes", False, "functional")
            pytest.fail(f"File handling modes test failed: {str(e)}")
    
    def test_integration(self):
        """Test integration of multiple functions together"""
        try:
            # Create sample data for testing
            create_sample_data()
            
            # Test complete workflow:
            # 1. Add sensor reading
            # 2. Add nutrient reading
            # 3. Update recipe
            # 4. Generate report
            # 5. Search logs
            # 6. Create backup
            
            # Step 1: Add sensor reading
            new_reading = {
                "date": "2023-06-20",
                "temperature": 26.5,
                "humidity": 68.0,
                "ph_level": 6.3,
                "light_level": 22500
            }
            
            existing_readings = read_sensor_data()
            existing_readings.append(new_reading)
            save_daily_readings(existing_readings)
            
            # Step 2: Add nutrient reading
            new_nutrient = {
                "date": "2023-06-20",
                "nitrogen": 185,
                "phosphorus": 47,
                "potassium": 212,
                "ec_level": 1.9
            }
            
            append_nutrient_reading(new_nutrient)
            
            # Step 3: Update recipe
            recipe_name = "Tomatoes"
            new_recipe = "Nitrogen: 170 ppm\nPhosphorus: 65 ppm\nPotassium: 200 ppm\nEC Range: 2.2-3.0\npH Range: 5.8-6.2"
            
            update_recipe(recipe_name, new_recipe)
            
            # Step 4: Generate report
            generate_weekly_report("sensor_readings.txt", "integration_report.txt")
            
            # Step 5: Search logs
            logs = search_logs("recipe")
            assert isinstance(logs, list), "Should return a list of log entries"
            
            # Step 6: Create backup
            backup_data_files("recipes.txt", "recipes_backup.txt")
            
            # Verify all operations worked correctly
            # Check sensor reading was added
            updated_readings = read_sensor_data()
            found_reading = False
            for reading in updated_readings:
                if reading["date"] == "2023-06-20":
                    found_reading = True
                    break
            assert found_reading, "Should find newly added sensor reading"
            
            # Check nutrient reading was added
            updated_nutrients = read_nutrient_levels()
            found_nutrient = False
            for nutrient in updated_nutrients:
                if nutrient["date"] == "2023-06-20":
                    found_nutrient = True
                    break
            assert found_nutrient, "Should find newly added nutrient reading"
            
            # Check recipe was updated
            with open("recipes.txt", "r") as file:
                content = file.read()
                assert "Nitrogen: 170 ppm" in content, "Recipe should be updated"
            
            # Check report was generated
            import os
            assert os.path.exists("integration_report.txt"), "Report should be created"
            
            # Check backup was created
            assert os.path.exists("recipes_backup.txt"), "Backup should be created"
            
            # Clean up test files
            for file in ["integration_report.txt", "recipes_backup.txt"]:
                if os.path.exists(file):
                    os.remove(file)
            
            TestUtils.yakshaAssert("TestIntegration", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("TestIntegration", False, "functional")
            pytest.fail(f"Integration test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])