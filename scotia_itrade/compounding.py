import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV
data = pd.read_csv("data2.csv")


# Function to simulate the investment return considering MER and calculating annualized returns
def simulate_investment(row):
    initial_investment = 1000
    current_value = initial_investment
    years_active = 0
    for year in range(
        2023, 2013, -1
    ):  # Adjust based on the earliest year in your dataset
        year_value = row[str(year)]
        if pd.notna(year_value) and year_value != "-":
            try:
                year_return = float(year_value)
                years_active += 1
                # Apply the annual return and subtract the MER
                current_value *= 1 + (year_return - row["MER"]) / 100
            except ValueError:
                print(f"Skipping non-numeric data for {year}: {year_value}")

    # Calculate annualized return if there are any active years
    if years_active > 0:
        annualized_return = (current_value / initial_investment) ** (
            1 / years_active
        ) - 1
    else:
        annualized_return = 0  # Default to 0 if no years active

    return current_value, years_active, annualized_return * 100  # Return percentage


# Apply the simulation to the data
data["Final Value"], data["Years Active"], data["Annualized Return"] = zip(
    *data.apply(simulate_investment, axis=1)
)

# Plot the results with the number of years active
plt.figure(figsize=(12, 8))
data.sort_values("Annualized Return", inplace=True)
bars = plt.barh(data["Fund Code"], data["Annualized Return"], color="skyblue")

# Annotate each bar with the number of years active
for bar, years in zip(bars, data["Years Active"]):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {years} yrs",
        va="center",
        ha="left",
        color="black",
        fontsize=10,
    )

plt.xlabel("Annualized Return (%)")
plt.ylabel("Fund Code")
plt.title("Annualized Return Comparison of Portfolios with Active Years")
plt.show()
