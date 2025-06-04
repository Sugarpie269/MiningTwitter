import tweepy
from tweepy import OAuthHandler
import boto3
from botocore.exceptions import ClientError
import json
import os

def get_secret():
    aws_secret = os.getenv("AWS_SECRET_NAME")
    aws_region = os.getenv("AWS_REGION")
    aws_profile = os.getenv("AWS_PROFILE")

    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name=aws_profile)
    client = session.client(
        service_name='secretsmanager',
        region_name=aws_region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=aws_secret
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

secrets = get_secret()
consumer_key = secrets["twitter_consumer_key"]
consumer_secret = secrets["twitter_consumer_secret"]
access_token = secrets["twitter_access_token"]
access_secret = secrets["twitter_access_secret"]
bearer_token = secrets["twitter_bearer_token"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

user = api.verify_credentials()

print(user.id, user.screen_name)