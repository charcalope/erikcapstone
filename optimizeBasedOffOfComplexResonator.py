#Closest I have to a working file.
import matplotlib.pyplot as plt
import numpy as np
import lmfit
import pandas as pd
import math

#f = omega = xdata
#Z(omega) =
#((x(3)*x(2)*xdata.^2 - 1) - 1j*(x(4)*x(2)*xdata)) ./ ( (x(4)*x(1)*x(2)*xdata.^2) + 1j*((x(3)*x(1)*x(2)*xdata.^3)-(xdata*(x(1)+x(2)))) );
# => x0 = [C0, C1, L1, R1]
#         [ 1,  2,  3,  4]
def objectiveFunction(omega, c0Real, c0Imag, c1Real, c1Imag, l1Real, l1Imag, r1Real, r1Imag):
    c0 = c0Real + 1j*c0Imag
    c1 = c1Real + 1j*c1Imag
    l1 = l1Real + 1j*l1Imag
    r1 = r1Real + 1j*r1Imag
    A = (l1 * c1 * omega ** 2) - 1
    B = r1 * c1 * omega
    C = r1 * c0 * c1 * omega ** 2
    D = l1 * c0 * c1 * omega ** 3
    E = omega * (c0 + c1)
    z = (A - 1j * B) / (C + 1j * (D - E))
    return z


# The standard practice of defining a ``lmfit`` model is as follows:
class objectiveFunctionModel(lmfit.model.Model):
    #__doc__ = "resonator model" + lmfit.models.COMMON_INIT_DOC

    def __init__(self, *args, **kwargs):
        # pass in the defining equation so the user doesn't have to later
        super().__init__(objectiveFunction, *args, **kwargs)

        #self.set_param_hint('Q', min=0)  # enforce Q is positive


#Need to import the data. Get ydata and xdata.
df = pd.read_excel('equivlentCircuitExperimentalData.xlsx', header=None)
omega = df[0].tolist()
ydata = df[1].tolist()
#df = pd.read_excel('experimentalDataRealAndImaginary.xlsx', header=None)
#x = df[0].tolist()
#ydataReal = df[1].tolist()
#ydataImag = df[2].tolist()
#ydata = complex(ydataReal, ydataImag)

objFunction = objectiveFunctionModel()
params = objFunction.make_params(c0Real=5.079322701323505e-10, c0Imag=0, c1Real=3.3412970018273238e-09, c1Imag=0, l1Real=2.3303111816188115e-06, l1Imag=0, r1Real=7.679492283758477, r1Imag=0)


result = objFunction.fit(ydata, params=params, omega=omega, verbose=True)
    #measured_s21 = ydata
    #params =
    #f = xdata = omega
print(result.fit_report() + '\n')
result.params.pretty_print()


# c0 = abs(result.params.get('c0Real').value + 1j*result.params.get('c0Imag').value)
# c1 = abs(result.params.get('c1Real').value + 1j*result.params.get('c1Imag').value)
# l1 = abs(result.params.get('l1Real').value + 1j*result.params.get('l1Imag').value)
# r1 = abs(result.params.get('r1Real').value + 1j*result.params.get('r1Imag').value)
# print(f"c0 = {c0}")
# print(f"c1 = {c1}")
# print(f"l1 = {l1}")
# print(f"r1 = {r1}")
