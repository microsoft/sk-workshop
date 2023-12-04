import semantic_kernel as sk
import os
from plugins.CallCenterPlugin.Transcribe import Transcribe


async def main():
    aispeech_subscription_key = "198d6d7eb8341ba90022f1224ee8967"
    aispeech_region = "brazilsouth"

    #Defining the input variables for the transcription funcion
    variables = sk.ContextVariables()
    
    #Specify the path to audio file
    
    current_directory = os.getcwd()
    audio_path = os.path.join(current_directory, "english_billing_process_sample.wav")

    variables["audio_path"] = "english_billing_process_sample.wav"
    variables["language"] = "en-US"
    variables["subscription_key"] = aispeech_subscription_key
    variables["region"] = aispeech_region
    
    # Initialize the kernel
    kernel = sk.Kernel()

    plugin = kernel.import_skill(Transcribe(), skill_name="CallCenterPlugin")
   
    # Add a text or chat completion service using either:
    # kernel.add_text_completion_service()
    # kernel.add_chat_service()

   # Run the Sqrt function with the context.
    result = await kernel.run_async(
        plugin["transcribe_audio"],
        input_vars=variables
    )

    print(result)


# Run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())