import pytest
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
    create_sample_data
)

class TestExceptional:
    """Exception handling tests for hydroponic farm monitoring system functions."""
    
    def test_exceptional_cases(self):
        """Test error handling and invalid inputs across all functions"""
        try:
            # Create sample data for testing
            create_sample_data()
            
            # ------------ PART 1: File Not Found Handling ------------
            
            # Test with non-existent files
            nonexistent_file = "nonexistent_file.txt"
            
            # Each function should handle nonexistent files gracefully
            sensor_data = read_sensor_data(nonexistent_file)
            assert isinstance(sensor_data, list) and len(sensor_data) == 0, "Should handle nonexistent sensor file"
            
            nutrients = read_nutrient_levels(nonexistent_file)
            assert isinstance(nutrients, list) and len(nutrients) == 0, "Should handle nonexistent nutrients file"
            
            search_results = search_logs("test", nonexistent_file)
            assert isinstance(search_results, list) and len(search_results) == 0, "Should handle nonexistent log file"
            
            report_result = generate_weekly_report(nonexistent_file, "report.txt")
            assert report_result is False, "Should handle nonexistent sensor file for report"
            
            backup_result = backup_data_files(nonexistent_file, "backup.txt")
            assert backup_result is False, "Should handle nonexistent source file for backup"
            
            update_result = update_recipe("TestRecipe", "New content", nonexistent_file)
            assert update_result is False, "Should handle nonexistent recipes file"
            
            # ------------ PART 2: Invalid Input Data Handling ------------
            
            # Test with invalid reading data (missing required fields)
            invalid_reading = [{
                "date": "2023-06-05"
                # Missing other required fields
            }]
            
            result = save_daily_readings(invalid_reading, "test_sensor.txt")
            assert isinstance(result, bool), "Should handle incomplete reading data"
            
            # Test with invalid nutrient data (missing required fields)
            invalid_nutrient = {
                "date": "2023-06-05"
                # Missing other required fields
            }
            
            result = append_nutrient_reading(invalid_nutrient, "test_nutrients.csv")
            assert isinstance(result, bool), "Should handle incomplete nutrient data"
            
            # Test updating non-existent recipe
            result = update_recipe("NonExistentRecipe", "New content", "recipes.txt")
            assert result is False, "Should handle non-existent recipe"
            
            # Test with invalid data types
            for func_name, func, args in [
                ("read_sensor_data", read_sensor_data, (123,)),
                ("read_nutrient_levels", read_nutrient_levels, (123,)),
                ("search_logs", search_logs, (123, "logs.txt")),
                ("generate_weekly_report", generate_weekly_report, (123, 456)),
                ("backup_data_files", backup_data_files, (123, 456)),
                ("update_recipe", update_recipe, (123, 456, 789))
            ]:
                try:
                    result = func(*args)
                    # Even with invalid types, functions should return appropriate default values without crashing
                    if func_name == "read_sensor_data" or func_name == "read_nutrient_levels" or func_name == "search_logs":
                        assert isinstance(result, list), f"{func_name} should return a list even with invalid input"
                    elif func_name == "generate_weekly_report" or func_name == "backup_data_files" or func_name == "update_recipe":
                        assert isinstance(result, bool), f"{func_name} should return a boolean even with invalid input"
                except Exception:
                    # If an exception is thrown, that's acceptable too
                    pass
            
            # ------------ PART 3: Corrupted Data Handling ------------
            
            # Create files with corrupted data
            with open("corrupted_sensor.txt", "w") as f:
                f.write("This is not a valid CSV format\n")
                f.write("2023-06-01,incomplete line\n")
                f.write(",,,,,\n")  # Empty fields
                f.write("2023-06-02,invalid_temp,60.0,6.0,20000\n")  # Invalid temperature
            
            with open("corrupted_nutrients.csv", "w") as f:
                f.write("date,nitrogen,phosphorus,potassium,ec_level\n")
                f.write("This is not a valid CSV format\n")
                f.write("2023-06-01,incomplete line\n")
                f.write("2023-06-02,invalid_nitrogen,40,200,1.7\n")  # Invalid nitrogen
            
            # Test reading corrupted files
            corrupted_readings = read_sensor_data("corrupted_sensor.txt")
            assert isinstance(corrupted_readings, list), "Should handle corrupted sensor data gracefully"
            
            corrupted_nutrients = read_nutrient_levels("corrupted_nutrients.csv")
            assert isinstance(corrupted_nutrients, list), "Should handle corrupted nutrients gracefully"
            
            # Test generating report with corrupted data
            report_result = generate_weekly_report("corrupted_sensor.txt", "corrupted_report.txt")
            assert isinstance(report_result, bool), "Should handle corrupted data for report"
            
            # ------------ PART 4: Edge Case Handling ------------
            
            # Test with empty list of readings
            empty_list_result = save_daily_readings([], "test_sensor.txt")
            assert isinstance(empty_list_result, bool), "Should handle empty list of readings"
            
            # Test with negative values for sensor readings
            negative_reading = [{
                "date": "2023-06-05",
                "temperature": -10.0,  # Negative temperature
                "humidity": 60.0,
                "ph_level": 6.0,
                "light_level": 20000
            }]
            
            result = save_daily_readings(negative_reading, "test_sensor.txt")
            assert isinstance(result, bool), "Should handle negative temperature appropriately"
            
            # Test with extreme values
            extreme_reading = [{
                "date": "2023-06-05",
                "temperature": 1000.0,  # Very high temperature
                "humidity": 150.0,  # Over 100% humidity
                "ph_level": 14.5,  # pH over normal range
                "light_level": 9999999  # Very high light
            }]
            
            result = save_daily_readings(extreme_reading, "test_sensor.txt")
            assert isinstance(result, bool), "Should handle extreme values appropriately"
            
            # Test with invalid file paths (directories, etc.)
            import os
            if not os.path.exists("test_dir"):
                os.mkdir("test_dir")
                
            try:
                result = read_sensor_data("test_dir")
                # Should handle directory path gracefully
            except Exception:
                # Exception is also acceptable
                pass
            
            # Clean up test files
            for file in ["corrupted_sensor.txt", "corrupted_nutrients.csv", "test_sensor.txt", 
                         "test_nutrients.csv", "corrupted_report.txt", "report.txt", "backup.txt"]:
                if os.path.exists(file):
                    os.remove(file)
                    
            if os.path.exists("test_dir"):
                os.rmdir("test_dir")
            
            TestUtils.yakshaAssert("TestExceptionalCases", True, "exception")
        except Exception as e:
            TestUtils.yakshaAssert("TestExceptionalCases", False, "exception")
            pytest.fail(f"Exception testing failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])