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
def objectiveFunction(omega, c0, c1, r1, l1):
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
df = pd.read_excel('experimentalDataRealAndImaginary.xlsx', header=None)
col_real = list(df.get(1))
col_imag = list(df.get(2))
zipped_data = list(zip(col_real, col_imag))
ydata = [r+(i*1j) for r,i in zipped_data][50:]
omega = df[0].tolist()[50:]

objFunction = objectiveFunctionModel()
params = objFunction.make_params(c0=5.079322701323505e-10, c1=3.3412970018273238e-9, l1=2.3303111816188115e-6, r1=7.679492283758477)
#c0:e-10
#c1:e-9
#l1:e-6

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

print(f"c0 = {result.params.get('c0').value}")
print(f"c1 = {result.params.get('c1').value}")
print(f"l1 = {result.params.get('l1').value}")
print(f"r1 = {result.params.get('r1').value}")
