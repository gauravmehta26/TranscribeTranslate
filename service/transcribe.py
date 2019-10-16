# transcribe.py
# 
# Purpose: The program provides a number of utility functions for leveraging the Amazon Transcribe API
#
# ==================================================================================

import boto3
import uuid
import requests

# ==================================================================================
# Function: createTranscribeJob
# Purpose: Function to format the input parameters and invoke the Amazon Transcribe service
# Parameters: 
#                 region - the AWS region in which to run AWS services (e.g. "eu-west-1")
#                 bucket - the Amazon S3 bucket name (e.g. "mybucket/") found in region that contains the media file for processing.   
#                 mediaFile - the content to process (e.g. "myaudio.wav")
#
# ==================================================================================
def createTranscribeJob( region, bucket, mediaFile, language ):

	# Set up the Transcribe client 
	transcribe = boto3.client('transcribe')
	
	# Set up the full uri for the bucket and media file
	mediaUri = "https://" + "s3-" + region + ".amazonaws.com/" + bucket + "/input/" + mediaFile 
	
	print( "Creating Job: " + "transcribe" + mediaFile + " for " + mediaUri )
	
	# Use the uuid functionality to generate a unique job name.  Otherwise, the Transcribe service will return an error
	response = transcribe.start_transcription_job( TranscriptionJobName="transcribe_" + uuid.uuid4().hex + "_" + mediaFile , \
		LanguageCode = language, \
		MediaFormat = "wav", \
		Media = { "MediaFileUri" : mediaUri }, \
		OutputBucketName = bucket + "/transcript/"
		#Settings = { "VocabularyName" : "MyVocabulary" } \
		)
	
	# return the response structure found in the Transcribe Documentation
	return response
	
	
# ==================================================================================
# Function: getTranscriptionJobStatus
# Purpose: Helper function to return the status of a job running the Amazon Transcribe service
# Parameters: 
#                 jobName - the unique jobName used to start the Amazon Transcribe job
# ==================================================================================
def getTranscriptionJobStatus( jobName ):
	transcribe = boto3.client('transcribe')
	
	response = transcribe.get_transcription_job( TranscriptionJobName=jobName )
	return response
	
	
# ==================================================================================
# Function: getTranscript
# Purpose: Helper function to return the transcript based on the signed URI in S3 as produced by the Transcript job
# Parameters: 
#                 transcriptURI - the signed S3 URI for the Transcribe output
# ==================================================================================
def getTranscript( transcriptURI ):
	# Get the resulting Transcription Job and store the JSON response in transcript
	s3 = boto3.client('s3')
	s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
	result = requests.get( transcriptURI )
	
	return result.text

	