import azure.cognitiveservices.speech as speechsdk
import time
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)

class Transcribe:    
    @sk_function(
            description="Transcribe an audio file",
            name="transcribe_audio",
            )
    @sk_function_context_parameter(
        name="audio",
        description="The path to the audio file to transcribe",
    )
    @sk_function_context_parameter(
        name="language",
        description="The language of the audio file in the format of Locale (BCP-47) (e.g. en-US)",
    )
    @sk_function_context_parameter(
        name="subscription_key",
        description="The subscription key for the Azure AI Speech resource",
    )
    @sk_function_context_parameter(
        name="region",
        description="The region of the Azure AI Speech resource",
    )  
    def transcribe_audio(audio, language, subscription_key, region):
        # Set up the speech configuration
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        # Define the language of the audio file
        speech_config.speech_recognition_language = language

        # Open the audio file
        audio_config = speechsdk.audio.AudioConfig(filename=audio)

        # Create a speech recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Define global variables
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
        while not done:
            time.sleep(.5)

        # Stop continuous speech recognition
        speech_recognizer.stop_continuous_recognition()
        
        # Convert to string and return the transcription
        return recognized_text_list