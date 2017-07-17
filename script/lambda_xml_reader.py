def lambda_handler(event, context):
    import boto3
    import xml.etree.ElementTree
    s3_client = boto3.client('s3')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        bucket = "gen3-interns-trigger" #TEST LINE SHOULD BE TAKEN FROM EVEN TRIGGER
        key = record['s3']['object']['key']
        key = "Battleship_02392_VZ_R_NBC.xml" # TEST LINE SHOULD BE TAKEN FROM EVENT TRIGGER IN THE END
        response = s3_client.get_object(Bucket=bucket, Key=key) # NEED TO FIGURE OUT WHAT TO DO WHEN OBJECT ISN'T public, maybe should look at the IAM roles
        text = response['Body'].read().decode('utf-8')
        print(bucket, key, response)
        print(text)
        root = xml.etree.ElementTree.fromstring(text)
        itemList = root.get
