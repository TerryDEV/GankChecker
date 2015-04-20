import config, json, time, requests

def summoner(name, region):
	name = name.replace(" ", "")
	url = 'https://euw.api.pvp.net/api/lol/%s/%s/summoner/by-name/%s?api_key=%s' % (region, config.API_SUMMONER_VERSION, name, config.API_KEY)
	r = requests.get(url)

	if r.status_code == 404:
		print('!!! ERROR: COULD NOT RESOLVE NAME.')
		exit()
	else:
		data = r.json()
		summonerId = data[name.lower()]['id']
		print('>>> RESOLVING %s to %s. Using Summoner %s.' % (name, summonerId, config.API_SUMMONER_VERSION))
		return summonerId

def currentGame(id, region):
	url = 'https://euw.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/%s1/%s?api_key=%s' % (region.upper(), id, config.API_KEY)
	error = '!!! ERROR: SUMMONER NOT INGAME, RETRYING IN 10 SECONDS...'
	r = requests.get(url)
	for i in range(0, 100):
		while True:
			if r.status_code == 404:
				print(error)
				time.sleep(10)
				continue
			break
	return r.json()

def champion(id, region):
	url = 'https://global.api.pvp.net/api/lol/static-data/%s/%s/champion/%s?api_key=%s' % (region.lower(), config.API_CHAMPION_VERSION, id, config.API_KEY)
	r = requests.get(url)

	if r.status_code == 404:
		print('!!! ERROR: COULD NOT RESOLVE CHAMPION DATA.')
		exit()
	else:
		data = r.json()
		return data['name']

def matchHistory(id, region):
	url = 'https://euw.api.pvp.net/api/lol/%s/%s/matchhistory/%s?api_key=%s' % (region.lower(), config.API_MATCHHISTORY_VERSION, id, config.API_KEY)
	r = requests.get(url)
	if r.status_code == 404:
		print('!!! ERROR: COULD NOT RESOLVE MATCH HISTORY DATA.')
		exit()
	else:
		data = r.json()
		return data

def league(id, region):
	url = 'https://euw.api.pvp.net/api/lol/%s/%s/league/by-summoner/%s/entry?api_key=%s' % (region.lower(), config.API_LEAGUE_VERSION, id, config.API_KEY)
	r = requests.get(url)
	if r.status_code == 404:
		print('!!! ERROR: COULD NOT RESOLVE LEAGUE DATA.')
		exit()
	else:
		return r.json()

def stats(id, region):
	url = 'https://euw.api.pvp.net/api/lol/%s/%s/stats/by-summoner/%s/ranked?season=SEASON2015&api_key=%s' % (region, config.API_STATS_VERSION, id, config.API_KEY)
	r = requests.get(url)
	if r.status_code == 404:
		print('!!! ERROR: COULD NOT RESOLVE CHAMPION STATS.')
		exit()
	else:
		return r.json()