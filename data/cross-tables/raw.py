import re
import sys
import requests

yearfrom = 2000
yearto   = 2023
url = f"https://www.cross-tables.com/tourneys.php?startyear={yearfrom}&endyear={yearto}&type=name&place=&query=&submitted=1&go=Find"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
response = requests.get(url, headers=headers)
content = response.text
matches = re.findall(r"<a href='tourney.php\?t=([0123456789]*?)'>", content, re.DOTALL)

def parse_contest(text):
	name = text.split('\n')[0]
	print(name, file=sys.stderr, flush=True)
	ret = []
	contests = text.split('  DIVISION ')[1:2]
	for contest in contests:
		rows = contest.split('. ')[1:]
		standings = []
		rank = 0
		for row in rows:
			rank += 1
			row = row.replace(' W-', '+W-')
			row = row.replace(' L-', '+L-')
			row = row.replace(' T-', '+T-')
			nxt = row.replace('  ', ' ')
			while nxt != row:
				row = nxt
				nxt = row.replace('  ', ' ')
			info = row.split(' ')
			if (len(info) < 8 or info[2].isdigit() == False or info[3][0] != '+' or info[4][0] == '+' or info[7][:-1].isdigit() == False):
				return []
			standings.append({'name' : info[0] + ' ' + info[1], 'old rating' : int(info[2]), 'rank' : rank, 'details' : info[3], 'wins' : info[4], 'new rating' : int(info[7][:-1])})
		thiscontest = {'name' : name, 'division' : int(contest[0]), 'standings' : standings}
		ret.append(thiscontest)
	return ret

contests = []
for match in matches:
	url = "https://www.cross-tables.com/texttable.php?t=" + match
	response = requests.get(url, headers=headers)
	result = parse_contest(response.text)
	for contest in result:
		contests.append(contest)

print(contests)