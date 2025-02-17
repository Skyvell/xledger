from shared.utils.time import (
    get_previous_month_yy_mm, 
    generate_periods
)

# Start and end period to fectch financial results from.
# The default end-period is current_month - 1.
FINANCIAL_RESULTS_START_PERIOD = 2401
FINANCIAL_RESULTS_END_PERIOD = get_previous_month_yy_mm()

# Generated periods based on start and end period.
FINANCIAL_RESULTS_PERIODS = generate_periods(FINANCIAL_RESULTS_START_PERIOD, FINANCIAL_RESULTS_END_PERIOD)a