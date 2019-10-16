#
# translatevideo.py
#
# Purpose: This code drives the process to create a transription job, translate it into another language,
#          create subtitles, use Amazon Polly to synthesize an alternate audio track, and finally put it all together
#          into a new video.
#
# ==================================================================================


import argparse
from transcribe import *
from synthesize import *
import time
#from videoUtils import *
#from audioUtils import *

# ==================================================================================
# Function: handler
# Purpose: writes the bytes associates with the stream to a binary file
# Parameters: 
#                 output_file - the name + extension of the ouptut file (e.g. "abc.mp3")
#                 stream - the stream of bytes to write to the output_file
# ==================================================================================
def handler(event, context):
    bucket_name     = event['bucket']
    audiofile_key   = event['key']
    source_language = event['sourceLanguage']
    target_language = event['targetLanguage']

    source_language = "hi-IN"
    print( "==> voicetranslator.py:\n")
    print( "==> Parameters: ")
    print("\tInput bucket/object: " + bucket_name + "\input" + audiofile_key )
    #print( "\tOutput bucket/object: " + args.outbucket + "\output" + args.outfilename + "." + args.outfiletype )
    
    print( "\n==> Target Language Translation Output: " )
    print( "\t" + bucket_name  + "\output" + audiofile_key + "-" + target_language + ".mp3")
    
    # Create Transcription Job
    response = createTranscribeJob( "eu-west-1", bucket_name, audiofile_key, source_language )

    # loop until the job successfully completes
    print( "\n==> Transcription Job: " + response["TranscriptionJob"]["TranscriptionJobName"] + "\n\tIn Progress"),

    while( response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS"):
        print( "."),
        time.sleep( 30 )
        response = getTranscriptionJobStatus( response["TranscriptionJob"]["TranscriptionJobName"] )

    print( "\nJob Complete")
    print( "\tStart Time: " + str(response["TranscriptionJob"]["CreationTime"]) )
    print( "\tEnd Time: "  + str(response["TranscriptionJob"]["CompletionTime"]) )
    print( "\tTranscript URI: " + str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) )
    
    # Now get the transcript JSON from AWS Transcribe
    transcript = getTranscript( str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) ) 
    # print( "\n==> Transcript: \n" + transcript)

    # Now write out the translation to the transcript for each of the target languages
        
    #Now that we have the subtitle files, let's create the audio track
    createAudioTrackFromTranslation( "eu-west-1", transcript, 'hi', target_language, "audio-" + target_language + ".mp3", bucket_name )