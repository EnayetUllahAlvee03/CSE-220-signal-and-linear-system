import numpy as np
import matplotlib.pyplot as plt

INF = 8

def plot(
        signal, 
        title=None, 
        y_range=(-1, 3), 
        figsize = (8, 3),
        x_label='n (Time Index)',
        y_label='x[n]',
        saveTo=None
    ):
    plt.figure(figsize=figsize)
    plt.xticks(np.arange(-INF, INF + 1, 1))
    
    y_range = (y_range[0], max(np.max(signal), y_range[1]) + 1)
    # set y range of 
    plt.ylim(*y_range)
    plt.stem(np.arange(-INF, INF + 1, 1), signal)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    if saveTo is not None:
        plt.savefig(saveTo)
    # plt.show()

def init_signal():
    return np.zeros(2 * INF + 1)


def time_shift_signal(x : np.ndarray, k : int) -> np.ndarray:
    # implement this function
    x_time_shifted = np.roll(x,k)
    return x_time_shifted
    

# def time_scale_signal(signal, scale):
#     # Create an array to hold the scaled signal
#     x_time_scaled = np.zeros(2 * INF + 1)
    
#     # Split the signal into two halves
#     x_first_half = signal[:INF][::-1]  # Reverse the first half for negative time indices
#     x_second_half = signal[INF:]
    
#     # Scale both halves
#     x_first_half_scaled = x_first_half[::scale][::-1]  # Reverse back after scaling
#     x_second_half_scaled = x_second_half[::scale]
    
#     # Combine the scaled halves into the final scaled signal array
#     x_time_scaled[:len(x_first_half_scaled)] = x_first_half_scaled
#     x_time_scaled[INF:INF + len(x_second_half_scaled)] = x_second_half_scaled
    
#     return x_time_scaled


    
def time_scale_signal(x: np.ndarray, scale: int) -> np.ndarray:
    n = len(x)
    if scale == 0:
        return np.zeros(n)
    x_time_scaled = np.interp(np.linspace(0, n, scale*n+1), np.arange(n), x)
    return x_time_scaled
    


def main():
    img_root_path = '.'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root_path}/x[n].png')

    plot(time_shift_signal(signal, 2), title='x[n-2]', saveTo=f'{img_root_path}/x[n-2].png')
    
    plot(time_shift_signal(signal, -2), title='x[n+2]', saveTo=f'{img_root_path}/x[n+2].png')
    
    plot(time_shift_signal(signal, 0), title='x[n+0]', saveTo=f'{img_root_path}/x[n+0].png')
    
    plot(time_scale_signal(signal, 2 ), title='x[2n]', saveTo=f'{img_root_path}/x[2n].png')
    
    plot(time_scale_signal(signal, 1 ), title='x[1n]', saveTo=f'{img_root_path}/x[1n].png')
    
        

main()