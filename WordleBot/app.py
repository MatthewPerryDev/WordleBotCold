import json
import boto3
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import re

ssm = boto3.client('ssm')
PUBLIC_KEY = ssm.get_parameter(Name='public-key', WithDecryption=False)['Parameter']['Value']


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        verify(event,body)
        # handle the interaction

        t = body['type']

        if t == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'type': 1
                })
            }
        elif t == 2:
            return command_handler(body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('unhandled request type')
            }
    except:
        raise


def command_handler(body):
    command = body['data']['name']

    if command == 'wordle':
        return wordle(body)


def wordle(body):
    reg = "^\s*Wordle\s*([0-9]+)\s*(\d)\/\d\s*((?:[🟩⬛🟨]{5}\s*){1,6})$"
    value = re.match(reg,body['data']['options'][0]['value'])
    if value:
        value= "Valid"
    else:
        value= "Not a valid input"
    return {
        'statusCode': 200,
        'body': json.dumps({
            'type': 4,
            'data': {
                'content': f"{value}",
            }
        })
    }


def leaderboard(body):
    pass


def stat(body):
    pass


def verify(event,body):

    signature = event['headers']['x-signature-ed25519']
    timestamp = event['headers']['x-signature-timestamp']

    # validate the interaction
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    message = timestamp + \
        json.dumps(body, separators=(',', ':'), ensure_ascii=False)

    try:
        verify_key.verify(message.encode(),
                          signature=bytes.fromhex(signature))
    except BadSignatureError:
        return {
            'statusCode': 401,
            'body': json.dumps('invalid request signature')
        }
