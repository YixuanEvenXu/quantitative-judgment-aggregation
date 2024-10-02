contests = eval(input())
contestants = {}

for contest in contests:
	for row in contest['standings']:
		handle = row['handle']
		if (handle not in contestants):
			contestants[handle] = 0
		contestants[handle] += 1

for i in range(len(contests)):
	contest = contests[i]
	newstandings = []
	for row in contest['standings']:
		handle = row['handle']
		if (contestants[handle] >= len(contests) // 2):
			newstandings.append({'name' : handle, 'score' : row['points']})
	contest['standings'] = newstandings
	contests[i] = contest

print(contests)