import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

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


def time_scale_signal(x: np.ndarray, k: int) -> np.ndarray:
   
    x_time_scaled = np.zeros(2 * INF + 1)
    x_time_scaled[INF] = x[INF]
    for i in range(-INF,0):
        temp=k*i #-8
        if(temp<-INF):
            x_time_scaled[i+INF] = 0
        
        x_time_scaled[INF+temp] = x[i+INF]
        
    for i in range(INF+1,2*INF+1):
        index=i-INF
        if(index*k <= INF):
            x_time_scaled[INF+index*k] = x[i]
        
    return x_time_scaled
    

def time_scale_signal_interpolate(x : np.ndarray, k : int) -> np.ndarray:
    # implement this function
    x_time_scaled = np.zeros(2 * INF + 1)
    x_time_scaled_1=time_scale_signal(x,k)
    for i in range(0,len(x_time_scaled_1)):
        for j in range(i,len(time_scale_signal(x,k))):
            if(x_time_scaled_1[j]==0):
                x_time_scaled_1[i]=x_time_scaled_1[j]
                
    None


def main():
    img_root = '.'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root}/x[n].png')
    plot(time_scale_signal(signal, 3), title='x[n/3]', saveTo=f'{img_root}/x[n divided by 3].png')
    plot(time_scale_signal(signal, 1), title='x[n/1]', saveTo=f'{img_root}/x[n divided by 1].png')
    # plot(time_scale_signal_interpolate(signal, 3), title='x[n/3] with interpolation', saveTo=f'{img_root}/x[n divided by 3]_with_interpolation.png')
    # plot(time_scale_signal_interpolate(signal, 1), title='x[n/1] with interpolation', saveTo=f'{img_root}/x[n divided by 1]_with_interpolation.png')

main()
