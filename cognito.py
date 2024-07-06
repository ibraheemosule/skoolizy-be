import boto3
import os

cognito_user_pool_id = os.getenv('FLASK_COGNITO_USER_POOL_ID')
cognito_client_id = os.getenv('FLASK_COGNITO_CLIENT_ID')
cognito_region = os.getenv('FLASK_COGNITO_REGION')

cognito_client = boto3.client('cognito-idp', region_name='eu-west-1')
