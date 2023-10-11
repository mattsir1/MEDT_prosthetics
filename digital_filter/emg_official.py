import matplotlib.pyplot as plt

import scipy
from scipy import signal
from scipy.fft import rfft, rfftfreq
from scipy.signal import savgol_filter

import numpy as np
from numpy.fft import fft


time = [] # list of times
raw_eeg = [] # volts

# sample rate for filters and duration of sample
sample_rate = 1000
duration = 12

# takes input arduino data file (2 columns, values separated by space) and gathers the data from it
# it also corrects the DC offset of the signal
# there is also a file that collects data straight from arduino to Python
def read_and_make_lists():

    # need this to change the global variables within a function
    global time
    global raw_eeg
    
    # open the file - sometimes there's weird errors, just ignore those
    f = open('emg1.txt',"r",errors = "ignore")

    data = f.readlines()


    # append the float data to a list called raw_eeg (and if the value is giving an error or its not a float for some reason, ignore it)
    # and also make a set of x values corresponding to the number of datapoints if an eeg value was appended
    time_index = 0
    for i in range(len(data)): 
        try:
            raw_eeg.append(float(data[i]))
            time.append(time_index)
            time_index += 1
        except:
            continue

    print("Number of Points: " + str(len(raw_eeg)))

    # now correct the DC offset by subtracting each value from the mean
    offset = np.mean(raw_eeg)
    print("DC Offset = " + str(offset))
    raw_eeg = raw_eeg - np.mean(raw_eeg)


# generic plot the magnitude and frequency spectra of given signal and its fft data
# feed in the x,y,title, xlab, and ylab for each
def plots(mag_x, mag_y, mag_title, mag_xlab, mag_ylab, fft_x, fft_y, fft_title, fft_xlab, fft_ylab):

    # plot the magnitude spectrum first (time on x, mag on y)
    # then plot 2 frequency spectrums, one of the full single-side freqs (half the fft freqs), 
    # and one of 0-100 for easier analysis
    fig, axs = plt.subplots(3,1)

    plt.draw()

    axs[0].plot(mag_x, mag_y)
    axs[0].set_title(mag_title)
    axs[0].set_ylabel(mag_ylab)
    axs[0].set_xlabel(mag_xlab)
    axs[0].set_xlim([0, max(mag_x)])
    axs[0].set_ylim([min(mag_y), max(mag_y)])
    
    axs[1].plot(fft_x, fft_y)
    axs[1].set_title(fft_title)
    axs[1].set_ylabel(fft_ylab)
    axs[1].set_xlabel(fft_xlab)
    axs[1].set_xlim([0, max(fft_x)/2])
    axs[1].set_ylim([0, max(fft_y)])

    axs[2].plot(fft_x, fft_y)
    axs[2].set_title(fft_title)
    axs[2].set_ylabel(fft_ylab)
    axs[2].set_xlabel(fft_xlab)
    axs[2].set_xlim([0, 20])
    axs[2].set_ylim([0, max(fft_y)])

    fig.tight_layout(pad=1.0)

    plt.show()

# does the fft of a signal and returns the x (freq) and y (power/magnitude) data for plotting
def do_fft(signal):
    
    print("Computing FFT ...")
    # compute the FFT
    power = fft(signal)

    # make the frequency band
    N = len(power)
    n = np.arange(N)
    T = N/sample_rate
    freq = n/T 

    return [freq,power]

# performs a butterworth highpass filter
def butter_highpass(data, order, cutoff, fs):
    
    # set the nyquist to half the sampling frequency, and divide the cutoff by the nyquist
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)

    y = signal.filtfilt(b, a, data)
    return y

# performs a butterworth lowpass filter
def butter_lowpass(data, order, cutoff, fs):

    # set the nyquist to half the sampling frequency, and divide the cutoff by the nyquist
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)

    y = signal.filtfilt(b, a, data)
    return y

# performs a butterworth bandpass filter
def butter_bandpass(data, order, lowcut, highcut, fs):
    
    # set the nyquist to half the sampling frequency, and divide the cutoffs by the nyquist
    nyq = 0.5 * fs
    b, a = signal.butter(order, [lowcut/nyq, highcut/nyq], btype='Bandpass', analog=False)

    y = signal.filtfilt(b, a, data)
    return y


def main():

    # read the text file and gather the appropriate data
    print("reading and making lists...")
    read_and_make_lists()

    
    # print the orignal data and its FFT
    [freq, power] = do_fft(raw_eeg)

    plots(time, raw_eeg,"Raw EMG Magnitude v Time","Time (s)","EMG Magnitude (mV)", 
         freq[1:], power[1:], "EMG Magnitude v Frequency","Frequency (Hz)","EMG Magnitude")
    
    # perform the bandpass filter
    print("creating bandpass filter...")
    bandpass_emg = butter_bandpass(raw_eeg, 8, 10, 100, 1000)

    # make the fft of the bandpass data for plotting
    [freq_b,power_b] = do_fft(bandpass_emg)
    
    # plot bandpassed signal and fft
    plots(time, bandpass_emg,"EMG Magnitude v Time w Bandpass = 10Hz to 400Hz","Time (s)","EMG Magnitude (mV)", 
         freq_b[1:], power_b[1:], "EMG Magnitude v Frequency w Bandpass = 10Hz to 400Hz","Frequency (Hz)","EMG Magnitude")

    print("now, rectify the signal to create an envelope")


    # pass rectified (absolute value) signal into a lowpass filter to create envelope
    # create and plot envelope data and fft of envelope
    print("enveloping signal ...")
    envelope_emg = butter_lowpass(abs(bandpass_emg), 8, 3, 1000)
    [freq_e,power_e] = do_fft(envelope_emg)

    plots(time, abs(envelope_emg),"EMG Magnitude v Time w Bandpass [10,400] Enveloped @ 3Hz","Time (s)","EMG Magnitude (mV)",
        freq_e[1:], power_e[1:], "EMG Magnitude v Frequency w Bandpass = 10Hz to 400Hz","Frequency (Hz)","EMG Magnitude")

    
    
main()






