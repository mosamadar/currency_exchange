import json
import requests
from deepdiff import DeepDiff
from api.lib import utils
from datetime import datetime, timedelta


def save_current_exchange_rates(event, context):
    """ This function will save exchange rates for every date in dynamoDB"""
    try:
        """ Using a third party api to get exchange rates according to EURO as base currency """
        get_rates = requests.get(url=utils.exchange_url)
        current_rates = json.loads(get_rates.text)
        # current_rates = utils.sample_json_1

        """ DynamoDb does not accept float values which are of different 
        currencies so converting them to string to store into the database """

        rates = current_rates.get("conversion_rates")
        current_rates.pop("conversion_rates")
        currency_value = rates.items()
        updated_currency = {str(currency): str(value) for currency, value in currency_value}
        current_rates.update({"conversion_rates": updated_currency})

        """ Making a dict object to save into the database """
        data_item = {
            "data": current_rates,
            "date": datetime.utcfromtimestamp(current_rates['time_last_update_unix']).strftime("%d %b %Y")
        }

        """ Finally put the item in the dynamoDB table """
        response = utils.ddb_generic_put_table_item(data_item=data_item)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Exchange rates have been saved.",
                "response": response,
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "There was problem while running the event.",
                "response": e,
            }),
        }


def get_today_exchange_rates(event, context):
    try:
        now_utc = datetime.now().date()
        my_scan_data = datetime.fromisoformat(str(now_utc)).strftime("%d %b %Y")
        response = utils.ddb_check_current_date_exchange_rates(date=my_scan_data)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Exchange rates for today.",
                "response": response.get("data").get("conversion_rates"),
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "There was problem while running the event.",
                "response": e,
            }),
        }


def compare_exchange_rates(event, context):
    try:
        """ According to task we wanted to compare today's date with previous day date """
        yesterday_utc = datetime.now().date() - timedelta(1)
        now_utc = datetime.now().date()

        """ Convert to format of Query (Partition Key) that is saved in dynamoDB """
        yesterday = datetime.fromisoformat(str(yesterday_utc)).strftime("%d %b %Y")
        today = datetime.fromisoformat(str(now_utc)).strftime("%d %b %Y")

        """ Get the previous day record from dynamoDB for exchange rates according to EURO """
        yesterday_values = utils.ddb_check_current_date_exchange_rates(date=yesterday)

        """ Get  today record from dynamoDB for exchange rates according to EURO """
        today_values = utils.ddb_check_current_date_exchange_rates(date=today)

        """ Get the previous day and current day difference which we can get with values """
        previous = yesterday_values.get("data").get("conversion_rates")
        current = today_values.get("data").get("conversion_rates")
        major_differences = DeepDiff(previous, current)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Compared exchange rates for yesterday {yesterday} and today {today}",
                "response": major_differences.get("values_changed"),
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "There was problem while running the event.",
                "response": e,
            }),
        }


def get_current_exchange_rates(event, context):
    try:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "hello exchange rates lambda test function",
                "response": "my test response"
            }),
        }
    except Exception as e:
        return {
            "errorMessage": str(e),
            "errorType": str(e),
            "stackTrace": ""
        }
