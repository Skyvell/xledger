
from azure import functions as func
from functions.timesheets.syncronize import bp as timesheets_bp
from functions.customers.syncronize import bp as customers_bp
from functions.employees.syncronize import bp as employees_bp
from functions.projects.syncronize import bp as projects_bp
from functions.suppliers.syncronize import bp as suppliers_bp
from functions.ap_transactions.syncronize import bp as ap_transactions_bp
from functions.ar_transactions.syncronize import bp as ar_transactions_bp
from functions.transactions.syncronize import bp as transactions_bp
from functions.cleanup.reset_state import bp as reset_state_bp
from functions.cleanup.wipe_storage import bp as wipe_storage_bp
from functions.report.get_report_data import bp as report_bp


# Create the function app.
app = func.FunctionApp()

# Register all the functions here for the app.
app.register_blueprint(timesheets_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(suppliers_bp)
app.register_blueprint(ap_transactions_bp)
app.register_blueprint(ar_transactions_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(reset_state_bp)
app.register_blueprint(wipe_storage_bp)
app.register_blueprint(report_bp)