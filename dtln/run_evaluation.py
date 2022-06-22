"""
Script to process a folder of .wav files with a trained DTLN model. 
This script supports subfolders and names the processed files the same as the 
original. The model expects 16kHz audio .wav files. Files with other 
sampling rates will be resampled. Stereo files will be downmixed to mono.
"""

import os
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from dtln.dtln import DTLN_model
from spectrum_drawer import convert_audio_to_spectogram


def process_file(
    model, audio_file_name, out_file_name, is_draw_spectrum: bool, is_sr_changed: bool
):
    """
    Funtion to read an audio file, rocess it by the network and write the
    enhanced audio to .wav file.

    Parameters
    ----------
    model : Keras model
        Keras model, which accepts audio in the size (1,timesteps).
    audio_file_name : STRING
        Name and path of the input audio file.
    out_file_name : STRING
        Name and path of the target file.

    """

    # read audio file with librosa to handle resampling and enforce mono
    in_data, fs = librosa.core.load(audio_file_name, sr=16000, mono=True)
    # get length of file
    len_orig = len(in_data)
    # pad audio
    zero_pad = np.zeros(384)
    in_data = np.concatenate((zero_pad, in_data, zero_pad), axis=0)
    # predict audio with the model
    predicted = model.predict_on_batch(
        np.expand_dims(in_data, axis=0).astype(np.float32)
    )
    # squeeze the batch dimension away
    predicted_speech = np.squeeze(predicted)
    predicted_speech = predicted_speech[384 : 384 + len_orig]
    # write the file to target destination
    sf.write(out_file_name, predicted_speech, fs)

    if is_sr_changed:
        f_data, fs = librosa.core.load(out_file_name, sr=8000, mono=True)
        sf.write(out_file_name, f_data, fs)

    if is_draw_spectrum:
        save_path = Path(out_file_name)
        convert_audio_to_spectogram(
            audio_file_name, save_path.with_name(save_path.stem + "_before.png")
        )
        convert_audio_to_spectogram(
            out_file_name, save_path.with_name(save_path.stem + "_after.png")
        )


def process_folder(
    model, folder_name, new_folder_name, is_draw_spectrum, is_sr_changed
):
    """
    Function to find .wav files in the folder and subfolders of "folder_name",
    process each .wav file with an algorithm and write it back to disk in the
    folder "new_folder_name". The structure of the original directory is
    preserved. The processed files will be saved with the same name as the
    original file.

    Parameters
    ----------
    model : Keras model
        Keras model, which accepts audio in the size (1,timesteps).
    folder_name : STRING
        Input folder with .wav files.
    new_folder_name : STRING
        Traget folder for the processed files.

    """

    # empty list for file and folder names
    file_names = []
    directories = []
    new_directories = []
    # walk through the directory
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            # look for .wav files
            if file.endswith(".wav"):
                # write paths and filenames to lists
                file_names.append(file)
                directories.append(root)
                # create new directory names
                new_directories.append(root.replace(folder_name, new_folder_name))
                # check if the new directory already exists, if not create it
                if not os.path.exists(root.replace(folder_name, new_folder_name)):
                    os.makedirs(root.replace(folder_name, new_folder_name))
    # iterate over all .wav files
    for idx in range(len(file_names)):
        # process each file with the model
        process_file(
            model,
            os.path.join(directories[idx], file_names[idx]),
            os.path.join(new_directories[idx], file_names[idx]),
            is_draw_spectrum,
            is_sr_changed,
        )
        print(file_names[idx] + " processed successfully!")


def run_process(
    in_folder, out_folder, trained_model_path, is_draw_spectrum, is_sr_changed
):
    model_obj = DTLN_model()
    model_obj.build_DTLN_model()
    model_obj.model.load_weights(trained_model_path)
    process_folder(
        model_obj.model, in_folder, out_folder, is_draw_spectrum, is_sr_changed
    )
