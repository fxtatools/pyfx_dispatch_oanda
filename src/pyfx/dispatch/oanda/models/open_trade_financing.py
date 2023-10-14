
"""model definition for OANDA v20 REST API (3.0.25)"""


from typing import Annotated, Optional


from ..transport import ApiObject, TransportField
from ..util import exporting


class OpenTradeFinancing(ApiObject):
    """
    OpenTradeFinancing is used to pay/collect daily financing charge for an open Trade within an Account
    """
    trade_id: Annotated[Optional[str], TransportField(None, alias="tradeID")]
    """
    The ID of the Trade that financing is being paid/collected for.
    """
    financing: Annotated[Optional[str], TransportField(None)]
    """
    The amount of financing paid/collected for the Trade.
    """


__all__ = exporting(__name__, ...)
