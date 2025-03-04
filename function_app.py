from azure import functions as func

from functions.api_functions.timesheets.syncronize import bp as timesheets_bp
from functions.api_functions.customers.syncronize import bp as customers_bp
from functions.api_functions.employees.syncronize import bp as employees_bp
from functions.api_functions.projects.syncronize import bp as projects_bp
from functions.api_functions.suppliers.syncronize import bp as suppliers_bp
from functions.api_functions.ap_transactions.syncronize import bp as ap_transactions_bp
from functions.api_functions.ar_transactions.syncronize import bp as ar_transactions_bp
from functions.api_functions.transactions.syncronize import bp as transactions_bp

from functions.cleanup_functions.reset_state import bp as reset_state_bp
from functions.cleanup_functions.wipe_storage import bp as wipe_storage_bp
from functions.cleanup_functions.reset_state_and_wipe_storage import bp as reset_state_and_wipe_storage_bp
from functions.cleanup_functions.full_data_resync.full_data_resync import bp as full_data_resync_bp

from functions.flexlink_functions.employee_groups.get_employee_groups import bp as employee_groups_bp
from functions.flexlink_functions.employment_types.get_employment_types import bp as employment_types_bp
from functions.flexlink_functions.project_groups.get_project_groups import bp as project_groups_bp
from functions.flexlink_functions.financial_results.get_financial_results import bp as financial_results_bp
from functions.flexlink_functions.part_time_employees.get_part_time_employees import bp as part_time_employees


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

## Cleanup functions.
app.register_blueprint(reset_state_bp)
app.register_blueprint(wipe_storage_bp)
app.register_blueprint(reset_state_and_wipe_storage_bp)
app.register_blueprint(full_data_resync_bp)

# Flexlink functions.
<<<<<<< HEAD
# Uncommented functions currently not in use.
#app.register_blueprint(cost_categories_bp)
#app.register_blueprint(cost_centers_bp)
#app.register_blueprint(project_cost_setups_bp)
#app.register_blueprint(cost_element_per_time_type_bp)
#app.register_blueprint(project_managers_bp)
#app.register_blueprint(price_list_bp)
=======
>>>>>>> dev
app.register_blueprint(employee_groups_bp)
app.register_blueprint(employment_types_bp)
app.register_blueprint(project_groups_bp)
app.register_blueprint(financial_results_bp)
app.register_blueprint(part_time_employees)