contests = eval(input())
contestants = {}

newcontests = []
for i in range(len(contests)):
	contest = contests[i]
	newstandings = []
	for row in contest['standings']:
		name = row['name']
		wins = row['wins']
		if (wins[-1] == '+'):
			wins = wins[:-1] + '.5'
		row['score'] = float(wins)
		newstandings.append(row)
	contest['standings'] = newstandings
	if (len(newstandings) > 1):
		newcontests.append(contest)

print(newcontests)