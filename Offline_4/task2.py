import numpy as np
import time
import matplotlib.pyplot as plt

# DFT Implementation
def dft(signal):
    n = len(signal)
    X = np.zeros(n, dtype=complex)
    for k in range(n):
        for j in range(n):
            X[k] += signal[j] * np.exp(-2j * np.pi * k * j / n)
    return X

# IDFT Implementation
def idft(X):
    n = len(X)
    x = np.zeros(n, dtype=complex)
    for k in range(n):
        for j in range(n):
            x[k] += X[j] * np.exp(2j * np.pi * k * j / n)
    return x / n

# FFT Implementation (Cooley-Tukey)
def fft(signal):
    n = len(signal)
    if n <= 1:
        return signal
    even = fft(signal[0::2])  # Recursive FFT on even-indexed terms
    odd = fft(signal[1::2])   # Recursive FFT on odd-indexed terms
    terms = np.exp(-2j * np.pi * np.arange(n) / n)  # Twiddle factors
    return np.concatenate([even + terms[:n // 2] * odd,
                           even - terms[:n // 2] * odd])

# IFFT Implementation
def ifft(X):
    n = len(X)
    if n <= 1:
        return X
    even = ifft(X[0::2])  # Recursive IFFT on even-indexed terms
    odd = ifft(X[1::2])   # Recursive IFFT on odd-indexed terms
    terms = np.exp(2j * np.pi * np.arange(n) / n)  # Conjugated twiddle factors
    result = np.concatenate([even + terms[:n // 2] * odd,
                             even - terms[:n // 2] * odd])
    return result / n  # Normalize by dividing by the number of samples

# Compare DFT and FFT
def compare_dft_fft():
    sizes = [2**k for k in range(2, 11)]  # n = 4, 8, 16, ..., 1024
    dft_times = []
    fft_times = []

    for n in sizes:
        signal = np.random.rand(n)

        # Measure DFT runtime
        dft_start = time.time()
        for _ in range(10):  # Run 10 times
            _ = dft(signal)
        dft_end = time.time()
        dft_times.append((dft_end - dft_start)/10)

        # Measure FFT runtime
        fft_start = time.time()
        for _ in range(10):  # Run 10 times
            _ = fft(signal)
        fft_end = time.time()
        fft_times.append((fft_end - fft_start)/10)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, dft_times, label="DFT Runtime", marker='o')
    plt.plot(sizes, fft_times, label="FFT Runtime", marker='x')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Average Runtime (seconds)")
    plt.title("Runtime Comparison of DFT and FFT")
    plt.legend()
    plt.grid(True)
    plt.show()

# Compare IDFT and IFFT
def compare_idft_ifft():
    sizes = [2**k for k in range(2, 11)]  # n = 4, 8, 16, ..., 1024
    idft_times = []
    ifft_times = []

    for n in sizes:
        # Generate a random signal and its Fourier transform
        signal = np.random.rand(n) + 1j * np.random.rand(n)  # Complex signal
        transform = fft(signal)  # Use our FFT implementation

        # Measure IDFT runtime
        idft_start = time.time()
        for _ in range(10):  # Run 10 times
            _ = idft(transform)
        idft_end = time.time()
        idft_times.append((idft_end - idft_start)/10)

        # Measure IFFT runtime
        ifft_start = time.time()
        for _ in range(10):  # Run 10 times
            _ = ifft(transform)
        ifft_end = time.time()
        ifft_times.append((ifft_end - ifft_start)/10 )

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, idft_times, label="IDFT Runtime", marker='o')
    plt.plot(sizes, ifft_times, label="IFFT Runtime", marker='x')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Average Runtime (seconds)")
    plt.title("Runtime Comparison of IDFT and IFFT")
    plt.legend()
    plt.grid(True)
    plt.show()

# Call both functions
compare_dft_fft()
compare_idft_ifft()
