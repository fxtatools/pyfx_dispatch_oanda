## Constants for the FxTrade v20 API

from pyfx.dispatch.oanda.mapped_enum import MappedEnum
from typing import TYPE_CHECKING

class FxLabel(str, MappedEnum):
    if TYPE_CHECKING:
        value: str

    NONE = ""
    #
    # common component columns
    #
    ASK = "ask"
    BID = "bid"
    MID = "mid"
    OPEN = "o"
    HIGH = "h"
    LOW = "l"
    CLOSE = "c"
    #
    # common component-generic columns
    #
    TIME = "time"
    VOLUME = "volume"


class FxCol(tuple[str, str], MappedEnum):
    # column schema names for fxpy v20 dataframes
    #
    # theoretically for convenience. Pandas tends to copy
    # any strings when constructing names for a multindex

    if TYPE_CHECKING:
        value: tuple[str, str]

    ASK_OPEN = (FxLabel.ASK.value, FxLabel.OPEN.value)
    ASK_HIGH = (FxLabel.ASK.value, FxLabel.HIGH.value)
    ASK_LOW = (FxLabel.ASK.value, FxLabel.LOW.value)
    ASK_CLOSE = (FxLabel.ASK.value, FxLabel.CLOSE.value)

    BID_OPEN = (FxLabel.BID.value, FxLabel.OPEN.value)
    BID_HIGH = (FxLabel.BID.value, FxLabel.HIGH.value)
    BID_LOW = (FxLabel.BID.value, FxLabel.LOW.value)
    BID_CLOSE = (FxLabel.BID.value, FxLabel.CLOSE.value)

    MID_OPEN = (FxLabel.MID.value, FxLabel.OPEN.value)
    MID_HIGH = (FxLabel.MID.value, FxLabel.HIGH.value)
    MID_LOW = (FxLabel.MID.value, FxLabel.LOW.value)
    MID_CLOSE = (FxLabel.MID.value, FxLabel.CLOSE.value)

    VOLUME = (FxLabel.VOLUME.value, FxLabel.NONE.value)
    TIME = (FxLabel.TIME.value, FxLabel.NONE.value)
    # ^ FIXME only used in the quotes static_merge_subset() prototype
    # ^ using named index otherwise
