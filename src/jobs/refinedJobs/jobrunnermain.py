import boto3
import sys
import utils.vaultUtil
import utils.awsUtil
sys.path.append(r'D:\GitHub\snowflake_demo\first_repo\src\utils')
from utils import VaultClient
from utils.awsUtil import AWSConnector


VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "fe6bd13b-04dd-c79d-d0e1-aea34a9cbb42"
SECRET_ID = "b4d8c763-d6a9-b2cd-44ec-4a5c182bef2d"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")


aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']

region = 'us-east-1'  # Replace with your preferred AWS region


client='iam'
aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

# Access the S3 client through the instance
iam_client = aws_connector.aws_client_conn

# Now you can use s3_client to perform S3 operations
response = iam_client.list_groups()

print("IAM groups:", response)