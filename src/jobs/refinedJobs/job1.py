import boto3
import sys
print("Before Append:", sys.path)

sys.path.append('D:\\GitHub\\snowflake_demo\\first_repo\\utils')
print("After Append:", sys.path)
from utils.vaultUtil import VaultClient
from utils.awsUtil import AWSConnector


VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "4e783bc0-6984-c0f1-d9d0-3f813e32e31c"
SECRET_ID = "d16ac449-2906-56bc-47cd-5d23d682e571"
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