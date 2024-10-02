contests = eval(input())
contestants = {}

for i in range(len(contests)):
	contest = contests[i]
	newstandings = []
	for row in contest['standings']:
		handle = row['handle']
		if (len(newstandings) <= 100):
			newstandings.append({'name' : handle, 'score' : row['points']})
	contest['standings'] = newstandings
	contests[i] = contest

contests.reverse()
print(contests)