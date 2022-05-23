import requests
import boto3
import json

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    GUILD_ID = ssm.get_parameter(Name='guild-id', WithDecryption=False)['Parameter']['Value']
    BOT_TOKEN = ssm.get_parameter(Name='bot-token', WithDecryption=False)['Parameter']['Value']
    APP_ID = ssm.get_parameter(Name='app-id', WithDecryption=False)['Parameter']['Value']
    
    url = f'https://discord.com/api/v8/applications/{APP_ID}/guilds/{GUILD_ID}/commands'

    commands = json.loads(open('commands.json','r').read())

    response = requests.post(url, headers={
        'Authorization': f'Bot {BOT_TOKEN}'
    }, json=commands)
