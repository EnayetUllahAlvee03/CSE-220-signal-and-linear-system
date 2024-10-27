
import math
from Discrete_LTI_Discrete_signal import plot_the_impulse_with_coef
import numpy as np
import matplotlib.pyplot as plt
import os

from Discrete_LTI_Discrete_signal import DiscreteSignal,  LTI_Discrete
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

    new_signals = []
    # Assuming impulses and coeffs have already been computed
    impulses, coeffs = lti_discrete.linear_combination_of_impulses(discrete_input)
    sum_signal = DiscreteSignal(INF)
    for i in range(len(impulses)):
        sum_signal = sum_signal.add(impulses[i].multiply_const_factor(coeffs[i]))
        
        new_signals.append(impulses[i].multiply_const_factor(coeffs[i]))
        print("Impulse: ",i,new_signals[i].values)
    print("sum signal: ",sum_signal.values)
    print("coeffs: ",coeffs)
    
    
    plot_the_impulse_with_coef("Impulses multiplied by coefficients",new_signals,coeffs,INF,sum_signal,"δ","impulses_and_sum_grid.png")
    
    discrete_output,out_impulses,out_coeffs = h.output(discrete_input)
    # for i in range(len(out_impulses)):
    #     print("Impulse: ",out_impulses[i].values)
    #     print("Coefficient: ",out_coeffs[i])
    # print("Output Signal:",discrete_output.values)
 
    plot_the_impulse_with_coef("Response of Input signal",out_impulses,out_coeffs,INF,discrete_output,"h","output_discrete.png")



if __name__ == "__main__":
    main()
