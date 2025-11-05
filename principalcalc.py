import datetime

def get_user_input():
    """
    Prompts the user for investment details and returns them in a dictionary.
    Handles potential EOFError for non-interactive environments.
    """
    inputs = {}
    try:
        # Principal (mandatory, numeric > 0)
        while True:
            principal_str = input("Enter Principal amount: ").strip()
            if principal_str == "":
                print("Principal is required. Please enter an amount.")
                continue
            try:
                principal_val = float(principal_str)
                if principal_val <= 0:
                    print("Principal must be greater than 0. Please enter a valid amount.")
                    continue
                inputs['principal'] = principal_val
                break
            except ValueError:
                print("Invalid number. Please enter a numeric principal amount.")

        # Currency (mandatory)
        while True:
            currency = input("Enter Currency (e.g., USD): ").strip()
            if currency == "":
                print("Currency is required. Please enter a valid currency code (e.g., USD).")
                continue
            inputs['currency'] = currency.upper()
            break

        # Issuer name (mandatory)
        while True:
            issuer = input("Enter Issuer Name: ").strip()
            if issuer == "":
                print("Issuer Name is required. Please enter the issuer name.")
                continue
            inputs['issuer_name'] = issuer
            break

        # Lender name (mandatory)
        while True:
            lender = input("Enter Lender Name: ").strip()
            if lender == "":
                print("Lender Name is required. Please enter the lender name.")
                continue
            inputs['lender_name'] = lender
            break

        # Guarantor name (mandatory)
        while True:
            guarantor = input("Enter Guarantor Name: ").strip()
            if guarantor == "":
                print("Guarantor Name is required. Please enter the guarantor name.")
                continue
            inputs['guarantor_name'] = guarantor
            break

        # Advisor name (optional)
        inputs['advisor_name'] = input("(Optional) Enter Advisor Name: ").strip()

        # Tenor value (mandatory, numeric > 0)
        while True:
            tenor_str = input("Enter Investment Tenor value: ").strip()
            if tenor_str == "":
                print("Investment Tenor value is required. Please enter a value.")
                continue
            try:
                tenor_val = float(tenor_str)
                if tenor_val <= 0:
                    print("Tenor value must be greater than 0. Please enter a valid tenor value.")
                    continue
                inputs['tenor_value'] = tenor_val
                break
            except ValueError:
                print("Invalid number. Please enter a numeric tenor value.")

        # Tenor unit (required but validated)
        while True:
            tenor_unit = input("Enter Investment Tenor unit (days, months, years): ").strip().lower()
            if tenor_unit in ('days', 'months', 'years'):
                inputs['tenor_unit'] = tenor_unit
                break
            print("Please enter a valid tenor unit: 'days', 'months' or 'years'.")

        # Effective rate (numeric)
        while True:
            rate_str = input("Enter Effective Rate (e.g., 0.1 for 10%): ").strip()
            try:
                rate_val = float(rate_str)
                inputs['effective_rate'] = rate_val
                break
            except ValueError:
                print("Invalid rate. Please enter a numeric effective rate (e.g., 0.1 for 10%).")

        # Effective date
        while True:
            effective_date_str = input("Enter Effective Date (YYYY-MM-DD): ").strip()
            try:
                inputs['effective_date'] = datetime.datetime.strptime(effective_date_str, '%Y-%m-%d').date()
                break
            except ValueError:
                print("Invalid date format. Please enter date as YYYY-MM-DD.")

    except EOFError:
        print("\nInput closed; exiting.")
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
        tenor_in_years = tenor_value / 365  # Use 365.25 for leap year consideration

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
        
        def handle_rollovers(inputs, amount_due, maturity_date):
            """
            Interactive loop to roll the final amount into a new investment.
            The final `amount_due` becomes the new principal. The effective_date
            for the rollover is set to the previous maturity date. The user can
            choose to reuse the previous tenor or enter a new tenor.
            """
            principal = amount_due
            current_maturity = maturity_date
            rollover_count = 0

            while True:
                try:
                    choice = input("\nWould you like to calculate an investment rollover? (Yes/No): ").strip().lower()
                except EOFError:
                    print("\nInput closed; stopping rollovers.")
                    break

                if choice in ('n', 'no', ''):
                    break
                if choice not in ('y', 'yes'):
                    print("Please enter 'y' or 'n'.")
                    continue

                rollover_count += 1

                # Decide whether to reuse previous tenor or get a new validated tenor
                while True:
                    try:
                        reuse = input("Use previous tenor (value and unit)? (y/n): ").strip().lower()
                    except EOFError:
                        print("\nInput closed; stopping rollovers.")
                        reuse = 'n'
                        break

                    if reuse in ('y', 'yes'):
                        tenor_value = inputs['tenor_value']
                        tenor_unit = inputs['tenor_unit']
                        break
                    if reuse in ('n', 'no'):
                        # Prompt for tenor value (required, numeric > 0)
                        while True:
                            try:
                                tenor_str = input("Enter new tenor value: ").strip()
                            except EOFError:
                                print("\nInput closed; stopping rollovers.")
                                tenor_str = ''
                            if tenor_str == "":
                                print("Investment Tenor value is required. Please enter a value.")
                                continue
                            try:
                                tenor_value = float(tenor_str)
                                if tenor_value <= 0:
                                    print("Tenor value must be greater than 0. Please enter a valid tenor value.")
                                    continue
                                break
                            except ValueError:
                                print("Invalid number. Please enter a numeric tenor value.")

                        # Prompt for tenor unit (validated)
                        while True:
                            try:
                                tenor_unit = input("Enter tenor unit (days, months, years): ").strip().lower()
                            except EOFError:
                                print("\nInput closed; stopping rollovers.")
                                tenor_unit = ''
                            if tenor_unit in ('days', 'months', 'years'):
                                break
                            print("Please enter a valid tenor unit: 'days', 'months' or 'years'.")

                        break
                    print("Please enter 'y' or 'n'.")

                # Ask whether to reuse the previous effective rate or enter a new one (validated)
                while True:
                    try:
                        use_prev_rate = input("Use previous effective rate? (y/n): ").strip().lower()
                    except EOFError:
                        print("\nInput closed; stopping rollovers.")
                        use_prev_rate = 'n'
                        break

                    if use_prev_rate in ('y', 'yes'):
                        effective_rate = inputs['effective_rate']
                        break
                    if use_prev_rate in ('n', 'no'):
                        while True:
                            try:
                                rate_str = input("Enter new effective rate (e.g., 0.1 for 10%): ").strip()
                            except EOFError:
                                print("\nInput closed; stopping rollovers.")
                                rate_str = ''
                            if rate_str == "":
                                print("Effective rate is required. Please enter a numeric rate (e.g., 0.08).")
                                continue
                            try:
                                effective_rate = float(rate_str)
                                break
                            except ValueError:
                                print("Invalid rate. Please enter a numeric effective rate (e.g., 0.1 for 10%).")
                        break
                    print("Please enter 'y' or 'n'.")
                effective_date = current_maturity

                maturity_value, withholding_tax, amount_due, new_maturity = calculate_investment(
                    principal,
                    tenor_value,
                    tenor_unit,
                    effective_rate,
                    effective_date
                )

                rollover_inputs = {
                    'principal': principal,
                    'currency': inputs.get('currency', ''),
                    'issuer_name': inputs.get('issuer_name', ''),
                    'lender_name': inputs.get('lender_name', ''),
                    'guarantor_name': inputs.get('guarantor_name', ''),
                    'advisor_name': inputs.get('advisor_name', ''),
                    'tenor_value': tenor_value,
                    'tenor_unit': tenor_unit,
                    'effective_rate': effective_rate,
                    'effective_date': effective_date
                }

                print(f"\n--- Rollover #{rollover_count} ---")
                display_summary(rollover_inputs, maturity_value, withholding_tax, amount_due, new_maturity)

                # Prepare for potential next rollover
                principal = amount_due
                current_maturity = new_maturity

            print("\nNo rollover.")

        # Start interactive rollover loop (if user wants)
        handle_rollovers(investment_inputs, amount_due, maturity_date)