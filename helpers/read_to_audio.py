import google.cloud.texttospeech as tts


def text_to_wav(text: str, filename_str: str, voice_name: str = "en-US-Standard-C"):
    """
    Read a specified segment of text into a .wav file using Google text-to-speech API.
    :param text: the specific text to be read
    :param filename_str: the file name under which the .wav file should be stored; this does not contain the .wav suffix
    :param voice_name: the name of the voice according to https://cloud.google.com/text-to-speech/docs/voices
    """
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{filename_str}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')


