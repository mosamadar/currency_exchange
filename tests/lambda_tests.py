import json
import os
import sys
from api import lmd_exchange

sys.path.append(os.getcwd())
import unittest

from api.lib.common import initilalized_logger
logger = initilalized_logger(__name__)

os.chdir('../api')
sys.path.append(os.getcwd())
logger.info('Current working dir is: {0}'.format(os.getcwd()))


class CallMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CallMethods, self).__init__(*args, **kwargs)
        # will make direct call to lambda function else use gateway
        # self.dev_portal_token = portal_credentials.main()
        self.event = {
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        self.context = {}

    """
    #################### UTILITY FUNCTIONS ####################
    """

    def test_save_exchange_rate_GET_LAMBDA(self):
        logger.info('Testing test_save_exchange_rate_GET_LAMBDA...')
        self.event['httpMethod'] = 'POST'
        self.event['body'] = {}
        # self.event['queryStringParameters'] = {
        #     'currency': 'USD',
        # }

        response = lmd_exchange.save_current_exchange_rates(
            event=self.event, context=self.context)

        logger.info('Got back response: {0}'.format(response))
        logger.info('Body: {0}'.format(
            json.loads(response.get('body', {}))
        ))
        self.assertTrue(True)

    def test_get_current_exchange_rates_GET_LAMBDA(self):
        logger.info('Testing test_get_current_exchange_rates_GET_LAMBDA...')
        self.event['httpMethod'] = 'GET'
        # self.event['queryStringParameters'] = {
        #     'date': '16 Jan 2023',
        # }
        response = lmd_exchange.get_current_exchange_rates(
            event=self.event, context=self.context
        )
        logger.info('Got back response: {0}'.format(response))
        logger.info('Body: {0}'.format(
            json.loads(response.get('body', {}))
        ))
        self.assertTrue(True)

    def test_get_compared_exchange_rate_GET_LAMBDA(self):
        logger.info('Testing test_get_compared_exchange_rate_GET_LAMBDA...')
        self.event['httpMethod'] = 'GET'
        # self.event['queryStringParameters'] = {
        #     'date': '16 Jan 2023',
        # }
        response = lmd_exchange.compare_exchange_rates(
            event=self.event, context=self.context
        )
        logger.info('Got back response: {0}'.format(response))
        logger.info('Body: {0}'.format(
            json.loads(response.get('body', {}))
        ))
        self.assertTrue(True)

    def test_get_test_current_exchange_rates_GET_LAMBDA(self):
        logger.info('Testing test_get_test_current_exchange_rates_GET_LAMBDA...')
        self.event['httpMethod'] = 'GET'
        # self.event['queryStringParameters'] = {
        #     'date': '16 Jan 2023',
        # }
        response = lmd_exchange.get_test_current_exchange_rates(
            event=self.event, context=self.context
        )
        logger.info('Got back response: {0}'.format(response))
        logger.info('Body: {0}'.format(
            json.loads(response.get('body', {}))
        ))
        self.assertTrue(True)
