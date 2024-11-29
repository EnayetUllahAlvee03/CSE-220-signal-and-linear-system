import numpy as np
import matplotlib.pyplot as plt
n=50
samples = np.arange(n) 
sampling_rate=100
wave_velocity=8000



#use this function to generate signal_A and signal_B with a random shift
def generate_signals(frequency=5):

    noise_freqs = [15, 30, 45]  # Default noise frequencies in Hz

    amplitudes = [0.5, 0.3, 0.1]  # Default noise amplitudes
    noise_freqs2 = [10, 20, 40] 
    amplitudes2 = [0.3, 0.2, 0.1]
    
     # Discrete sample indices
    dt = 1 / sampling_rate  # Sampling interval in seconds
    time = samples * dt  # Time points corresponding to each sample

    # Original clean signal (sinusoidal)
    original_signal = np.sin(2 * np.pi * frequency * time)

    # Adding noise
    noise_for_sigal_A = sum(amplitude * np.sin(2 * np.pi * noise_freq * time)
                for noise_freq, amplitude in zip(noise_freqs, amplitudes))
    noise_for_sigal_B = sum(amplitude * np.sin(2 * np.pi * noise_freq * time)
                for noise_freq, amplitude in zip(noise_freqs2, amplitudes2))
    signal_A = original_signal + noise_for_sigal_A 
    noisy_signal_B = signal_A + noise_for_sigal_B

    # Applying random shift
    shift_samples = np.random.randint(-n // 2, n // 2)  # Random shift
    print(f"Shift Samples: {shift_samples}")
    signal_B = np.roll(noisy_signal_B, shift_samples)
    
    return signal_A, signal_B
#implement other functions and logic

#plot the signals
def plot_original_signal(signal, title, color):
   
    plt.figure(figsize=(5, 6))
    plt.stem(samples, signal, linefmt=color, markerfmt=color, basefmt=" ")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.show()

def plot_magnitude_spectrum(dft_signal, title, color):
    magnitudes = np.abs(dft_signal)
    plt.figure(figsize=(8, 6))
    plt.stem(np.arange(n), magnitudes, linefmt=color, markerfmt=color, basefmt=" ")
    plt.xlabel("Frequency Bin")
    plt.ylabel("Magnitude")
    plt.title(title)
    plt.show()


    


signal_A,signal_B=generate_signals()
plot_original_signal(signal_A, "Signal A", "b")
plot_original_signal(signal_B, "Signal B", "r")






