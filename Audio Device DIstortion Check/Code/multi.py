import sounddevice
import soundfile
import threading
import os
import wave
import contextlib
from scipy.io import wavfile
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment

DATA_TYPE = "float32"


def get_file_duration(path):
    with contextlib.closing(wave.open(path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def increase_volume(path, vol_change):
    louder = AudioSegment.from_wav(path) + vol_change
    louder.export(path, format='wav')


def equalize_file_times(command_path, background_path):
    print(command_path)
    command_duration = get_file_duration(command_path)
    # background_duration = get_file_duration(background_path)
    # sampleRate, waveData = wavfile.read(background_path)
    # endSample = int(command_duration * sampleRate)
    # wavfile.write("background_noise.wav", sampleRate, waveData[0:endSample])
    print("background path:" + background_path)
    ffmpeg_extract_subclip(background_path, 0, command_duration, targetname="background_noise.wav")


def load_sound_file_into_memory(path):
    audio_data, _ = soundfile.read(path, dtype=DATA_TYPE)
    return audio_data


def get_device_number_if_usb_soundcard(index_info):
    """
    Given a device dict, return True if the device is one of our USB sound cards and False if otherwise
    :param index_info: a device info dict from PyAudio.
    :return: True if usb sound card, False if otherwise
    """

    index, info = index_info

    if "USB Audio Device" in info["name"]:
        return index
    return False


def play_wav_on_index(audio_data, stream_object):

    stream_object.write(audio_data)


def create_running_output_stream(index):

    output = sounddevice.OutputStream(
        device=index,
        dtype=DATA_TYPE
    )
    output.start()
    return output


def init_multi_play(human_path, noise_path, volume, human_speaker_index="1", noise_speaker_index="5", multiple=True):
    if multiple:
        equalize_file_times(human_path, noise_path)
        print(volume)
        increase_volume("background_noise.wav", volume)
        sound_file_paths = [
            human_path, "background_noise.wav"
        ]

        files = [load_sound_file_into_memory(path) for path in sound_file_paths]

        # usb_sound_card_indices = list(filter(lambda x: x is not False,
        #                                     map(get_device_number_if_usb_soundcard,
        #                                         [index_info for index_info in enumerate(sounddevice.query_devices())])))

        # print("Discovered the following usb sound devices", usb_sound_card_indices)
        usb_sound_card_indices = [3, 3]
        streams = [create_running_output_stream(index) for index in usb_sound_card_indices]

        # running = True

        if not len(streams) > 0:
            running = False
            print("No audio devices found, stopping")

        if not len(files) > 0:
            running = False
            print("No sound files found, stopping")

            print("Playing files")

        threads = [threading.Thread(target=play_wav_on_index, args=[file_path, stream])
                   for file_path, stream in zip(files, streams)]

        try:

            for thread in threads:
                thread.start()

            for thread, device_index in zip(threads, usb_sound_card_indices):
                print("Waiting for device", device_index, "to finish")
                thread.join()

        except KeyboardInterrupt:
            print("Stopping stream")
            for stream in streams:
                stream.abort(ignore_errors=True)
                stream.close()
            print("Streams stopped")
    else:
        file = load_sound_file_into_memory("background_noise.wav")
        stream = create_running_output_stream(1)
        play_wav_on_index(file, stream)
