# Parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset")
args = parser.parse_args()
dataset = args.dataset

# Read the experiment log
file = open(f'logs/main/{dataset}.log', 'r')
content = file.read().split('\n')[2:]
file.close()
algorithms = eval(content[0])
num_algorithms = len(algorithms)
accuracy = eval(content[1])
lossl1 = eval(content[2])

# Read the loss of all zero predicton
file = open(f'logs/zero/{dataset}.log', 'r')
zerol1 = eval(file.read().split('\n')[0])
file.close()

# Normalize the loss
lossl1 = [lossl1[i] if lossl1[i] == -1
          else lossl1[i] / zerol1 for i in range(num_algorithms)]

# Plot the metrics for the matrix factorization experiments
import numpy as np
import matplotlib.pyplot as plt

def plot_accuracy(algorithms, accuracy, dataset):
    # Plot the ordinal accuracy
    plt.figure(figsize=(10, 2.8))
    bars = plt.bar(algorithms, accuracy, color='#1E90FF', label='Ordinal Accuracy')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                f'{height*100:.1f}%', ha='center', va='bottom', fontsize=20)
    dev = max(accuracy) - min(accuracy)
    plt.ylim(min(accuracy) - dev * 0.3, max(accuracy) + dev * 0.3)
    if (dataset == 'chess'):
        plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(top=0.98, bottom=0.13, left=0.11, right=0.99)
    plt.savefig(f'figures/mf/{dataset}_accuracy.jpg')
    plt.savefig(f'figures/mf/{dataset}_accuracy.pdf')
    plt.clf()

def plot_lossl1(algorithms, loss, dataset):
    # Plot the L1 quantitative loss
    plt.figure(figsize=(10, 2.8))
    bars = plt.bar(algorithms, loss, color='#FF4500', label='Quantitative Loss')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{height:.4f}', ha='center', va='bottom', fontsize=20)
    dev = max(loss) - min(loss)
    plt.ylim(max(min(loss) - dev * 0.3, 0), max(loss) + dev * 0.3)
    if (dataset == 'chess'):
        plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(top=0.98, bottom=0.13, left=0.11, right=0.99)
    plt.savefig(f'figures/mf/{dataset}_loss.jpg')
    plt.savefig(f'figures/mf/{dataset}_loss.pdf')
    plt.clf()

# Plot the ordinal accuracy and L1 quantitative loss
plot_accuracy(algorithms[6:], accuracy[6:], dataset)
plot_lossl1(algorithms[6:], lossl1[6:], dataset)