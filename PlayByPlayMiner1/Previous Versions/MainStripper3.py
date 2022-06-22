# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:15:00 2019

@author: Jan
"""
# import BeautifulSoup web scraping library
# https://www.crummy.com/software/BeautifulSoup/bs4/
from bs4 import BeautifulSoup
import os

import Game
import Lineup
import PlayByPlay
import ActionUnit
import CsvStuff


# Box Score/Play By Play url pattern
# https://static.ekusports.com/custompages/BB/Stats/2019/3-16-19.htm



#//////////////////////////// STATIC FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
# end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#////////////////////////// CLOSE STATIC FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\ 
  #45,72,146,161,167
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN1 - iterates through a folder of files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main1():
    #list of htm files 
    file_list = os.listdir(path = "C:/Users/Jan/Desktop/Scrape/htm files/")
    
    for fi,f in enumerate(file_list):
        #enter the htm file name
        filename = "C:/Users/Jan/Desktop/Scrape/htm files/" + f
        soup = open_soup(filename)
                
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MAIN2: Processes a single csv file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main3():
#enter the htm file name
    DoubleHeader = False
    GameofDay = 1
    
    f = "4-12-19.htm" #enter file here
    #check to see if game is part of a double header
    if "a" in f:
        DoubleHeader = True
        GameofDay = 1
    elif "b" in f:
        DoubleHeader = True
        GameofDay = 2
    
    filename = "C:/Users/Jan/Desktop/Scrape/htm files/" + f
    soup = open_soup(filename)
    
    #==========================================================================
    ### Game object ###
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    g1 = Game.Game(soup)
    ### output of Game class ###
    
    AwayTeam = g1.away_team
    HomeTeam = g1.home_team
    GameMonth = g1.game_month
    GameDay = g1.game_day
    GameYear = g1.game_year
    
    GameID = GameYear + get_numeric_month(GameMonth) + GameDay + "0" + str(GameofDay)
    print("Game ID: "+GameID)
    print()
    
    
    lus = g1.get_lineups() #this is a dict of four lists
    #extracting lists from dict
    away_starters = lus["away_starters"]
    away_subs = lus["away_subs"]
    home_starters = lus["home_starters"]
    home_subs = lus["home_subs"]
    #lineups are still in original format
    
    
    print("Away Starters:")
    print(away_starters)
    print("Away Subs:")
    print(away_subs)
    print("Home Starters:")
    print(home_starters)
    print("Home Subs:")
    print(home_subs)
    
    pbps = g1.get_pbp_strings() #this is a list of half-inning strings
    #dividing half-inning strings into away and home
    away_pbps = pbps[0::2]
    home_pbps = pbps[1::2]
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    #==========================================================================
    
    #==========================================================================
    ### Lineup Object ###
    # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
    lu1 = Lineup.Lineup(away_starters, away_subs, home_starters, home_subs, GameID)
    
    AwayPos,HomePos = lu1.get_pos_order() #returns dicts of positions and names
    AwayOrder,HomeOrder = lu1.get_batting_orders() #returns lists of names in order (hole = i+1)
    AwayRelievers,HomeRelievers = lu1.get_relievers() #returns string lists of names
    AwayOffSubs,HomeOffSubs = lu1.get_off_subs() #returns string lists of offensive sub names
    
    #producing csv dataset
    lu1.get_lineup_data()

    #==========================================================================
    ### PlayByPlay Objects ###
    # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
    #pbp object takes a single pbp string - loop to iterate through play by play string lists
    '''
    print("AwayOrder: ")
    print(AwayOrder)
    print()
    
    ### AWAY ###
    #Away play by play strings
    for s in away_pbps:
        p1 = PlayByPlay.PlayByPlay(s)
        
        p1.get_action_units()
        p1.get_types()
        p1.get_au_nums()
        p1.print_stuff()
    '''
    ### HOME ###
    
    print("HomeOrder: ")
    print(HomeOrder)
    print("home_subs: ")
    print(home_subs)
    print()
    
    #Home play by play strings
    side = "Home" #element of Plate Appearance ID
    
    for c,s in enumerate(home_pbps): #c is element of Plate Appearance ID
        inn = c+1
        
        #PlayByPlay object
        p1 = PlayByPlay.PlayByPlay(s)
        
        p1.do_stuff()
        p1.print_stuff()
        
        ActionUnits = p1.au
        UnitTypes = p1.au_types
        PA_ID = get_pa_id(ActionUnits, UnitTypes, side, inn, GameID)
               
        for i,u in enumerate(ActionUnits):
        #these iterate together: ActionUnits, UnitTypes, PA_ID
            if UnitTypes[i] == "bat":
                #create bat object
                #output stats in new row
                print("PA ID: " + PA_ID[i])
                print("bat: "+u)
                
            elif UnitTypes[i] == "batbr":
                #create bat object and br object(?)
                #output stats in new row
                print("PA ID: " + PA_ID[i])
                print("batbr: "+u)
                
            elif UnitTypes[i] == "br":
                #create br object
                #output stats in same row
                print("PA ID: " + PA_ID[i])
                print("br: "+u)
                
            elif UnitTypes[i] == "sub":
                #create sub object
                #modify game state, batting orders, etc
                #output dataset?
                print("PA ID: " + PA_ID[i])
                print("sub: "+u)
                
            else:
                print("!!!ERROR: Main, for Action Units, Invalid Unit Type")
       
    
    # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
    #==========================================================================                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN3
#______________________________________________________________________________
    
#______________________________________________________________________________
#==============================================================================
#                                 global methods
#______________________________________________________________________________
#==============================================================================
#______________________________________________________________________________
def get_pa_id(action_units, unit_types, team, inning, game_id):
    r = []
    d = 0 #element of Plate Appearance ID
    
    for i,u in enumerate(action_units):
            if unit_types[i] == "bat":
                d += 1
                r.append(game_id + team+"0"+str(inning)+"0"+str(d)+"b")
                
            elif unit_types[i] == "batbr":
                d += 1
                r.append(game_id + team+"0"+str(inning)+"0"+str(d)+"b")
            
            elif unit_types[i] == "br":
                r.append(game_id + team+"0"+str(inning)+"0"+str(d)+"b")
                
            else:
                d += 1
                r.append(game_id + team+"0"+str(inning)+"0"+str(d)+"s")
    return r
#______________________________________________________________________________
def get_numeric_month(month):
    if month == "Mar":
        return "03"
    elif month == "Apr":
        return "04"
    elif month == "May":
        return "05"
    elif month == "Feb":
        return "02"
    elif month == "Jun":
        return "06"
    elif month == "Jan":
        return "01"
    else:
        print("!!!Error: Month out of range")
    
#______________________________________________________________________________
#==============================================================================    
    
main3()
    
        
               
    
    
    
    
    
    
    
