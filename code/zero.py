# This file is used to run the all-zero predictions on a dataset.

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

# Run the algorithm
from utils import *
predictions = run_zero(cnt_matches, cnt_contestants, standings)

# We only predict for contestants who has appeared at least once
appeared = [False for i in range(cnt_contestants)]

# The metric
quant = [0, 0, 0]
entrywise = [0, 0, 0]

# Calculate the metrics
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
		idi = contest[ti]['id']
		if (appeared[idi]):
			pscore = predicted[idi]['score']
			ascore = contest[ti]['score']
			entrywise[0] += 1
			entrywise[1] += abs(pscore - ascore)
			entrywise[2] += (pscore - ascore) ** 2
		for tj in range(ti):
			idj = contest[tj]['id']
			# We only predict for contestants who has appeared at least once
			if (appeared[idi] and appeared[idj]):
				# If the algorithm is quantitative
				pdiff = predicted[idi]['score'] - predicted[idj]['score']
				adiff = contest[ti]['score'] - contest[tj]['score']
				quant[0] += 1
				quant[1] += abs(pdiff - adiff)
				quant[2] += (pdiff - adiff) ** 2
	# Update the appeared list
	for row in contest:
		appeared[row['id']] = True

# Output the results
print(quant[1] / quant[0])
print(quant[2] / quant[0])
print(entrywise[1] / entrywise[0])
print(entrywise[2] / entrywise[0])