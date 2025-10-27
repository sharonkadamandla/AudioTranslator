import gradio as gr
import os
from translator import main


def translate_audio(file):
    output_path = main(file)
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Expected output file at {output_path}, but it was not found.")
    
    return output_path, output_path  # this should be the audio file path

iface = gr.Interface(
    fn=translate_audio,
    inputs=gr.Audio(sources=["microphone", "upload"], type="filepath"),
    outputs=[
        gr.Audio(type="filepath", label="Play Translated Audio"),
        gr.File(label="Download Translated Audio")
    ],
    title="AI Speech Translator",
    description="Upload or record speech, and get translated audio back!"
)

if __name__ == "__main__":
    iface.launch()