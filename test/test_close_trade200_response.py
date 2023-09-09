# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25
    Contact: api@oanda.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.close_trade200_response import CloseTrade200Response  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestCloseTrade200Response(unittest.TestCase):
    """CloseTrade200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CloseTrade200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CloseTrade200Response`
        """
        model = pyfx.dispatch.oanda.models.close_trade200_response.CloseTrade200Response()  # noqa: E501
        if include_optional :
            return CloseTrade200Response(
                order_create_transaction = pyfx.dispatch.oanda.models.market_order_transaction.MarketOrderTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    instrument = '', 
                    units = '', 
                    time_in_force = 'GTC', 
                    price_bound = '', 
                    position_fill = 'OPEN_ONLY', 
                    trade_close = pyfx.dispatch.oanda.models.market_order_trade_close.MarketOrderTradeClose(
                        trade_id = '', 
                        client_trade_id = '', 
                        units = '', ), 
                    long_position_closeout = pyfx.dispatch.oanda.models.market_order_position_closeout.MarketOrderPositionCloseout(
                        instrument = '', 
                        units = '', ), 
                    short_position_closeout = pyfx.dispatch.oanda.models.market_order_position_closeout.MarketOrderPositionCloseout(
                        instrument = '', 
                        units = '', ), 
                    margin_closeout = pyfx.dispatch.oanda.models.market_order_margin_closeout.MarketOrderMarginCloseout(
                        reason = 'MARGIN_CHECK_VIOLATION', ), 
                    delayed_trade_close = pyfx.dispatch.oanda.models.market_order_delayed_trade_close.MarketOrderDelayedTradeClose(
                        trade_id = '', 
                        client_trade_id = '', 
                        source_transaction_id = '', ), 
                    reason = 'CLIENT_ORDER', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    take_profit_on_fill = pyfx.dispatch.oanda.models.take_profit_details.TakeProfitDetails(
                        price = '', 
                        time_in_force = 'GTC', 
                        gtd_time = '', ), 
                    stop_loss_on_fill = pyfx.dispatch.oanda.models.stop_loss_details.StopLossDetails(
                        price = '', 
                        distance = '', 
                        time_in_force = 'GTC', 
                        gtd_time = '', 
                        guaranteed = True, ), 
                    trailing_stop_loss_on_fill = pyfx.dispatch.oanda.models.trailing_stop_loss_details.TrailingStopLossDetails(
                        distance = '', 
                        time_in_force = 'GTC', 
                        gtd_time = '', ), 
                    trade_client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), ), 
                order_fill_transaction = pyfx.dispatch.oanda.models.order_fill_transaction.OrderFillTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    order_id = '', 
                    client_order_id = '', 
                    instrument = '', 
                    units = '', 
                    gain_quote_home_conversion_factor = '', 
                    loss_quote_home_conversion_factor = '', 
                    price = '', 
                    full_vwap = '', 
                    full_price = pyfx.dispatch.oanda.models.client_price.ClientPrice(
                        type = '', 
                        instrument = '', 
                        time = '', 
                        status = 'tradeable', 
                        tradeable = True, 
                        bids = [
                            pyfx.dispatch.oanda.models.price_bucket.PriceBucket(
                                price = '', 
                                liquidity = 56, )
                            ], 
                        asks = [
                            pyfx.dispatch.oanda.models.price_bucket.PriceBucket(
                                price = '', 
                                liquidity = 56, )
                            ], 
                        closeout_bid = '', 
                        closeout_ask = '', 
                        quote_home_conversion_factors = pyfx.dispatch.oanda.models.quote_home_conversion_factors.QuoteHomeConversionFactors(
                            positive_units = '', 
                            negative_units = '', ), 
                        units_available = pyfx.dispatch.oanda.models.units_available.UnitsAvailable(
                            default = pyfx.dispatch.oanda.models.units_available_details.UnitsAvailableDetails(
                                long = '', 
                                short = '', ), 
                            reduce_first = pyfx.dispatch.oanda.models.units_available_details.UnitsAvailableDetails(
                                long = '', 
                                short = '', ), 
                            reduce_only = , 
                            open_only = , ), ), 
                    reason = 'LIMIT_ORDER', 
                    pl = '', 
                    financing = '', 
                    commission = '', 
                    guaranteed_execution_fee = '', 
                    account_balance = '', 
                    trade_opened = pyfx.dispatch.oanda.models.trade_open.TradeOpen(
                        trade_id = '', 
                        units = '', 
                        price = '', 
                        guaranteed_execution_fee = '', 
                        client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                            id = '', 
                            tag = '', 
                            comment = '', ), 
                        half_spread_cost = '', 
                        initial_margin_required = '', ), 
                    trades_closed = [
                        pyfx.dispatch.oanda.models.trade_reduce.TradeReduce(
                            trade_id = '', 
                            units = '', 
                            price = '', 
                            realized_pl = '', 
                            financing = '', 
                            guaranteed_execution_fee = '', 
                            half_spread_cost = '', )
                        ], 
                    trade_reduced = pyfx.dispatch.oanda.models.trade_reduce.TradeReduce(
                        trade_id = '', 
                        units = '', 
                        price = '', 
                        realized_pl = '', 
                        financing = '', 
                        guaranteed_execution_fee = '', 
                        half_spread_cost = '', ), 
                    half_spread_cost = '', ), 
                order_cancel_transaction = pyfx.dispatch.oanda.models.order_cancel_transaction.OrderCancelTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    order_id = '', 
                    client_order_id = '', 
                    reason = 'INTERNAL_SERVER_ERROR', 
                    replaced_by_order_id = '', ), 
                related_transaction_ids = [
                    ''
                    ], 
                last_transaction_id = ''
            )
        else :
            return CloseTrade200Response(
        )
        """

    def testCloseTrade200Response(self):
        """Test CloseTrade200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
