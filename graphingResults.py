import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

#Dale results parameters. Resnorm of ~500.
# r1 = 10.0744
# l1 = 3.5088e-7
# c1 = 4.6395e-10
# c0 = 2.1318e-10

#Erik Hand Calculated Values:
# c0 = 5.079322701323505e-10
# r1 = 7.679492283758477
# c1 = 3.3412970018273238e-09
# l1 = 2.3303111816188115e-06

#Dale compstart Hand Calculated Values:
# r1 = 9.02163369520457
# l1 = 3.19821073572867e-7
# c1 = 6.09429515447423e-10
# c0 = 9.58326846224047e-10

#high resnorm output values:
# r1 = 9.5788
# l1 = 6.0943e-7
# c1 = 3.1982e-10
# c0 = 9.0216e-10

#optimizeBasedOffOfComplexResonator values:
#Kinda works!!! Works well for earlier frequencies, but worse for everything else.
# c0 = 6.254898371965035e-10
# c1 = 2.2980803047590613e-09
# l1 = 2.0945423768673787e-06
# r1 = 4.885782639497406

#Same as above, just using the last 150 values for omega and ydata.
c0 = 6.376963493093867e-10
c1 = 2.5158909595665646e-09
l1 = 2.02427713142698e-06
r1 = 4.702785407629514


#Generating frequencies and angular frequencies
df = pd.read_excel('equivlentCircuitExperimentalData.xlsx', header=None)
frequencyValuesList = df[0].tolist()
experimentalImpedenceValues = df[1].tolist()
c = 2*math.pi
omegaValuesList = [c * x for x in frequencyValuesList]

#Empty list to append impedence values (aka z values but in list form)
zList = []

#Evaluating the impedence function at frequencies from 1MHz to 50MHz
for omega in frequencyValuesList:
  #z = (((l1*c1*(omega**2))-1) - 1j*(r1*c1*omega)) / ((r1*c0*c1*(omega**2)) + 1j*((l1*c0*c1*(omega**3)) - (omega*(c0+c1))))
  A = (l1 * c1 * omega ** 2) - 1
  B = r1 * c1 * omega
  C = r1 * c0 * c1 * omega ** 2
  D = l1 * c0 * c1 * omega ** 3
  E = omega * (c0 + c1)
  z = (A - 1j * B) / (C + 1j * (D - E))
  zAbs = abs(z)
  zList.append(zAbs)


#plotting
plt.xscale('log',base=10)
plt.yscale('log',base=10)
plt.xlim(1e6,50e6)
plt.ylim(1,10e3)
plt.ylabel('Impedence Magnitude (Ohm)')
plt.xlabel('Frequency (Hz)')
plt.plot(frequencyValuesList, zList, '--', label='Hand Calculations')
plt.plot(frequencyValuesList, experimentalImpedenceValues, label='Experimental Data')
plt.axvspan(0.9e7, 1.6e7, color='red', alpha=0.5)
plt.legend()
plt.figure()
plt.show()
