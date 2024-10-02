import re
import sys
import requests

def parse_driver(text):
	spanmatches = re.findall(r"<span.*?>(.*?)</span>", text, re.DOTALL)
	tdclassmatches = re.findall(r"<td class.*?>(.*?)</td>", text, re.DOTALL)
	return {
		'name' : spanmatches[0] + ' ' + spanmatches[1],
		'laps' : tdclassmatches[5],
		'time' : tdclassmatches[6].replace('<span class="suffix seconds">s</span>', 's').replace('<span class="suffix"> lap</span>', ' lap').replace('<span class="suffix"> laps</span>', ' laps')
	}

def parse_contest(text):
	matches = re.findall(r"<tr>(.*?)</tr>", text, re.DOTALL)
	contest = []
	for match in matches:
		contest.append(parse_driver(match))
	return contest

contests = []
for year in range(1950, 2024):
	url = f"https://www.formula1.com/en/results.html/{year}/races.html"
	response = requests.get(url)
	content = response.text
	matches = re.findall(r'data-value="([1234567890]*?\/[qwertyuiopasdfghjklzxcvbnm]*?)"', content, re.DOTALL)
	for name in matches:
		print(f"{year} {name}", file=sys.stderr)
		url = f"https://www.formula1.com/en/results.html/{year}/races/{name}/race-result.html"
		response = requests.get(url)
		content = response.text
		match = re.search(r"<tbody>(.*?)</tbody>", content, re.DOTALL)
		if match:
			text = match.group(1)
			contests.append({'year' : year, 'name' : name, 'standings' : parse_contest(text)})
			

print(contests)
print(len(contests))
cnt = 0
for contest in contests:
	cnt += len(contest['standings']) * (len(contest['standings']) - 1) / 2
print(cnt)