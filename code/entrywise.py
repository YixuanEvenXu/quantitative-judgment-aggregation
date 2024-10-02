# This file is used to run the experiments about entrywise metrics on a dataset.

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

# The algorithms
num_algoritms = 5
algorithms = ['Median', 'Mean', 'R1 MF', 'R2 MF', 'R5 MF']

# Run the algorithms
from utils import *
predictions = []
predictions.append(run_median(cnt_matches, cnt_contestants, standings))
predictions.append(run_mean(cnt_matches, cnt_contestants, standings))
predictions.append(run_matrix_factorization(cnt_matches, cnt_contestants, standings, rank=1, iters=1000, lr=0.01))
predictions.append(run_matrix_factorization(cnt_matches, cnt_contestants, standings, rank=2, iters=1000, lr=0.01))
predictions.append(run_matrix_factorization(cnt_matches, cnt_contestants, standings, rank=5, iters=1000, lr=0.01))

# We only predict for contestants who has appeared at least once
appeared = [False for i in range(cnt_contestants)]

# The metrics
quant = [[0, 0, 0] for i in range(num_algoritms)]

# Calculate the metrics
for i in range(cnt_matches):
	contest = standings[i]
	for j in range(num_algoritms):
		# Get the prediction of algorithm j
		prediction = predictions[j][i]
		prediction.sort(key = lambda row : row['score'], reverse = True)
		predicted = {}
		for ti in range(len(prediction)):
			row = prediction[ti]
			if (appeared[row['id']]):
				predicted[row['id']] = {'score' : row['score'], 'rank' : ti}
		# Update the metrics
		for ti in range(len(contest)):
			idi = contest[ti]['id']
			# We only predict for contestants who has appeared at least once
			if (appeared[idi]):
				pscore = predicted[idi]['score']
				ascore = contest[ti]['score']
				quant[j][0] += 1
				quant[j][1] += abs(pscore - ascore)
				quant[j][2] += (pscore - ascore) ** 2
	# Update the appeared list
	for row in contest:
		appeared[row['id']] = True

# Output the results
print(algorithms)
print([quant[i][1] / quant[i][0] for i in range(num_algoritms)])
print([quant[i][2] / quant[i][0] for i in range(num_algoritms)])