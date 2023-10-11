
"""model definition for OANDA v20 REST API (3.0.25)"""

from pandas import Timestamp
from typing import Optional

from ..transport import ApiObject, TransportField
from ..util import exporting


from .transaction_filter import TransactionFilter
from .transaction import TransactionId


class ListTransactions200Response(ApiObject):
    """
    listTransactions200Response
    """
    var_from: Optional[Timestamp] = TransportField(None, alias="from")
    """
    The starting time provided in the request.
    """
    to: Optional[Timestamp] = TransportField(None)
    """
    The ending time provided in the request.
    """
    page_size: Optional[int] = TransportField(None, alias="pageSize")
    """
    The pageSize provided in the request
    """
    type: Optional[list[TransactionFilter]] = TransportField(None)
    """
    The Transaction-type filter provided in the request
    """
    count: Optional[int] = TransportField(None)
    """
    The number of Transactions that are contained in the pages returned
    """
    pages: Optional[list[str]] = TransportField(None)
    """
    The list of URLs that represent idrange queries providing the data for each page in the query results
    """
    last_transaction_id: Optional[TransactionId] = TransportField(None, alias="lastTransactionID")
    """
    The ID of the most recent Transaction created for the Account
    """


__all__ = exporting(__name__, ...)
