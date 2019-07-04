import boto3

if __name__ == "__main__":

    maxResults=2
    collectionId='Gamers'
	
    client=boto3.client('rekognition')

    #Create a collection
    print('Creating collection:' + collectionId)
    response=client.create_collection(CollectionId=collectionId)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

    #aws:rekognition:us-west-1:019895355269:collection/Gamers