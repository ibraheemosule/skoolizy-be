import base64
import hashlib
import hmac
import boto3
import os


def cognito_client():
    return boto3.client('cognito-idp', region_name=os.getenv('FLASK_COGNITO-REGION'))


def generate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    secret_hash = base64.b64encode(dig).decode()
    return secret_hash
