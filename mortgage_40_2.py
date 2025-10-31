import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
years = 40
start_income = 40000 + 45000  # couple's first year combined
annual_raise = 2000  # household raise per year

# Mortgage terms
rate = 0.04  # annual interest rate
amort_years = 25  # amortization period

# Single house purchase (expensive house only)
house_price = 500000
house_year = 1

# --- Helper function to compute monthly payment ---
def monthly_payment(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

# --- Simulation storage ---
money_pool = []
interest_paid_cumulative = []
total_mortgage_outlay = []

# --- State variables ---
income = start_income
pool = 0
cumulative_interest = 0
cumulative_outlay = 0

# Active mortgage trackers
mortgage_balance = 0
mortgage_payment = 0
active_mortgage = False

# --- Simulation loop ---
for year in range(1, years + 1):
    # Add annual income
    pool += income

    # If year 1: buy house
    if year == house_year:
        down = 0.10 * house_price
        pool -= down
        mortgage_balance = house_price - down
        mortgage_payment = monthly_payment(mortgage_balance, rate, amort_years) * 12
        active_mortgage = True
        cumulative_outlay += down

    # Mortgage active: pay for this year
    if active_mortgage and mortgage_balance > 0:
        # Split payment into interest + principal
        r = rate / 12
        interest_year = 0
        principal_year = 0
        for m in range(12):
            interest_m = mortgage_balance * r
            principal_m = mortgage_payment / 12 - interest_m
            mortgage_balance -= principal_m
            interest_year += interest_m
            principal_year += principal_m
        pool -= (interest_year + principal_year)
        cumulative_interest += interest_year
        cumulative_outlay += (interest_year + principal_year)

    # Track values
    money_pool.append(pool)
    interest_paid_cumulative.append(cumulative_interest)
    total_mortgage_outlay.append(cumulative_outlay)

    # Raise income for next year
    income += annual_raise

# --- Plotting ---
plt.figure(figsize=(12, 7))
plt.plot(range(1, years + 1), money_pool, label="Money Pool", color="green")
plt.plot(range(1, years + 1), interest_paid_cumulative, label="Bank Interest Pocketed", color="red")
plt.plot(range(1, years + 1), total_mortgage_outlay, label="Total Mortgage Outlay", color="blue")

plt.axvline(house_year, color="gray", linestyle="--", alpha=0.5)
plt.text(house_year, max(money_pool)*0.05, "Buy $500k", rotation=90, va="bottom")

plt.title("40-Year Mortgage & Income Simulation (Only Expensive House)")
plt.xlabel("Year")
plt.ylabel("Dollars")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()