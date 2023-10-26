"""
This file will perform a nine step calculation for the force of tension in my M3 lab. (It is not elegant! very brute force!)
"""

import math


def round_to_sig_figs(x, n):
    if x == 0:
        return "0"
    elif abs(x) < 1:
        exponent = -int(math.floor(math.log10(abs(x))))
        x *= 10**exponent
        rounded_x = round(x, n - 1)
        rounded_x /= 10**exponent
        format_str = "{:." + str(exponent + n - 1) + "f}"
        return format_str.format(rounded_x)
    else:
        exponent = int(math.floor(math.log10(abs(x))))
        rounded_x = round(x / (10**exponent), n - 1) * (10**exponent)
        if exponent >= n - 1:
            return str(int(rounded_x))
        else:
            format_str = "{:." + str(n - 1 - exponent) + "f}"
            return format_str.format(rounded_x)


def round_to_same_decimal_places(reference_str, number_to_round):
    num_decimals = len(reference_str.split(".")[1]) if "." in reference_str else 0
    return round(number_to_round, num_decimals)


def main():
    # 1
    grams = float(input("Enter mass of grams: "))
    uncertainty = float(input("Enter uncertainty in grams: "))

    # 2
    m = grams / 1000
    dm = uncertainty / 1000

    # 3
    g = 9.811

    # 4
    f = m * g

    # 5, 6, 7
    df = dm / m * f
    df_rounded_str = round_to_sig_figs(df, 2)  # Rounded df to 2 significant figures

    # 8, 9
    f_rounded = round_to_same_decimal_places(
        df_rounded_str, f
    )  # Rounded f to the same number of decimal places as df

    print(f"df rounded to 2 significant figures: {df_rounded_str}")
    print(f"f rounded to the same number of decimal places as df: {f_rounded}")


if __name__ == "__main__":
    main()
