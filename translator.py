rom dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment  
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


# Split audio into chunks if larger than 25MB
def split_audio(file_path, chunk_length_ms=600000):  # 10 min = 600000 ms
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunk_name = f"chunk_{i//chunk_length_ms}.mp3"
        chunk.export(chunk_name, format="mp3")
        chunks.append(chunk_name)
    return chunks


def transcribe_file_and_dub(audio_file_path: str):
    # Check file size
    file_size_mb = os.path.getsize(audio_file_path) / (1024 * 1024)

    if file_size_mb > 25:
        print(f"⚠️ File is {file_size_mb:.2f} MB, splitting into chunks...")
        audio_files = split_audio(audio_file_path)
    else:
        audio_files = [audio_file_path]

    full_transcript = []

    # Process each chunk
    for idx, chunk_path in enumerate(audio_files):
        with open(chunk_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        text_block = response.text
        print(f"📝 Transcript from chunk {idx}: {text_block[:50]}...")
        full_transcript.append(text_block)

    # Combine transcripts
    combined_text = " ".join(full_transcript)

    # Translate whole text at once
    translated_text = translate(combined_text, language="Telugu")

    # Save translated audio
    os.makedirs("translated_audios", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"translated_audios/translated_{timestamp}.mp3"

    text_to_speech(translated_text, output_path)
    return output_path


# TRANSLATION
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
    print("🌐 Translated:", translation[:100], "...")
    return translation


# GOOGLE TTS 
from google.cloud import texttospeech
from google.oauth2 import service_account
import json

# added to fix credentials not found error
creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not creds_json:
    raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable")

creds_dict = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(creds_dict)


tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
#

def text_to_speech(text, output_file):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="te-IN",
        name="te-IN-Chirp3-HD-Charon"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=["small-bluetooth-speaker-class-device"],
        speaking_rate=1.0,
    )
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'✅ Audio content written to file "{output_file}"')
        return output_file


# MAIN 
def main(audio_file_path: str):
    output_file = transcribe_file_and_dub(audio_file_path)
    return output_file

if __name__ == "__main__":
    test_file = "/Users/sharon/Desktop/audio.m4a"
    output = main(test_file)
    print(f"Translated audio saved at: {output}")
