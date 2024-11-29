import math
import numpy as np
import matplotlib.pyplot as plt
import os

from temp import  ContinuousSignal, LTI_Continuous
def main():

    print("\ncontinuous signal starts here:\n")
    """  # conti_f = ContinuousSignal(lambda t: np.where((t < 0) | (t > 1), 0, 1))
    # conti_f.plot(t_range=(-2, 2), title="x(t)", filename="demosignal.png")
    # conti_f.shift(-1).plot(t_range=(-2, 2), title="x(t-1)", filename="shifted_signal.png")
    # conti_f.multiply_const_factor(2).plot(t_range=(-2, 2), title="2x(t)", filename="scaled_signal.png")
    # conti_f.add(conti_f.shift(1)).plot(t_range=(-2, 2), title="x(t) + x(t-1)", filename="added_signal.png")
    # conti_f.multiply(conti_f).plot(t_range=(-2, 2), title="x(t) * x(t-1)", filename="multiplied_signal.png")
    """
    INF = 3

    continuous_impulse = ContinuousSignal(lambda t: np.where(t < 0, 0, np.exp(-t)))
    lti_continuous = LTI_Continuous(continuous_impulse)
    continuous_impulse.plot(t_range=(-INF, INF), title="x(t),INF={INF}", filename="x(t)_input_signal.png")

    delta = .5
    impulses, coeffs = lti_continuous.linear_combination_of_impulses(continuous_impulse,delta,INF)
    sum_signal = ContinuousSignal(lambda t: 0)
    for i, (impulse,coeff) in enumerate(zip(impulses,coeffs)):
        impulse.plot(t_range=(-INF, INF), title=f"δ(t-({i-INF/delta}∇)x({i-INF/delta})∇)∇", filename=f"δ(t-({i-INF/delta}∇))x({i-INF/delta})∇)∇.png")
        sum_signal = sum_signal.add(impulse)
    sum_signal.plot(t_range=(-INF, INF), title="Reconstruced Signal", filename="Reconstructed_sum_of_impulse.png")
    
    
    """# print(type(impulses))
    # print(type(impulses[0]))
    # print(type(coeffs[0]))
    # print(type(coeffs))
    # print(coeffs)"""


    """ # sum_signal = ContinuousSignal(lambda t: 0)
            # for i, (impulse,coeff) in enumerate(zip(impulses,coeffs)):
            #     # impulse.plot(t_range=(-INF, INF), title=f"δ(t-({i-INF/delta}∇))", filename=f"δ(t-({i-INF/delta}∇)).png")
            #     print("Coefficient: ",coeff)
            #     # temp=impulse.multiply_const_factor(coeff*delta)
            #     impulse.plot(t_range=(-INF, INF), title=f"δ(t-({i-INF/delta}∇)x({i-INF/delta}∇)∇)", filename=f"δ(t-({i-INF/delta}∇)x({i-INF/delta}∇)∇).png")
            #     sum_signal = sum_signal.add(impulse)
            # sum_signal.plot(t_range=(-INF, INF), title="Sum of impulses", filename="sum_of_impulses.png")
    """


    #Reconstructed signal for different delta values


    delta_values = [.5, 0.1, 0.05,.01]
    for delta in delta_values:
        impulses, coeffs = lti_continuous.linear_combination_of_impulses(continuous_impulse,delta,INF)
        sum_signal = ContinuousSignal(lambda t: 0)
        for i, (impulse,coeff) in enumerate(zip(impulses,coeffs)):
            sum_signal = sum_signal.add(impulse)
        sum_signal.plot_together(t_range=(-INF, INF), title=f"Sum of impulses for δ={delta}", filename=f"Reconstructed ∇={delta}.png",newsig=continuous_impulse)
       
    output_sig,response_of_impulses=lti_continuous.output_approx(continuous_impulse,.5,INF)
    
    # print("Output Signal:",output_sig.values)   
    # output_sig.plot(t_range=(-INF, INF), title="Output Signal", filename="output_signal.png")
    # print(type(response_of_impulses))
    # print(type(response_of_impulses[0]))
    # print(type(output_sig))
    # print(len(response_of_impulses))

    delta=0.5
    for i, response in enumerate(response_of_impulses):
        response.plot(t_range=(-INF, INF), title=f"Response of Impulse h(t-({i - INF / delta}∇))*x({i-INF/delta})∇)∇", filename=f"h(t-({i - INF / delta}∇))x({i-INF/delta})∇)∇.png")
        # print("i inf delta: ",i,INF,delta)
        # print("i-inf/delta: ",i-INF/delta)  
    output_sig.plot(t_range=(-INF, INF), title="Output Signal", filename="output_signal.png")

    continuous_signal_y = ContinuousSignal(lambda t: np.where(t >= 0, 1 - np.exp(-t), 0))

    continuous_signal_y.plot(t_range=(-INF, INF), title="1 - exp(-t)u(t)", filename="1_minus_exp_y(t).png")
    lti_continuous = LTI_Continuous(continuous_impulse)
    
    delta_values = [.5, 0.1, 0.05,.01]
    for delta in delta_values:
        output_signal, responses = lti_continuous.output_approx(continuous_impulse, delta, INF)
        # output_signal.plot(t_range=(-INF, INF), title=f"Output signal for δ={delta} (1 - exp(-t)u(t))", filename=f"Output_{delta}.png")
        output_signal.plot_together(t_range=(-INF, INF), title=f"approximate output for ∇={delta} (1 - exp(-t)u(t))", filename=f"Approx_out_∇{delta}.png", newsig=continuous_signal_y)

    
if __name__ == "__main__":
    main()