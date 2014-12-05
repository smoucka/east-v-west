# NBA Season Records for 1977 - 2014
# 

import requests, re, json
from bs4 import BeautifulSoup

data = {}
base = 'http://www.basketball-reference.com/leagues/NBA_'

for year in range(1977, 2015):
	data[year] = {}
	
	url = base + str(year) + '.html'
	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	standings = soup.find('div', id='all_standings')
	
	conf_id = ['div_E_standings', 'div_W_standings']
	for index, cid in enumerate(conf_id):
		conf_table = standings.find('div', id=cid)
		if index == 0:
			conference = 'East'
		else:
			conference = 'West'
		
		data[year][conference] = {}
		
		for team_table in conf_table.find_all('tr', 'full_table'):
			team = team_table.a.text
			data[year][conference][team] = {}

			for idx, stat in enumerate(team_table.find_all('td')):
				if idx == 0:
					if '*' in stat.text:
						data[year][conference][team]['playoffs'] = 'Y'
					else:
						data[year][conference][team]['playoffs'] = 'N'
					data[year][conference][team]['conf_rank'] = re.sub('[()]', '', stat.span.text)
				if idx == 1:
					data[year][conference][team]['w'] = stat.text
				if idx == 2:
					data[year][conference][team]['l'] = stat.text
				if idx == 3:
					data[year][conference][team]['pct'] = stat.text

with open('seasons_1977_2014.json', 'wb') as f:
	f.write(json.dumps(data))