
"""model definition for OANDA v20 REST API (3.0.25)"""


from enum import Enum





from ..transport.data import ApiObject
from ..transport.transport_fields import TransportField
from ..util import exporting



class FundingReason(str, Enum):
    """
    The reason that an Account is being funded.
    """

    """
    allowed enum values
    """
    CLIENT_FUNDING = 'CLIENT_FUNDING'
    ACCOUNT_TRANSFER = 'ACCOUNT_TRANSFER'
    DIVISION_MIGRATION = 'DIVISION_MIGRATION'
    SITE_MIGRATION = 'SITE_MIGRATION'
    ADJUSTMENT = 'ADJUSTMENT'



__all__ = exporting(__name__, ...)

