import json,os
import boto3
from datetime import datetime,timezone
def handle(event,context):
    client=boto3.client('s3'); failed=[]
    for record in event.get('Records',[]):
        try:
            payload=json.loads(record['body'])
            if not isinstance(payload,dict) or not isinstance(payload.get('id'),str) or not payload['id']:
                raise ValueError('nonempty event id required')
            import hashlib
            key=hashlib.sha256(payload['id'].encode()).hexdigest()
            client.put_object(Bucket=os.environ['BUCKET'],Key=f'raw/{key}.json',
                              Body=json.dumps(payload).encode(),ContentType='application/json')
        except Exception:
            failed.append({'itemIdentifier':record['messageId']})
    return {'batchItemFailures':failed}
