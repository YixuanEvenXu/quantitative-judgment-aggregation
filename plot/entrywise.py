# Parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset")
args = parser.parse_args()
dataset = args.dataset

# Read the experiment log
file = open(f'logs/entrywise/{dataset}.log', 'r')
content = file.read().split('\n')
file.close()
algorithms = eval(content[0])
lossl1 = eval(content[1])
lossl2 = eval(content[2])

# Read the loss of all zero predicton
file = open(f'logs/zero/{dataset}.log', 'r')
content = file.read().split('\n')
file.close()
zerol1 = eval(content[2])
zerol2 = eval(content[3])

# Normalize the loss
lossl1 = [lossl1[i] / zerol1 for i in range(len(lossl1))]
lossl2 = [lossl2[i] / zerol2 for i in range(len(lossl2))]

# Import matplotlib
import matplotlib.pyplot as plt

# Entrywise L1 Loss
plt.figure(figsize=(10, 2.8))
bars = plt.bar(algorithms, lossl1, color='#FF4500', label='Entrywise L1 Loss')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height,
             f'{height:.4f}', ha='center', va='bottom', fontsize=20)
dev = max(lossl1) - min(lossl1)
plt.ylim(max(min(lossl1) - dev * 0.3, 0), max(lossl1) + dev * 0.3)
if (dataset == 'chess'):
    plt.legend(fontsize=20, loc='upper left')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.subplots_adjust(top=0.97, bottom=0.12, left=0.11, right=0.99)
plt.savefig(f'figures/entrywise/{dataset}_l1.jpg')
plt.savefig(f'figures/entrywise/{dataset}_l1.pdf')
plt.clf()

# Entrywise L2 Loss
plt.figure(figsize=(10, 2.8))
bars = plt.bar(algorithms, lossl2, color='#880088', label='Entrywise L2 Loss')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height,
             f'{height:.4f}', ha='center', va='bottom', fontsize=20)
dev = max(lossl2) - min(lossl2)
plt.ylim(max(min(lossl2) - dev * 0.3, 0), max(lossl2) + dev * 0.3)
if (dataset == 'chess'):
    plt.legend(fontsize=20, loc='upper left')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.subplots_adjust(top=0.97, bottom=0.12, left=0.11, right=0.99)
plt.savefig(f'figures/entrywise/{dataset}_l2.jpg')
plt.savefig(f'figures/entrywise/{dataset}_l2.pdf')
plt.clf()