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
from pyfx.dispatch.oanda.models.get_account200_response import GetAccount200Response  # noqa: E501
from pyfx.dispatch.oanda.rest import ApiException

class TestGetAccount200Response(unittest.TestCase):
    """GetAccount200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GetAccount200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetAccount200Response`
        """
        model = pyfx.dispatch.oanda.models.get_account200_response.GetAccount200Response()  # noqa: E501
        if include_optional :
            return GetAccount200Response(
                account = pyfx.dispatch.oanda.models.account.Account(
                    id = '', 
                    alias = '', 
                    currency = '', 
                    balance = '', 
                    created_by_user_id = 56, 
                    created_time = '', 
                    guaranteed_stop_loss_order_mode = 'DISABLED', 
                    pl = '', 
                    resettable_pl = '', 
                    resettable_pl_time = '', 
                    financing = '', 
                    commission = '', 
                    guaranteed_execution_fees = '', 
                    margin_rate = '', 
                    margin_call_enter_time = '', 
                    margin_call_extension_count = 56, 
                    last_margin_call_extension_time = '', 
                    open_trade_count = 56, 
                    open_position_count = 56, 
                    pending_order_count = 56, 
                    hedging_enabled = True, 
                    last_order_fill_timestamp = '', 
                    unrealized_pl = '', 
                    nav = '', 
                    margin_used = '', 
                    margin_available = '', 
                    position_value = '', 
                    margin_closeout_unrealized_pl = '', 
                    margin_closeout_nav = '', 
                    margin_closeout_margin_used = '', 
                    margin_closeout_percent = '', 
                    margin_closeout_position_value = '', 
                    withdrawal_limit = '', 
                    margin_call_margin_used = '', 
                    margin_call_percent = '', 
                    last_transaction_id = '', 
                    trades = [
                        pyfx.dispatch.oanda.models.trade_summary.TradeSummary(
                            id = '', 
                            instrument = '', 
                            price = '', 
                            open_time = '', 
                            state = 'OPEN', 
                            initial_units = '', 
                            initial_margin_required = '', 
                            current_units = '', 
                            realized_pl = '', 
                            unrealized_pl = '', 
                            margin_used = '', 
                            average_close_price = '', 
                            closing_transaction_ids = [
                                ''
                                ], 
                            financing = '', 
                            close_time = '', 
                            client_extensions = pyfx.dispatch.oanda.models.client_extensions.ClientExtensions(
                                id = '', 
                                tag = '', 
                                comment = '', ), 
                            take_profit_order_id = '', 
                            stop_loss_order_id = '', 
                            trailing_stop_loss_order_id = '', )
                        ], 
                    positions = [
                        pyfx.dispatch.oanda.models.position.Position(
                            instrument = '', 
                            pl = '', 
                            unrealized_pl = '', 
                            margin_used = '', 
                            resettable_pl = '', 
                            financing = '', 
                            commission = '', 
                            guaranteed_execution_fees = '', 
                            long = pyfx.dispatch.oanda.models.position_side.PositionSide(
                                units = '', 
                                average_price = '', 
                                trade_ids = [
                                    ''
                                    ], 
                                pl = '', 
                                unrealized_pl = '', 
                                resettable_pl = '', 
                                financing = '', 
                                guaranteed_execution_fees = '', ), 
                            short = pyfx.dispatch.oanda.models.position_side.PositionSide(
                                units = '', 
                                average_price = '', 
                                pl = '', 
                                unrealized_pl = '', 
                                resettable_pl = '', 
                                financing = '', 
                                guaranteed_execution_fees = '', ), )
                        ], 
                    orders = [
                        pyfx.dispatch.oanda.models.order.Order(
                            id = '', 
                            create_time = '', 
                            state = 'PENDING', )
                        ], ), 
                last_transaction_id = ''
            )
        else :
            return GetAccount200Response(
        )
        """

    def testGetAccount200Response(self):
        """Test GetAccount200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
