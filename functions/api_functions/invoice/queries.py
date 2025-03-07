from gql import gql


GET_INVOICE_PDF = gql("""
query get_invoice_pdf($invoiceNumber: String!) {
  arTransactions(first: 1, ownerSet: "MINE",  filter: { invoiceNumber: $invoiceNumber }) {
    edges {
      node {
        invoiceFile {
          url
        }
      }
    }
  }
}
""")