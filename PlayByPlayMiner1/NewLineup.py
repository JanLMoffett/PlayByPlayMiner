# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:25:11 2019
@author: Jan
"""
import StdzNames

pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                                 Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
class Lineup:
    #__________________________________________________________________________
    #__________________________________________________________________________
    def __init__(self, away_name_list, away_pos_list, away_startsub_list, home_name_list, home_pos_list, home_startsub_list, gameid):
        
        #parameters lineup initialized with:
        #===---===---===---===---===---===---===---===---===---===---===---===-
        self.gameid = gameid
        
        self.awaynames = away_name_list
        self.awaypos = away_pos_list
        self.awaystartsub = away_startsub_list
        
        self.homenames = home_name_list
        self.homepos = home_pos_list
        self.homestartsub = home_startsub_list
        #===---===---===---===---===---===---===---===---===---===---===---===-
        
        #set with get_starters_subs:
        #===---===---===---===---===---===---===---===---===---===---===---===-
        self.awaystarters = []
        self.awaystarterpos = []
        self.awaysubs = []
        self.awaysubpos = []
        
        self.homestarters = []
        self.homestarterpos = []
        self.homesubs = []
        self.homesubpos = []
        #===---===---===---===---===---===---===---===---===---===---===---===-
        
        #set with get_subs:
        #===---===---===---===---===---===---===---===---===---===---===---===-
        self.awayrelievers = []
        self.awayoffsubs = [] #substitute position players
        
        self.homerelievers = []
        self.homeoffsubs = [] #substitute position players
        #===---===---===---===---===---===---===---===---===---===---===---===-
        
        #set with get_batting_orders:
        #===---===---===---===---===---===---===---===---===---===---===---===-
        self.awayorder = []
        self.homeorder = []
        #===---===---===---===---===---===---===---===---===---===---===---===-
    #__________________________________________________________________________
    #__________________________________________________________________________
    def get_starters_subs(self):
        for i,n in enumerate(self.awaynames):
            if self.awaystartsub[i] == "starter":
                self.awaystarters.append(StdzNames.last_only(n))
                self.awaystarterpos.append(self.awaypos[i])
            elif self.awaystartsub[i] == "sub":
                self.awaysubs.append(StdzNames.last_only(n))
                self.awaysubpos.append(self.awaypos[i])
            else:
                print("!!!Error: Lineup.get_starters_subs; awaystartsub[i]: " + self.awaystartsub[i])
                
        for i,n in enumerate(self.homenames):
            if self.homestartsub[i] == "starter":
                self.homestarters.append(StdzNames.last_only(n))
                self.homestarterpos.append(self.homepos[i])
            elif self.homestartsub[i] == "sub":
                self.homesubs.append(StdzNames.last_only(n))
                self.homesubpos.append(self.homepos[i])
            else:
                print("!!!Error: Lineup.get_starters_subs; homestartsub[i]: " + self.homestartsub[i])
    #__________________________________________________________________________
    
    def get_subs(self): #run get_starters_subs first
        
        for i,n in enumerate(self.awaysubs):
            #if pos is 'p', add to reliever list, otherwise add to offensive sub list
            if self.awaysubpos[i] == 'p':
                self.awayrelievers.append(StdzNames.last_only(n))
            else:
                self.awayoffsubs.append(StdzNames.last_only(n))
        
        for i,n in enumerate(self.homesubs):
            #if pos is 'p', add to reliever list, otherwise add to offensive sub list
            if self.homesubpos[i] == 'p':
                self.homerelievers.append(StdzNames.last_only(n))
            else:
                self.homeoffsubs.append(StdzNames.last_only(n))
                
    #__________________________________________________________________________
    def get_batting_orders(self):
        for i,n in enumerate(self.awaystarters):
            if self.awaystarterpos[i] != 'p':
                self.awayorder.append(n)
        
        for i,n in enumerate(self.homestarters):
            if self.homestarterpos[i] != 'p':
                self.homeorder.append(n)
                
    #__________________________________________________________________________
    def do_stuff(self):
        self.get_starters_subs()
        self.get_subs()
        self.get_batting_orders()
    #__________________________________________________________________________
    
    def print_stuff(self):
        print("Away Starters and Positions:")
        print(self.awaystarters)
        print(self.awaystarterpos)
        print()
        print("Away Subs and Positions:")
        print(self.awaysubs)
        print(self.awaysubpos)
        print()
        print("Away Relievers:")
        print(self.awayrelievers)
        print()
        print("Away Offensive Subs:")
        print(self.awayoffsubs)
        print()
        print("Away Batting Order:")
        print(self.awayorder)
        print()
        
        
        print("Home Starters and Positions:")
        print(self.homestarters)
        print(self.homestarterpos)
        print()
        print("Home Subs and Positions:")
        print(self.homesubs)
        print(self.homesubpos)
        print()
        print("Home Relievers:")
        print(self.homerelievers)
        print()
        print("Home Offensive Subs:")
        print(self.homeoffsubs)
        print()
        print("Home Batting Order:")
        print(self.homeorder)
        print()
        
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                            Close Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
        
def test():
    #dummy data
    GameID = "G_TEST_02"

    AwayNames = ['Justin Ammons', 'Jay Charleston', 'Andre Lipcius', 'Alerick Soularie', 'Evan Russell', 'Zach Daniels', 'Landon Gray', 'Connor Pavolony', 'Ricky Martinez', 'Pete Derkay', 'Max Ferguson', 'Jake Rucker', 'Garrett Stallings', 'Camden Sewell']
    AwayPositions = ['rf', 'cf', '3b', 'lf', 'dh', 'ph', 'c', 'ph', 'ss', '1b', '1b', '2b', 'p', 'p']
    AwayStartSubs = ['starter', 'starter', 'starter', 'starter', 'starter', 'sub', 'starter', 'sub', 'starter', 'starter', 'sub', 'starter', 'starter', 'sub']

    HomeNames = ['Holland, Will', 'Williams, Steven', 'Woley, Rankin', 'Julien, Edouard', 'Davis, Conor', 'Eaton, Jarrett', 'Bliss, Ryan', 'Howell, Kason', 'Ward, Judd', 'Scheffler, Matt', 'Burns, Tanner', 'Anderson, Elliott', 'Greenhill, Cody']
    HomePositions = ['ss', 'rf', '1b', '3b', 'dh', 'pr', '2b', 'cf', 'lf', 'c', 'p', 'p', 'p']
    HomeStartSubs = ['starter', 'starter', 'starter', 'starter', 'starter', 'sub', 'starter', 'starter', 'starter', 'starter', 'starter', 'sub', 'sub']
    
    #initialize lineup
    lu = Lineup(AwayNames,AwayPositions,AwayStartSubs,HomeNames,HomePositions,HomeStartSubs,GameID)
     
    lu.do_stuff()
    lu.print_stuff()
    
 
