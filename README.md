# Audio Translator
Being a divoted christian and only software daughter in the family, I take responsibility to bring the best sermons from all over the world to my mom.   
I am making a AI Website that will traslate audio sermons to Telugu but eventually making it translate into any language. Stay tuned and check the latest version. 

### When Cloning : create .env file and add openai & google could api key. Then execute app_gradio.py file to launch the webpage. 

## Version 2 
Uses 2 different AI platforms to translate audio. 

### They are:

Chatgpt: Transcribes(Whisper AI) & Translates text to target language 

Google text-to-speech: Produces highquality audio from the translated text. 

### Improvemets Possible:

OpenAI has a limit of 25mb in 1 go, hence need to change the code to process audio >25mb by breaking down into segments. 

Add front end.

## Version 1 
Uses 3 different AI platforms to translate audio. 

### They are:

Assembly AI: Converts audio to text.

Chatgpt: Translates text to target language 

ElevenLabs: Produces audio from the translated text. 

### Improvemets Possible:

Make Chatgpt convert audio to text to make application much simpler. 

Audio produced through code is much lower quality than the app. Work on improving that.

Add front end.


