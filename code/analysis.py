# This file is used to analyze a dataset.

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

# Analyze the dataset
n = 0
m = 0
cnt_matches = 0
tot_length  = 0
contestants = {}
for contest in contests:
	for row in contest['standings']:
		name = row['name']
		if (name not in contestants):
			contestants[name] = len(contestants)
	tot_length += len(contest['standings'])
	m += len(contest['standings']) * (len(contest['standings']) - 1) // 2
n = len(contestants)
cnt_matches = len(contests)

# Print the analysis
print(f"dataset: {dataset}")
print(f"n: {n}")
print(f"m: {m}")
print(f"tot_length: {tot_length}")
print(f"cnt_matches: {cnt_matches}")
print(f"matrix ratio: {tot_length / cnt_matches / n}")