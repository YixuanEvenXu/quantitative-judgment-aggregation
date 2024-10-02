def parse_name(text):
	texts = text.split(' ')
	while (texts[-1][0] != '('):
		texts = texts[:-1]
	texts = texts[:-1]
	if (texts[0] == ''):
		texts = texts[1:]
	if (texts[0] == 'GM' or texts[0] == 'IM' or texts[0] == 'FM' or texts[0] == 'WGM' or texts[0] == 'WIM' or texts[0] == 'WFM'):
		texts = texts[1:]
	return ' '.join(texts)

def	parse_wins(text):
	if (text[-1] == '½'):
		text = text[:-1] + '.5'
	return float(text)

contests = []
name = input()
while name != '':
	contest = {'name' : name}
	columns = input().split('	')
	num_players = 0
	tpr_column = -1
	for i in range(len(columns)):
		if (columns[i].isdigit()):
			num_players += 1
		if (columns[i] == 'TPR'):
			tpr_column = i + 1
	contest['num_players'] = num_players
	contest['cross_table'] = [[0 for i in range(num_players)] for j in range(num_players)]
	standings = []
	for i in range(num_players):
		line = input().split('	')
		thisplayer = {'name' : parse_name(line[1]), 'score' : parse_wins(line[num_players + 3])}
		for j in range(num_players):
			contest['cross_table'][i][j] = line[j + 3]
		standings.append(thisplayer)
	contest['standings'] = standings
	contests.append(contest)
	try:
		name = input()
	except EOFError:
		name = ''

print(contests)