# This file is used to run the overtime experiments.

# Parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset")
args = parser.parse_args()
dataset = args.dataset

# Read dataset
file = open(f'data/{dataset}/clean.in', 'r')
content = file.read()
contests = eval(content)
file.close()

# Parse the dataset
contestants = {}
standings = []
for contest in contests:
	standing = []
	for row in contest['standings']:
		name = row['name']
		if (name not in contestants):
			contestants[name] = len(contestants)
		score = row['score']
		standing.append({'id' : contestants[name], 'score' : score})
	standings.append(standing)
cnt_matches = len(standings)
cnt_contestants = len(contestants)

from utils import *
def run(r, iters):
	predictions = run_matrix_factorization(cnt_matches, cnt_contestants, standings, rank = r, iters = iters)
	appeared = [False for i in range(cnt_contestants)]
	order = [0, 0]
	quant = [0, 0]
	for i in range(cnt_matches):
		contest = standings[i]
		prediction = predictions[i]
		prediction.sort(key = lambda row : row['score'], reverse = True)
		predicted = {}
		for ti in range(len(prediction)):
			row = prediction[ti]
			if (appeared[row['id']]):
				predicted[row['id']] = {'score' : row['score'], 'rank' : ti}
		# Update the metrics
		for ti in range(len(contest)):
			for tj in range(ti):
				idi = contest[ti]['id']
				idj = contest[tj]['id']
				# We only predict for contestants who has appeared at least once
				if (appeared[idi] and appeared[idj]):
					# If the two contestants have different scores in the real contest
					if (contest[ti]['score'] != contest[tj]['score']):
						order[0] += (predicted[idi]['rank'] > predicted[idj]['rank'])
						order[1] += 1
					# If the algorithm is quantitative
					pdiff = predicted[idi]['score'] - predicted[idj]['score']
					adiff = contest[ti]['score'] - contest[tj]['score']
					quant[0] += abs(pdiff - adiff)
					quant[1] += 1
		# Update the appeared list
		for row in contest:
			appeared[row['id']] = True
	return order[0] / order[1], quant[0] / quant[1]

# The algorithms
skip = 10
if (dataset == 'chess'):
	skip = 20
if (dataset == 'cross-tables'):
	skip = 50
if (dataset == 'f1' or dataset == 'f1-core'):
	skip = 100
iters = [i * skip for i in range(11)]
R1Accuracy = []
R2Accuracy = []
R5Accuracy = []
R1Loss = []
R2Loss = []
R5Loss = []

for it in iters:
	Accuracy, Loss = run(1, it)
	R1Accuracy.append(Accuracy)
	R1Loss.append(Loss)
	Accuracy, Loss = run(2, it)
	R2Accuracy.append(Accuracy)
	R2Loss.append(Loss)
	Accuracy, Loss = run(5, it)
	R5Accuracy.append(Accuracy)
	R5Loss.append(Loss)

print(iters)
print(R1Accuracy)
print(R2Accuracy)
print(R5Accuracy)
print(R1Loss)
print(R2Loss)
print(R5Loss)