from azure import functions as func
from azure.identity import DefaultAzureCredential
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
@bp.route(route=f"trigger-{NAME}", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def manual_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual HTTP trigger to get financial results for specific periods.
    
    Request Body:
    {
        "invoice_number": int
    }
    """
    credential = DefaultAzureCredential()
    config = EnvironmentConfig()
    
    req_body = req.get_json()
    invoice_number = req_body.get("invoice_number")
    
    if not invoice_number:
        return func.HttpResponse("The 'invoice_number' parameter is required.", status_code=400)

    invoice_link = get_invoice_link_pdf(config, invoice_number)
    
    return func.HttpResponse(
        "",
        status_code=302,  # Redirect
        headers={"Location": invoice_link}
    )        
    
def get_invoice_link_pdf(config: EnvironmentConfig, invoice_number: int) -> str:
    graphql_client = GraphQLClient(config.api_endpoint, config.api_key)
    variables = {"invoiceNumber": invoice_number}
    response = graphql_client.execute_graphql_query(GET_INVOICE_PDF, variables)
    return response["data"]["arTransactions"]["edges"][0]["node"]["invoiceFile"]["url"]

