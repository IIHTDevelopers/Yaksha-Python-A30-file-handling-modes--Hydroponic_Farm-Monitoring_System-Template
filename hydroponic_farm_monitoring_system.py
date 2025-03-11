"""
Hydroponic Farm Monitoring System

This module provides functions for tracking plant growth, nutrient levels,
and environmental conditions using different file handling modes.
"""

def read_sensor_data(file_path="sensor_readings.txt"):
    """
    Reads sensor data from a file using read ('r') mode.
    
    Args:
        file_path (str): Path to the sensor readings file
        
    Returns:
        list: List of dictionaries containing sensor readings
    """
    readings = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        reading = {
                            "date": parts[0],
                            "temperature": float(parts[1]),
                            "humidity": float(parts[2]),
                            "ph_level": float(parts[3]),
                            "light_level": float(parts[4])
                        }
                        readings.append(reading)
        return readings
    except FileNotFoundError:
        print(f"Sensor data file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return []


def save_daily_readings(data, file_path="sensor_readings.txt"):
    """
    Saves sensor readings to a file using write ('w') mode.
    This will overwrite any existing file.
    
    Args:
        data (list): List of dictionaries containing sensor readings
        file_path (str): Path to the sensor readings file
        
    Returns:
        bool: True if the data was saved successfully
    """
    try:
        with open(file_path, "w") as file:
            for reading in data:
                line = (f"{reading['date']},{reading['temperature']},"
                        f"{reading['humidity']},{reading['ph_level']},"
                        f"{reading['light_level']}\n")
                file.write(line)
        
        log_system_event("Data saved", f"Saved {len(data)} readings to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving readings: {e}")
        return False


def log_system_event(event_type, message, file_path="system_log.txt"):
    """
    Logs a system event using append ('a') mode.
    
    Args:
        event_type (str): Type of event
        message (str): Event details
        file_path (str): Path to the log file
        
    Returns:
        bool: True if the event was logged successfully
    """
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(file_path, "a") as file:
            log_entry = f"{timestamp},{event_type},{message}\n"
            file.write(log_entry)
        
        return True
    except Exception as e:
        print(f"Error logging event: {e}")
        return False


def update_recipe(recipe_name, new_instructions, file_path="recipes.txt"):
    """
    Updates a nutrient recipe using read/write ('r+') mode.
    
    Args:
        recipe_name (str): Name of the recipe to update
        new_instructions (str): New recipe instructions
        file_path (str): Path to the recipes file
        
    Returns:
        bool: True if the recipe was updated successfully
    """
    try:
        # Read all recipes
        recipes = []
        with open(file_path, "r") as file:
            content = file.read()
            recipe_blocks = content.split("\n\n")
            
            for block in recipe_blocks:
                if block.strip():
                    recipes.append(block)
        
        # Find and update the specific recipe
        recipe_found = False
        for i, recipe in enumerate(recipes):
            if recipe.startswith(f"Recipe: {recipe_name}"):
                # Update recipe
                recipe_lines = recipe.split("\n")
                recipe_header = recipe_lines[0]
                recipes[i] = f"{recipe_header}\n{new_instructions}"
                recipe_found = True
                break
        
        if not recipe_found:
            print(f"Recipe not found: {recipe_name}")
            return False
        
        # Write back all recipes
        with open(file_path, "w") as file:
            file.write("\n\n".join(recipes))
        
        log_system_event("Recipe updated", f"Updated recipe '{recipe_name}'")
        return True
    except FileNotFoundError:
        print(f"Recipes file not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error updating recipe: {e}")
        return False


def read_nutrient_levels(file_path="nutrient_levels.csv"):
    """
    Reads nutrient level data from a CSV file using read ('r') mode.
    
    Args:
        file_path (str): Path to the nutrient levels file
        
    Returns:
        list: List of dictionaries containing nutrient readings
    """
    nutrients = []
    try:
        with open(file_path, "r") as file:
            # Skip header line
            header = file.readline()
            
            for line in file:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        nutrient = {
                            "date": parts[0],
                            "nitrogen": float(parts[1]),
                            "phosphorus": float(parts[2]),
                            "potassium": float(parts[3]),
                            "ec_level": float(parts[4])
                        }
                        nutrients.append(nutrient)
        return nutrients
    except FileNotFoundError:
        print(f"Nutrient levels file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading nutrient levels: {e}")
        return []


def append_nutrient_reading(reading, file_path="nutrient_levels.csv"):
    """
    Appends a new nutrient reading to the CSV file using append ('a') mode.
    
    Args:
        reading (dict): Dictionary containing nutrient reading data
        file_path (str): Path to the nutrient levels file
        
    Returns:
        bool: True if the reading was appended successfully
    """
    try:
        # Check if file exists
        file_exists = True
        try:
            with open(file_path, "r"):
                pass
        except FileNotFoundError:
            file_exists = False
        
        with open(file_path, "a") as file:
            # Write header if file is new
            if not file_exists:
                file.write("date,nitrogen,phosphorus,potassium,ec_level\n")
            
            # Write reading
            line = (f"{reading['date']},{reading['nitrogen']},"
                    f"{reading['phosphorus']},{reading['potassium']},"
                    f"{reading['ec_level']}\n")
            file.write(line)
        
        log_system_event("Nutrient reading", f"Added reading for {reading['date']}")
        return True
    except Exception as e:
        print(f"Error appending nutrient reading: {e}")
        return False


def generate_weekly_report(data_file_path, output_file_path="weekly_report.txt"):
    """
    Generates a weekly report from sensor data using read ('r') and write ('w') modes.
    
    Args:
        data_file_path (str): Path to the sensor readings file
        output_file_path (str): Path to the output report file
        
    Returns:
        bool: True if the report was generated successfully
    """
    try:
        # Read sensor data
        readings = read_sensor_data(data_file_path)
        
        if not readings:
            print("No sensor data available for report")
            return False
        
        # Calculate averages
        total_temp = sum(reading["temperature"] for reading in readings)
        total_humidity = sum(reading["humidity"] for reading in readings)
        total_ph = sum(reading["ph_level"] for reading in readings)
        total_light = sum(reading["light_level"] for reading in readings)
        
        count = len(readings)
        avg_temp = total_temp / count
        avg_humidity = total_humidity / count
        avg_ph = total_ph / count
        avg_light = total_light / count
        
        # Get date range
        start_date = readings[0]["date"]
        end_date = readings[-1]["date"]
        
        # Generate report
        with open(output_file_path, "w") as file:
            file.write(f"WEEKLY HYDROPONIC MONITORING REPORT\n")
            file.write(f"Period: {start_date} to {end_date}\n")
            file.write(f"Number of readings: {count}\n\n")
            
            file.write(f"AVERAGES:\n")
            file.write(f"Temperature: {avg_temp:.1f}°C\n")
            file.write(f"Humidity: {avg_humidity:.1f}%\n")
            file.write(f"pH Level: {avg_ph:.2f}\n")
            file.write(f"Light Level: {avg_light:.1f} lux\n\n")
            
            file.write(f"DAILY READINGS:\n")
            for reading in readings:
                file.write(f"Date: {reading['date']}\n")
                file.write(f"  Temperature: {reading['temperature']}°C\n")
                file.write(f"  Humidity: {reading['humidity']}%\n")
                file.write(f"  pH Level: {reading['ph_level']}\n")
                file.write(f"  Light Level: {reading['light_level']} lux\n\n")
        
        log_system_event("Report generated", f"Created weekly report {output_file_path}")
        return True
    except Exception as e:
        print(f"Error generating report: {e}")
        return False


def search_logs(search_term, file_path="system_log.txt"):
    """
    Searches the log file for entries containing a specific term using read ('r') mode.
    
    Args:
        search_term (str): Term to search for
        file_path (str): Path to the log file
        
    Returns:
        list: List of log entries containing the search term
    """
    results = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                if search_term.lower() in line.lower():
                    parts = line.strip().split(",", 2)
                    if len(parts) >= 3:
                        log_entry = {
                            "timestamp": parts[0],
                            "event_type": parts[1],
                            "message": parts[2]
                        }
                        results.append(log_entry)
        return results
    except FileNotFoundError:
        print(f"Log file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error searching logs: {e}")
        return []


def backup_data_files(source_path, backup_path):
    """
    Creates backup copies of data files using read ('r') and write ('w') modes.
    
    Args:
        source_path (str): Path to the source file
        backup_path (str): Path to the backup file
        
    Returns:
        bool: True if the backup was created successfully
    """
    try:
        # Read source file
        with open(source_path, "r") as source_file:
            content = source_file.read()
        
        # Write to backup file
        with open(backup_path, "w") as backup_file:
            backup_file.write(content)
        
        log_system_event("Backup created", f"Backed up {source_path} to {backup_path}")
        return True
    except FileNotFoundError:
        print(f"Source file not found: {source_path}")
        return False
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False


def create_sample_data():
    """
    Creates sample data files for demonstration purposes.
    
    Returns:
        bool: True if sample data was created successfully
    """
    try:
        # Create sensor readings file
        with open("sensor_readings.txt", "w") as file:
            file.write("2023-06-01,24.5,65.2,6.2,22000\n")
            file.write("2023-06-02,25.1,63.7,6.3,21800\n")
            file.write("2023-06-03,24.8,67.5,6.1,22500\n")
        
        # Create nutrient levels file
        with open("nutrient_levels.csv", "w") as file:
            file.write("date,nitrogen,phosphorus,potassium,ec_level\n")
            file.write("2023-06-01,180,45,210,1.8\n")
            file.write("2023-06-02,175,42,205,1.7\n")
            file.write("2023-06-03,185,48,215,1.9\n")
        
        # Create recipes file
        with open("recipes.txt", "w") as file:
            file.write("Recipe: Leafy Greens\n")
            file.write("Nitrogen: 180 ppm\n")
            file.write("Phosphorus: 50 ppm\n")
            file.write("Potassium: 210 ppm\n")
            file.write("EC Range: 1.6-2.0\n")
            file.write("pH Range: 5.8-6.2\n\n")
            
            file.write("Recipe: Tomatoes\n")
            file.write("Nitrogen: 160 ppm\n")
            file.write("Phosphorus: 60 ppm\n")
            file.write("Potassium: 190 ppm\n")
            file.write("EC Range: 2.0-3.5\n")
            file.write("pH Range: 5.5-6.5\n")
        
        log_system_event("Setup", "Created sample data files")
        return True
    except Exception as e:
        print(f"Error creating sample data: {e}")
        return False


def main():
    """
    Main function demonstrating the hydroponic farm monitoring system.
    """
    print("===== HYDROPONIC FARM MONITORING SYSTEM =====")
    
    # Create sample data if needed
    create_data = input("Create sample data? (y/n): ").lower()
    if create_data == 'y':
        if create_sample_data():
            print("Sample data created successfully.")
        else:
            print("Failed to create sample data.")
    
    while True:
        print("\nOptions:")
        print("1. View sensor readings")
        print("2. Add new sensor reading")
        print("3. View nutrient levels")
        print("4. Add new nutrient reading")
        print("5. Update recipe")
        print("6. Generate weekly report")
        print("7. Search system logs")
        print("8. Create backup")
        print("0. Exit")
        
        choice = input("\nEnter option: ")
        
        if choice == '1':
            readings = read_sensor_data()
            if readings:
                print("\n=== SENSOR READINGS ===")
                for reading in readings:
                    print(f"Date: {reading['date']}")
                    print(f"  Temp: {reading['temperature']}°C, Humidity: {reading['humidity']}%")
                    print(f"  pH: {reading['ph_level']}, Light: {reading['light_level']} lux")
            else:
                print("No sensor readings available.")
                
        elif choice == '2':
            date = input("Enter date (YYYY-MM-DD): ")
            
            try:
                temp = float(input("Enter temperature (°C): "))
                humidity = float(input("Enter humidity (%): "))
                ph_level = float(input("Enter pH level: "))
                light_level = float(input("Enter light level (lux): "))
                
                reading = {
                    "date": date,
                    "temperature": temp,
                    "humidity": humidity,
                    "ph_level": ph_level,
                    "light_level": light_level
                }
                
                # Read existing data
                existing_readings = read_sensor_data()
                existing_readings.append(reading)
                
                # Save all data
                if save_daily_readings(existing_readings):
                    print("Sensor reading added successfully.")
                else:
                    print("Failed to add sensor reading.")
            except ValueError:
                print("Invalid input. Please enter numerical values.")
                
        elif choice == '3':
            nutrients = read_nutrient_levels()
            if nutrients:
                print("\n=== NUTRIENT LEVELS ===")
                for nutrient in nutrients:
                    print(f"Date: {nutrient['date']}")
                    print(f"  N: {nutrient['nitrogen']} ppm, P: {nutrient['phosphorus']} ppm, K: {nutrient['potassium']} ppm")
                    print(f"  EC Level: {nutrient['ec_level']}")
            else:
                print("No nutrient readings available.")
                
        elif choice == '4':
            date = input("Enter date (YYYY-MM-DD): ")
            
            try:
                nitrogen = float(input("Enter nitrogen level (ppm): "))
                phosphorus = float(input("Enter phosphorus level (ppm): "))
                potassium = float(input("Enter potassium level (ppm): "))
                ec_level = float(input("Enter EC level: "))
                
                reading = {
                    "date": date,
                    "nitrogen": nitrogen,
                    "phosphorus": phosphorus,
                    "potassium": potassium,
                    "ec_level": ec_level
                }
                
                if append_nutrient_reading(reading):
                    print("Nutrient reading added successfully.")
                else:
                    print("Failed to add nutrient reading.")
            except ValueError:
                print("Invalid input. Please enter numerical values.")
                
        elif choice == '5':
            recipe_name = input("Enter recipe name to update: ")
            print("Enter new instructions (one instruction per line, blank line to finish):")
            
            instructions = []
            while True:
                line = input()
                if not line:
                    break
                instructions.append(line)
            
            new_instructions = "\n".join(instructions)
            
            if update_recipe(recipe_name, new_instructions):
                print("Recipe updated successfully.")
            else:
                print("Failed to update recipe.")
                
        elif choice == '6':
            data_file = input("Enter path to sensor data file (default: sensor_readings.txt): ")
            if not data_file:
                data_file = "sensor_readings.txt"
                
            output_file = input("Enter path for report output (default: weekly_report.txt): ")
            if not output_file:
                output_file = "weekly_report.txt"
                
            if generate_weekly_report(data_file, output_file):
                print(f"Report generated successfully: {output_file}")
            else:
                print("Failed to generate report.")
                
        elif choice == '7':
            term = input("Enter search term: ")
            results = search_logs(term)
            
            if results:
                print("\n=== SEARCH RESULTS ===")
                for result in results:
                    print(f"{result['timestamp']} - {result['event_type']} - {result['message']}")
            else:
                print("No matching log entries found.")
                
        elif choice == '8':
            source = input("Enter source file path: ")
            backup = input("Enter backup file path: ")
            
            if backup_data_files(source, backup):
                print("Backup created successfully.")
            else:
                print("Failed to create backup.")
                
        elif choice == '0':
            print("Exiting program. Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()