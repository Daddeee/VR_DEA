from dea import DEA, CCR, BCC
import numpy as np


inputs = np.array([[2, 3, 3, 4, 5, 5, 6, 8]]).T
outputs = np.array([[1, 3, 2, 3, 4, 2, 3, 5]]).T

dea = DEA(inputs, outputs)
dea_status, dea_efficiency = dea.solve()

ccr = CCR(inputs, outputs)
ccr_status, ccr_efficiency = ccr.solve()

bcc = BCC(inputs, outputs)
bcc_status, bcc_efficiency = bcc.solve()


print("\n\n==============================\n\n")

print(dea_status)
print(dea_efficiency)

print("\n\n==============================\n\n")

print(ccr_status)
print(ccr_efficiency)

print("\n\n==============================\n\n")

print(bcc_status)
print(bcc_efficiency)

print("\n\n==============================\n\n")