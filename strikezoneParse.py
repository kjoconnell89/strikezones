import datetime
import json
import pymongo
import mlbCalls as mlbc

currentDate = str(datetime.date.today())
dateCCYY = currentDate.split('-')[0]
dateMM = currentDate.split('-')[1]
dateDD = currentDate.split('-')[2]

#leaving this as list, open to changing values for each particular result
pitchBalls = ['B']
pitchStrikes = ['C']
pitchResults = pitchBalls + pitchStrikes

szRight = 8.5/12
szLeft = -8.5/12

awayPitchCt = 0
awayPitchTracked = 0
awayAtBats = 0
homePitchCt = 0
homePitchTracked = 0
homeAtBats = 0
homePitchers = {}
awayPitchers = {}
pitchArray = []
gameArray = []
playerArray = []

#some arrays for possible future enhancements and QC / tracking
gameRawArray = []
trackingArray = []

dateGames = mlbc.dailyScheduleCall('09', '01', '2019')

gamePKs = [game['gamePk'] for game in dateGames['dates'][0]['games']]

gameExample = mlbc.dailyGameCall('566634')


#parse out relevant game information
for gamePK in gamePKs:
    gameDict = {}

    gameDict['gameID'] = gamePK
    gameDict['awayTeamID'] = gameExample['gameData']['teams']['away']['id']
    gameDict['homeTeamID'] = gameExample['gameData']['teams']['home']['id']
    gameDict['venueID'] = gameExample['gameData']['venue']['id']
    gameDict['seasonYear'] = gameExample['gameData']['game']['season']
    gameDict['gameType'] = gameExample['gameData']['game']['type']
    gameDict['date'] = gameExample['gameData']['datetime']['dateTime'][:10]
    gameDict['time'] = gameExample['gameData']['datetime']['time'] + gameExample['gameData']['datetime']['ampm']
    gameDict['dayNight'] = gameExample['gameData']['datetime']['dayNight'][:1].upper()
    gameDict['timeZone'] = gameExample['gameData']['venue']['timeZone']['tz']
    gameDict['weatherCondition'] = gameExample['gameData']['weather']['condition']
    gameDict['weatherTemp'] = gameExample['gameData']['weather']['temp']
    for umps in gameExample['liveData']['boxscore']['officials']:
        if umps['officialType'] == 'Home Plate':
            gameDict['umpID'] = umps['official']['id']
    
    gameDict['modified'] = currentDate
    gameArray.append(gameDict)
    gameRawArray.append(gameExample)


#parse out relevant pitch / at bat information
pitchBase = gameExample['liveData']['plays']['allPlays'] #this returns an array of dicts, adjust accordingly
for atBat in pitchBase:
    for pitch in atBat['playEvents']:
        pitchDict = {}
        trackingDict = {}    

        if pitch['isPitch'] == True and pitch['details']['call']['code'] in pitchResults:
            pitchDict['gameID'] = '566634' #this will be referencing gameID when looping
            pitchDict['pitchID'] = pitch['pfxId']
            pitchDict['pitchNum'] = pitch['pitchNumber']
            pitchDict['szTop'] = pitch['pitchData']['strikeZoneTop'] #changes within each pitch of at bat?
            pitchDict['szBottom'] = pitch['pitchData']['strikeZoneBottom'] #changes within each pitch of at bat?
            pitchDict['pitchType'] = pitch['details']['type']['code']
            pitchDict['pitchSpeed'] = pitch['pitchData']['startSpeed']
            pitchDict['pitchZone'] = pitch['pitchData']['zone']
            pitchDict['pitchX'] = pitch['pitchData']['coordinates']['pX']
            pitchDict['pitchY'] = pitch['pitchData']['coordinates']['pZ']
            pitchDict['inningNum'] = atBat['about']['inning']
            pitchDict['inningHalf'] = atBat['about']['halfInning']
            pitchDict['pitcherID'] = atBat['matchup']['pitcher']['id']
            pitchDict['pitchSide'] = atBat['matchup']['pitchHand']['code']
            pitchDict['batterID'] = atBat['matchup']['batter']['id']
            pitchDict['batSide'] = atBat['matchup']['batSide']['code']
            if pitch['details']['call']['code'] in pitchBalls:
                pitchDict['countBalls'] = pitch['count']['balls'] - 1
                pitchDict['countStrikes'] = pitch['count']['strikes']
                pitchDict['pitchCall'] = 'Ball'
            if pitch['details']['call']['code'] in pitchStrikes:
                pitchDict['countBalls'] = pitch['count']['balls']
                pitchDict['countStrikes'] = pitch['count']['strikes'] - 1
                pitchDict['pitchCall'] = 'Strike'
            #move players above and incorporate logic to compare player sz to pitch sz and define a correct / missed call value?

            pitchDict['modified'] = currentDate
            pitchArray.append(pitchDict)
            trackingArray.append(trackingDict)


#parse out relevant player information
playerBase = gameExample['gameData']['players'] #dict of dicts
for player in playerBase.keys():
    playerDict = {}
    playerDict['playerID'] = playerBase[player]['id']
    playerDict['teamID'] = 'xyz' #not in player info?
    playerDict['playerName'] = playerBase[player]['fullName']
    playerDict['szTopPlayer'] = playerBase['strikeZoneTop']
    playerDict['szBottomPlayer'] = playerBase['strikeZoneBottom']
    
    playerDict['modified'] = currentDate
    playerArray.append(playerDict)


print(json.dumps(trackingDict, indent = 4))