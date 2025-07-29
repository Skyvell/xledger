from datetime import timedelta

SYNC_ALERT_THRESHOLDS_BY_FUNCTION = {
    "ap_transactions": timedelta(days=3),
    "ar_transactions": timedelta(days=3),
    "customers": timedelta(days=7),
    "employees": timedelta(days=7),
    "projects": timedelta(days=7),
    "suppliers": timedelta(days=7),
    "timesheets": timedelta(days=3),
    "transactions": timedelta(days=3),
}