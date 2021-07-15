import boto3
from pprint import pprint
import pandas as pd
client = boto3.client("ec2", region_name='us-east-2')

response = client.describe_volumes()

#dict_keys(['Attachments', 'AvailabilityZone', 'CreateTime', 
#'Encrypted', 'KmsKeyId', 'Size', 'SnapshotId', 
#'State', 'VolumeId', 'Tags', 'VolumeType', 'MultiAttachEnabled']


# 'tags': [{'Key': 'sb.business-unit', 'Value': 'finance'}, 
#           {'Key': 'CostCenter', 'Value': 'SBCorporate'}, 
#           {'Key': 'Name', 'Value': 'SBAWSALTDB03P'}, 
#           {'Key': 'sb.approver', 'Value': 'ryan.norsworthy@securitybenefit.com'}, 
#           {'Key': 'sb.application-role', 'Value': 'db'}, 
#           {'Key': 'CloudreachSupport', 'Value': 'BaseSupport'}, 
#           {'Key': 'sb.application-name', 'Value': 'alteryx'}, 
#           {'Key': 'sb.environment', 'Value': 'prod '}], 


status = []

def preprocess_tags(tags_):
	dict_ = {}
	for item in tags_:
		dict_[item['Key']] = item['Value']
	return dict_ 

for item in response['Volumes']:
	preprocess_tags_ = preprocess_tags(item['Tags'])
	status.append({'size': item['Size'], 
		           'state': item['State'], 
		           'volume_id': item['VolumeId'], 
		           'tags_approver': preprocess_tags_.get('sb.approver', 'None'),
		           'tags_name':  preprocess_tags_.get('Name', 'None'), 
		           'volume_type': item['VolumeType']})

pprint(status)


df = pd.DataFrame()
df['size'] = [item['size'] for item in status]
df['state'] = [item['state'] for item in status]
df['volume_id'] = [item['volume_id'] for item in status]
df['tags_approver'] = [item['tags_approver'] for item in status]
df['tags_name'] = [item['tags_name'] for item in status]
df['volume_type'] = [item['volume_type'] for item in status]

pprint(df)

df.to_csv("Secben_prod_us-east-2_vol_gp2.1.0.csv", index=False)






