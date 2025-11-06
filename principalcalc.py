import datetime
import calendar
from typing import Tuple, Dict, Optional


def get_user_input() -> Optional[Dict]:
    """Collect and normalize user input for an investment calculation."""
    try:
        principal_str = input("Enter Principal amount: ").strip()
        principal = float(principal_str)
        if principal <= 0:
            print("Principal must be greater than 0.")
            return None
    except (ValueError, EOFError):
        print("Invalid principal input; exiting.")
        return None

    currency = input("Enter Currency (e.g., USD): ").strip().upper()
    issuer = input("Enter Issuer Name: ").strip()
    lender = input("Enter Lender Name: ").strip()
    guarantor = input("Enter Guarantor Name: ").strip()
    advisor = input("(Optional) Enter Advisor Name: ").strip()

    try:
        tenor_value = float(input("Enter Investment Tenor value: ").strip())
        tenor_unit = input("Enter Investment Tenor unit (days, months, years): ").strip().lower()
        if tenor_unit not in ("days", "months", "years"):
            print("Invalid tenor unit; expected days, months, or years.")
            return None
    except (ValueError, EOFError):
        print("Invalid tenor input; exiting.")
        return None

    # Accept either 8 or 0.08 for 8%: normalize to percent value (8.0)
    try:
        rate_input = float(input("Enter Effective Rate (e.g., 8 for 8% or 0.08 for 8%): ").strip())
        rate_percent = rate_input * 100.0 if rate_input <= 1 else rate_input
    except (ValueError, EOFError):
        print("Invalid rate input; exiting.")
        return None

    try:
        eff_str = input("Enter Effective Date (YYYY-MM-DD): ").strip()
        effective_date = datetime.datetime.strptime(eff_str, "%Y-%m-%d").date()
    except (ValueError, EOFError):
        print("Invalid effective date; exiting.")
        return None

    return {
        "principal": principal,
        "currency": currency,
        "issuer_name": issuer,
        "lender_name": lender,
        "guarantor_name": guarantor,
        "advisor_name": advisor,
        "tenor_value": tenor_value,
        "tenor_unit": tenor_unit,
        "rate_percent": rate_percent,
        "effective_date": effective_date,
    }


def add_years_safe(d: datetime.date, years: float) -> datetime.date:
    years_i = int(years)
    new_year = d.year + years_i
    last_day = calendar.monthrange(new_year, d.month)[1]
    new_day = min(d.day, last_day)
    return datetime.date(new_year, d.month, new_day)


def add_months_safe(d: datetime.date, months: float) -> datetime.date:
    months_i = int(months)
    total = (d.month - 1) + months_i
    new_year = d.year + total // 12
    new_month = (total % 12) + 1
    last_day = calendar.monthrange(new_year, new_month)[1]
    new_day = min(d.day, last_day)
    return datetime.date(new_year, new_month, new_day)


def add_days_safe(d: datetime.date, days: float) -> datetime.date:
    return d + datetime.timedelta(days=int(days))


def compute_maturity_date(effective_date: datetime.date, tenor_value: float, tenor_unit: str) -> datetime.date:
    """Return the maturity date by adding tenor to effective_date."""
    if tenor_unit == "years":
        return add_years_safe(effective_date, tenor_value)
    if tenor_unit == "months":
        return add_months_safe(effective_date, tenor_value)
    return add_days_safe(effective_date, tenor_value)


def compute_yearly_interest(principal: float, rate_percent: float) -> float:
    """Interest = Principal * (Rate / 100). Rate passed as percent (e.g., 8.0)."""
    return principal * (rate_percent / 100.0)


def compute_day_length(start: datetime.date, end: datetime.date) -> int:
    """Inclusive day count: (end - start) + 1."""
    return (end - start).days + 1


def days_in_year(year: int) -> int:
    return 366 if calendar.isleap(year) else 365


def compute_year_fraction(start: datetime.date, end: datetime.date) -> float:
    """Compute exact year fraction using actual/actual: sum over calendar years the fraction of days in that year.

    This accurately accounts for leap years.
    """
    if start > end:
        return 0.0
    total_fraction = 0.0
    for year in range(start.year, end.year + 1):
        year_start = datetime.date(year, 1, 1)
        year_end = datetime.date(year, 12, 31)
        overlap_start = max(start, year_start)
        overlap_end = min(end, year_end)
        if overlap_start <= overlap_end:
            overlap_days = (overlap_end - overlap_start).days + 1
            total_fraction += overlap_days / days_in_year(year)
    return total_fraction


def compute_total_interest_due(principal: float, rate_percent: float, start: datetime.date, end: datetime.date) -> Tuple[float, float]:
    """Return (total_interest_due, year_fraction).

    Total interest due is computed as YearlyInterest * year_fraction where yearly interest = principal*(rate/100).
    """
    yearly_interest = compute_yearly_interest(principal, rate_percent)
    year_frac = compute_year_fraction(start, end)
    total_interest = yearly_interest * year_frac
    return total_interest, year_frac


def compute_withholding_tax(total_interest: float) -> float:
    return total_interest * 0.10


def compute_net_interest(total_interest: float) -> float:
    return total_interest * 0.90


def compute_net_maturity(principal: float, total_interest: float) -> float:
    return principal + total_interest


def display_summary(data: Dict, start: datetime.date, end: datetime.date, year_frac: float, yearly_interest: float, total_interest: float, wht: float, net_interest: float, net_maturity: float) -> None:
    print("\n--- Investment Summary ---")
    print(f"Principal Amount: {data['currency']} {data['principal']:.2f}")
    print(f"Issuer Name: {data['issuer_name']}")
    print(f"Lender Name: {data['lender_name']}")
    print(f"Guarantor Name: {data['guarantor_name']}")
    print(f"Advisor Name: {data['advisor_name']}")
    print(f"Effective Date: {start.strftime('%Y-%m-%d')}")
    print(f"Maturity Date: {end.strftime('%Y-%m-%d')}")
    print(f"Day Length (inclusive): {compute_day_length(start, end)} days")
    print(f"Year Fraction (actual/actual): {year_frac:.8f}")
    print(f"Annual (YoY) Interest: {data['currency']} {yearly_interest:.2f}")
    print(f"Total Interest Due: {data['currency']} {total_interest:.2f}")
    print(f"Withholding Tax (10%): {data['currency']} {wht:.2f}")
    print(f"Net Interest Due (90%): {data['currency']} {net_interest:.2f}")
    print(f"Net Maturity (Principal + Total Interest): {data['currency']} {net_maturity:.2f}")


def handle_rollovers(data: Dict, principal: float, effective_date: datetime.date) -> None:
    current_principal = principal
    current_effective = effective_date
    count = 0
    while True:
        try:
            ans = input("\nWould you like to calculate an investment rollover? (Yes/No): ").strip().lower()
        except EOFError:
            break
        if ans in ('n', 'no', ''):
            break
        if ans not in ('y', 'yes'):
            print("Please answer y or n.")
            continue

        count += 1
        use_prev_tenor = input("Use previous tenor (value and unit)? (y/n): ").strip().lower() in ('y', 'yes')
        if use_prev_tenor:
            tenor_value = data['tenor_value']
            tenor_unit = data['tenor_unit']
        else:
            try:
                tenor_value = float(input("Enter new tenor value: ").strip())
            except (ValueError, EOFError):
                print("Invalid tenor value; aborting rollover.")
                break
            tenor_unit = input("Enter tenor unit (days, months, years): ").strip().lower()

        use_prev_rate = input("Use previous effective rate? (y/n): ").strip().lower() in ('y', 'yes')
        if use_prev_rate:
            rate_percent = data['rate_percent']
        else:
            try:
                inp = float(input("Enter new effective rate (e.g., 8 for 8% or 0.08 for 8%): ").strip())
            except (ValueError, EOFError):
                print("Invalid rate; aborting rollover.")
                break
            rate_percent = inp * 100.0 if inp <= 1 else inp

        new_maturity = compute_maturity_date(current_effective, tenor_value, tenor_unit)
        total_interest, year_frac = compute_total_interest_due(current_principal, rate_percent, current_effective, new_maturity)
        wht = compute_withholding_tax(total_interest)
        net_interest = compute_net_interest(total_interest)
        net_maturity = compute_net_maturity(current_principal, total_interest)

        print(f"\n--- Rollover #{count} ---")
        display_summary(data, current_effective, new_maturity, year_frac, compute_yearly_interest(current_principal, rate_percent), total_interest, wht, net_interest, net_maturity)

        current_principal = net_maturity
        current_effective = new_maturity


if __name__ == "__main__":
    user_data = get_user_input()
    if not user_data:
        exit(1)

    principal = user_data['principal']
    tenor_value = user_data['tenor_value']
    tenor_unit = user_data['tenor_unit']
    rate_percent = user_data['rate_percent']
    effective_date = user_data['effective_date']

    maturity_date = compute_maturity_date(effective_date, tenor_value, tenor_unit)

    yearly_interest = compute_yearly_interest(principal, rate_percent)
    total_interest, year_frac = compute_total_interest_due(principal, rate_percent, effective_date, maturity_date)
    wht = compute_withholding_tax(total_interest)
    net_interest = compute_net_interest(total_interest)
    net_maturity = compute_net_maturity(principal, total_interest)

    display_summary(user_data, effective_date, maturity_date, year_frac, yearly_interest, total_interest, wht, net_interest, net_maturity)

    handle_rollovers(user_data, principal, maturity_date)