import datetime

def calculate_maturity_value(principal: float, effective_rate: float, tenor_years: float) -> tuple[float, float, float]:
    """
    Calculates the maturity value, withholding tax, and final amount due
    based on simple interest.

    Args:
        principal (float): The initial investment amount.
        effective_rate (float): The annual simple interest rate (e.g., 0.05 for 5%).
        tenor_years (float): The investment period in years.

    Returns:
        tuple[float, float, float]: A tuple containing the maturity value,
                                    withholding tax, and final amount due.
    """
    # Calculate maturity value using the simple interest formula
    maturity_value = principal * (1 + effective_rate * tenor_years)

    # Calculate the 10% withholding tax
    withholding_tax = maturity_value * 0.10

    # Calculate the final amount due after tax
    amount_due = maturity_value - withholding_tax

    return maturity_value, withholding_tax, amount_due

def get_user_input(prompt: str, type_cast: callable = str):
    """
    Gets user input and handles potential ValueError for numeric inputs
    and EOFError for non-interactive environments.
    """
    while True:
        try:
            user_input = input(prompt)
            # Check for empty input and continue the loop if found
            if not user_input.strip():
                print("Input cannot be empty. Please try again.")
                continue
            return type_cast(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except EOFError:
            print("\nError: End of input stream reached. The script requires interactive input.")
            return None

if __name__ == "__main__":
    print("--- Investment Calculation Script ---")

    # Get all the required inputs from the user
    try:
        principal = get_user_input("Enter Principal amount: ", float)
        issuer_name = input("Enter Issuer Name: ")
        lender_name = input("Enter Lender Name: ")
        guarantor_name = input("Enter Guarantor Name: ")
        advisor_name = input("Enter Advisor Name: ")
        investment_tenor = get_user_input("Enter Investment Tenor (in years): ", float)
        effective_date_str = input("Enter Effective Date (YYYY-MM-DD): ")
        maturity_date_str = input("Enter Maturity Date (YYYY-MM-DD): ")
        effective_rate = get_user_input("Enter Effective Rate (e.g., 0.10 for 10%): ", float)
    except EOFError as e:
        print(f"\nAn error occurred: {e}. The script requires interactive input and could not find it.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred during input: {e}")
        exit()

    # Check if any input failed before continuing
    if any(var is None for var in [principal, investment_tenor, effective_rate]):
        print("Script terminated due to missing required input.")
        exit()

    # Perform the calculation
    maturity_value, withholding_tax, amount_due = calculate_maturity_value(
        principal, effective_rate, investment_tenor
    )

    # Format currency values for a clean display
    currency_format = "{:,.2f}"

    # Print the summary of investment details
    print("\n--- Investment Details Summary ---")
    print(f"Principal Amount: {currency_format.format(principal)}")
    print(f"Issuer Name: {issuer_name}")
    print(f"Lender Name: {lender_name}")
    print(f"Guarantor Name: {guarantor_name}")
    print(f"Advisor Name: {advisor_name}")
    print(f"Investment Tenor: {investment_tenor} years")
    print(f"Effective Date: {effective_date_str}")
    print(f"Maturity Date: {maturity_date_str}")
    print(f"Effective Rate: {effective_rate * 100:.2f}%")
    print("-" * 30)

    # Print the final calculated values
    print(f"Calculated Maturity Value: {currency_format.format(maturity_value)}")
    print(f"10% Withholding tax in the sum of {currency_format.format(withholding_tax)} which sall be deducted from the Maturity Value")
    print(f"Final Amount Due: {currency_format.format(amount_due)}")
    print("-" * 30)
    print("Thank you for using the Investment Calculation Script!")