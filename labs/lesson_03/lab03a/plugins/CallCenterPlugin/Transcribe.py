import time

#Importing Azure Cognitive Services Speech SDK package
import azure.cognitiveservices.speech as speechsdk

#Importing Semantic Kernel packages to define the function and its parameters
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
#Importing Semantic Kernel package to parse input variables
from semantic_kernel.orchestration.sk_context import SKContext

#Defining the Transcribe class to be used as a plugin to transcribe audio files
class Transcribe:
    @sk_function(
        description="Transcribe an audio file and output its text transcription.",
        name="transcribe_audio",
    )
    @sk_function_context_parameter(
        name="input",
        description="The path in disk to the audio file to transcribe. Required parameter",
    )
    @sk_function_context_parameter(
        name="language",
        description="The language of the audio file in the format of Locale (BCP-47) (e.g. en-US). Required parameter",
    )
    @sk_function_context_parameter(
        name="subscription_key",
        description="The subscription key for the Azure AI Speech resource. Required parameter.",
    )
    @sk_function_context_parameter(
        name="region",
        description="The region of the Azure AI Speech resource. Required parameter.",
    )         
    def transcribe_audio(self, context: SKContext) -> str:
        #Obtaining and parsing input parameters from SKContext
        audio_path = context["input"]
        language = context["language"]
        subscription_key = context["subscription_key"]
        region = context["region"]

        #Set up the speech configuration
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        # Define the language of the audio file
        speech_config.speech_recognition_language = language

        # Open the audio file
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)

        # Create a speech recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Define global variables to control the continuous recognition loop and accumulate text
        global done 
        done = False
        global recognized_text_list 
        recognized_text_list=[]

        # Define the stop callback function
        def stop_cb(evt: speechsdk.SessionEventArgs):
            """callback that signals to stop continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            global done
            done = True

        # Define the recognize callback function
        def recognize_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            """callback for recognizing the recognized text"""
            global recognized_text_list
            recognized_text_list.append(evt.result.text)

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognized.connect(recognize_cb)
        speech_recognizer.session_started.connect(lambda evt: print('STT SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('STT SESSION STOPPED {}'.format(evt)))
        speech_recognizer.session_stopped.connect(stop_cb)
    
        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()
        print("Continuous speech recognition started. Waiting to complete transcription...")
        while not done:
            time.sleep(.1)

        #Stop continuous speech recognition
        speech_recognizer.stop_continuous_recognition()
        
        print("Transcription complete.")
                
        return str(recognized_text_list)
