import numpy as np
bp = np.array([
    [120,80],
    [135,85],
    [140,90],
    [110,70],
    [125,75]
])

systolic_values = bp[:,0]
print(systolic_values)
high_systolic_patient = [i for i in range(len(systolic_values)) if i > 130]
print(high_systolic_patient)
systolic_values= [80 for i in systolic_values if i<80]
print(systolic_values)

