"""import numpy as np

class Polynomial:
    def __init__(self, degree, coefficients):
        self.degree = degree
        self.coefficients = coefficients

    def convolve_with(self, other):
        # Perform discrete convolution
        result_coeffs = np.convolve(self.coefficients, other.coefficients)
        result_degree = self.degree + other.degree
        return Polynomial(result_degree, result_coeffs)

    def __str__(self):
        coeff_str = " ".join(map(str, map(int, self.coefficients)))
        return f"Degree of the Polynomial: {self.degree}\nCoefficients: {coeff_str}"

# Helper function to read polynomial input
def read_polynomial():
    degree = int(input("Degree of the Polynomial: "))
    coefficients = list(map(int, input("Coefficients: ").split()))
    return Polynomial(degree, coefficients)

# Main function to execute the program
def main():
    print("Enter the first polynomial:")
    poly1 = read_polynomial()

    print("Enter the second polynomial:")
    poly2 = read_polynomial()

    # Multiply using convolution
    result_poly = poly1.convolve_with(poly2)
    print(result_poly)

# Run the main function
if __name__ == "__main__":
    main()
"""



# Assuming DiscreteSignal and LTI_Discrete classes are imported from the code provided


from Discrete_LTI_Discrete_signal import DiscreteSignal, LTI_Discrete   


def polynomial_multiplication():
    # Input polynomial degrees and coefficients
    d1 = int(input("Degree of the first Polynomial: "))
    coeffs1 = list(map(int, input("Coefficients: ").split()))
    # coeffs1.reverse()
    d2 = int(input("Degree of the second Polynomial: "))
    coeffs2 = list(map(int, input("Coefficients: ").split()))
    # coeffs2.reverse()
    print("coeffs1: ",coeffs1)
    print("coeffs2: ",coeffs2)

    # Set up the input signals for both polynomials
    inf = d1 + d2  # INF should be set to the maximum degree after multiplication
    poly1_signal = DiscreteSignal(inf)
    poly2_signal = DiscreteSignal(inf)
    
    # Populate the discrete signals with coefficients
    for i, coeff in enumerate(coeffs1):
        poly1_signal.set_value_at_time(d1 - i, coeff)
    for i, coeff in enumerate(coeffs2):
        poly2_signal.set_value_at_time(d2 - i, coeff)

    print("poly1_signal: ",poly1_signal.values)
    print("poly2_signal: ",poly2_signal.values)

    # Create the LTI system with poly2_signal as impulse response (to simulate convolution)
    lti_system = LTI_Discrete(poly2_signal)
    
    # Get the output signal from convolution
    result_signal, out_impulses, out_coeffs = lti_system.output(poly1_signal)
    print("result_signal: ",result_signal.values)
    # result_signal.reverse()
    newlti_sys=LTI_Discrete(result_signal)
    r,arr,c=newlti_sys.output(result_signal)
    print("r: ",r.values)
    # print("arr: ",arr)
    

    c.reverse()
    print("c: ",c)

    for i in range(len(c)):
        print(i)
        if (i<=inf and c[i]==0 ):
            
            c.pop(i)
    print("c: ",c)
   

    # Extract the result degree and coefficients
    degree_result = d1 + d2
    #coefficients_result = result_signal[inf-degree_result:inf+1]  # Trim to highest non-zero degree
    
    # Print the result
    print("Degree of the Polynomial:", degree_result)
    print("Coefficients:", c)
    
    
# Example call to function
polynomial_multiplication()

def non_zero_values(signal):
    non_zero_values = [value for value in signal.values if value != 0]
    return non_zero_values
