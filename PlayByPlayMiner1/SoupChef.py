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

def main(): #iterates through directory of html files
    #create game data file
    gdfn = "C:/Users/Jan/Desktop/Scrape/Output/SEC/GameData.csv"
    gh = "GameID,AwayTeamID,HomeTeamID,StartTime,DayNight,Duration,Attendance,City,State,Park,Weather,Umpires" #add variables from new game class
    CsvStuff.make_csv_file(gdfn,gh)
    
    #folder of html files 
    file_list = os.listdir(path = "C:/Users/Jan/Desktop/Scrape/htm files/SEC/")
    
    test_file = file_list[100:103]
    
    #==========================================================================
    #change input here:
    #==========================================================================
    for fe in test_file:
        file_info_dict = get_file_info(fe)
        #these variables will go into game data file
        GameID = file_info_dict["GameID"]
        AwayID = file_info_dict["AwayID"]
        HomeID = file_info_dict["HomeID"]
        
        #test print to id errors
        print("GameID: " + GameID)
        
        #enter the htm file name
        filename = "C:/Users/Jan/Desktop/Scrape/htm files/SEC/" + fe
        soup = open_soup(filename)
        
        #Creating Game object
        game1 = NewGame.Game(soup)
        game1.do_stuff()
        #test print
        #game1.print_stuff()
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
        #test print
        #print("Lineup print $$$$$$$$$$$$$$$$$$$$$$$$$")
        #lu1.print_stuff()
        #print()
        
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
        
        #these iterate together:
        ActionUnits = pbp1.actionunits
        AUTypes = pbp1.autypes
        AUPAIDs = pbp1.aupaids
        AUSides = pbp1.ausides
        AUHalfInnings = pbp1.auhalfinnings
        
        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        BaseOutEnd = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
    
        current_inning = 0 #compare to AUInnings[i] to determine if StartBaseOutState should be reset 
        current_pa = ""
        
        #iterate through home and away action units, split up based on type
        for i,u in enumerate(ActionUnits):
            if AUSides[i] == "AWAY":
                if AUTypes[i] == "bat":
                    #setting current pa
                    current_pa = AUPAIDs[i]
                    
                    #chaining BaseOut states between plate appearances, resetting if inning has changed
                    if current_inning < AUHalfInnings[i]:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = {"Outs":BaseOutEnd["Outs"], "OnFirst":BaseOutEnd["OnFirst"], "OnSecond":BaseOutEnd["OnSecond"], "OnThird":BaseOutEnd["OnThird"], "BaseState":BaseOutEnd["BaseState"], "BaseOutState":BaseOutEnd["BaseOutState"]}
                    
                    #update current_inning
                    current_inning = AUHalfInnings[i]
                    
                    #initialize batting unit
                    bat1 = ActionUnit.BatUnit(u, "away", AwayOrder, BaseOutStart)
                    bat1.do_stuff()
                    #test print
                    #bat1.print_stuff()
                    #print()
                    #update ending baseout state to be passed to next br
                    BaseOutEnd = bat1.get_baseout_end()
                    
                    #add row to csv file
                    ds = bat1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(","," "), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], bat1.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    
                    #test print
                    #print("qcds bat: " + qcds)
                    #print()
                    
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                elif AUTypes[i] == "batbr":
                    #setting current pa
                    current_pa = AUPAIDs[i]
                    
                    #chaining BaseOut states between plate appearances, resetting if inning has changed
                    if current_inning < AUHalfInnings[i]:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = {"Outs":BaseOutEnd["Outs"], "OnFirst":BaseOutEnd["OnFirst"], "OnSecond":BaseOutEnd["OnSecond"], "OnThird":BaseOutEnd["OnThird"], "BaseState":BaseOutEnd["BaseState"], "BaseOutState":BaseOutEnd["BaseOutState"]}
                    
                    #update current_inning
                    current_inning = AUHalfInnings[i]
                        
                    bbr1a = ActionUnit.BatUnit(u,"away",AwayOrder,BaseOutStart)
                    bbr1a.do_stuff()
                    BaseOutEnd = bbr1a.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1a.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",",""), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], bbr1a.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    #test print
                    #print("qcds batbr bat: " + qcds)
                    #print()
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                    bbr1b = ActionUnit.BRUnit(u,"away",AwayOrder,BaseOutStart,BaseOutEnd)
                    bbr1b.do_stuff_batbr()
                    BaseOutEnd = bbr1b.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1b.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",",""), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], bbr1b.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    #test print
                    #print("qcds batbr br: " + qcds)
                    #print()
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                elif AUTypes[i] == "br":
                    #create br object
                    
                    #distinguish between stand-alone baserunning units and those that are part of a plate appearance
                    #look to see if pa id stays the same
                    #if new pa id, update baseoutstart to baseoutend
                    
                    #create a totally new dict to keep it from muting
                    if current_pa != AUPAIDs[i]:
                        BaseOutStart = {"Outs":BaseOutEnd["Outs"], "OnFirst":BaseOutEnd["OnFirst"], "OnSecond":BaseOutEnd["OnSecond"], "OnThird":BaseOutEnd["OnThird"], "BaseState":BaseOutEnd["BaseState"], "BaseOutState":BaseOutEnd["BaseOutState"]}
                    
                    #initialize baserunning unit
                    br1 = ActionUnit.BRUnit(u, "away", AwayOrder, BaseOutStart, BaseOutEnd)
                    br1.do_stuff()
                    #br1.print_stuff()
                    #print()
                    
                    #update baseout state to pass to next br
                    BaseOutEnd = br1.get_baseout_end()
                    
                    #add row to csv file
                    ds = br1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",",""), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], br1.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    #print("qcds br: "+qcds)
                    #print()
                    
                elif AUTypes[i] == "sub":
                    #run sub unit
                    #create sub object
                    #modify game state, batting orders, etc
                    #output dataset
                    
                    sub1 = ActionUnit.SubUnit(u, "away", AwayOrder, AwayOffenSubs, AwayRelievers, HomeOrder, HomeOffenSubs, HomeRelievers)
                    sub1.do_stuff()
                    #sub1.print_stuff()
                    #print()
                    
                    ds = sub1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(sfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",","")] + ["NA"]*13
                    qcds = CsvStuff.make_csv_row(qcd)
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                    #get modified batting order
                    AwayOrder, HomeOrder = sub1.get_updated_bo()
                    
                #add in "other" contingency
                elif AUTypes[i] == "other" :
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",","")] + ["NA"]*13
                    qcds = CsvStuff.make_csv_row(qcd)
                    CsvStuff.add_row_csv_file(qcfn,qcds)    
                    
                    print("!!!Warning: 'other' value for AUTypes[i]; " + u)
                else:
                    print("!!!Error: invalid value for AUTypes[i]; " + u)
                    
        #this was originally an else, but switching between sides causes logic errors            
        #for i,u in enumerate(ActionUnits): #side is HOME
            elif AUSides[i] == "HOME":       
                if AUTypes[i] == "bat":
                    #setting current pa
                    current_pa = AUPAIDs[i]
                    
                    #chaining BaseOut states between plate appearances, resetting if inning has changed
                    if current_inning < AUHalfInnings[i]:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = {"Outs":BaseOutEnd["Outs"], "OnFirst":BaseOutEnd["OnFirst"], "OnSecond":BaseOutEnd["OnSecond"], "OnThird":BaseOutEnd["OnThird"], "BaseState":BaseOutEnd["BaseState"], "BaseOutState":BaseOutEnd["BaseOutState"]}
                    
                    #update current_inning
                    current_inning = AUHalfInnings[i]
                    
                    #initialize batting unit
                    bat1 = ActionUnit.BatUnit(u, "home", HomeOrder, BaseOutStart)
                    bat1.do_stuff()
                    #test print
                    #bat1.print_stuff()
                    #print()
                    #update ending baseout state to be passed to next br
                    BaseOutEnd = bat1.get_baseout_end()
                    
                    #add row to csv file
                    ds = bat1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(","," "), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], bat1.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    
                    #test print
                    #print("qcds bat: " + qcds)
                    #print()
                    
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                elif AUTypes[i] == "batbr":
                    #setting current pa
                    current_pa = AUPAIDs[i]
                    
                    #chaining BaseOut states between plate appearances, resetting if inning has changed
                    if current_inning < AUHalfInnings[i]:
                        BaseOutStart = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
                    else:
                        BaseOutStart = {"Outs":BaseOutEnd["Outs"], "OnFirst":BaseOutEnd["OnFirst"], "OnSecond":BaseOutEnd["OnSecond"], "OnThird":BaseOutEnd["OnThird"], "BaseState":BaseOutEnd["BaseState"], "BaseOutState":BaseOutEnd["BaseOutState"]}
                    
                    #update current_inning
                    current_inning = AUHalfInnings[i]
                        
                    bbr1a = ActionUnit.BatUnit(u,"home",HomeOrder,BaseOutStart)
                    bbr1a.do_stuff()
                    BaseOutEnd = bbr1a.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1a.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(btfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",",""), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], bbr1a.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    #test print
                    #print("qcds batbr bat: " + qcds)
                    #print()
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                    bbr1b = ActionUnit.BRUnit(u,"home",HomeOrder,BaseOutStart,BaseOutEnd)
                    bbr1b.do_stuff_batbr()
                    BaseOutEnd = bbr1b.get_baseout_end()
                    
                    #add row to csv file
                    ds = bbr1b.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",",""), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], bbr1b.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    #test print
                    #print("qcds batbr br: " + qcds)
                    #print()
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                elif AUTypes[i] == "br":
                    #create br object
                    
                    #distinguish between stand-alone baserunning units and those that are part of a plate appearance
                    #look to see if pa id stays the same
                    #if new pa id, update baseoutstart to baseoutend
                    
                    #create a totally new dict to keep it from muting
                    if current_pa != AUPAIDs[i]:
                        #if br unit isn't part of a batting plate appearance (like a wild pitch or stolen base)
                        BaseOutStart = {"Outs":BaseOutEnd["Outs"], "OnFirst":BaseOutEnd["OnFirst"], "OnSecond":BaseOutEnd["OnSecond"], "OnThird":BaseOutEnd["OnThird"], "BaseState":BaseOutEnd["BaseState"], "BaseOutState":BaseOutEnd["BaseOutState"]}
                        #reset current_pa
                        current_pa = AUPAIDs[i] #?
                    
                    
                    #initialize baserunning unit
                    br1 = ActionUnit.BRUnit(u, "home", HomeOrder, BaseOutStart, BaseOutEnd)
                    br1.do_stuff()
                    #test print
                    #br1.print_stuff()
                    #print()
                    
                    #update baseout state to pass to next br
                    BaseOutEnd = br1.get_baseout_end()
                    
                    #add row to csv file
                    ds = br1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(brfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",",""), BaseOutStart["Outs"], BaseOutStart["OnFirst"], BaseOutStart["OnSecond"], BaseOutStart["OnThird"], BaseOutStart["BaseState"], BaseOutStart["BaseOutState"], BaseOutEnd["Outs"], BaseOutEnd["OnFirst"], BaseOutEnd["OnSecond"], BaseOutEnd["OnThird"], BaseOutEnd["BaseState"], BaseOutEnd["BaseOutState"], br1.runsadded]
                    qcds = CsvStuff.make_csv_row(qcd)
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    #print("qcds br: "+qcds)
                    #print()
                    
                elif AUTypes[i] == "sub":
                    #run sub unit
                    #create sub object
                    #modify game state, batting orders, etc
                    #output dataset
                    sub1 = ActionUnit.SubUnit(u, "home", AwayOrder, AwayOffenSubs, AwayRelievers, HomeOrder, HomeOffenSubs, HomeRelievers)
                    sub1.do_stuff()
                    #test print
                    #sub1.print_stuff()
                    #print()
                    
                    ds = sub1.get_data_string()
                    ds = GameID + "," + (GameID+"_"+AUPAIDs[i]) + "," + ds
                    CsvStuff.add_row_csv_file(sfn,ds)
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",","")] + ["NA"]*13
                    qcds = CsvStuff.make_csv_row(qcd)
                    CsvStuff.add_row_csv_file(qcfn,qcds)
                    
                    #get modified batting order
                    AwayOrder, HomeOrder = sub1.get_updated_bo()
                    
                #add in "other" contingency
                elif AUTypes[i] == "other" :
                    
                    qcd = [GameID, (GameID+"_"+AUPAIDs[i]), AUTypes[i], u.replace(",","")] + ["NA"]*13
                    qcds = CsvStuff.make_csv_row(qcd)
                    CsvStuff.add_row_csv_file(qcfn,qcds)    
                    
                    print("!!!Warning: 'other' value for AUTypes[i]; " + u)
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
main()               
    
    
    
    
    
    
    
