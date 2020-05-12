from google.cloud import texttospeech
from google.cloud.texttospeech import enums

class GoogleCloudTTS(object):
    def __init__(self, language):
        self.language = language
        self.language_code='en-US'
        self.__init_language_code()
    
    def __init_language_code(self):
        if self.language == 'hi':
            self.language_code = 'hi-IN'
    

    ## Input --> One text file containing one sentence, One file containing multiple sentences delimited by new line, Similar for CSV
    
    def get_available_voices():
    """Lists the available voices."""

    client = texttospeech.TextToSpeechClient()

    voices = client.list_voices()

    available_voices = []
    voice_dict = []
    for voice in voices.voices:
        for language_code in voice.language_codes:
            if language_code == self.language_code :
                available_voices.append(voice)

                ssml_gender = enums.SsmlVoiceGender(voice.ssml_gender)

                local_voice = {'gender_name':ssml_gender.name, 'sample_rate': voice.natural_sample_rate_hertz}
                voice_dict.add(local_voice)
            
    return available_voices, voice_dict


            

    def synthesize_text(text, save_directory):
    """Synthesizes speech from the input file of text."""
    
    client = texttospeech.TextToSpeechClient()


    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)


    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
# [END tts_synthesize_text_file]


# [START tts_synthesize_ssml_file]
    def synthesize_ssml_file(ssml_file):
        """Synthesizes speech from the input file of ssml.
        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """
        from google.cloud import texttospeech
        client = texttospeech.TextToSpeechClient()

        with open(ssml_file, 'r') as f:
            ssml = f.read()
            input_text = texttospeech.types.SynthesisInput(ssml=ssml)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(input_text, voice, audio_config)

        # The response's audio_content is binary.
        with open('output.mp3', 'wb') as out:
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')