# Parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset")
args = parser.parse_args()
dataset = args.dataset

# Read the experiment log
file = open(f'logs/subsample/{dataset}.log', 'r')
content = file.read().split('\n')[2:]
file.close()
rate = eval(content[0])
L1accuracy = eval(content[1])
L2accuracy = eval(content[2])
L1loss = eval(content[3])
L2loss = eval(content[4])
n = len(rate)

# Read the loss of all zero predicton
file = open(f'logs/zero/{dataset}.log', 'r')
zero = eval(file.read().split('\n')[0])
file.close()

# Normalize the loss
L1loss = [(L1loss[i][0] / zero, L1loss[i][1] / zero) for i in range(n)]
L2loss = [(L2loss[i][0] / zero, L2loss[i][1] / zero) for i in range(n)]

# Import the plotting library
import numpy as np
import matplotlib.pyplot as plt

# Plot the ordinal accuracy
height = 2.8 if dataset == 'chess' else 3.2
plt.figure(figsize=(10, height))
# L1 QRJA
y = np.array([L1accuracy[i][0] for i in range(n)])
e = np.array([L1accuracy[i][1] for i in range(n)])
plt.plot(rate, y, marker='+', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='L1')
plt.fill_between(rate, y - e, y + e, alpha=0.2)
# L2 QRJA
y = np.array([L2accuracy[i][0] for i in range(n)])
e = np.array([L2accuracy[i][1] for i in range(n)])
plt.plot(rate, y, marker='x', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='L2')
plt.fill_between(rate, y - e, y + e, alpha=0.2)
# Configurations
if (dataset == 'chess' or dataset == 'f1-core'):
	plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Subsample Rate (α)', fontsize=20)
plt.ylabel('Accuracy', fontsize=20)
if (dataset == 'chess'):
	plt.subplots_adjust(top=0.98, bottom=0.25, left=0.15, right=0.99)
else:
	plt.subplots_adjust(top=0.96, bottom=0.23, left=0.15, right=0.99)
plt.savefig(f'figures/subsample/{dataset}_accuracy.jpg')
plt.savefig(f'figures/subsample/{dataset}_accuracy.pdf')
plt.clf()

# Plot the quantitative loss
plt.figure(figsize=(10, height))
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#FF4500', '#880088'])
# L1 QRJA
y = np.array([L1loss[i][0] for i in range(n)])
e = np.array([L1loss[i][1] for i in range(n)])
plt.plot(rate, y, marker='+', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='L1')
plt.fill_between(rate, y - e, y + e, alpha=0.2)
# L2 QRJA
y = np.array([L2loss[i][0] for i in range(n)])
e = np.array([L2loss[i][1] for i in range(n)])
plt.plot(rate, y, marker='x', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='L2')
plt.fill_between(rate, y - e, y + e, alpha=0.2)
# Configurations
if (dataset == 'chess' or dataset == 'f1-core'):
	plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Subsample Rate (α)', fontsize=20)
plt.ylabel('Loss', fontsize=20)
if (dataset == 'chess'):
	plt.subplots_adjust(top=0.98, bottom=0.25, left=0.15, right=0.99)
else:
	plt.subplots_adjust(top=0.96, bottom=0.23, left=0.15, right=0.99)
plt.savefig(f'figures/subsample/{dataset}_loss.jpg')
plt.savefig(f'figures/subsample/{dataset}_loss.pdf')
plt.clf()