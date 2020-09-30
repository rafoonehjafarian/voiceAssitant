"""
In this module, the functions for speech recognition are provided;

"""
import speech_recognition as sr
import pyaudio
import wave
import yaml
import win32com.client
import config

r = None
p = None
config_file = './config/config.yaml'



def fetch_audio():
    """
    using  PyAudio class from pyaudio package, This function records a single phrase from microphone (as source).
    This is done by waiting until the audio has an energy above ``recognizer_instance.energy_threshold`` (the user has started speaking),
    and then recording until it encounters ``recognizer_instance.pause_threshold`` seconds of non-speaking or there is no more audio input.
    The ending silence is not included.

    :return: ``AudioData`` instance.The raw audio data is specified by ``frame_data``, which is a sequence of bytes representing audio samples.

    """
    global r
    r = sr.Recognizer()
    global p
    p = pyaudio.PyAudio()
    with sr.Microphone(device_index=1) as source:
        print(p.get_device_info_by_host_api_device_index(0, 1).get('name'))
        print("Say something!")
        text_to_speech("Say something!")
        audio = r.listen(source, phrase_time_limit=8)
    return audio


def recognition_witai(audio):

    """
    using wit.ai API key, this function employs NLP service provided by wit.ai. and convert audio data into
    scentence.

    :param audio: the audio instance
    :return: the
    """
    WIT_AI_KEY = "STZCUNIDUQJJZ4FXIAHLKAEARFEW475A"
    try:
        print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
        return r.recognize_wit(audio, key=WIT_AI_KEY)
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

def text_to_speech(text):
    """
    converts text to speech.
    :param text: string to be read out
    """
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def available_source():

    """
    checks out the devices that can be used as microphone for pyaudio.
    :return: the name and the index of the available microphones
    """
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


def save_audio_to_wav():
    """
    This function record audio from a microphone (blocking i.e. the program waits until the audio is recorded before anything else happens),
    and writing that data to a .wav file in Python with PyAudio.
    """
    with open(config_file) as f:
        conf = yaml.load(f)
    config = conf['info']
    FORMAT = pyaudio.paInt16  # data type formate
    CHANNELS = config['CHANNELS']  # Adjust to your number of channels
    RATE = config['RATE'] # Sample Rate
    CHUNK =  config['CHUNK']# Block Size
    RECORD_SECONDS = config['RECORD_SECOND'] # Record time
    WAVE_OUTPUT_FILENAME = config['WAVE_OUTPUT_FILENAME']

    # Startup pyaudio instance
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    # Record for RECORD_SECONDS
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Write your new .wav file with built in Python 3 Wave module
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()



