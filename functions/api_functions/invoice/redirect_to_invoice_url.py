from azure import functions as func
import logging

from shared.gql_client import GraphQLClient
from shared.environment_config import EnvironmentConfig

from functions.api_functions.invoice.queries import (
    GET_INVOICE_PDF
)

NAME = "invoice"
logging.basicConfig(level=logging.INFO)
bp = func.Blueprint()

@bp.function_name(f"get_{NAME}_link_pdf")
@bp.route(route=f"trigger-{NAME}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def manual_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual HTTP trigger to get financial results for specific periods.

    Request Query Parameters:
    ?invoice_number=<int>
    """
    config = EnvironmentConfig()
    
    invoice_number = req.params.get("invoice_number")

    if not invoice_number:
        return func.HttpResponse("The 'invoice_number' parameter is required.", status_code=400)

    try:
        invoice_number = int(invoice_number)  # Ensure it's an integer
    except ValueError:
        return func.HttpResponse("Invalid 'invoice_number' format. Must be an integer.", status_code=400)

    invoice_link = get_invoice_link_pdf(config, invoice_number)
    
    return func.HttpResponse(
        "",
        status_code=302,  # Redirect
        headers={"Location": invoice_link}
    )        

def get_invoice_link_pdf(config: EnvironmentConfig, invoice_number: int) -> str:
    graphql_client = GraphQLClient(config.api_endpoint, config.api_key)
    variables = {"invoiceNumber": str(invoice_number)}
    response = graphql_client.execute_graphql_query(GET_INVOICE_PDF, variables)
    
    edges = response.get("data", {}).get("arTransactions", {}).get("edges", [])
    if not edges:
        raise ValueError(f"No invoice found for invoice number {invoice_number}")

    return edges[0]["node"]["invoiceFile"]["url"]
