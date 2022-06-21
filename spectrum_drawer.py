import librosa
import librosa.display
import matplotlib.pyplot as plt


def convert_audio_to_spectogram(filename, savetofile):
    """
    convert_audio_to_spectogram -- using librosa to simply plot a spectogram

    Arguments:
    filename -- filepath to the file that you want to see the waveplot for

    Returns -- None
    """

    # sr == sampling rate
    x, sr = librosa.load(filename, sr=44100)

    # stft is short time fourier transform
    X = librosa.stft(x)

    # convert the slices to amplitude
    Xdb = librosa.amplitude_to_db(abs(X))

    # ... and plot, magic!
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis="time", y_axis="hz")
    plt.colorbar()
    plt.savefig(savetofile)
