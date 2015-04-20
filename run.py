import config, api

# Predefined Summoner Information Check
if config.SUMMONER_REGION and config.SUMMONER_NAME:
	INPUT_SUMMONER_NAME = config.SUMMONER_NAME
	INPUT_SUMMONER_REGION = config.SUMMONER_REGION
else:
	INPUT_SUMMONER_NAME = input('Summoner Name: ')
	INPUT_SUMMONER_REGION = input('Summoner Region: ')

# Fucking temp fix
ENEMY_CHAMPIONS_ID = {}

# Retrieve information from api.py
def run():
	summonerId = api.summoner(INPUT_SUMMONER_NAME, INPUT_SUMMONER_REGION)
	currentGameData = api.currentGame(summonerId, INPUT_SUMMONER_REGION)
	enemySummonersData = currentGameMain(currentGameData, summonerId)

	# Loop Enemies
	for x in enemySummonersData:
		print(previousGameStats(x, enemySummonersData[x], INPUT_SUMMONER_REGION))

# Pretty print current game info and return enemies
def currentGameMain(data, summonerId):
	print('>>> GAME FOUND ON PLATFORM ID %s' % (data['platformId']))
	gameInfo = 'Game Type: %s | Game Mode: %s | Game ID: %s' % (data['gameType'], 
		data['gameMode'], data['gameId'])

	# Resolve Current Team ID
	currentTeam = ''
	for participants in data['participants']:
		if participants['summonerId'] == summonerId:
			currentTeam = participants['teamId']

	# Resolve Enemy Team Members
	enemyTeamChampions = 'Enemy Champions:'
	enemyTeamJson = {}
	for participants in data['participants']:
		if participants['teamId'] != currentTeam:
			ENEMY_CHAMPIONS_ID[participants['summonerId']] = participants['championId']
			championName = api.champion(participants['championId'], INPUT_SUMMONER_REGION)
			enemyTeamJson[participants['summonerId']] = championName
			enemyTeamChampions += ' ' + championName

	# Print Informatiom
	print('\n' + gameInfo + '\n' + enemyTeamChampions + '\n')
	return enemyTeamJson

# Fetch previous game info, losing sprees etc...
def previousGameStats(id, champion, region):
	print('>>> %s STATS:' % champion.upper())
	data = api.matchHistory(id, region)

	# Fetch Losing Spree Data
	previousGamesResults = {}
	for x in data['matches']:
		gameId = x['matchId']
		for y in x['participants']:
			previousGamesResults[gameId] = y['stats']['winner']

	losingSpree = 0
	for z in previousGamesResults:
		if previousGamesResults[z] == False:
			losingSpree += 1
		else:
			break

	if losingSpree == 0:
		spreeText = 'Won the last game'
	elif losingSpree == 1:
		spreeText = 'Lost the last game'
	else:
		spreeText = 'Lost the last %s games' % losingSpree

	# Fetch Current Rank Data
	leagueData = api.league(id, region)

	if leagueData[str(id)] is not None:
		for league in leagueData[str(id)]:
			if league['queue'] == 'RANKED_SOLO_5x5':
				tier = league['tier']
				for entry in league['entries']:
					division = entry['division']
					leaguePoints = entry['leaguePoints']
	else:
		tier = 'UNRANKED'
		division = ''
		leaguePoints = ''

	# Fetch Champion Stats
	championData = api.stats(id, INPUT_SUMMONER_REGION)
	championWins = 1
	championLosses = 0
	championPlays = championWins + championLosses
	for xy in ENEMY_CHAMPIONS_ID:
		if xy == id:
			for championGet in championData['champions']:
				if championGet['id'] == ENEMY_CHAMPIONS_ID[xy]:
					championWins = championGet['stats']['totalSessionsWon']
					championLosses = championGet['stats']['totalSessionsLost']
					#championTotalAssists = championGet['stats']['totalAssists']
					#championTotalKills = championGet['stats']['totalChampionKills']
					#championTotalDeaths = championGet['stats']['totalDeathsPerSession']
					#championTotalMinionKills = championGet['stats']['totalMinionKills']

	championStatsText = '%s: %sW %sL' % (champion, championWins, championLosses)

	return 'Spree Stats (General): %s \nChampion Stats (Ranked): %s \nLeague Stats (Ranked): %s %s (%sLP) \n' % (spreeText, championStatsText, tier, division, leaguePoints)


# Run application
if __name__ == '__main__':
	run()