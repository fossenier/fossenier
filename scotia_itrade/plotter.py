import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file
data = pd.read_csv("fund_facts.csv")

# List to hold annual performance data for plotting
annual_data = []

# Process each row in the data
for index, row in data.iterrows():
    name = row["name"]
    code = row["code"]
    mer = row["mer"]

    # Extract performance data and adjust for MER
    performance = row[4:] - mer

    # Get the years where performance data is available
    years = performance.index[performance.notnull()].astype(int)

    # Add to annual data list if the fund has at least 3 years of data
    if len(years) >= 3:
        annual_data.append(
            {
                "name": name,
                "code": code,
                "performance": performance,
                "years": sorted(years),
            }
        )

# Calculate average annual performance (CAGR) for each fund
for fund in annual_data:
    start_year = fund["years"][0]
    end_year = fund["years"][-1]
    num_years = end_year - start_year
    start_value = 100  # Assume an initial value of 100
    end_value = start_value * (
        1 + fund["performance"][str(start_year)] / 100
    )  # Adjust start value by first year performance

    for year in fund["years"][1:]:
        end_value *= 1 + fund["performance"][str(year)] / 100

    fund["cagr"] = ((end_value / start_value) ** (1 / num_years) - 1) * 100

# Sort funds by CAGR and select top 20
plot_data = sorted(annual_data, key=lambda x: x["cagr"], reverse=True)[:20]

# Plot the performance data
fig, ax = plt.subplots(figsize=(14, 8))

# Prepare labels for the additional box
labels = []
for fund in plot_data:
    label = f"{fund['name']} ({fund['code']}) - {len(fund['years'])} years"
    ax.plot(
        fund["years"],
        [fund["performance"][str(year)] for year in fund["years"]],
        label=label,
    )
    labels.append(f"{fund['name']} ({fund['code']}): {fund['cagr']:.2f}%")

# Place the additional box with average annual performance
props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
textstr = "\n".join(labels)

# Manually adjust the position of the box
plt.gcf().text(0.70, 0.05, textstr, fontsize=9, bbox=props)  # Adjusted position

ax.set_xlabel("Year")
ax.set_ylabel("Annual Performance (%)")
ax.set_title("Fund Annual Performance Adjusted for MER")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize="small")
plt.tight_layout()
plt.show()
