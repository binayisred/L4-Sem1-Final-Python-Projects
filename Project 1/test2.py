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

def get_top_fastest_drivers(fastest_laps, top_n=3):
    """Get the top N fastest drivers based on their fastest lap times."""
    sorted_drivers = sorted(fastest_laps.items(), key=lambda x: x[1])  # Sort by fastest lap time
    return sorted_drivers[:top_n]

def display_unique_data(drivers):
    """Display unique data for each driver."""
    print("Unique Driver Data:")
    for code, driver in drivers.items():
        if "lap_times" in driver:
            total_laps = len(driver["lap_times"])
            slowest_lap = max(driver["lap_times"])
            print(f"Driver: {driver['name']} (Car Number: {driver['car_number']}) - Team: {driver['team']}")
            print(f"Total Laps Completed: {total_laps}")
            print(f"Slowest Lap Time: {slowest_lap}")
            print("-" * 40)

def display_results(race_name, drivers, fastest_laps, averages):
    """Display the results for a given race."""
    print(f"Results for {race_name}:")
    for code, driver in drivers.items():
        name = driver["name"]
        team = driver["team"]
        car_number = driver["car_number"]
        fastest_lap = fastest_laps.get(code, "N/A")
        average_lap = averages.get(code, "N/A")
        
        print(f"Driver: {name} (Car Number: {car_number}) - Team: {team}")
        print(f"Fastest Lap Time: {fastest_lap}")
        print(f"Average Lap Time: {average_lap}")
        print("-" * 40)

def display_top_fastest_drivers(drivers, top_fastest):
    """Display the top fastest drivers."""
    print("Top 3 Fastest Drivers:")
    for rank, (code, lap_time) in enumerate(top_fastest, 1):
        driver = drivers[code]
        print(f"{rank}. Driver: {driver['name']} (Car Number: {driver['car_number']}) - Team: {driver['team']}")
        print(f"Fastest Lap Time: {lap_time}")
        print("-" * 40)


# Function to format and print results (using basic clean layout)
def print_results_basic(title, results):
    print(f"\n=== {title} ===")
    for result in results:
        print("----------------------------------------")
        for key, value in result.items():
            print(f"{key}: {value}")
    print("----------------------------------------")

# Modify the display_results function to use the print_results_basic function
def display_results(race_name, drivers, fastest_laps, averages):
    """Display the results for a given race in a clean format."""
    results = []
    for code, driver in drivers.items():
        name = driver["name"]
        team = driver["team"]
        car_number = driver["car_number"]
        fastest_lap = fastest_laps.get(code, "N/A")
        average_lap = averages.get(code, "N/A")

        results.append({
            "Driver": name,
            "Car Number": car_number,
            "Team": team,
            "Fastest Lap Time": fastest_lap,
            "Average Lap Time": average_lap
        })
    
    print_results_basic(f"Results for {race_name}", results)

# Modify the display_top_fastest_drivers function to use the print_results_basic function
def display_top_fastest_drivers(drivers, top_fastest):
    """Display the top fastest drivers in a clean format."""
    results = []
    for rank, (code, lap_time) in enumerate(top_fastest, 1):
        driver = drivers[code]
        results.append({
            "Rank": rank,
            "Driver": driver['name'],
            "Car Number": driver['car_number'],
            "Team": driver['team'],
            "Fastest Lap Time": lap_time
        })
    
    print_results_basic("Top 3 Fastest Drivers", results)

# You can keep the rest of your code as is. 
# Make sure to call `display_results` and `display_top_fastest_drivers` in the main function.


def main():
    # File paths
    driver_file = r"C:\Users\Binay Ghimire\OneDrive - iTechno\Documents\TBC'\Level 4\Fundamentals of Computer Programming\Project_Work\Project 1\f1_drivers.txt"  # Full path to the driver file
    lap_time_files = [
        r"C:\Users\Binay Ghimire\OneDrive - iTechno\Documents\TBC'\Level 4\Fundamentals of Computer Programming\Project_Work\Project 1\lap_times_1.txt",  # Full path to lap time file 1
        r"C:\Users\Binay Ghimire\OneDrive - iTechno\Documents\TBC'\Level 4\Fundamentals of Computer Programming\Project_Work\Project 1\lap_times_2.txt",  # Full path to lap time file 2
        r"C:\Users\Binay Ghimire\OneDrive - iTechno\Documents\TBC'\Level 4\Fundamentals of Computer Programming\Project_Work\Project 1\lap_times_3.txt"   # Full path to lap time file 3
    ]
    
    # Step 1: Read data from files
    drivers = read_driver_details(driver_file)
    race_names, lap_data = read_lap_times(lap_time_files)
    
    # Step 2: Merge data
    drivers = merge_driver_and_lap_data(drivers, lap_data)
    
    # Step 3: Calculate stats
    fastest_laps = calculate_fastest_laps(drivers)
    averages = calculate_average_laps(drivers)
    
    # Step 4: Display results
    print(f"Races: {', '.join(race_names)}")
    display_results(race_names[-1], drivers, fastest_laps, averages)  # Show stats for the last race
    
    # Step 5: Get and display top 3 fastest drivers
    top_fastest = get_top_fastest_drivers(fastest_laps, top_n=3)
    display_top_fastest_drivers(drivers, top_fastest)
    
    # Step 6: Display unique data like slowest lap and total laps
    display_unique_data(drivers)

# Main execution
if __name__ == "__main__":
    main()




