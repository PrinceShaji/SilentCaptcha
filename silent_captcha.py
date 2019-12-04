#!/usr/bin/env python3
""" For labeling audio files and generating waveform image. """

import matplotlib.pyplot as plt
import numpy as np
import wave
import io
import shutil
from os import listdir, rename
from subprocess import call
from sys import argv

def SilentCaptcha(filename, save_image=True):
    wav_file = wave.open(filename, 'r')

    #Extract Raw Audio from Wav File
    signal = wav_file.readframes(-1)
    if wav_file.getsampwidth() == 1:
        signal = np.array(np.frombuffer(signal, dtype='UInt8')-128, dtype='Int8')
    elif wav_file.getsampwidth() == 2:
        signal = np.frombuffer(signal, dtype='Int16')
    else:
        raise RuntimeError("Unsupported sample width")

    # http://schlameel.com/2017/06/09/interleaving-and-de-interleaving-data-with-python/
    deinterleaved = [signal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())]

    #Get time from indices
    fs = wav_file.getframerate()
    Time=np.linspace(0, len(signal)/wav_file.getnchannels()/fs, num=len(signal)/wav_file.getnchannels())
    plt.figure(figsize=(50,3))
    plt.axis('off')

    for channel in deinterleaved:
        plt.plot(Time,channel, linewidth=3, color='black')

    # Saving file/returning file
    if save_image:
        output_fileneme = filename.split('.')[0]
        plt.savefig(output_fileneme)
    else:
        buff = io.BytesIO()
        plt.savefig(buff, format='png')
        # Loading from BytesIO object and returning the data in bytes.
        buff.seek(0)
        loaded_file = buff.getvalue()
        return loaded_file

def RenameAudio():

    def rename_files(renamed_list):
        for i in renamed_list:
            rename(i['old_name'], i['new_name'])
        exit()
        
    renamed_files = []
    for files in listdir():
        if files.endswith('.wav') and len(files.split('.')[0]) > 5:
            while True:
                call(['cvlc', '--play-and-exit', files])
                user_response = input()
                if user_response == '':
                    temp = {}
                    temp['old_name'] = files
                    temp['new_name'] = input('Enter CAPTCHA value: ') + '.wav'
                    renamed_files.append(temp)
                    break
                elif user_response == '\'':
                    continue
                elif user_response == 'q':
                    rename_files(renamed_files)
                else:
                    continue
    rename_files(renamed_files)

if __name__ == "__main__":

    if len(argv) > 0:
        if argv[1].lower().strip() == 'silentcaptcha':
            files = listdir()
            for i in files:
                if i.endswith('.wav') and len(i.split('.')[0]) == 5:
                    SilentCaptcha(i)
        elif argv[1].lower().strip() == 'renameaudio':
            RenameAudio()
    else:
        print('Specify which function to use.')
        exit()