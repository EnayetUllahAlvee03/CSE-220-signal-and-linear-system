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
        axs[i].set_yticks(np.arange(-1, 5, 1))
        axs[i].set_xticks(np.arange(-INF, INF + 1, 1))

    # Plot the sum signal in the last subplot
    axs[-1].stem(range(-sum_signal.INF, sum_signal.INF + 1), sum_signal.values, basefmt=" ")
    axs[-1].set_title("Sum")
    axs[-1].set_xlabel("n (Time Index)")
    axs[-1].set_ylabel("x[n]")
    axs[-1].set_yticks(np.arange(-1, 5, 1))
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
        # plt.yticks(np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1))
        plt.yticks(np.arange(-1,5,1))
        # Ensure output directory exists
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        plt.savefig(f"{folder}/{filename}")
        plt.close()

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

        if filename or ax is None:
            output_folder = "continuous_plots"
            print("output_folder: ",output_folder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            fig.savefig(f"{output_folder}/{filename}")
            plt.close(fig)


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

class LTI_Continuous:
    def __init__(self, impulse_response):
        self.impulse_response = impulse_response #this will be an continuous signal

    def linear_combination_of_impulses(self, input_signal, delta,INF=5):
        t = np.arange(-INF, INF, delta)
        impulses=[]
        #impulses = [self.impulse_response.shift(i) for i in t] 
        coefficients = [input_signal.func(i)  for i in t]
        for i in range(len(t)):
            conti_f = ContinuousSignal(lambda t, c=coefficients, idx=(i - 6)*delta: np.where((t >= idx) & (t <= (idx + delta)),  c, 0))
            impulses.append(conti_f)
        return impulses, coefficients

    def output_approx(self, input_signal, delta):
        impulses, coefficients = self.linear_combination_of_impulses(input_signal, delta)
        def output_func(t):
            return sum(coef * impulse.func(t) for coef, impulse in zip(coefficients, impulses))
        return ContinuousSignal(output_func)

def main():
    INF = 5
    discrete_impulse = DiscreteSignal(INF)
    discrete_impulse.set_value_at_time(0, 1)
    lti_discrete = LTI_Discrete(discrete_impulse)

    discrete_impulse0 = DiscreteSignal(INF)
    h = LTI_Discrete(discrete_impulse0)

    discrete_input = DiscreteSignal(INF)
    for i in range(-INF, INF):
        if i == 0:
            discrete_input.set_value_at_time(i, 0.5)
        elif i == 1:
            discrete_input.set_value_at_time(i, 2)
        else:
            discrete_input.set_value_at_time(i, 0)
    discrete_input.plot(title="x[n]", filename="x[n].png")

    for i in range(-INF, INF):
        if i == 0 or i == 1 or i == 2:
            h.impulse_response.set_value_at_time(i, 1)
        else:
            h.impulse_response.set_value_at_time(i, 0)
    h.impulse_response.plot(title="h[n]", filename="h[n].png")

    # Assuming impulses and coeffs have already been computed
    impulses, coeffs = lti_discrete.linear_combination_of_impulses(discrete_input)
    sum_signal = DiscreteSignal(INF)
    for i in range(len(impulses)):
        sum_signal = sum_signal.add(impulses[i].multiply_const_factor(coeffs[i]))
        impulses[i].multiply_const_factor(coeffs[i])
    # print("sum signal: ",sum_signal.values)
    # print("coeffs: ",coeffs)
    
    
    # plot_the_impulse_with_coef("Impulses multiplied by coefficients",impulses,coeffs,INF,sum_signal,"δ","impulses_and_sum_grid.png")
    
    




    discrete_output,out_impulses,out_coeffs = h.output(discrete_input)
    # for i in range(len(out_impulses)):
    #     print("Impulse: ",out_impulses[i].values)
    #     print("Coefficient: ",out_coeffs[i])
    # print("Output Signal:",discrete_output.values)
    
    
    
    # plot_the_impulse_with_coef("Response of Input signal",out_impulses,out_coeffs,INF,discrete_output,"h","output_discrete.png")


    print("\ncontinuous signal starts here:\n")

    # discrete_output[1].plot(title="Outputalvee", filename="output_discrete.png")
    # Your main plotting code with subplots
    INF = 3

    conti_f = ContinuousSignal(lambda t: np.where((t < 0) | (t > 1), 0, 1))
    # Plot the signal
    conti_f.plot(t_range=(-2, 2), title="x(t)", filename="demosignal.png")



    continuous_impulse = ContinuousSignal(lambda t: np.where(t < 0, 0, np.exp(-t)))
    lti_continuous = LTI_Continuous(continuous_impulse)
    continuous_impulse.plot(t_range=(-INF, INF), title="x(t)", filename="x(t)_cont_input.png")

    delta = .5
    
    impulses, coeffs = lti_continuous.linear_combination_of_impulses(continuous_impulse, delta,INF=INF)


    print("impulses: ",impulses)
    print("coeffs: ",coeffs)    
    print(type(impulses))

    # Adjust epsilon to be small enough for an impulse-like signal
    epsilon = 0.001  

    cont_impulse_signals = []
    # for i, (impulse, coef) in enumerate(zip(impulses, coeffs)):
    #     conti_f = ContinuousSignal(lambda t: np.where((t>i) | (t<(i+1)), coef,0))
    #     conti_f.plot(t_range=(-INF, INF), title=f"δ(t-{i}Δ)x[{i}]", filename=f"cont_impulse_{i}.png")
    #     cont_impulse_signals.append(impulse.multiply(conti_f))




    # for i, (impulse, coef) in enumerate(zip(impulses, coeffs)):
    #     impulse.plot(title=f"Continuous Impulse {i-6}", filename=f"impulse_{i-6}.png")
    # print("coeffs: ",coeffs)



   
    # Initialize the sum signal
    

    # sum_signal = ContinuousSignal(lambda t: 0)
    for i, (impulse, coef) in enumerate(zip(impulses, coeffs)):
        # Plot each individual impulse
        # impulse.plot(t_range=(-INF, INF), title=f"δ(t-{i-INF}Δ)", filename=f"impulse_{i-INF}.png")
        print("i: impulse",i,impulse)
        # Add each impulse to the sum signal
        # Create a continuous signal for the coefficient at the specific range
        conti_f = ContinuousSignal(lambda t, c=coef, idx=(i - INF) * delta: np.where((t >= idx) & (t < (idx + delta)), c, 0))
        conti_f.plot(t_range=(-INF, INF), title=f"δ(t-{i-INF}Δ)x[{i-INF}]", filename=f"cont_impulse_{i-INF}.png")
        # # Add each impulse to the sum signal
        # sum_signal = sum_signal.add(conti_f)
    # Plot the sum of all impulses
    # sum_signal.plot(t_range=(-INF, INF), title="Sum of Impulses", filename="sum_impulses.png")
       
    # cont_impulse_signals.plot(t_range=(-INF, INF), title="Sum of Impulses", filename="sum_impulses.png")

    # Optionally, you can plot the multiplied results for visualization
    # for idx, signal in enumerate(cont_impulse_signals):
    #     signal.plot(t_range=(-3, 3), title=f"Multiple δ(t-{i-6}∇)*({i-6}∇)∇", filename=f"multiplied_signal_{idx-6}.png")




    # Define grid dimensions for subplots
    # num_signals = len(cont_impulse_signals)
    # cols = 3
    # rows = (num_signals // cols) + (num_signals % cols > 0)
    # print(f"cols: {cols}, rows: {rows}, num_signals: {num_signals}")

    # fig, axs = plt.subplots(rows, cols, figsize=(21, 12), constrained_layout=True)
    # axs = axs.flatten()

    # print("len(cont_impulse_signals): ",len(cont_impulse_signals))
    # print("data type: ",type(cont_impulse_signals[0]))

    


    # for i in range(len(cont_impulse_signals)):
    #     cont_impulse_signals[i].plot(t_range=(-INF, INF), title=f"Impulse {i} * Coefficient", ax=axs[i])
    # print("coeffs: ",coeffs)

    # Plot each signal on its respective subplot
    # for i, signal in enumerate(cont_impulse_signals):
    #     signal.plot(t_range=(-INF, INF), title=f"Impulse {(i)-num_signals/2} * Coefficient", ax=axs[i])
    #     axs[i].set_xlabel("Time (t)")
    #     axs[i].set_ylabel("Amplitude")
    #     axs[i].set_yticks(np.arange(0, 1.5, 0.5))

    # Hide unused subplots if there are any
    # for j in range(i + 1, len(axs)):
    #     axs[j].axis('off')

    # Save the complete plot grid
    # output_folder = "continuous_plots"
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    # plt.savefig(f"{output_folder}/impulses_and_sum_grid_cont.png")
    # plt.close()

    # for i, (impulse, coef) in enumerate(zip(impulses, coeffs)):
    #     impulse.multiply_const_factor(coef).plot(title=f"Continuous Impulse {i+1}", filename=f"cont_impulse_{i+1}.png")
    # plot_the_impulse_with_coef("Impulses multiplied by coefficients",impulses,coeffs,INF,continuous_impulse,"δ","impulses_and_sum_grid_cont.png",continuous=True)
    # output_approx = lti_continuous.output_approx(continuous_input, delta)
    # output_approx.plot(title="Approximate Continuous Output", filename="output_continuous.png")

if __name__ == "__main__":
    main()
