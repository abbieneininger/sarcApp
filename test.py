import numpy as np
import matplotlib.pyplot as pp

numData = np.arange(0, 10, .5)
numData2 = np.arange(0, 20, 1)
numData = np.stack((numData, numData2, numData, numData2))
#print(numData,np.shape(numData))
#print(sum(numData[(numData[:,4] >= 3), 4]))

uploadBools = [True, False, True]
if (uploadBools[0] and not uploadBools[2]):
    print("yee")

scan1 = [1, 2, 3, 4, 5, 6]
scan1pts = len(scan1)
scan1X = np.linspace(0,scan1pts-1,num=scan1pts)
print(scan1X)
plot1 = pp.plot(scan1X, scan1)
plot1.show()