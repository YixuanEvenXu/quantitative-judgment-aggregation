import sys
import requests

def get_contest_list():
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    data = response.json()
    assert(data['status'] == "OK")
    return data['result']

def get_standings(contest_id):
    url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&from=1&count=10000"
    response = requests.get(url)
    data = response.json()
    assert(data['status'] == "OK")
    return data['result']

def get_user_info(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    data = response.json()
    return data

ids = []
names = []
contest_list = get_contest_list()
for contest in contest_list:
    if (contest['phase'] != "FINISHED" or contest['type'] != "CF" or contest['name'].find("Div. 1") == -1 or contest['name'].find("Div. 2") != -1):
        continue
    ids.append(contest['id'])
    names.append(contest['name'])
# print(ids)
# print(names)

contests = []
for i in range(len(ids)):
    print(ids[i], names[i], file=sys.stderr)
    success = False
    while (not success):
        try:
            raw_standings = get_standings(ids[i])
            success = True
        except:
            print("Error", file=sys.stderr)
            success = False
    processed_standings = []
    for row in raw_standings['rows']:
        handle = row['party']['members'][0]['handle']
        points = row['points']
        rank = row['rank']
        processed_standings.append({'handle': handle, 'points': points, 'rank': rank})
    contests.append({'id': ids[i], 'name': names[i], 'standings': processed_standings})

print(contests)