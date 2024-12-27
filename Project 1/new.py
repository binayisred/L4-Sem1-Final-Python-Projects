import sys
from tabulate import tabulate

def read_driver_details(filename):
    """Read driver details from a file."""
    drivers = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                car_number, code, name, team = parts
                drivers[code] = {
                    "car_number": int(car_number),
                    "name": name,
                    "team": team,
                }
    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        exit(1)  # Exit if the file is missing
    return drivers

def read_lap_times(filenames):
    """Read lap times from multiple files."""
    race_names = []
    lap_data = {}
    for filename in filenames:
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                race_name = lines[0].strip()  # First line is the race name
                race_names.append(race_name)
                for line in lines[1:]:
                    code = line[:3]
                    time = float(line[3:])
                    if code not in lap_data:
                        lap_data[code] = []
                    lap_data[code].append(time)
        except FileNotFoundError:
            print(f"Error: File {filename} not found!")
            exit(1)  # Exit if a lap time file is missing
    return race_names, lap_data

def merge_driver_and_lap_data(drivers, lap_data):
    """Merge driver details with lap times."""
    for code, times in lap_data.items():
        if code in drivers:
            drivers[code]["lap_times"] = times
        else:
            drivers[code] = {"name": "Unknown", "team": "Unknown", "car_number": None, "lap_times": times}
    return drivers

def calculate_fastest_laps(drivers):
    """Calculate the fastest lap for each driver."""
    fastest_laps = {}
    for code, driver in drivers.items():
        if "lap_times" in driver:
            fastest_laps[code] = min(driver["lap_times"])  # Get the minimum lap time (fastest)
    return fastest_laps

def calculate_average_laps(drivers):
    """Calculate the average lap time for each driver."""
    averages = {}
    for code, driver in drivers.items():
        if "lap_times" in driver:
            avg_time = sum(driver["lap_times"]) / len(driver["lap_times"])
            averages[code] = avg_time
    return averages

def calculate_overall_average(lap_data):
    """Calculate the overall average lap time across all drivers."""
    total_time = 0
    total_laps = 0
    for times in lap_data.values():
        total_time += sum(times)
        total_laps += len(times)
    return total_time / total_laps if total_laps > 0 else 0

def display_sorted_fastest_times(fastest_laps, drivers):
    """Display the fastest laps sorted in descending order."""
    sorted_laps = sorted(fastest_laps.items(), key=lambda x: x[1])
    print("Sorted Fastest Lap Times (from fastest to slowest):")
    table_data = []
    for code, time in sorted_laps:
        driver = drivers[code]
        table_data.append([code, driver["name"], driver["team"], driver["car_number"], time])
    print(tabulate(table_data, headers=["Code", "Name", "Team", "Car Number", "Fastest Lap Time"]))
    print("-" * 40)

def display_results(race_name, drivers, fastest_laps, averages, overall_avg):
    """Display the results for a given race."""
    print(f"Results for {race_name}:")
    table_data = []
    for code, driver in drivers.items():
        name = driver["name"]
        team = driver["team"]
        car_number = driver["car_number"]
        fastest_lap = fastest_laps.get(code, "N/A")
        average_lap = averages.get(code, "N/A")
        table_data.append([name, car_number, team, fastest_lap, average_lap])
    
    # Display results in a table format
    print(tabulate(table_data, headers=["Driver", "Car Number", "Team", "Fastest Lap Time", "Average Lap Time"]))
    print(f"Overall Average Lap Time: {overall_avg:.3f}")
    print("-" * 40)

def main():
    # Get command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python script.py <driver_file> <lap_time_file1> [<lap_time_file2> ...]")
        exit(1)
    
    driver_file = sys.argv[1]
    lap_time_files = sys.argv[2:]
    
    # Step 1: Read data from files
    drivers = read_driver_details(driver_file)
    race_names, lap_data = read_lap_times(lap_time_files)
    
    # Step 2: Merge data
    drivers = merge_driver_and_lap_data(drivers, lap_data)
    
    # Step 3: Calculate stats
    fastest_laps = calculate_fastest_laps(drivers)
    averages = calculate_average_laps(drivers)
    overall_avg = calculate_overall_average(lap_data)
    
    # Step 4: Display sorted fastest laps
    display_sorted_fastest_times(fastest_laps, drivers)
    
    # Step 5: Display final results
    print(f"Races: {', '.join(race_names)}")
    display_results(race_names[-1], drivers, fastest_laps, averages, overall_avg)

# Main execution
if __name__ == "__main__":
    main()