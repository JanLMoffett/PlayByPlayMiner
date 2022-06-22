# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:15:00 2019

@author: Jan
"""
# import BeautifulSoup web scraping library
# https://www.crummy.com/software/BeautifulSoup/bs4/
from bs4 import BeautifulSoup
import os
import NewGame
import NewLineup
import NewPlayByPlay
import ActionUnit
import CsvStuff

def main2(): #iterates through directory of html files
    #create game data file
    gdfn = "C:/Users/Jan/Desktop/Scrape/Output/SEC/GameData.csv"
    gh = "GameID,AwayTeamID,HomeTeamID,StartTime,DayNight,Duration,Attendance,City,State,Park,Weather,Umpires" #add variables from new game class
    CsvStuff.make_csv_file(gdfn,gh)
    
    #folder of html files 
    file_list = os.listdir(path = "C:/Users/Jan/Desktop/Scrape/htm files/SEC/")
    
    file_list1 = file_list[1:2]
    
    #test_file_list = file_list[12:13]
    
    for fe in file_list1:
        file_info_dict = get_file_info(fe)
        #these variables will go into game data file
        GameID = file_info_dict["GameID"]
        AwayID = file_info_dict["AwayID"]
        HomeID = file_info_dict["HomeID"]
        
        #test print
        print("GameID: " + GameID)
        
        #enter the htm file name
        filename = "C:/Users/Jan/Desktop/Scrape/htm files/SEC/" + fe
        soup = open_soup(filename)
        
        #Creating Game object
        game1 = NewGame.Game(soup)
        game1.do_stuff()
        #game1.print_stuff()
        #print()
        #print()
        
        #add variables from new game class to GameData csv file gdfn
        #"GameID,AwayTeamID,HomeTeamID,StartTime,DayNight,Duration,Attendance,City,State,Park,Weather,Umpires"
        gdrow = [GameID, AwayID, HomeID, game1.starttime, game1.daynight, game1.duration, game1.attendance, game1.city, game1.state, game1.park, game1.weather, game1.umpires] #game data row
        gdrow_s = CsvStuff.make_csv_row(gdrow)
        CsvStuff.add_row_csv_file(gdfn, gdrow_s)
           
        #get plate appearances and corresponding info from game class
        PAUnits = game1.paunits
        PAUnitSides = game1.paside
        PAUnitIDs = game1.paunitids
        
        #creating Lineup object with lists from game object
        lu1 = NewLineup.Lineup(game1.awaynames, game1.awaypositions, game1.awaystartsub, game1.homenames, game1.homepositions, game1.homestartsub, GameID)
        lu1.do_stuff()
        
        #get lists from lineup class to use in actionunit classes
        AwayOrder = lu1.awayorder
        AwayOffenSubs = lu1.awayoffsubs
        AwayRelievers = lu1.awayrelievers
        
        HomeOrder = lu1.homeorder
        HomeOffenSubs = lu1.homeoffsubs
        HomeRelievers = lu1.homerelievers
        
        #creating files for batting, baserunning, and substitution datasets
        btfn = "C:/Users/Jan/Desktop/Scrape/Output/SEC/" + GameID + "_batting.csv"
        brfn = "C:/Users/Jan/Desktop/Scrape/Output/SEC/" + GameID + "_baserunning.csv"
        sfn = "C:/Users/Jan/Desktop/Scrape/Output/SEC/" + GameID + "_substitutions.csv"
        qcfn = "C:/Users/Jan/Desktop/Scrape/Output/SEC/" + GameID + "_quality.csv"
        
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
        
        dh = "GameID,PlateAppID,AUType,AUString,startOuts,startOnFirst,startOnSecond,startOnThird,startBaseState,startBaseOutState,endOuts,endOnFirst,endOnSecond,endOnThird,endBaseState,endBaseOutState,RPrime"
        CsvStuff.make_csv_file(qcfn,dh)
        
        #create new Play by play object
        pbp1 = NewPlayByPlay.PlayByPlay(PAUnits, PAUnitSides, PAUnitIDs)
        pbp1.do_stuff()
        
        ActionUnits = pbp1.actionunits
        AUTypes = pbp1.autypes
        AUPAIDs = pbp1.aupaids
        AUSides = pbp1.ausides
        
        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        BaseOutEnd = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
    
        
        #iterate through home and away action units, split up based on type
        for i,u in enumerate(ActionUnits):
            if AUSides[i] == "AWAY":
                
                #things i need for qc dataset:
                
                #GameID, PlateAppID, AUType, AUString,
                #startOuts, startOnFirst, startOnSecond,
                #startOnThird, startBaseState, startBaseOutState,
                #endOuts, endOnFirst, endOnSecond, endOnThird,
                #endBaseState, endBaseOutState,
                #RPrime
                
                if AUTypes[i] == "bat":
                    #test print
                    #print("****************bat")
                    
                    #chaining BaseOut states between plate appearances
                    if BaseOutEnd["Outs"] == 3:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = BaseOutEnd
                    
                    #initialize batting unit
                    bat1 = ActionUnit.BatUnit(u, "away", AwayOrder, BaseOutStart)
                    bat1.do_stuff()
                    #bat1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = bat1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    #update ending baseout state to be passed to next br
                    BaseOutEnd = bat1.get_baseout_end()
                    
                    
                elif AUTypes[i] == "batbr":
                    #test print
                    #print("-------------batbr")
                    
                    if BaseOutEnd["Outs"] == 3:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = BaseOutEnd
                        
                    bbr1a = ActionUnit.BatUnit(u,"away",AwayOrder,BaseOutStart)
                    bbr1a.do_stuff()
                    BaseOutEnd = bbr1a.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1a.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    bbr1b = ActionUnit.BRUnit(u,"away",AwayOrder,BaseOutStart,BaseOutEnd)
                    bbr1b.do_stuff_batbr()
                    BaseOutEnd = bbr1b.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1b.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    
                elif AUTypes[i] == "br":
                    #test print
                    #print("================== br")
                    #create br object
                    #initialize baserunning unit
                    br1 = ActionUnit.BRUnit(u, "away", AwayOrder, BaseOutStart, BaseOutEnd)
                    br1.do_stuff()
                    #br1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = br1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    #update baseout state to pass to next br
                    BaseOutEnd = br1.get_baseout_end()
                    
                elif AUTypes[i] == "sub":
                    #run sub unit
                    #create sub object
                    #modify game state, batting orders, etc
                    #output dataset
                    sub1 = ActionUnit.SubUnit(u, "away", AwayOrder, AwayOffenSubs, AwayRelievers)
                    sub1.do_stuff()
                    #sub1.print_stuff()
                    #print()
                    ds = sub1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(sfn,ds)
                    
                    #get modified batting order
                    AwayOrder = sub1.get_updated_bo()
                else:
                    print("!!!Error: invalid value for AUTypes[i]; " + u)
                    
        #this was originally an else, but switching between sides causes logic errors            
        for i,u in enumerate(ActionUnits): #side is HOME
             if AUSides[i] == "HOME":       
                if AUTypes[i] == "bat":
                    #chaining BaseOut states between plate appearances
                    if BaseOutEnd["Outs"] == 3:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = BaseOutEnd
                    
                    #initialize batting unit
                    bat1 = ActionUnit.BatUnit(u, "home", HomeOrder, BaseOutStart)
                    bat1.do_stuff()
                    #bat1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = bat1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn, ds)
                    
                    #update ending baseout state to be passed to next br
                    BaseOutEnd = bat1.get_baseout_end()
                    
                elif AUTypes[i] == "batbr":
                    #chaining BaseOut states between plate appearances
                    if BaseOutEnd["Outs"] == 3:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = BaseOutEnd
                        
                    bbr1a = ActionUnit.BatUnit(u, "home", HomeOrder, BaseOutStart)
                    bbr1a.do_stuff()
                    BaseOutEnd = bbr1a.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1a.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    bbr1b = ActionUnit.BRUnit(u, "home", HomeOrder, BaseOutStart, BaseOutEnd)
                    bbr1b.do_stuff_batbr()
                    BaseOutEnd = bbr1b.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1b.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    
                elif AUTypes[i] == "br":
                    #create br object
                    #initialize baserunning unit
                    br1 = ActionUnit.BRUnit(u, "home", HomeOrder, BaseOutStart, BaseOutEnd)
                    
                    br1.do_stuff()
                    #br1.print_stuff()
                    #print()
                    
                    #add row to csv file
                    ds = br1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    #update baseout state to pass to next br
                    BaseOutEnd = br1.get_baseout_end()
                    
                elif AUTypes[i] == "sub":
                    #run sub unit
                    #create sub object
                    #modify game state, batting orders, etc
                    #output dataset
                    sub1 = ActionUnit.SubUnit(u, "home", HomeOrder, HomeOffenSubs, HomeRelievers)
                    sub1.do_stuff()
                    #sub1.print_stuff()
                    #print()
                    ds = sub1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(sfn,ds)
                    
                    #get modified batting order
                    HomeOrder = sub1.get_updated_bo()
                    
                else:
                    print("!!!Error: invalid value for AUTypes[i]; " + u)
        
        
#______________________________________________________________________________
#==============================================================================
#                                 static methods
#______________________________________________________________________________
#==============================================================================    
#______________________________________________________________________________
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string, encoding = 'utf8') as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup   
#______________________________________________________________________________
def get_file_info(file_end_string):
    #get game id
    gameid = file_end_string[0:file_end_string.find(".html")]
    
    #get away team id
    awayid = file_end_string[0:file_end_string.find("_")]
    
    #get home team id
    homeid = file_end_string[file_end_string.find("_")+1:file_end_string.rfind("_")]
    
    return {"GameID":gameid, "AwayID":awayid, "HomeID":homeid}
#______________________________________________________________________________




#______________________________________________________________________________        
main2()               
    
    
    
    
    
    
    
