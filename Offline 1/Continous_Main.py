
import math
from temp import plot_the_impulse_with_coef
import numpy as np
import matplotlib.pyplot as plt
import os

from temp import DiscreteSignal, ContinuousSignal, LTI_Discrete, LTI_Continuous
def main():

    print("\ncontinuous signal starts here:\n")
    conti_f = ContinuousSignal(lambda t: np.where((t < 0) | (t > 1), 0, 1))
    conti_f.plot(t_range=(-2, 2), title="x(t)", filename="demosignal.png")
    INF = 3

    continuous_impulse = ContinuousSignal(lambda t: np.where(t < 0, 0, np.exp(-t)))
    lti_continuous = LTI_Continuous(continuous_impulse)
    continuous_impulse.plot(t_range=(-INF, INF), title="x(t)", filename="x(t)_cont_input.png")

    delta = .5
    impulses, coeffs = lti_continuous.linear_combination_of_impulses(continuous_impulse,delta,INF)
    print(type(impulses))
    print(type(impulses[0]))
    print(type(coeffs[0]))
    print(type(coeffs))
    print(coeffs)
    sum_signal = ContinuousSignal(lambda t: 0)
    for i, (impulse,coeff) in enumerate(zip(impulses,coeffs)):
        impulse.plot(t_range=(-INF, INF), title=f"δ(t-({i-INF/delta}∇))", filename=f"δ(t-({i-INF/delta}∇)).png")
        print("Coefficient: ",coeff)
        sum_signal = sum_signal.add(impulse.multiply_const_factor(coeff))
    sum_signal.plot(t_range=(-INF, INF), title="Sum of impulses", filename="sum_of_impulses.png")

    


if __name__ == "__main__":
    main()