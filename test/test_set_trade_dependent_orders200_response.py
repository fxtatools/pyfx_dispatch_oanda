# coding: utf-8

"""
    OANDA v20 REST API

    The full OANDA v20 REST API Specification. This specification defines how to interact with v20 Accounts, Trades, Orders, Pricing and more.

    The version of the OpenAPI document: 3.0.25

    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

import pyfx.dispatch.oanda
from pyfx.dispatch.oanda.models.set_trade_dependent_orders200_response import SetTradeDependentOrders200Response  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestSetTradeDependentOrders200Response(unittest.TestCase):
    """SetTradeDependentOrders200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SetTradeDependentOrders200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SetTradeDependentOrders200Response`
        """
        model = pyfx.dispatch.oanda.models.set_trade_dependent_orders200_response.SetTradeDependentOrders200Response()  # noqa: E501
        if include_optional :
            return SetTradeDependentOrders200Response(
                take_profit_order_cancel_transaction = pyfx.dispatch.oanda.models.order_cancel_transaction.OrderCancelTransaction(
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
                take_profit_order_transaction = pyfx.dispatch.oanda.models.take_profit_order_transaction.TakeProfitOrderTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    trade_id = '', 
                    client_trade_id = '', 
                    price = '', 
                    time_in_force = 'GTC', 
                    gtd_time = '', 
                    trigger_condition = 'DEFAULT', 
                    reason = 'CLIENT_ORDER', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    order_fill_transaction_id = '', 
                    replaces_order_id = '', 
                    cancelling_transaction_id = '', ), 
                take_profit_order_fill_transaction = pyfx.dispatch.oanda.models.order_fill_transaction.OrderFillTransaction(
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
                take_profit_order_created_cancel_transaction = pyfx.dispatch.oanda.models.order_cancel_transaction.OrderCancelTransaction(
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
                stop_loss_order_cancel_transaction = pyfx.dispatch.oanda.models.order_cancel_transaction.OrderCancelTransaction(
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
                stop_loss_order_transaction = pyfx.dispatch.oanda.models.stop_loss_order_transaction.StopLossOrderTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    trade_id = '', 
                    client_trade_id = '', 
                    price = '', 
                    distance = '', 
                    time_in_force = 'GTC', 
                    gtd_time = '', 
                    trigger_condition = 'DEFAULT', 
                    guaranteed = True, 
                    guaranteed_execution_premium = '', 
                    reason = 'CLIENT_ORDER', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    order_fill_transaction_id = '', 
                    replaces_order_id = '', 
                    cancelling_transaction_id = '', ), 
                stop_loss_order_fill_transaction = pyfx.dispatch.oanda.models.order_fill_transaction.OrderFillTransaction(
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
                stop_loss_order_created_cancel_transaction = pyfx.dispatch.oanda.models.order_cancel_transaction.OrderCancelTransaction(
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
                trailing_stop_loss_order_cancel_transaction = pyfx.dispatch.oanda.models.order_cancel_transaction.OrderCancelTransaction(
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
                trailing_stop_loss_order_transaction = pyfx.dispatch.oanda.models.trailing_stop_loss_order_transaction.TrailingStopLossOrderTransaction(
                    id = '', 
                    time = '', 
                    user_id = 56, 
                    account_id = '', 
                    batch_id = '', 
                    request_id = '', 
                    type = 'CREATE', 
                    trade_id = '', 
                    client_trade_id = '', 
                    distance = '', 
                    time_in_force = 'GTC', 
                    gtd_time = '', 
                    trigger_condition = 'DEFAULT', 
                    reason = 'CLIENT_ORDER', 
                    client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                        id = '', 
                        tag = '', 
                        comment = '', ), 
                    order_fill_transaction_id = '', 
                    replaces_order_id = '', 
                    cancelling_transaction_id = '', ), 
                related_transaction_ids = [
                    ''
                    ], 
                last_transaction_id = ''
            )
        else :
            return SetTradeDependentOrders200Response(
        )
        """

    def testSetTradeDependentOrders200Response(self):
        """Test SetTradeDependentOrders200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
