## Constants for the FxTrade v20 API

from pyfx.dispatch.oanda.mapped_enum import MappedEnum
from typing import TYPE_CHECKING

class FxLabel(str, MappedEnum):
    if TYPE_CHECKING:
        name: str
        value: str

    NONE = ""
    #
    # component columns
    #
    ASK = "ask"
    BID = "bid"
    MID = "mid"
    OPEN = "o"
    HIGH = "h"
    LOW = "l"
    CLOSE = "c"
    #
    # component-generic columns
    #
    TIME = "time"
    VOLUME = "volume"
    PERIOD = "period"
    # NPTIME = "nptime" # np.timestamp64 index (unused)
    UTIME = "utime" # np.timestamp64 index truncated to np.uint64
    #
    # price models
    #
    MEDIAN = "mean" ## median (mean) price
    TYPICAL = "typical" ## HLC mean price
    WEIGHTED = "weighted" ## HLCC mean price
    SMOOTHED = "smoothed" ## uncommon, FIR-smoothed price


class FxCol(tuple[str, str], MappedEnum):
    # column schema names for fxpy v20 dataframes
    #
    # theoretically for convenience. Pandas tends to copy
    # any strings when constructing names for a multindex

    if TYPE_CHECKING:
        name: str
        value: tuple[str, str]

    ASK_OPEN = (FxLabel.ASK.value, FxLabel.OPEN.value)
    ASK_HIGH = (FxLabel.ASK.value, FxLabel.HIGH.value)
    ASK_LOW = (FxLabel.ASK.value, FxLabel.LOW.value)
    ASK_CLOSE = (FxLabel.ASK.value, FxLabel.CLOSE.value)
    ASK_TYPICAL = (FxLabel.ASK.value, FxLabel.TYPICAL.value)

    BID_OPEN = (FxLabel.BID.value, FxLabel.OPEN.value)
    BID_HIGH = (FxLabel.BID.value, FxLabel.HIGH.value)
    BID_LOW = (FxLabel.BID.value, FxLabel.LOW.value)
    BID_CLOSE = (FxLabel.BID.value, FxLabel.CLOSE.value)
    BID_TYPICAL = (FxLabel.BID.value, FxLabel.TYPICAL.value)

    MID_OPEN = (FxLabel.MID.value, FxLabel.OPEN.value)
    MID_HIGH = (FxLabel.MID.value, FxLabel.HIGH.value)
    MID_LOW = (FxLabel.MID.value, FxLabel.LOW.value)
    MID_CLOSE = (FxLabel.MID.value, FxLabel.CLOSE.value)
    MID_TYPICAL = (FxLabel.MID.value, FxLabel.TYPICAL.value)

    VOLUME = (FxLabel.VOLUME.value, FxLabel.NONE.value)
    TIME = (FxLabel.TIME.value, FxLabel.NONE.value) # FIXME remove, use named index
    PERIOD = (FxLabel.PERIOD.value, FxLabel.NONE.value)
    UTIME = (FxLabel.UTIME.value, FxLabel.NONE.value)
