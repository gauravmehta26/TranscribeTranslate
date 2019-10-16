import boto3
import json

# ==================================================================================
# Function: translateTranscript
# Purpose: Based on the JSON transcript provided by Amazon Transcribe, get the JSON response of translated text
# Parameters: 
#                 transcript - the JSON output from Amazon Transcribe
#                 sourceLangCode - the language code for the original content (e.g. English = "EN")
#                 targetLangCode - the language code for the translated content (e.g. Spanich = "ES")
#                 region - the AWS region in which to run the Translation (e.g. "us-east-1")
# ==================================================================================
def translateTranscript( transcript, sourceLangCode, targetLangCode, region ):
	# Get the translation in the target language.  We want to do this first so that the translation is in the full context
	# of what is said vs. 1 phrase at a time.  This really matters in some lanaguages

	# stringify the transcript
	ts = json.loads( transcript )

	# pull out the transcript text and put it in the txt variable
	txt = ts["results"]["transcripts"][0]["transcript"]
		
	#set up the Amazon Translate client
	translate = boto3.client(service_name='translate', region_name=region, use_ssl=True)
	
	# call Translate  with the text, source language code, and target language code.  The result is a JSON structure containing the 
	# translated text
	translation = translate.translate_text(Text=txt,SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode)
	
	return translation
	