import datetime

def get_user_input():
    """
    Prompts the user for investment details and returns them in a dictionary.
    Handles potential EOFError for non-interactive environments.
    """
    inputs = {}
    try:
        inputs['principal'] = float(input("Enter Principal amount: "))
        inputs['currency'] = input("Enter Currency (e.g., USD): ").upper()
        inputs['issuer_name'] = input("Enter Issuer Name: ")
        inputs['lender_name'] = input("Enter Lender Name: ")
        inputs['guarantor_name'] = input("Enter Guarantor Name: ")
        inputs['advisor_name'] = input("Enter Advisor Name: ")
        inputs['tenor_value'] = float(input("Enter Investment Tenor value: "))
        inputs['tenor_unit'] = input("Enter Investment Tenor unit (days, months, years): ").lower()
        inputs['effective_rate'] = float(input("Enter Effective Rate (e.g., 0.1 for 10%): "))
        
        effective_date_str = input("Enter Effective Date (YYYY-MM-DD): ")
        inputs['effective_date'] = datetime.datetime.strptime(effective_date_str, '%Y-%m-%d').date()

    except (ValueError, EOFError) as e:
        print(f"An error occurred during input: {e}")
        return None
    
    return inputs

def calculate_investment(principal, tenor_value, tenor_unit, effective_rate, effective_date):
    """
    Calculates the maturity value, withholding tax, and final amount due.
    
    Args:
        principal (float): The initial investment amount.
        tenor_value (float): The duration of the investment.
        tenor_unit (str): The unit of the duration (days, months, or years).
        effective_rate (float): The simple interest rate per year.
        effective_date (datetime.date): The start date of the investment.
    
    Returns:
        tuple: A tuple containing the maturity value, withholding tax, final amount due, and maturity date.
    """
    # Calculate maturity date
    maturity_date = effective_date
    if tenor_unit == 'years':
        maturity_date = effective_date.replace(year=effective_date.year + int(tenor_value))
    elif tenor_unit == 'months':
        total_months = effective_date.month + int(tenor_value)
        year_change = total_months // 12
        month_change = total_months % 12
        maturity_date = effective_date.replace(year=effective_date.year + year_change, month=month_change)
    elif tenor_unit == 'days':
        maturity_date = effective_date + datetime.timedelta(days=tenor_value)
    
    # Convert tenor to years for the simple interest formula
    tenor_in_years = 0
    if tenor_unit == 'years':
        tenor_in_years = tenor_value
    elif tenor_unit == 'months':
        tenor_in_years = tenor_value / 12
    elif tenor_unit == 'days':
        tenor_in_years = tenor_value / 365.25  # Use 365.25 for leap year consideration

    # Calculate final maturity value
    maturity_value = principal * (1 + effective_rate * tenor_in_years)
    
    # Calculate withholding tax from the interest generated
    interest_generated = maturity_value - principal
    withholding_tax = interest_generated * 0.10
    
    # Calculate final amount due
    amount_due = maturity_value - withholding_tax

    return maturity_value, withholding_tax, amount_due, maturity_date

def display_summary(inputs, maturity_value, withholding_tax, amount_due, maturity_date):
    """
    Prints a summary of the investment details and calculations.
    
    Args:
        inputs (dict): A dictionary containing all user inputs.
        maturity_value (float): The calculated final maturity value.
        withholding_tax (float): The calculated withholding tax.
        amount_due (float): The calculated final amount due.
        maturity_date (datetime.date): The calculated maturity date.
    """
    print("\n--- Investment Summary ---")
    print(f"Principal Amount: {inputs['currency']} {inputs['principal']:.2f}")
    print(f"Issuer Name: {inputs['issuer_name']}")
    print(f"Lender Name: {inputs['lender_name']}")
    print(f"Guarantor Name: {inputs['guarantor_name']}")
    print(f"Advisor Name: {inputs['advisor_name']}")
    print(f"Investment Tenor: {inputs['tenor_value']} {inputs['tenor_unit']}")
    print(f"Effective Date: {inputs['effective_date'].strftime('%Y-%m-%d')}")
    print(f"Maturity Date: {maturity_date.strftime('%Y-%m-%d')}")
    print(f"Effective Rate: {inputs['effective_rate'] * 100:.2f}%")
    print("-" * 25)
    print(f"Calculated Maturity Value: {inputs['currency']} {maturity_value:.2f}")
    print(f"Withholding Tax (10% on interest): {inputs['currency']} {withholding_tax:.2f}")
    print(f"Final Amount Due: {inputs['currency']} {amount_due:.2f}")

if __name__ == "__main__":
    investment_inputs = get_user_input()
    
    if investment_inputs:
        maturity_value, withholding_tax, amount_due, maturity_date = calculate_investment(
            investment_inputs['principal'],
            investment_inputs['tenor_value'],
            investment_inputs['tenor_unit'],
            investment_inputs['effective_rate'],
            investment_inputs['effective_date']
        )
        
        display_summary(investment_inputs, maturity_value, withholding_tax, amount_due, maturity_date)
