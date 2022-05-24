import requests
import boto3
import json

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    GUILD_ID = ssm.get_parameter(Name='guild-id', WithDecryption=False)['Parameter']['Value']
    BOT_TOKEN = ssm.get_parameter(Name='bot-token', WithDecryption=False)['Parameter']['Value']
    APP_ID = ssm.get_parameter(Name='app-id', WithDecryption=False)['Parameter']['Value']
    
    url = f'https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands'

    with open('commands.json','r') as f:
        commands = json.loads(f.read())

    response = requests.put(url, headers={
        'Authorization': f'Bot {BOT_TOKEN}'
    }, json=commands)
    print(response.text)