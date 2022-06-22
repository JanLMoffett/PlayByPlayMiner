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
    #folder of htm files 
    file_list = os.listdir(path = "C:/Users/Jan/Desktop/Scrape/htm files/EKU/")
    
    gdfn = "C:/Users/Jan/Desktop/Scrape/Output/GameData.csv"
    gh = "GameID,AwayTeam,HomeTeam,GameMonth,GameDay,GameYear,DH,GameofDay"
    #create csv for dataset of games and gameid's
    CsvStuff.make_csv_file(gdfn,gh)
    
    for fi,f in enumerate(file_list): #each file represents a game
        DoubleHeader = False
        GameofDay = 1
    
        if "a" in f:
            DoubleHeader = True
            GameofDay = 1
        elif "b" in f:
            DoubleHeader = True
            GameofDay = 2
        
        #enter the htm file name
        filename = "C:/Users/Jan/Desktop/Scrape/htm files/EKU/" + f
        soup = open_soup(filename)
        
        #==========================================================================
        ### Game object ###
        g1 = Game.Game(soup)
        ### output of Game class ###
        AwayTeam = g1.away_team
        HomeTeam = g1.home_team
        GameMonth = g1.game_month
        GameDay = g1.game_day
        GameYear = g1.game_year
        
        GameID = GameYear + get_numeric_month(GameMonth) + GameDay + "0" + str(GameofDay)
        print("************************************")
        print("Game ID: "+GameID)
        print()
        
        #output a dataset of GameID | AwayTeam | HomeTeam | Month | Day | Year for GameID table in database
        g = "G" + GameID + "_gameid.csv"
        gamefilename = "C:/Users/Jan/Desktop/Scrape/Output/" + g
        CsvStuff.make_csv_file(gamefilename, "GameID,DoubleHeader,GameofDay,AwayTeam,HomeTeam,GameMonth,GameDay,GameYear")
        gamerowlist = [GameID, DoubleHeader, GameofDay, AwayTeam, HomeTeam, GameMonth, GameDay, GameYear]
        gamerow = CsvStuff.make_csv_row(gamerowlist)
        CsvStuff.add_row_csv_file(gamefilename, gamerow)
        
        lus = g1.get_lineups() #this is a dict of four lists
        #extracting lists from dict
        away_starters = lus["away_starters"]
        away_subs = lus["away_subs"]
        home_starters = lus["home_starters"]
        home_subs = lus["home_subs"]
        #lineups are still in original format
        
        pbps = g1.get_pbp_strings() #this is a list of half-inning strings
        #dividing half-inning strings into away and home
        away_pbps = pbps[0::2]
        home_pbps = pbps[1::2]
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        #==========================================================================
        
        #==========================================================================
        ### Lineup Object ###
        # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
        
        # Lineup Object Parameters:
        # away_starter_list, away_sub_list, home_starter_list, home_sub_list, game_id
        lu1 = Lineup.Lineup(away_starters, away_subs, home_starters, home_subs, GameID)
        
        #Output of Lineup class
        AwayOrder, HomeOrder = lu1.get_batting_orders()
        AwayOffenSubs, HomeOffenSubs = lu1.get_off_subs()
        AwayRelievers, HomeRelievers = lu1.get_relievers()
        
        #producing csv dataset
        lu1.get_lineup_data()
        
        #filename for batting dataset
        btfn = "C:/Users/Jan/Desktop/Scrape/Output/EKU_G" + GameID + "_batting.csv"
        brfn = "C:/Users/Jan/Desktop/Scrape/Output/EKU_G" + GameID + "_baserunning.csv"
        sfn = "C:/Users/Jan/Desktop/Scrape/Output/EKU_G" + GameID + "substitutions.csv"
        
        #initialize datasets for Batters and Baserunners
        dh = ActionUnit.get_bat_data_header()
        dh = "GameID,PlateAppID," + dh
        CsvStuff.make_csv_file(btfn,dh)
        
        dh = ActionUnit.get_br_data_header()
        dh = "GameID,PlateAppID," + dh
        CsvStuff.make_csv_file(brfn,dh)
        
        dh = ActionUnit.get_sub_data_header()
        dh = "GameID,PlateAppID," + dh
        CsvStuff.make_csv_file(sfn,dh)
    
        #==========================================================================
        ### PlayByPlay Objects ###
        # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
        #pbp object takes a single pbp string - loop to iterate through play by play string lists
        
        ### AWAY ###
        #Away play by play strings
        
        #Home play by play strings
        side = "Away" #element of Plate Appearance ID
        
        for c,s in enumerate(away_pbps): #c is element of Plate Appearance ID
            #inn keeps track of inning
            inn = c+1
            #inning always begins with no outs and no one on
            BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
            BaseOutEnd = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
            
            #PlayByPlay object, parameter: PlayByPlay (half-inning) string
            p1 = PlayByPlay.PlayByPlay(s)
            p1.do_stuff()
            #p1.print_stuff()
            
            #Output of PlayByPlay class
            ActionUnits = p1.au
            UnitTypes = p1.au_types
            
            #Assign Unique IDs to Plate Appearances
            PA_ID = get_pa_id(ActionUnits, UnitTypes, side, inn, GameID)
                   
            for i,u in enumerate(ActionUnits):
            #these iterate together: ActionUnits, UnitTypes, PA_ID
                if UnitTypes[i] == "bat":
                    #chaining BaseOut states between plate appearances
                    BaseOutStart = BaseOutEnd
                    
                    #initialize batting unit
                    bat1 = ActionUnit.BatUnit(u, "away", AwayOrder, BaseOutStart)
                    bat1.do_stuff()
                    #bat1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = bat1.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    #update ending baseout state to be passed to next br
                    BaseOutEnd = bat1.get_baseout_end()
                    
                elif UnitTypes[i] == "batbr":
                    
                    BaseOutStart = BaseOutEnd
                    
                    bbr1a = ActionUnit.BatUnit(u,"away",AwayOrder,BaseOutStart)
                    bbr1a.do_stuff()
                    BaseOutEnd = bbr1a.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1a.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    bbr1b = ActionUnit.BRUnit(u,"away",AwayOrder,BaseOutStart,BaseOutEnd)
                    bbr1b.do_stuff_batbr()
                    BaseOutEnd = bbr1b.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1b.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                elif UnitTypes[i] == "br":
                    #create br object
                    #initialize baserunning unit
                    br1 = ActionUnit.BRUnit(u, "away", AwayOrder, BaseOutStart, BaseOutEnd)
                    br1.do_stuff()
                    #br1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = br1.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    #update baseout state to pass to next br
                    BaseOutEnd = br1.get_baseout_end()
                    
                elif UnitTypes[i] == "sub":
                    #create sub object
                    #modify game state, batting orders, etc
                    #output dataset
                    sub1 = ActionUnit.SubUnit(u, "away", AwayOrder, AwayOffenSubs, AwayRelievers)
                    sub1.do_stuff()
                    #sub1.print_stuff()
                    #print()
                    ds = sub1.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(sfn,ds)
                    
                    #get modified batting order
                    AwayOrder = sub1.get_updated_bo()
                    
                    
                    
                else:
                    print("!!!ERROR: Main, for Action Units, Invalid Unit Type")
        
        
        ### HOME ###
        #Home play by play strings
        side = "Home" #element of Plate Appearance ID
        
        for c,s in enumerate(home_pbps): #c is element of Plate Appearance ID
            #inn keeps track of inning
            inn = c+1
            #inning always begins with no outs and no one on
            BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
            BaseOutEnd = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
            
            #PlayByPlay object, parameter: PlayByPlay (half-inning) string
            p1 = PlayByPlay.PlayByPlay(s)
            p1.do_stuff()
            #p1.print_stuff()
            
            #Output of PlayByPlay class
            ActionUnits = p1.au
            UnitTypes = p1.au_types
            
            #Assign Unique IDs to Plate Appearances
            PA_ID = get_pa_id(ActionUnits, UnitTypes, side, inn, GameID)
                   
            for i,u in enumerate(ActionUnits):
            #these iterate together: ActionUnits, UnitTypes, PA_ID
                if UnitTypes[i] == "bat":
                    #chaining BaseOut states between plate appearances
                    BaseOutStart = BaseOutEnd
                    
                    #initialize batting unit
                    bat1 = ActionUnit.BatUnit(u, "home", HomeOrder, BaseOutStart)
                    bat1.do_stuff()
                    #bat1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = bat1.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    #update ending baseout state to be passed to next br
                    BaseOutEnd = bat1.get_baseout_end()
                    
                elif UnitTypes[i] == "batbr":
                    
                    BaseOutStart = BaseOutEnd
                    #create bat object and br object
                    
                    bbr1a = ActionUnit.BatUnit(u,"home",HomeOrder,BaseOutStart)
                    bbr1a.do_stuff()
                    BaseOutEnd = bbr1a.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1a.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    bbr1b = ActionUnit.BRUnit(u,"home",HomeOrder,BaseOutStart,BaseOutEnd)
                    bbr1b.do_stuff_batbr()
                    BaseOutEnd = bbr1b.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1b.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                elif UnitTypes[i] == "br":
                    #initialize baserunning unit
                    br1 = ActionUnit.BRUnit(u, "home", HomeOrder, BaseOutStart, BaseOutEnd)
                    br1.do_stuff()
                    #br1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = br1.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    #update baseout state to pass to next br
                    BaseOutEnd = br1.get_baseout_end()
                    
                elif UnitTypes[i] == "sub":
                    #create sub object
                    #modify game state, batting orders, etc
                    #output dataset
                    sub1 = ActionUnit.SubUnit(u, "home", HomeOrder, HomeOffenSubs, HomeRelievers)
                    sub1.do_stuff()
                    #sub1.print_stuff()
                    #print()
                    
                    ds = sub1.get_data_string()
                    ds = GameID + "," + PA_ID[i] + "," + ds
                    CsvStuff.add_row_csv_file(sfn,ds)
                    
                    HomeOrder = sub1.get_updated_bo()
                    
                else:
                    print("!!!ERROR: Main, for Action Units, Invalid Unit Type")
                
        
        # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
        #==========================================================================        
                
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MAIN2: Processes a single csv file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main3():
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
    
    #opening htm file
    filename = "C:/Users/Jan/Desktop/Scrape/htm files/EKU/" + f
    soup = open_soup(filename)
    
    #==========================================================================
    ### Game object ###
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
    
    #output a dataset of GameID | AwayTeam | HomeTeam | Month | Day | Year for GameID table in database
    g = "G" + GameID + "_gameid.csv"
    gamefilename = "C:/Users/Jan/Desktop/Scrape/Output/" + g
    CsvStuff.make_csv_file(gamefilename, "GameID,DoubleHeader,GameofDay,AwayTeam,HomeTeam,GameMonth,GameDay,GameYear")
    gamerowlist = [GameID, DoubleHeader, GameofDay, AwayTeam, HomeTeam, GameMonth, GameDay, GameYear]
    gamerow = CsvStuff.make_csv_row(gamerowlist)
    CsvStuff.add_row_csv_file(gamefilename, gamerow)
    
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
    
    # Lineup Object Parameters:
    # away_starter_list, away_sub_list, home_starter_list, home_sub_list, game_id
    lu1 = Lineup.Lineup(away_starters, away_subs, home_starters, home_subs, GameID)
    
    #Output of Lineup class
    AwayOrder, HomeOrder = lu1.get_batting_orders()
    AwayOffenSubs, HomeOffenSubs = lu1.get_off_subs()
    AwayRelievers, HomeRelievers = lu1.get_relievers()
    
    #producing csv dataset
    lu1.get_lineup_data()
    
    #filename for batting dataset
    btfn = "C:/Users/Jan/Desktop/Scrape/Output/EKU_G" + GameID + "_batting.csv"
    brfn = "C:/Users/Jan/Desktop/Scrape/Output/EKU_G" + GameID + "_baserunning.csv"
    
    #initialize datasets for Batters and Baserunners
    dh = ActionUnit.get_bat_data_header()
    dh = "GameID,PlateAppID," + dh
    CsvStuff.make_csv_file(btfn,dh)
    
    dh = ActionUnit.get_br_data_header()
    dh = "GameID,PlateAppID," + dh
    CsvStuff.make_csv_file(brfn,dh)

    #==========================================================================
    ### PlayByPlay Objects ###
    # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
    #pbp object takes a single pbp string - loop to iterate through play by play string lists
    
    ### AWAY ###
    #Away play by play strings
    
    #Home play by play strings
    side = "Away" #element of Plate Appearance ID
    
    for c,s in enumerate(away_pbps): #c is element of Plate Appearance ID
        #inn keeps track of inning
        inn = c+1
        #inning always begins with no outs and no one on
        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        BaseOutEnd = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        
        #PlayByPlay object, parameter: PlayByPlay (half-inning) string
        p1 = PlayByPlay.PlayByPlay(s)
        p1.do_stuff()
        #p1.print_stuff()
        
        #Output of PlayByPlay class
        ActionUnits = p1.au
        UnitTypes = p1.au_types
        
        #Assign Unique IDs to Plate Appearances
        PA_ID = get_pa_id(ActionUnits, UnitTypes, side, inn, GameID)
               
        for i,u in enumerate(ActionUnits):
        #these iterate together: ActionUnits, UnitTypes, PA_ID
            if UnitTypes[i] == "bat":
                #chaining BaseOut states between plate appearances
                BaseOutStart = BaseOutEnd
                
                #create bat object
                #output stats in new row
                print("PA ID: " + PA_ID[i])
                print("bat: "+u)
                print()
                
                #initialize batting unit
                bat1 = ActionUnit.BatUnit(u, "away", AwayOrder, BaseOutStart)
                bat1.do_stuff()
                #bat1.print_stuff()
                #print()
                
                #add row to csv file
                ds = bat1.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(btfn,ds)
                
                #update ending baseout state to be passed to next br
                BaseOutEnd = bat1.get_baseout_end()
                
            elif UnitTypes[i] == "batbr":
                
                BaseOutStart = BaseOutEnd
                #create bat object and br object(?)
                #output stats in new row
                print("PA ID: " + PA_ID[i])
                print("batbr: "+u)
                print()
                bbr1a = ActionUnit.BatUnit(u,"away",AwayOrder,BaseOutStart)
                bbr1a.do_stuff()
                BaseOutEnd = bbr1a.get_baseout_end()
                
                #add row to csv file
                ds = bbr1a.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(btfn,ds)
                
                bbr1b = ActionUnit.BRUnit(u,"away",AwayOrder,BaseOutStart,BaseOutEnd)
                bbr1b.do_stuff_batbr()
                BaseOutEnd = bbr1b.get_baseout_end()
                
                #add row to csv file
                ds = bbr1b.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(brfn,ds)
                
            elif UnitTypes[i] == "br":
                #create br object
                #output stats in same row
                print("PA ID: " + PA_ID[i])
                print("br: "+u)
                print()
                
                #initialize baserunning unit
                br1 = ActionUnit.BRUnit(u, "away", AwayOrder, BaseOutStart, BaseOutEnd)
                br1.do_stuff()
                #br1.print_stuff()
                #print()
                
                #add row to csv file
                ds = br1.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(brfn,ds)
                
                #update baseout state to pass to next br
                BaseOutEnd = br1.get_baseout_end()
                
            elif UnitTypes[i] == "sub":
                #create sub object
                #modify game state, batting orders, etc
                #output dataset?
                print("PA ID: " + PA_ID[i])
                print("sub: "+u)
                print()
                
                sub1 = ActionUnit.SubUnit(u, "away", AwayOrder, AwayOffenSubs, AwayRelievers)
                sub1.do_stuff()
                sub1.print_stuff()
                print()
                
                AwayOrder = sub1.get_updated_bo()
                
            else:
                print("!!!ERROR: Main, for Action Units, Invalid Unit Type")
    
    
    ### HOME ###
    #Home play by play strings
    side = "Home" #element of Plate Appearance ID
    
    for c,s in enumerate(home_pbps): #c is element of Plate Appearance ID
        #inn keeps track of inning
        inn = c+1
        #inning always begins with no outs and no one on
        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        BaseOutEnd = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        
        #PlayByPlay object, parameter: PlayByPlay (half-inning) string
        p1 = PlayByPlay.PlayByPlay(s)
        p1.do_stuff()
        #p1.print_stuff()
        
        #Output of PlayByPlay class
        ActionUnits = p1.au
        UnitTypes = p1.au_types
        
        #Assign Unique IDs to Plate Appearances
        PA_ID = get_pa_id(ActionUnits, UnitTypes, side, inn, GameID)
               
        for i,u in enumerate(ActionUnits):
        #these iterate together: ActionUnits, UnitTypes, PA_ID
            if UnitTypes[i] == "bat":
                #chaining BaseOut states between plate appearances
                BaseOutStart = BaseOutEnd
                
                #create bat object
                #output stats in new row
                print("PA ID: " + PA_ID[i])
                print("bat: "+u)
                print()
                
                #initialize batting unit
                bat1 = ActionUnit.BatUnit(u, "home", HomeOrder, BaseOutStart)
                bat1.do_stuff()
                #bat1.print_stuff()
                #print()
                
                #add row to csv file
                ds = bat1.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(btfn,ds)
                
                #update ending baseout state to be passed to next br
                BaseOutEnd = bat1.get_baseout_end()
                
            elif UnitTypes[i] == "batbr":
                
                BaseOutStart = BaseOutEnd
                #create bat object and br object(?)
                #output stats in new row
                print("PA ID: " + PA_ID[i])
                print("batbr: "+u)
                print()
                bbr1a = ActionUnit.BatUnit(u,"home",HomeOrder,BaseOutStart)
                bbr1a.do_stuff()
                BaseOutEnd = bbr1a.get_baseout_end()
                
                #add row to csv file
                ds = bbr1a.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(btfn,ds)
                
                bbr1b = ActionUnit.BRUnit(u,"home",HomeOrder,BaseOutStart,BaseOutEnd)
                bbr1b.do_stuff_batbr()
                BaseOutEnd = bbr1b.get_baseout_end()
                
                #add row to csv file
                ds = bbr1b.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(brfn,ds)
                
            elif UnitTypes[i] == "br":
                #create br object
                #output stats in same row
                print("PA ID: " + PA_ID[i])
                print("br: "+u)
                print()
                
                #initialize baserunning unit
                br1 = ActionUnit.BRUnit(u, "home", HomeOrder, BaseOutStart, BaseOutEnd)
                br1.do_stuff()
                #br1.print_stuff()
                #print()
                
                #add row to csv file
                ds = br1.get_data_string()
                ds = GameID + "," + PA_ID[i] + "," + ds
                CsvStuff.add_row_csv_file(brfn,ds)
                
                #update baseout state to pass to next br
                BaseOutEnd = br1.get_baseout_end()
                
            elif UnitTypes[i] == "sub":
                #create sub object
                #modify game state, batting orders, etc
                #output dataset?
                print("PA ID: " + PA_ID[i])
                print("sub: "+u)
                print()
                
                sub1 = ActionUnit.SubUnit(u, "home", HomeOrder, HomeOffenSubs, HomeRelievers)
                sub1.do_stuff()
                sub1.print_stuff()
                print()
                
                HomeOrder = sub1.get_updated_bo()
                
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
    
main1()
    
        
               
    
    
    
    
    
    
    
