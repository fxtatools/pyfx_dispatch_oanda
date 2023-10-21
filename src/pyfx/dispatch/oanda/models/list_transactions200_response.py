"""ListTransactions200Response model definition for OANDA v20 REST API (3.0.25)"""

from typing import Annotated, Optional

from .response_mixins import LastTransactionResponse
from ..transport.transport_fields import TransportField

from .transaction_filter import TransactionFilter
from .common_types import Time


class ListTransactions200Response(LastTransactionResponse):
    """
    listTransactions200Response
    """

    var_from: Annotated[Optional[Time], TransportField(None, alias="from")]
    """
    The starting time provided in the request.
    """

    to: Annotated[Optional[Time], TransportField(None)]
    """
    The ending time provided in the request.
    """

    page_size: Annotated[Optional[int], TransportField(None, alias="pageSize")]
    """
    The pageSize provided in the request
    """

    type: Annotated[Optional[list[TransactionFilter]], TransportField(None)]
    """
    The Transaction-type filter provided in the request
    """

    count: Annotated[int, TransportField(...)]
    """
    The number of Transactions that are contained in the pages returned
    """

    pages: Annotated[Optional[list[str]], TransportField(None)]
    """
    The list of URLs that represent idrange queries providing the data for each page in the query results
    """


__all__ = ("ListTransactions200Response",)
