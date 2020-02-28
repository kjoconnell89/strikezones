import requests
import datetime

baseURL = 'http://statsapi.mlb.com/api/'


#get game list for day
def dailyScheduleCall(month, day, year):

    scheduleURL = baseURL + 'v1/schedule/games/?sportId=1&date={}/{}/{}'.format(month, day, year)
    scheduleResponse = requests.get(scheduleURL)
    return scheduleResponse.json()


#get individual game info
def dailyGameCall(gameID):

    gameURL = baseURL + 'v1.1/game/{}/feed/live'.format(gameID)
    gameResponse = requests.get(gameURL)
    return gameResponse.json()


#get team info
def teamCall(teamID):

    teamURL = baseURL + 'v1/teams/{}'.format(teamID)
    teamResponse = requests.get(teamURL)
    return teamResponse.json()


#get player info
def playerCall(playerID):

    playerURL = baseURL + 'v1/people/{}'.format(playerID)
    playerResponse = requests.get(playerURL)
    return playerResponse.json()