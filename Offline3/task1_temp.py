
import numpy as np
import matplotlib.pyplot as plt

def parabolic_function(x):
    return np.where((x >= -2) & (x <= 2), x**2, 0)

def triangular_function(x):
    return np.where((x >= -2) & (x <= 2), 1 - np.abs(x / 2), 0)

def sawtooth_function(x):
    return np.where((x >= -2) & (x <= 2), x / 2 + 1, 0)

def rectangular_function(x):
    return np.where((x >= -2) & (x <= 2), 1, 0)









def fourier_transform(signal, frequencies, sampled_times):
    num_freqs = len(frequencies)
    ft_result_real = np.zeros(num_freqs)
    ft_result_imag = np.zeros(num_freqs)
    dt = sampled_times[1] - sampled_times[0]  # Time step for integration
    
    for i, freq in enumerate(frequencies):
        cos_term = np.cos(2 * np.pi * freq * sampled_times)
        sin_term = -np.sin(2 * np.pi * freq * sampled_times)
        ft_result_real[i] = np.trapz(signal * cos_term, dx=dt)
        ft_result_imag[i] = np.trapz(signal * sin_term, dx=dt)
    
    return ft_result_real, ft_result_imag






# Inverse Fourier Transform 
def inverse_fourier_transform(ft_signal, frequencies, sampled_times):
    n = len(sampled_times)
    reconstructed_signal = np.zeros(n)
    # Reconstruct the signal by summing over all frequencies for each time in sampled_times.
    # use trapezoidal integration to calculate the real part
    # You have to return only the real part of the reconstructed signal

    for i, t in enumerate(sampled_times):
        real_ftSig = ft_signal[0]*np.cos(2*np.pi*frequencies*t)
        imag_ftSig = ft_signal[1]*np.sin(2*np.pi*frequencies*t)

        reconstructed_signal[i] = np.trapz(real_ftSig-imag_ftSig, frequencies)
    
    return reconstructed_signal



frequencies = np.linspace(-5, 5, 1000)  # Adjust frequency range for experimentation




# Define x values and sample each function
x_values = np.linspace(-10, 10, 1000)  # Sampling interval
functions = {
    "Parabolic": parabolic_function,
    # "Triangular": triangular_function,
    # "Sawtooth": sawtooth_function,
    # "Rectangular": rectangular_function,
}

print("typeof functions: ",type(functions))

for name, func in functions.items():
    y_values = func(x_values)
    plt.figure(figsize=(12, 4))
    plt.plot(x_values, y_values, label=f"{name} Function")
    plt.title(f"Original {name} Function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    
    # Fourier Transform and Frequency Spectrum
    sampled_times = x_values
    ft_data = fourier_transform(y_values, frequencies, sampled_times)
    magnitude = np.sqrt(ft_data[0]**2 + ft_data[1]**2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, magnitude)
    plt.title(f"Frequency Spectrum of {name} Function")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()
    
    # Inverse Fourier Transform and Reconstruction
    reconstructed_y_values = inverse_fourier_transform(ft_data, frequencies, sampled_times)
    plt.figure(figsize=(12, 4))
    plt.plot(x_values, y_values, label="Original", color="blue")
    plt.plot(sampled_times, reconstructed_y_values, label="Reconstructed", color="red", linestyle="--")
    plt.title(f"Original vs Reconstructed {name} Function")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()


