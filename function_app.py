
from azure import functions as func
from functions.timesheets.syncronize import bp as timesheets_bp
from functions.customers.syncronize_customers import bp as customers_bp
from functions.employees.syncronize import bp as employees_bp
from functions.projects.syncronize import bp as projects_bp
from functions.suppliers.syncronize import bp as suppliers_bp
from functions.ap_transactions.syncronize_ap_transactions import bp as ap_transactions_bp
from functions.ar_transactions.syncronize import bp as ar_transactions_bp
from functions.transactions.syncronize import bp as transactions_bp


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