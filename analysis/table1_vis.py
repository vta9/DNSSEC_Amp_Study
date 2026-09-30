import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("table1_with_amp.csv")

# df["amplification"] = df["Response size"] / df["Query size"]

#for now, assume that if there are no answers, then the domain is not signed
# df["dnssec_signed"] = df["# of Answers"] > 0

# df.to_csv("table1_with_amp.csv", index=False)



print(df.head())

signed = df[df["dnssec_signed"]]["amplification"]
unsigned = df[~df["dnssec_signed"]]["amplification"]

def cdf(data):
    x = np.sort(data)
    y = np.arange(1, len(x)+1) / len(x)
    return x, y

x1, y1 = cdf(signed)
x2, y2 = cdf(unsigned)

plt.plot(x1, y1, label="DNSKEY Returned")
plt.plot(x2, y2, label="No Answers (Assumed unsigned)")

plt.xlabel("Amplification Factor")
plt.ylabel("Fraction of Domains")
plt.title("DNSKEY Amplification Distribution")

plt.legend()
plt.show()
