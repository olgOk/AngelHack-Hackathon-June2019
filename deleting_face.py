import boto3

if __name__ == "__main__":

    collectionId='Gamers'
    faces=["d5e10426-1383-4674-8025-384a6fff661b"]

    client=boto3.client('rekognition')

    response=client.delete_faces(CollectionId=collectionId,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)