from tabulate import tabulate

data = [["Alice", 24, "Engineer"], ["Bob", 27, "Artist"], ["Charlie", 22, "Doctor"]]
headers = ["Name", "Age", "Occupation"]

# Display data as a table
print(tabulate(data, headers=headers, tablefmt="pretty"))
