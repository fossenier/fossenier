import pandas as pd

# load the csv
df = pd.read_csv("rooms_square_footage.csv")

# calculate totals per floor
floor_totals = df.groupby("level")["area_sqft"].sum().reset_index()

# nicer floor labels
floor_names = {
    "M": "Main Floor",
    "2": "Second Floor",
    "3": "Third Floor",
    "B": "Basement"
}

floor_totals["level"] = floor_totals["level"].map(fcodeloor_names)

print("\nSquare Footage per Floor:\n")
print(floor_totals.to_string(index=False))

print("\nTotal Square Footage (rooms only):")
print(round(df["area_sqft"].sum(), 2), "sqft")