import numpy as np
import matplotlib.pyplot as plt

# Mortgage parameters
house_cost = 207000  # Total cost of the house
down_payment = 13000  # Down payment
principal = house_cost - down_payment  # Loan principal after down payment
annual_interest_rate = 0.02  # Annual interest rate (2%)
monthly_payment = 866  # Total monthly payment
semi_monthly_payment = monthly_payment / 2  # Payment made twice a month
loan_term_years = 24  # Loan term in years
num_payments = loan_term_years * 12 * 2  # Total semi-monthly payments

# Convert annual interest rate to semi-monthly rate
semi_monthly_interest_rate = (1 + annual_interest_rate) ** (1 / 24) - 1

# Simulation variables
remaining_principal_no_extra = principal  # without extra payment
remaining_principal_with_extra = (
    principal - 10000
)  # with $10,000 extra payment at start
total_interest_paid_no_extra = 0
total_interest_paid_with_extra = 0
equity_no_extra = down_payment
equity_with_extra = down_payment + 10000

# Lists to store values for each payment period
interest_paid_over_time_no_extra = []
principal_over_time_no_extra = []
equity_over_time_no_extra = []

interest_paid_over_time_with_extra = []
principal_over_time_with_extra = []
equity_over_time_with_extra = []

# Perform the simulation for each semi-monthly payment
for i in range(num_payments):
    # Calculate for scenario without extra payment
    interest_payment_no_extra = (
        remaining_principal_no_extra * semi_monthly_interest_rate
    )
    principal_payment_no_extra = semi_monthly_payment - interest_payment_no_extra
    total_interest_paid_no_extra += interest_payment_no_extra
    remaining_principal_no_extra -= principal_payment_no_extra
    equity_no_extra = house_cost - remaining_principal_no_extra

    # Ensure principal doesn't go negative in case of rounding issues at the end
    if remaining_principal_no_extra < 0:
        remaining_principal_no_extra = 0

    # Store values for no extra payment scenario
    interest_paid_over_time_no_extra.append(total_interest_paid_no_extra)
    principal_over_time_no_extra.append(remaining_principal_no_extra)
    equity_over_time_no_extra.append(equity_no_extra)

    # Calculate for scenario with $10,000 extra payment
    interest_payment_with_extra = (
        remaining_principal_with_extra * semi_monthly_interest_rate
    )
    principal_payment_with_extra = semi_monthly_payment - interest_payment_with_extra
    total_interest_paid_with_extra += interest_payment_with_extra
    remaining_principal_with_extra -= principal_payment_with_extra
    equity_with_extra = house_cost - remaining_principal_with_extra

    # Ensure principal doesn't go negative in case of rounding issues at the end
    if remaining_principal_with_extra < 0:
        remaining_principal_with_extra = 0

    # Store values for extra payment scenario
    interest_paid_over_time_with_extra.append(total_interest_paid_with_extra)
    principal_over_time_with_extra.append(remaining_principal_with_extra)
    equity_over_time_with_extra.append(equity_with_extra)

# Plotting
plt.figure(figsize=(14, 8))
time = np.arange(0, num_payments)

# Plot for no extra payment scenario
plt.plot(
    time,
    interest_paid_over_time_no_extra,
    label="Total Interest Paid (No Extra Payment)",
    color="red",
    linestyle="--",
)
plt.plot(
    time,
    principal_over_time_no_extra,
    label="Remaining Principal (No Extra Payment)",
    color="blue",
)
plt.plot(
    time,
    equity_over_time_no_extra,
    label="Home Equity (No Extra Payment)",
    color="green",
)

# Plot for extra payment scenario
plt.plot(
    time,
    interest_paid_over_time_with_extra,
    label="Total Interest Paid (With $10,000 Extra)",
    color="orange",
    linestyle="--",
)
plt.plot(
    time,
    principal_over_time_with_extra,
    label="Remaining Principal (With $10,000 Extra)",
    color="purple",
)
plt.plot(
    time,
    equity_over_time_with_extra,
    label="Home Equity (With $10,000 Extra)",
    color="teal",
)

# Add labels at start, middle, and end of each line
mid_index = len(time) // 2
end_index = len(time) - 1

# No extra payment scenario labels
plt.text(
    0,
    interest_paid_over_time_no_extra[0],
    f"${interest_paid_over_time_no_extra[0]:,.0f}",
    color="red",
)
plt.text(
    mid_index,
    interest_paid_over_time_no_extra[mid_index],
    f"${interest_paid_over_time_no_extra[mid_index]:,.0f}",
    color="red",
)
plt.text(
    end_index,
    interest_paid_over_time_no_extra[end_index],
    f"${interest_paid_over_time_no_extra[end_index]:,.0f}",
    color="red",
)

plt.text(
    0,
    principal_over_time_no_extra[0],
    f"${principal_over_time_no_extra[0]:,.0f}",
    color="blue",
)
plt.text(
    mid_index,
    principal_over_time_no_extra[mid_index],
    f"${principal_over_time_no_extra[mid_index]:,.0f}",
    color="blue",
)
plt.text(
    end_index,
    principal_over_time_no_extra[end_index],
    f"${principal_over_time_no_extra[end_index]:,.0f}",
    color="blue",
)

plt.text(
    0,
    equity_over_time_no_extra[0],
    f"${equity_over_time_no_extra[0]:,.0f}",
    color="green",
)
plt.text(
    mid_index,
    equity_over_time_no_extra[mid_index],
    f"${equity_over_time_no_extra[mid_index]:,.0f}",
    color="green",
)
plt.text(
    end_index,
    equity_over_time_no_extra[end_index],
    f"${equity_over_time_no_extra[end_index]:,.0f}",
    color="green",
)

# Extra payment scenario labels
plt.text(
    0,
    interest_paid_over_time_with_extra[0],
    f"${interest_paid_over_time_with_extra[0]:,.0f}",
    color="orange",
)
plt.text(
    mid_index,
    interest_paid_over_time_with_extra[mid_index],
    f"${interest_paid_over_time_with_extra[mid_index]:,.0f}",
    color="orange",
)
plt.text(
    end_index,
    interest_paid_over_time_with_extra[end_index],
    f"${interest_paid_over_time_with_extra[end_index]:,.0f}",
    color="orange",
)

plt.text(
    0,
    principal_over_time_with_extra[0],
    f"${principal_over_time_with_extra[0]:,.0f}",
    color="purple",
)
plt.text(
    mid_index,
    principal_over_time_with_extra[mid_index],
    f"${principal_over_time_with_extra[mid_index]:,.0f}",
    color="purple",
)
plt.text(
    end_index,
    principal_over_time_with_extra[end_index],
    f"${principal_over_time_with_extra[end_index]:,.0f}",
    color="purple",
)

plt.text(
    0,
    equity_over_time_with_extra[0],
    f"${equity_over_time_with_extra[0]:,.0f}",
    color="teal",
)
plt.text(
    mid_index,
    equity_over_time_with_extra[mid_index],
    f"${equity_over_time_with_extra[mid_index]:,.0f}",
    color="teal",
)
plt.text(
    end_index,
    equity_over_time_with_extra[end_index],
    f"${equity_over_time_with_extra[end_index]:,.0f}",
    color="teal",
)

# Adding titles and labels
plt.title(
    "Mortgage Simulation Over 5 Years (2% Interest Rate) - With and Without Extra Payment"
)
plt.xlabel("Semi-Monthly Payments")
plt.ylabel("Amount in Dollars")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()
