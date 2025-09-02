
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


from openai import OpenAI

client = OpenAI(api_key = OPENAI_API_KEY)

def transcribe_file_and_dub(audio_file_path: str):
    with open(audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    
    text_block = response.text
    
    print(text_block)

    text_block = translate(text_block, language="Telugu")
    
    # Change the audio name and location based on how you want it to be saved
    output_path = "/Users/sharon/Desktop/AudioTranslator/transalted_recordings/telugu_audio.mp3"
    text_to_speech(text_block, output_path)
    return output_path



from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

translation_template = """
Translate the following sentence into {language}, return ONLY the translation, nothing else.

Sentence: {sentence}
"""

output_parser = StrOutputParser()
llm = ChatOpenAI(model="gpt-5")
translation_prompt = ChatPromptTemplate.from_template(translation_template)

translation_chain = (
    {"language": RunnablePassthrough(), "sentence": RunnablePassthrough()} 
    | translation_prompt
    | llm
    | output_parser
)

def translate(sentence, language):
    data_input = {"language": language, "sentence": sentence}
    translation = translation_chain.invoke(data_input)
    print(translation)
    return translation



# %% [markdown]
# ---
# ## Google Cloud For Text to Speech
# 
# Languages and Voices list -> https://cloud.google.com/text-to-speech/docs/list-voices-and-types

# %%
from google.cloud import texttospeech

# Initialize the client once (outside the function, so it doesn't re-initialize every call)
tts_client = texttospeech.TextToSpeechClient()

def text_to_speech(text, output_file):
    
    # Prepare the input text
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Choose the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="te-IN",
        name="te-IN-Chirp3-HD-Charon"
    )

    # Configure audio output
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=["small-bluetooth-speaker-class-device"],
        speaking_rate=1.0,
    )

    # Call the API
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save to file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'✅ Audio content written to file "{output_file}"')




# %% [markdown]
# ---
# ## Main Script
# 

# %%
#audio_path = "/Users/sharon/Downloads/acts/acts17(part2).mp3"  # or .wav/.m4a, etc.
def main(audio_file_path: str):
    """Takes an audio file path and returns translated audio path."""
    output_file = transcribe_file_and_dub(audio_file_path)
    
    os.makedirs("transalted_audios", exist_ok=True)

    # Create a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"outputs/translated_{timestamp}.mp3"
    return output_file

if __name__ == "__main__":
    # Keep this for running locally
    test_file = "/Users/sharon/Desktop/audio.m4a"
    output = main(test_file)
    print(f"Translated audio saved at: {output}")

