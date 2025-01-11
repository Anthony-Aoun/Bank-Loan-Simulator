import os
from matplotlib import pyplot as plt

def mensuality(cost, rate, nb_years):
    """
    Calculate the monthly payment (mensuality) for a loan.

    Parameters:
    - cost: Total loan amount (in euros).
    - rate: Annual interest rate (in percentage).
    - nb_years: Loan duration (in years).

    Returns:
    - Monthly payment amount (rounded to integer).
    """
    rate = rate / 12  # Convert annual rate to monthly.
    rate = rate / 100  # Convert percentage to decimal.
    n = nb_years * 12  # Total number of months.

    # Monthly payment formula (amortization formula).
    m = (cost * rate * (1 + rate)**n) / ((1 + rate)**n - 1)
    return int(m)

def describePlan(cost, downpayment_rate, notary_rate, rate, nb_years):
    """
    Calculate and describe the financial plan for a property purchase.

    Parameters:
    - cost: Property cost (in euros).
    - downpayment_rate: Downpayment rate (in percentage).
    - notary_rate: Notary fees rate (in percentage).
    - rate: Annual interest rate (in percentage).
    - nb_years: Loan duration (in years).

    Returns:
    - Tuple containing:
        - Monthly payment amount.
        - Monthly borrowed amount.
        - Monthly interest amount.
        - Total payment amount.
        - Downpayment amount.
        - Total borrowed amount.
        - Total interest amount.
    """
    # Calculate notary fees and downpayment.
    notary_fees = (notary_rate / 100) * cost
    downpayment_fees = (downpayment_rate / 100) * cost

    # Calculate the total borrowed amount (property cost minus downpayment plus notary fees).
    total_borrowed = (1 - downpayment_rate / 100) * cost + notary_fees

    # Calculate monthly payment.
    mensuality_pay = mensuality(total_borrowed, rate, nb_years)

    # Calculate total payment and total interest.
    total_pay = nb_years * 12 * mensuality_pay + downpayment_fees
    total_interest = total_pay - cost - notary_fees

    # Break down monthly payment into borrowed and interest components.
    monthly_borrowed = total_borrowed / (nb_years * 12)
    monthly_interest = mensuality_pay - monthly_borrowed

    return mensuality_pay, monthly_borrowed, monthly_interest, total_pay, downpayment_fees, total_borrowed, total_interest

def plotDescription(monthly_borrowed, monthly_interest, downpayment_fees, total_borrowed, total_interest, darkTheme=True):
    """
    Generate pie charts visualizing the monthly and total costs.

    Parameters:
    - monthly_borrowed: Monthly borrowed amount.
    - monthly_interest: Monthly interest amount.
    - downpayment_fees: Downpayment amount.
    - total_borrowed: Total borrowed amount.
    - total_interest: Total interest amount.
    - darkTheme: Boolean to enable/disable dark theme.
    """
    fig = plt.figure(figsize=(10, 3))

    # Apply dark theme if enabled.
    if darkTheme:
        fig.patch.set_facecolor('black')
        plt.rcParams['text.color'] = 'white'

    # Create subplots for monthly and total costs.
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # Labels and values for pie charts.
    labels1 = ['Borrowed', 'Interests']
    labels2 = ['Down Payment', 'Borrowed', 'Interests']
    values1 = [monthly_borrowed, monthly_interest]
    values2 = [downpayment_fees, total_borrowed, total_interest]

    # Colors for pie charts.
    colors1 = ['#0000ff', '#1e90ff']
    colors2 = ['#4b0082', '#9400d3', '#ba55d3']

    # Create pie charts.
    ax1.pie(values1, wedgeprops=dict(width=0.3), colors=colors1, labels=labels1, autopct='%1.0f%%', startangle=90, pctdistance=0.85)
    ax2.pie(values2, wedgeprops=dict(width=0.3), colors=colors2, labels=labels2, autopct='%1.0f%%', startangle=90, pctdistance=0.85)

    # Set titles and legends.
    ax1.set_title(f"{int(monthly_borrowed + monthly_interest):,} € per Month", pad=12)
    ax2.set_title(f"{int(downpayment_fees + total_borrowed + total_interest):,} € in Total", pad=12)
    ax1.legend([f"{int(monthly_borrowed):,} €", f"{int(monthly_interest):,} €"], loc='best', fancybox=True, framealpha=0)
    ax2.legend([f"{int(downpayment_fees):,} €", f"{int(total_borrowed):,} €", f"{int(total_interest):,} €"], loc='best', fancybox=True, framealpha=0)

    # Equal aspect ratio for pie charts.
    ax1.axis('equal')
    ax2.axis('equal')
    plt.tight_layout()

    # Save and display the plot.
    my_path = os.path.dirname(__file__)
    plt.savefig(os.path.join(my_path, 'RealEstate.png'))
    plt.show()

if __name__ == "__main__":
    # Collect input data from the user.
    print("\nINPUT DATA")
    print("----------")
    cost = float(input("> Enter property's cost (in €): "))
    downpayment_rate = float(input("> Enter downpayment rate (in %): "))
    notary_rate = float(input("> Enter notary fees rate (in %): "))
    rate = float(input("> Enter yearly rate (in %): "))
    nb_years = int(input("> Enter number of years: "))

    # Calculate the financial plan.
    mensuality_pay, monthly_borrowed, monthly_interest, total_pay, downpayment_fees, total_borrowed, total_interest = describePlan(cost, downpayment_rate, notary_rate, rate, nb_years)

    # Display the results.
    print("\nRESULTS")
    print("-------")
    print(f"Monthly pay = {int(mensuality_pay):,} €")
    print(f"Monthly borrowed (property + notary) = {int(monthly_borrowed):,} €")
    print(f"Monthly interest = {int(monthly_interest):,} €")
    print(f"Total pay = {int(total_pay):,} €")
    print(f"Down Payment = {int(downpayment_fees):,} €")
    print(f"Total borrowed (property + notary) = {int(total_borrowed):,} €")
    print(f"Total interest = {int(total_interest):,} €")

    # Suggest an annual salary based on monthly payment.
    print(f"\nAnnual salary before tax should be at least {int(mensuality_pay * 3 * 12 / 0.7):,} €")

    # Plot the financial plan description.
    plotDescription(monthly_borrowed, monthly_interest, downpayment_fees, total_borrowed, total_interest)
