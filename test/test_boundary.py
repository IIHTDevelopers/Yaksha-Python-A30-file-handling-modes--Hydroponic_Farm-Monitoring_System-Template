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

class TestBoundary:
    """Boundary tests for hydroponic farm monitoring system functions."""
    
    def test_boundary_scenarios(self):
        """Test boundary cases for hydroponic farm functions"""
        try:
            # Create sample data for testing
            create_sample_data()
            
            # Test with empty files
            # Create empty files for testing
            with open("empty_sensor.txt", "w") as f:
                pass
                
            with open("empty_nutrients.csv", "w") as f:
                pass
                
            with open("empty_logs.txt", "w") as f:
                pass
            
            # Test reading empty sensor file
            empty_readings = read_sensor_data("empty_sensor.txt")
            assert len(empty_readings) == 0, "Empty sensor file should return empty list"
            
            # Test reading empty nutrients file
            empty_nutrients = read_nutrient_levels("empty_nutrients.csv")
            assert len(empty_nutrients) == 0, "Empty nutrients file should return empty list"
            
            # Test searching empty logs file
            empty_logs = search_logs("test", "empty_logs.txt")
            assert len(empty_logs) == 0, "Empty logs file should return empty list"
            
            # Test generating report with empty data
            report_result = generate_weekly_report("empty_sensor.txt", "empty_report.txt")
            assert report_result is False, "Empty sensor data should fail to generate report"
            
            # Test with minimal single-record files
            # Create minimal files
            with open("single_sensor.txt", "w") as f:
                f.write("2023-06-01,24.5,65.2,6.2,22000\n")
                
            with open("single_nutrients.csv", "w") as f:
                f.write("date,nitrogen,phosphorus,potassium,ec_level\n")
                f.write("2023-06-01,180,45,210,1.8\n")
                
            with open("single_recipe.txt", "w") as f:
                f.write("Recipe: TestRecipe\n")
                f.write("Test Line 1\n")
                f.write("Test Line 2\n")
            
            # Test reading single-record sensor data
            single_reading = read_sensor_data("single_sensor.txt")
            assert len(single_reading) == 1, "Single record sensor file should return list with one item"
            assert single_reading[0]["date"] == "2023-06-01", "Should read the correct date"
            
            # Test reading single-record nutrients
            single_nutrients = read_nutrient_levels("single_nutrients.csv")
            assert len(single_nutrients) == 1, "Single record nutrients file should return list with one item"
            assert single_nutrients[0]["date"] == "2023-06-01", "Should read the correct date"
            
            # Test updating single recipe
            update_result = update_recipe("TestRecipe", "New Line 1\nNew Line 2", "single_recipe.txt")
            assert update_result is True, "Should successfully update single recipe"
            
            # Test reading updated recipe
            with open("single_recipe.txt", "r") as f:
                content = f.read()
                assert "New Line 1" in content, "Recipe should be updated with new content"
                assert "Test Line 1" not in content, "Old recipe content should be replaced"
            
            # Test boundary cases for save_daily_readings
            # Test with minimal required fields
            minimal_reading = [{
                "date": "2023-06-05",
                "temperature": 25.0,
                "humidity": 60.0,
                "ph_level": 6.0,
                "light_level": 20000
            }]
            result = save_daily_readings(minimal_reading, "test_sensor.txt")
            assert result is True, "Should successfully save minimal reading"
            
            # Test appending nutrient reading
            minimal_nutrient = {
                "date": "2023-06-05",
                "nitrogen": 170,
                "phosphorus": 40,
                "potassium": 200,
                "ec_level": 1.7
            }
            append_result = append_nutrient_reading(minimal_nutrient, "test_nutrients.csv")
            assert append_result is True, "Should successfully append nutrient reading"
            
            # Test backup with single file
            backup_result = backup_data_files("single_sensor.txt", "backup_sensor.txt")
            assert backup_result is True, "Should successfully backup single file"
            
            # Verify backup file content
            with open("backup_sensor.txt", "r") as f:
                content = f.read()
                assert "2023-06-01,24.5,65.2,6.2,22000" in content, "Backup should contain original content"
            
            # Test logging with minimal info
            log_result = log_system_event("test", "minimal test", "test_log.txt")
            assert log_result is True, "Should successfully log event"
            
            # Clean up test files
            import os
            for file in ["empty_sensor.txt", "empty_nutrients.csv", "empty_logs.txt", 
                        "single_sensor.txt", "single_nutrients.csv", "single_recipe.txt",
                        "test_sensor.txt", "test_nutrients.csv", "backup_sensor.txt", 
                        "test_log.txt", "empty_report.txt"]:
                if os.path.exists(file):
                    os.remove(file)
            
            TestUtils.yakshaAssert("TestBoundaryScenarios", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            pytest.fail(f"Boundary scenarios test failed: {str(e)}")


if __name__ == '__main__':
    pytest.main(['-v'])