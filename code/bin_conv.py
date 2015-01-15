import numpy as np
import random
import matplotlib.pyplot as plt

outcome = []
est = []
act = []
total = 0
lim = 100

for i in range(200000):
    if random.randint(1,lim) == 1:
        outcome.append(1)
        total += 1
    else:
        outcome.append(0)
    est.append(float(total)/(i+1))
    act.append(float(1)/lim)

plt.plot(est)
plt.plot(act)
# plt.axis([0,20000,act[0]/2,min(1,3*act[0]/2)])
plt.axis([0,200000,0,min(1,3*act[0]/2)])
plt.show()

