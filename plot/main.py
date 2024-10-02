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
lossl2 = eval(content[3])

# Read the loss of all zero predicton
file = open(f'logs/zero/{dataset}.log', 'r')
lines = file.read().split('\n')
zerol1 = eval(lines[0])
zerol2 = eval(lines[1])
file.close()

# Normalize the loss
lossl1 = [lossl1[i] if lossl1[i] == -1  
          else lossl1[i] / zerol1 for i in range(num_algorithms)]
lossl2 = [lossl2[i] if lossl2[i] == -1
          else lossl2[i] / zerol2 for i in range(num_algorithms)]

# Import matplotlib
import matplotlib.pyplot as plt

def plot_accuracy(algorithms, accuracy, dataset):
    # Plot the ordinal accuracy
    plt.figure(figsize=(10, 2.5))
    plt.subplots_adjust(top=0.96, bottom=0.14, left=0.11, right=0.99)
    bars = plt.bar(algorithms, accuracy, color='#1E90FF', label='Ordinal Accuracy')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                f'{height*100:.1f}%', ha='center', va='bottom', fontsize=20)
    dev = max(accuracy) - min(accuracy)
    plt.ylim(min(accuracy) - dev * 0.3, max(accuracy) + dev * 0.3)
    if (dataset == 'chess' or dataset == 'cross-tables'):
        plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f'figures/main/{dataset}_accuracy.jpg')
    plt.savefig(f'figures/main/{dataset}_accuracy.pdf')
    plt.clf()

def plot_lossl1(algorithms, loss, dataset):
    # Plot the L1 quantitative loss
    plt.figure(figsize=(10, 2.5))
    plt.subplots_adjust(top=0.96, bottom=0.14, left=0.11, right=0.99)
    bars = plt.bar(algorithms, loss, color='#FF4500', label='Quantitative Loss')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{height:.4f}', ha='center', va='bottom', fontsize=20)
    dev = max(loss) - min(loss)
    plt.ylim(max(min(loss) - dev * 0.3, 0), max(loss) + dev * 0.3)
    if (dataset == 'chess' or dataset == 'cross-tables'):
        plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f'figures/main/{dataset}_loss.jpg')
    plt.savefig(f'figures/main/{dataset}_loss.pdf')
    plt.clf()

def plot_lossl2(algorithms, loss, dataset):
    # Plot the L2 quantitative loss
    plt.figure(figsize=(10, 3))
    plt.subplots_adjust(top=0.98, bottom=0.12, left=0.11, right=0.99)
    bars = plt.bar(algorithms, loss, color='#FF4500', label='L2 Quantitative Loss')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{height:.4f}', ha='center', va='bottom', fontsize=20)
    dev = max(loss) - min(loss)
    plt.ylim(max(min(loss) - dev * 0.3, 0), max(loss) + dev * 0.3)
    if (dataset == 'chess' or dataset == 'cross-tables'):
        plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f'figures/main/{dataset}_loss_l2.jpg')
    plt.savefig(f'figures/main/{dataset}_loss_l2.pdf')
    plt.clf()

# Plot the ordinal accuracy
# We only plot one version of MF in the main figures
algorithms[6] = 'MF'
plot_accuracy(algorithms[:7], accuracy[:7], dataset)

# Plot the L1 and L2 quantitative loss
# Remove Kemeny-Young and Borda since they are not quantitative
qalgorithms = []
qvaluesl1 = []
qvaluesl2 = []
for i in range(num_algorithms):
	if (lossl1[i] != -1):
		qalgorithms.append(algorithms[i])
		qvaluesl1.append(lossl1[i])
		qvaluesl2.append(lossl2[i])
qalgorithms[4] = 'MF'
plot_lossl1(qalgorithms[:5], qvaluesl1[:5], dataset)
plot_lossl2(qalgorithms[:5], qvaluesl2[:5], dataset)