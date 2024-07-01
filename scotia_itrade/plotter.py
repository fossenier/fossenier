import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
csv_file_path = "path_to_your_csv_file.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path)

# Parameters for simulation
initial_investment = 1000  # Initial investment amount in dollars
mer = 0.02  # Management Expense Ratio (MER) in decimal form


# Function to simulate portfolio through time for a specific fund
def simulate_portfolio(data, initial_investment, mer):
    portfolio_value = [initial_investment]
    for year in data:
        growth_rate = data[year] / 100
        new_value = portfolio_value[-1] * (1 + growth_rate) * (1 - mer)
        portfolio_value.append(new_value)
    return portfolio_value[1:]


# Simulate portfolio for each fund
for fund in df["Fund name"].unique():
    fund_data = df[df["Fund name"] == fund].iloc[0]
    years = df.columns[3:]  # Year columns start from the fourth column
    growth_data = fund_data[years].astype(float).to_dict()
    portfolio_values = simulate_portfolio(growth_data, initial_investment, mer)

    # Plot the portfolio value over time
    plt.figure(figsize=(10, 6))
    plt.plot(years, portfolio_values, marker="o", linestyle="-", label=fund)
    plt.title(f"Portfolio Value Over Time for {fund}")
    plt.xlabel("Year")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True)
    plt.show()
