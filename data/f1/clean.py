contests = eval(input())
contestants = {}

for i in range(len(contests)):
	for j in range(len(contests[i]['standings'])):
		name = contests[i]['standings'][j]['name']
		contests[i]['standings'][j]['name'] = name.replace('  ', ' ')

for i in range(len(contests)):
	contest = contests[i]
	newstandings = []
	for row in contest['standings']:
		name = row['name']
		if (row['time'] != 'SHC' and row['time'] != 'DSQ'):
			newstandings.append(row)
	contest['standings'] = newstandings
	contests[i] = contest

def convert_to_seconds(time_string):
    parts = time_string.split(':')
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
    elif len(parts) == 2:
        hours = 0
        minutes = int(parts[0])
        seconds = float(parts[1])
    else:
        raise ValueError("Invalid time format")

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds

for i in range(len(contests)):
	winner = contests[i]['standings'][0]
	winnerlaps = int(winner['laps'])
	winnertime = convert_to_seconds(winner['time'])
	contests[i]['standings'][0]['score'] = winnertime
	for j in range(1, len(contests[i]['standings'])):
		this = contests[i]['standings'][j]
		thislaps = int(this['laps']) if (this['laps'] != '') else 0
		if (thislaps > winnerlaps):
			this['score'] = -1
		elif (thislaps < winnerlaps):
			this['score'] = winnertime + 1000 * (winnerlaps - thislaps)
		else:
			this['score'] = winnertime + float(this['time'][1:-1])
		
for i in range(len(contests)):
	contest = contests[i]
	newstandings = []
	for row in contest['standings']:
		name = row['name']
		if (row['score'] != -1):
			newstandings.append(row)
	contest['standings'] = newstandings
	contests[i] = contest

for contest in contests:
	for row in contest['standings']:
		name = row['name']
		if (name not in contestants):
			contestants[name] = 0
		contestants[name] += 1

for i in range(len(contests)):
	contest = contests[i]
	newstandings = []
	for row in contest['standings']:
		name = row['name']
		row['score'] = -row['score']
		if (contestants[name] >= 0):
			newstandings.append(row)
	contest['standings'] = newstandings
	contests[i] = contest

print(contests)