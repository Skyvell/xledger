class Incvoice:
    def __init__(
        self, 
        invoice_id: int, 
        invoice_date: str,
        due_data: str,
        invoice_amount: float,
        remaining_amount: float,
        currency: str,
        company_name: str,
        company_phone_number: str,
        company_email: str,
        company_address: str,
    ) -> None:
        self.invoice_id = invoice_id
        self.invoice_date = invoice_date
        self.due_data = due_data
        self.invoice_amount = invoice_amount
        self.remaining_amount = remaining_amount
        self.currency = currency
        self.company_name = company_name
        self.company_phone_number = company_phone_number
        self.company_email = company_email
        self.company_address = company_address

    def pdf(self) -> None:
        raise NotImplementedError("This method is not implemented yet.")