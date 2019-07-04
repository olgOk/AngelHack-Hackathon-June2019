import boto3
import json
import sys

class VideoDetect:
	jobId = ''
	rek = boto3.client('rekognition')
	queueUrl = 'https://sqs.us-west-1.amazonaws.com/019895355269/gamers_queue'
	roleArn = 'arn:aws:iam::019895355269:role/gamers_sns'
	topicArn = 'arn:aws:sns:us-west-1:019895355269:AmazonRekognition_gamers'
	bucket = 'gamers.frply'
	video = 'Video/knaumov.mov'
	profile = "rtsaturi_profile.jpg"
	match = 0

	def GetResultsFaceSearchCollection(self, jobId):
		maxResults = 10
		paginationToken = ''

		finished = False

		while finished == False:
			response = self.rek.get_face_search(JobId=jobId,
										MaxResults=maxResults,
										NextToken=paginationToken)

			for personMatch in response['Persons']:
				if ('FaceMatches' in personMatch):
					for faceMatch in personMatch['FaceMatches']:
						if self.profile == faceMatch['Face']['ExternalImageId']:
							self.match = 1
						print('Face ID: ' + faceMatch['Face']['FaceId'])
						print('ExternalImageId: ' + faceMatch['Face']['ExternalImageId'])
						print('Similarity: ' + str(faceMatch['Similarity']))
						print()
			if 'NextToken' in response:
				paginationToken = response['NextToken']
			else:
				finished = True

	def main(self):

		jobFound = False
		sqs = boto3.client('sqs')

		response = self.rek.start_face_search(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
			CollectionId='Gamers',
			NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn})
		dotLine=0
		while jobFound == False:
			sqsResponse = sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
										  MaxNumberOfMessages=10)

			if sqsResponse:
				
				if 'Messages' not in sqsResponse:
					if dotLine<20:
						print('.', end='')
						dotLine=dotLine+1
					else:
						print()
						dotLine=0    
					sys.stdout.flush()
					continue
				for message in sqsResponse['Messages']:
					notification = json.loads(message['Body'])
					rekMessage = json.loads(notification['Message'])
					if str(rekMessage['JobId']) == response['JobId']:
						jobFound = True
						self.GetResultsFaceSearchCollection(rekMessage['JobId'])
						sqs.delete_message(QueueUrl=self.queueUrl,
									ReceiptHandle=message['ReceiptHandle'])
					sqs.delete_message(QueueUrl=self.queueUrl,
								ReceiptHandle=message['ReceiptHandle'])

if __name__ == "__main__":

	analyzer=VideoDetect()
	analyzer.main()
	if analyzer.match == 0:
		print('No match found')
	else:
		print('Match found')