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
from functions.cleanup.reset_state_and_wipe_storage import bp as reset_state_and_wipe_storage_bp
from functions.report.get_report_data import bp as report_bp
from functions.cost_categories.get_cost_categories import bp as cost_categories_bp
from functions.cost_element_per_time_type.get_cost_element_per_time_type import bp as cost_element_per_time_type_bp
from functions.project_cost_setups.get_project_cost_setups import bp as project_cost_setups_bp
from functions.project_managers.get_project_managers import bp as project_managers_bp
from functions.price_list.get_price_list import bp as price_list_bp
from functions.cost_centers.get_cost_centers import bp as cost_centers_bp
from functions.employee_groups.get_employee_groups import bp as employee_groups_bp
from functions.employment_types.get_employment_types import bp as employment_types_bp


# Create the function app.
app = func.FunctionApp()

# Register all the functions below here for the app.

# API Syncronization functions.
app.register_blueprint(timesheets_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(suppliers_bp)
app.register_blueprint(ap_transactions_bp)
app.register_blueprint(ar_transactions_bp)
app.register_blueprint(transactions_bp)

# Cleanup functions.
app.register_blueprint(reset_state_bp)
app.register_blueprint(wipe_storage_bp)
app.register_blueprint(reset_state_and_wipe_storage_bp)

# Flexlink functions.
# Uncommented functions currently not in use.
# app.register_blueprint(report_bp)
# app.register_blueprint(cost_categories_bp)
# app.register_blueprint(cost_centers_bp)
# app.register_blueprint(project_cost_setups_bp)
# app.register_blueprint(cost_element_per_time_type_bp)
# app.register_blueprint(project_managers_bp)
# app.register_blueprint(price_list_bp)
app.register_blueprint(employee_groups_bp)
app.register_blueprint(employment_types_bp)