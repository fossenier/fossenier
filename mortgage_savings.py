import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
house_A = 179000
house_B = 480000
annual_interest_rate = 0.04
loan_term_years = 25   # assume 25-year amortization
sell_after_years = 8

# --- Helper functions ---
def monthly_payment(principal, annual_rate, years):
    """Calculate the fixed monthly mortgage payment."""
    r = annual_rate / 12
    n = years * 12
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

def simulate_interest_over_time(principal, annual_rate, years, sell_after):
    """Simulate mortgage payments until sale, returning cumulative interest timeline."""
    r = annual_rate / 12
    n = years * 12
    payment = monthly_payment(principal, annual_rate, years)

    remaining_principal = principal
    total_interest_paid = 0

    months = sell_after * 12
    interest_over_time = []

    for _ in range(months):
        interest_payment = remaining_principal * r
        principal_payment = payment - interest_payment
        total_interest_paid += interest_payment
        remaining_principal -= principal_payment

        interest_over_time.append(total_interest_paid)

    return interest_over_time, total_interest_paid

# --- Simulation ---
interest_over_time_A, final_interest_A = simulate_interest_over_time(house_A, annual_interest_rate, loan_term_years, sell_after_years)
interest_over_time_B, final_interest_B = simulate_interest_over_time(house_B, annual_interest_rate, loan_term_years, sell_after_years)

savings = final_interest_B - final_interest_A

# --- Plot over time ---
months = np.arange(1, sell_after_years * 12 + 1)
plt.figure(figsize=(12, 7))
plt.plot(months, interest_over_time_A, label=f"House A ($179k) - Final: ${final_interest_A:,.0f}", color="green")
plt.plot(months, interest_over_time_B, label=f"House B ($480k) - Final: ${final_interest_B:,.0f}", color="red")

# Labels and grid
plt.title("Cumulative Interest Paid Over 8 Years (4% Mortgage Rate)")
plt.xlabel("Months")
plt.ylabel("Cumulative Interest Paid ($)")
plt.legend(loc="upper left")
plt.grid(True, linestyle="--", alpha=0.6)

# Overlay text box with summary
textstr = (f"House A Interest: ${final_interest_A:,.0f}\n"
           f"House B Interest: ${final_interest_B:,.0f}\n"
           f"Savings Choosing A: ${savings:,.0f}")

plt.gca().text(0.65, 0.25, textstr, transform=plt.gca().transAxes,
               fontsize=11, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

plt.show()