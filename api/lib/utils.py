from api.lib.common import initilalized_logger
import boto3
import humps
import json
import decimal
from datetime import datetime

logger = initilalized_logger(__name__)

exchange_url= "https://v6.exchangerate-api.com/v6/c85c4dd12f12fad95e00b0b2/latest/EUR"


class Encoder(json.JSONEncoder):
    def default(self, o):
        try:
            if type(o) is datetime:
                return o.isoformat()
            elif type(o) is decimal.Decimal:
                return str(o)
            elif type(o) is bytes:
                return o.decode('utf-8')
            else:
                return o.__dict__
        except Exception as e:
            logger.exception('Could not convert object: {0} to json: {1}'.format(o, e))
            return {}


def ddb_connection():
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table("ExchangeRates")
  return {
    "db": dynamodb,
    "table": table
  }

def ddb_check_current_date_exchange_rates(date):
    try:
        response = ddb_connection().get("table").get_item(
            Key={
              'date': date
            }
        )
        return response['Item']
    except Exception as e:
        raise e

def ddb_generic_put_table_item(data_item):
  """
  update any table with the passed data_item, the item must already have the
  required partition and sort keys set in the object that match the tables
  defined partition and sort_key named fields
  :param ddb_table_name:
  :param data_item: Object that is json serializable or dict
  :return: DynamoDB response
  """
  response = None
  try:
    # update DynamoDB rec then done
    table = ddb_connection().get("table")

    # creating new record
    if type(data_item) is not dict:
      response = table.put_item(Item=data_item.__dict__)
    else:
      response = table.put_item(Item=data_item)
    logger.info('Put DDB data item {0}'.format(data_item))

  except Exception as e:
    msg = 'ERROR updating DynamoDB rec: {0} - {1}'.format(
      data_item, e)
    logger.exception(msg)
  return response

def obj_to_json(obj, camelize=True):
    """
    converts an object into json
    using python int conversion
    :param obj: object to be converted
    :param camelize: flag to camelCase keys
    :return: json or None
    """
    try:
        if camelize:
            # convert keys to camelCase
            obj = humps.camelize(obj)
        return json.dumps(obj, cls=Encoder)

    except Exception as e:
        # return input variable
        logger.exception('ERROR converting object to json: {0}'.format(e))
        return ''
