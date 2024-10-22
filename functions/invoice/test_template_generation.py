from jinja2 import Environment, FileSystemLoader

# Mock data
invoice_data = {
    "invoice_id": 1234,
    "invoice_date": "2024-10-10",
    "company_name": "Data Ductus",
    "company_address": "1234 Street Name",
    "company_location": "City, Country",
    "client_name": "Client Company",
    "due_date": "2024-11-10",
    "items": [
        {"description": "Web Development Services", "quantity": 10, "unit_price": 100.00, "total": 1000.00},
        {"description": "Consultation", "quantity": 5, "unit_price": 50.00, "total": 250.00}
    ],
    "subtotal": 1250.00,
    "remaining_amount": 500.00,
    "contact_email": "info@dataductus.com"
}

# Load the template
file_loader = FileSystemLoader('./')  # Folder where the template is stored
env = Environment(loader=file_loader)
template = env.get_template('invoice.html')

# Render the template with the data
output = template.render(invoice_data)

# Save the output to an HTML file
with open("invoice_generated.html", "w") as file:
    file.write(output)

print("Invoice generated: invoice_generated.html")