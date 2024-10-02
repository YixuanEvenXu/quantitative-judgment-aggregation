# This file is used to run the subsample experiments.

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
def run(p, rate):
	predictions = run_qrja(cnt_matches, cnt_contestants, standings, p, rate)
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
rate = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
repeat = 10
L1Accuracy = []
L2Accuracy = []
L1Loss = []
L2Loss = []

for r in rate:
	L1Accuracy.append([])
	L2Accuracy.append([])
	L1Loss.append([])
	L2Loss.append([])
	for i in range(repeat):
		Accuracy, Loss = run(1, r)
		L1Accuracy[-1].append(Accuracy)
		L1Loss[-1].append(Loss)
		Accuracy, Loss = run(2, r)
		L2Accuracy[-1].append(Accuracy)
		L2Loss[-1].append(Loss)

import numpy as np
for i in range(len(rate)):
	L1Accuracy[i] = (np.mean(L1Accuracy[i]), np.std(L1Accuracy[i]))
	L2Accuracy[i] = (np.mean(L2Accuracy[i]), np.std(L2Accuracy[i]))
	L1Loss[i] = (np.mean(L1Loss[i]), np.std(L1Loss[i]))
	L2Loss[i] = (np.mean(L2Loss[i]), np.std(L2Loss[i]))

print(rate)
print(L1Accuracy)
print(L2Accuracy)
print(L1Loss)
print(L2Loss)