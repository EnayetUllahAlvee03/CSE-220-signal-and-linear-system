
import numpy as np
import matplotlib.pyplot as plt


def parabolic_function(x):
    # return np.where(((x >= -3)  & (x <= -1)) | ((x >= 1)  & (x <= 3)), (abs(x)-3)**2, 0)
    arr1=np.where(((x >= -3)  & (x <= -1)) | ((x >= 1)  & (x <= 3)), (abs(x)-3)**2, 0)
    arr2=np.where((x>=-1) & (x <=0 ),5+x,0)
    arr3=np.where((x>=0) & (x <=1 ),5-x,0)
    return arr1+arr2+arr3
    

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


x_values = np.linspace(-10, 10, 1000)
y_values=parabolic_function(x_values)


plt.figure(figsize=(12, 6))
plt.plot(x_values, y_values, label=f"original function")
plt.title(f"OriginalFunction")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()


frequencies=np.linspace(-5,5,1000)
ft_signal=fourier_transform(y_values,frequencies,x_values)
magnitude = np.sqrt(ft_signal[0]**2 + ft_signal[1]**2)

plt.figure(figsize=(12, 4))
plt.plot(frequencies, magnitude, label=f"fourier transform function")
plt.title(f"FT signal")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()



#define f(t) square

f_t_square=np.square(y_values)
t_integral=np.trapz(f_t_square,x_values)

print(t_integral)

# plt.figure(figsize=(12, 4))
# plt.plot(t_integral, x_values, label=f"ft energy function")
# plt.title(f"ft energy")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.legend()
# plt.show()



f_f_square=(ft_signal[0]**2+ft_signal[1]**2)
f_integral=np.trapz(f_f_square,frequencies)
print(f_integral)

# plt.figure(figsize=(12, 4))
# plt.plot(f_integral, frequencies, label=f"ff energy function")
# plt.title(f"ff energy")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.legend()
# plt.show()

