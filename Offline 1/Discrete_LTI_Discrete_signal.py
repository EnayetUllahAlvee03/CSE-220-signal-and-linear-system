import math
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_the_impulse_with_coef(plot_title,impulses,coeffs,INF,sum_signal,subplot_sign,output_file,continuous=False):
    fig, axs = plt.subplots(4, 3, figsize=(12, 12), constrained_layout=True)
    # Flatten the 2D array of axes for easier indexing
    axs = axs.flatten()
    fig.suptitle(plot_title, fontsize=16)
    # Plot each impulse multiplied by its coefficient
    for i, (impulse, coef) in enumerate(zip(impulses, coeffs)):
        # Scale impulse by coefficient
        # scaled_impulse = impulse.multiply_const_factor(coef)
        
        # Add scaled impulse to sum signal
        # sum_signal = sum_signal.add(scaled_impulse)
        
        # Plot the scaled impulse in the i-th subplot
        axs[i].stem(range(-impulse.INF, impulse.INF + 1), impulse.values, basefmt=" ")
        if(continuous==False):
            axs[i].set_title(f"{subplot_sign}[n-({i-INF})]x[{i-INF}]")
        else:
            axs[i].set_title(f"{subplot_sign}[t-({i-INF}Δ)]x[{i-INF}]")
        axs[i].set_xlabel("n (Time Index)")
        axs[i].set_ylabel("x[n]")
        # axs[i].set_yticks(np.arange(-1, 5, 1))
        axs[i].set_xticks(np.arange(-INF, INF + 1, 1))
        # axs[i].set_yticks(np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1))

    # Plot the sum signal in the last subplot
    axs[-1].stem(range(-sum_signal.INF, sum_signal.INF + 1), sum_signal.values, basefmt=" ")
    axs[-1].set_title("Sum")
    axs[-1].set_xlabel("n (Time Index)")
    axs[-1].set_ylabel("x[n]")
    # axs[-1].set_yticks(np.arange(-1, 5, 1))
    axs[-1].set_xticks(np.arange(-INF, INF + 1, 1))

    # Hide any unused subplots
    # for j in range(i + 1, len(axs)):
    #     axs[j].axis('off')

    # Save the complete plot
    output_folder = "discrete_plots"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(f"{output_folder}/{output_file}")
    plt.close(fig)
    # plt.show()
    

class DiscreteSignal:
    def __init__(self, INF):
        self.INF = INF
        self.values = np.zeros(2 * INF + 1)

    def set_value_at_time(self, time, value):
        index = time + self.INF
        if 0 <= index < len(self.values):
            self.values[index] = value

    def shift(self, shift):
        shifted_signal = DiscreteSignal(self.INF)
        shifted_signal.values = np.roll(self.values, shift)
        return shifted_signal

    def add(self, other):
        new_signal = DiscreteSignal(self.INF)
        new_signal.values = self.values + other.values
        return new_signal

    def multiply(self, other):
        new_signal = DiscreteSignal(self.INF)
        new_signal.values = self.values * other.values
        return new_signal

    def multiply_const_factor(self, scaler):
        new_signal = DiscreteSignal(self.INF)
        new_signal.values = self.values * scaler
        return new_signal

    def plot(self, title="Discrete Signal", folder="discrete_plots", filename="signal.png"):
        x_values = range(-self.INF, self.INF + 1)
        plt.stem(x_values, self.values, basefmt=" ")
        plt.title(title)
        plt.xlabel("n (Time Index)")
        plt.ylabel("x[n]")
        
        # Set x-ticks at every integer position
        plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1))
        
        # Set y-ticks at every integer position, or customize range if needed
        y_min, y_max = min(self.values), max(self.values)
        plt.yticks(np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1))
        # plt.yticks(np.arange(-1,5,1))
        # Ensure output directory exists
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        plt.savefig(f"{folder}/{filename}")
        plt.close()



class LTI_Discrete:
    
    def __init__(self, impulse_response):
        self.impulse_response = impulse_response  #this will be an discrete signal

    def linear_combination_of_impulses(self, input_signal):
        impulses, coefficients = [], []
        for i, value in enumerate(input_signal.values):
                impulses.append(self.impulse_response.shift(i - self.impulse_response.INF))
                coefficients.append(value)
        return impulses, coefficients

    def output(self, input_signal):
        # print("Input Signal _x:",input_signal.values)
        # print("Impulse Response_h:",self.impulse_response.values)
        #impulses: list of DiscreteSignal objects
        impulses, coefficients = self.linear_combination_of_impulses(input_signal)
        out_impulses,out_coefficients = [], []
        output_signal = DiscreteSignal(self.impulse_response.INF)

        # print(impulses)
        # print("coef: ", coefficients)
        # print(len(impulses),len(coefficients))
        inf=self.impulse_response.INF
        # print("inf value: ",inf)
        i=0
        for impulse, coef in zip(impulses, coefficients):
            # print("i: ",i);i+=1
            # print("impulse_ values: ",impulse.values)
            scalled_impulse=(impulse.multiply_const_factor(coef))
            out_impulses.append(scalled_impulse)
            out_coefficients.append(coef)
            # print("scalled_impulse: ",scalled_impulse.values)
            # shifted_impulse_h=self.impulse_response.shift(i-inf)
            output_signal = output_signal.add(scalled_impulse)
        # print("Output Signal:")
        # print(output_signal.values)
        print(type(output_signal))
        return output_signal,out_impulses,out_coefficients