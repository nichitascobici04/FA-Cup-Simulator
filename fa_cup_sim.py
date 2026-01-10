from math import *
from random import *
import json
with open('data-sample.json', 'r') as file:
    a = json.load(file)
roundLabels = [
	'First Qualifying Round', 'Second Qualifying Round', 'Third Qualifying Round', 'Fourth Qualifying Round', 'First Round', 'Second Round', 
	'Third Round', 'Fourth Round', 'Fifth Round', 'Quarterfinals', 'Semifinals', '3rd Place Match', 'Final'
]
class team:
	def __init__(self, teamId, name, rating):
		self.teamId = teamId
		self.name = name
		self.rating = rating
		self.trophies = [0, 0, 0, 0]
def displayMatchPreview(m):
	print(f'{m[0].name} - {m[1].name}')
clearRating = lambda rating : round(rating * 100) / 100
generateRound = lambda teams : [[teams[x * 2], teams[x * 2 + 1]] for x in range(floor(len(teams) / 2))]
getMatchResult = lambda m, homeWin : f'{m[0].name} 1 - 0 {m[1].name}' if homeWin == True else f'{m[0].name} 0 - 1 {m[1].name}'
convert2strength = lambda team, dr, drc : drc ** (team.rating / dr)
detHomeWinChance = lambda m, dr, drc : convert2strength(m[0], dr, drc) / (convert2strength(m[0], dr, drc) + convert2strength(m[1], dr, drc))
sim = lambda m, dr, drc : True if random() < detHomeWinChance(m, dr, drc) else False
detWinner = lambda m, homeWin : m[0] if homeWin == True else m[1]
detLoser = lambda m, homeWin : m[1] if homeWin == True else m[0]
detDiff = lambda m, dr, drc, mcr, hw : clearRating((1 - detHomeWinChance(m, dr, drc)) * mcr if hw == True else detHomeWinChance(m, dr, drc) * mcr)
fairOdds     = [2.15, 3.45]
unfairOdds   = [1 / x for x in fairOdds]
realChances  = [x / sum(unfairOdds) for x in unfairOdds]
strongRating = 2602.27
weakRating   = 2490.96
dr           = strongRating - weakRating       # deltaRating
drc          = realChances[0] / realChances[1] # deltaRatingCoef
targetCoef   = 10
targetDeltaRating = clearRating(log(targetCoef) / log(drc) * dr)
qualificationStructure = [68, 30, 48, 24, 48, 0, 44]
#teamList = [team(x, DATA_SAMPLE[x]['name'], DATA_SAMPLE[x]['rating']) for x in range(len(DATA_SAMPLE))]
teamList = [team(x, a[x]['name'], a[x]['rating']) for x in range(len(a))]
matchesPerTap = 16
maxChangeCoef = 0.1
maxChangeRating = clearRating(maxChangeCoef * targetDeltaRating)
remainingTeamNumber = sum(qualificationStructure)
currentRoundId = -1
currentRoundTeams = []
newRoundTeams = []
currentRound = []
resultsMode = False
partCounter = 1
seasonCounter = 1
changeMode = False
m = ''
print(f"\nType 'e' for exiting and anything else for continuing\n\nSeason {seasonCounter}")
while m != 'e':
	if resultsMode == False:
		if len(currentRound) == 0:
			currentRoundId += 1
			if currentRoundId == len(roundLabels):
				currentRoundId = 0
				newRoundTeams = []
				currentRoundTeams = []
				seasonCounter += 1
				remainingTeamNumber = sum(qualificationStructure)
				if changeMode == True:
					for x in range(len(teamList) - 1):
						for y in range(x + 1, len(teamList)):
							if teamList[x].rating < teamList[y].rating:
								aux = teamList[x]
								teamList[x] = teamList[y]
								teamList[y] = aux
					print('Team Ratings:')
					for x in range(matchesPerTap):
						print(f'{x + 1}. {teamList[x].name}: {teamList[x].rating}')
				print(f'Season {seasonCounter}')
			elif currentRoundId == len(roundLabels) - 2:
				currentRoundTeams = [newRoundTeams.pop(0) for x in range(2)]
			else:
				currentRoundTeams = newRoundTeams.copy()
				newRoundTeams = []
			if currentRoundId < len(qualificationStructure):
				remainingTeamNumber -= qualificationStructure[currentRoundId]
				for x in range(remainingTeamNumber, remainingTeamNumber + qualificationStructure[currentRoundId]):
					currentRoundTeams.append(teamList[x])
			shuffle(currentRoundTeams)
			currentRound = generateRound(currentRoundTeams)
			partCounter = 1
		print(f'{roundLabels[currentRoundId]} {f'Part {partCounter}' if len(currentRoundTeams) > matchesPerTap * 2 else ''}')
		print('Preview')
		for x in range(min(matchesPerTap, len(currentRound))):
			displayMatchPreview(currentRound[x])
		resultsMode = True
	else:
		print('Results')
		for x in range(min(matchesPerTap, len(currentRound))):
			homeWin = sim(currentRound[0], dr, drc)
			print(getMatchResult(currentRound[0], homeWin))
			if changeMode == True:
				diff = detDiff(currentRound[0], dr, drc, maxChangeRating, homeWin)
				if homeWin == True:
					currentRound[0][0].rating = clearRating(currentRound[0][0].rating + diff)
					currentRound[0][1].rating = clearRating(currentRound[0][1].rating - diff)
				else:
					currentRound[0][0].rating = clearRating(currentRound[0][0].rating - diff)
					currentRound[0][1].rating = clearRating(currentRound[0][1].rating + diff)
			if currentRoundId == len(roundLabels) - 3:
				newRoundTeams.insert(0, detLoser(currentRound[0], homeWin))
			if currentRoundId == len(roundLabels) - 2:
				teamList[detLoser(currentRound[0], homeWin).teamId].trophies[3] += 1
				teamList[detWinner(currentRound[0], homeWin).teamId].trophies[2] += 1
				currentRound.pop(0)
			if currentRoundId == len(roundLabels) - 1:
				teamList[detLoser(currentRound[0], homeWin).teamId].trophies[1] += 1
				teamList[detWinner(currentRound[0], homeWin).teamId].trophies[0] += 1
			if currentRoundId != len(roundLabels) - 2:
				newRoundTeams.append(detWinner(currentRound.pop(0), homeWin))
		partCounter += 1
		resultsMode = False
	m = input()