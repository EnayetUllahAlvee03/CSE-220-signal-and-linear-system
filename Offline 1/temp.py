import math
import numpy as np
import matplotlib.pyplot as plt
import os


class ContinuousSignal:
    def __init__(self, func):
        self.func = func

    def shift(self, shift):
        return ContinuousSignal(lambda t: self.func(t - shift))

    def add(self, other):
        return ContinuousSignal(lambda t: self.func(t) + other.func(t))

    def multiply(self, other):
        return ContinuousSignal(lambda t: self.func(t) * other.func(t))

    def multiply_const_factor(self, scaler):
        return ContinuousSignal(lambda t: scaler * self.func(t))

    def plot(self, t_range=(-3, 3), title="Continuous Signal", filename="signal.png", ax=None):
        t = np.linspace(t_range[0], t_range[1], 500)
        y = self.func(t)

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.figure
        ax.plot(t, y)
        ax.set_title(title)
        ax.set_xlabel("Time (t)")
        ax.set_ylabel("Amplitude")
        ax.yaxis.set_ticks(np.arange(0, 1.5, .5))
        ax.grid=True
        if filename or ax is None:
            output_folder = "continuous_plots"
            # print("output_folder: ",output_folder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            fig.savefig(f"{output_folder}/{filename}")
            plt.close(fig)
    def plot_together(self, newsig, t_range=(-3, 3), title="Continuous Signal 2 signals", filename="signal.png", ax=None):
        fig, ax = plt.subplots()
        t = np.linspace(t_range[0], t_range[1], 500)
        y = self.func(t)
        y1 = newsig.func(t)
        ax.plot(t, y)
        ax.plot(t, y1)
        ax.set_title(title)
        ax.set_xlabel("Time (t)")
        ax.set_ylabel("Amplitude")
        ax.yaxis.set_ticks(np.arange(0, 1.5, .5))
        ax.grid=True
        if filename or ax is None:
            output_folder = "continuous_plots"
            # print("output_folder: ",output_folder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            fig.savefig(f"{output_folder}/{filename}")
            plt.close(fig)



class LTI_Continuous:
    def __init__(self, impulse_response):
        self.impulse_response = impulse_response

    def linear_combination_of_impulses(self, input_signal, delta, INF=5):
        t_values = np.arange(-INF, INF, delta)
        coefficients = [input_signal.func(t) for t in t_values]
        impulses = []
        
        for i, coef in enumerate(coefficients):
            # Create an impulse function centered at t = i * delta
            # impulse = ContinuousSignal(lambda t, idx=(i - INF/delta): np.where((t >= idx * delta) & (t < (idx * delta + delta)), 1 / delta, 0))
            impulse = ContinuousSignal(lambda t, idx=(i - INF/delta): np.where((t>=0)&(t<0+delta), 1 / delta, 0))
            # impulse.plot(t_range=(-INF, INF), title=f"δ(t-({i-INF/delta}∇))", filename=f"impulse{i-INF/delta}.png")
            # Shift the impulse to the correct time and append it to the list
            impulses.append(impulse.shift((i-INF/delta) * delta).multiply_const_factor(coef*delta))
        
        return impulses, coefficients


    def output_approx(self, input_signal, delta, INF=5):
        # Generate the impulses and their coefficients from the input signal
        print("delta: ", delta, "INF: ", INF)
        impulses, coefficients = self.linear_combination_of_impulses(input_signal, delta, INF)
        
        # Create the unit step function
        unit_step = ContinuousSignal(lambda t: np.where(t >= 0, 1, 0))
        unit_step.plot(t_range=(-INF, INF), title="u(t)", filename="unit_step.png")

        print("coeffs: ", len(coefficients))
        new_impulses = []
        output_signal = ContinuousSignal(lambda t: 0)
        
        # Plot each impulse response
        for i, coef in enumerate(coefficients):
            # Multiply the impulse by the unit step, shifted and scaled by the coefficient
            conti_f = unit_step.shift((i - INF / delta) * delta).multiply_const_factor(coef*delta)
            new_impulses.append(conti_f)
            output_signal = output_signal.add(conti_f)
            
            # Plot the impulse response
            # conti_f.plot(t_range=(-INF, INF), title=f"Response of Impulse {i-INF/delta}", filename=f"response_of_impulse_{i-INF/delta}.png")
        
        # Plot the final output signal
        # output_signal.plot(t_range=(-INF, INF), title="Output Signal", filename="output_signal.png")
        
        print("last of output approx")
        return output_signal, new_impulses
    
    

       
