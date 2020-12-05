import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import normalize
from IPython.display import Audio
from playsound import playsound
import numpy as np


def morseAudioToText(audio, optn = 'alphanumeric'):
    playsound('morse.wav')  # plays the morse code sound

    Fs, data = read(audio)  # the function read() returns the sampling frequency (here 44100 Hz, which is the standard for most
    # audio) and the data from the wav file

    data = data[:, 0]  # only taking one channel because the sound is stereo

    finalCode = ''
    t = 0  # variable to iterate over the length where there is a pulse7
    # (ie a "dit" or a "dat")
    j = 0  # variable to iterate over the length of the silence (ie the space between letters or words)

    def hl_envelopes_idx(s, dmax=20):  # function to get envelope of the data since the raw data had fluctuations
        # because of the sinusoidal nature of sound waves and produced inconsistencies which affected the result
        lmax = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[0] + 1

        lmax = lmax[[i + np.argmax(s[lmax[i:i + dmax]]) for i in range(0, len(lmax), dmax)]]

        return lmax

    s = data
    high_idx = hl_envelopes_idx(s)

    tao = np.linspace(0, 1, len(s))
    plt.plot(tao, s, 'b')  # plotting the data on a normalized scale
    plt.plot(tao[high_idx], s[high_idx], 'r')  # here we plot the envelope of the signal to visualize it to know
    # the ranges of t and j
    plt.show()
    envelope = s[high_idx]
    for i in range(0, len(envelope)):  # looping the values of the envelope of data
        if abs(envelope[i]) > 4000:  # if the magnitude of data becomes greater than 4000, then there is a pulse
            t += 1  # we increment t because there is a pulse
            if j > 110:  # here we check previous entry for j, if > 110 then definitely it is the spacing between words
                finalCode += "   "
                j = 0  # we reset j so we get the value for next silence
            elif 50 < j < 110:  # if j is in this range then it is the space between letters
                finalCode += " "
                j = 0
            elif j < 50:  # if there is a silence, but it is only to differentiate the "dits" and "dats" and not words
                # and letters, we do nothing and reset j
                j = 0

        if abs(envelope[i]) < 1000:  # if magnitude of data is < 1000, it is definitely silence and there is no pulse
            j += 1  # we increment j because there is silence

            if t > 7:  # if t > 7 then it is definitely a long pulse, a "dat" or "-"
                finalCode += "-"  # we add a dash to signify the long pulse "dat"
                t = 0  # we set t = 0 to check the pulse after it has finished

            elif 7 > t > 1:  # if t is < 7 but > 1 then there is definitely a short pulse, a "dit" or "."
                finalCode += "."  # we add a dot to signify the short pulse "dit"
                t = 0

    Morse1 = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h',
              '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
              '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
              '-.--': 'y', '--..': 'z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
              '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0', '--..--': ', ',
              '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')'}
    # python dictionary to convert morse to alphanumeric

    recoveredMsg = ''
    sentence = finalCode.split('   ')  # split the words where there is 3 spaces
    for word in sentence:
        for letter in word.split(' '):  # split the letters in the word
            if letter not in Morse1.keys():  # avoids errors
                continue
            recoveredMsg += Morse1[letter]
        recoveredMsg += ' '  # adds a space after the word
    if optn == 'morse' or optn == 'Morse':
        return finalCode
    elif optn == 'alphanumeric' or optn == 'Alphanumeric':
        return recoveredMsg
