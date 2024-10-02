def parse_name(text):
	texts = text.split(' ')
	texts = texts[:-1]
	return ' '.join(texts).upper()

def	parse_time(text):
	time = text.split(':')
	hours = int(time[0])
	minutes = int(time[1])
	seconds = int(time[2])
	return hours * 3600 + minutes * 60 + seconds

contests = []
name = input()
while name != '':
	contest = {'name' : name}
	num_players = 100
	contest['num_players'] = num_players
	standings = []
	for i in range(num_players):
		line = input().split('	')
		time = ''
		for entry in line:
			if (entry.find(':') != -1):
				time = entry
				break
		thisplayer = {'name' : parse_name(line[0]), 'score' : -parse_time(time)}
		standings.append(thisplayer)
	contest['standings'] = standings
	contests.append(contest)
	try:
		name = input()
	except EOFError:
		name = ''

print(contests)