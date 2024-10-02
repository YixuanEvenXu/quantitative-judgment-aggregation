# Parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset")
args = parser.parse_args()
dataset = args.dataset

# Read the experiment log
file = open(f'logs/overtime/{dataset}.log', 'r')
content = file.read().split('\n')
file.close()
iters = eval(content[0])
R1accuracy = eval(content[1])
R2accuracy = eval(content[2])
R5accuracy = eval(content[3])
R1loss = eval(content[4])
R2loss = eval(content[5])
R5loss = eval(content[6])
n = len(iters)

# Read the loss of all zero predicton
file = open(f'logs/zero/{dataset}.log', 'r')
zero = eval(file.read().split('\n')[0])
file.close()

# Normalize the loss
R1loss = [R1loss[i] / zero for i in range(len(R1loss))]
R2loss = [R2loss[i] / zero for i in range(len(R2loss))]
R5loss = [R5loss[i] / zero for i in range(len(R5loss))]

# Import matplotlib
import matplotlib.pyplot as plt

# Plot the ordinal accuracy
plt.figure(figsize=(10, 2.8))
plt.plot(iters, R1accuracy, marker='+', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='R1')
plt.plot(iters, R2accuracy, marker='x', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='R2')
plt.plot(iters, R5accuracy, marker='*', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='R5')
if (dataset == 'chess'):
	plt.legend(fontsize=20, loc='right')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Number of epoches', fontsize=20)
plt.ylabel('Accuracy', fontsize=20)
plt.subplots_adjust(top=0.96, bottom=0.25, left=0.135, right=0.99)
plt.savefig(f'figures/overtime/{dataset}_accuracy.jpg')
plt.savefig(f'figures/overtime/{dataset}_accuracy.pdf')
plt.clf()

# Plot the quantitative loss
plt.figure(figsize=(10, 2.8))
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#FF4500', '#880088', '#D35400'])
plt.plot(iters, R1loss, marker='+', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='R1')
plt.plot(iters, R2loss, marker='x', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='R2')
plt.plot(iters, R5loss, marker='*', markersize=25, markeredgewidth=6, alpha=0.7, linewidth=4, label='R5')
if (dataset == 'chess'):
	plt.legend(fontsize=20, loc='right')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Number of epoches', fontsize=20)
plt.ylabel('Loss', fontsize=20)
plt.subplots_adjust(top=0.96, bottom=0.25, left=0.135, right=0.99)
plt.savefig(f'figures/overtime/{dataset}_loss.jpg')
plt.savefig(f'figures/overtime/{dataset}_loss.pdf')
plt.clf()