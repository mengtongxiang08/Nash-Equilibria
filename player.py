
# SahuPlayer.py
# Author sahwho
'''
    Represent a Player for Mod/Sim Fall 2024 Project 1 (MBHS)
    A Player has an id (like "P1"), as well as preferences for 2 strategies (which sum to 1.0).
    and keeps track of how many games they've played, plus their total score and average score.
    If you use this class, feel free to rename it Player.py

    Inspiration drawn from the work done by Dr. Andrew Davison (PSU)

    sample usage: p1 = SahuPlayer("P1")
'''

import random

class SahuPlayer:
    def __init__(self, id):
        self.id = id
        self.prefs = [0.5, 0.5] # strategy1, strategy2
        self.currentGameScore = 0
        self.numGamesPlayed = 0.0
        self.totalScore = 0;
        self.averageScore = 0

    def getId(self):
        return self.id

    def getPrefs(self):
        return self.prefs

    # no getters needed for currentGameScore, numGamesPlayed, totalScore, or averageScore,
    # since those are used internally within these methods

    # todo: based on the preferences, pseduorandomly select strategy1 or strategy2
    def getStrategy(self):
        print('getStrategy() not implemented yet')

    # todo: update totalScore, numGamesPlayed, and averageScore
    # this method assumes that a game has been played
    def updateScore(self, score):
        print('updateScore() not implemented yet')

    # todo: use a formula to update the current Player's preferences
    def updatePrefs(self):
        print('updatePrefs() not implemented yet')

    # format the object for printing: P1: <0.5, 0.5>
    def __str__(self):
        return self.id + ': <' + self.prefs[0] + ',' + self.prefs[1] + '>'
