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
    ) -> None:
        self.invoice_id = invoice_id
        self.invoice_date = invoice_date
        self.due_data = due_data
        self.invoice_amount = invoice_amount
        self.remaining_amount = remaining_amount
        self.currency = currency
        self.company_name = company_name

    def pdf(self) -> None:
        raise NotImplementedError("This method is not implemented yet.")
    
    