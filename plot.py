import matplotlib.pyplot as plt
import numpy as np
import os

x = ['a', 'b', 'c', 'd']
y = [1, 2, 3, 4]
l = [x for x in range(20)]

fig, ax = plt.subplots()
ax.bar(x, y)
plt.savefig('franco')

fig, ax_2 = plt.subplots()
ax_2.bar(x, [4, 3, 2, 1])
plt.savefig('mario')
