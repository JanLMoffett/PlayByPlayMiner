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

def main2():
#enter the htm file name
    f = "4-12-19.htm" #enter file here
    filename = "C:/Users/Jan/Desktop/Scrape/htm files/" + f
    soup = open_soup(filename)
    
    #==========================================================================
    ### Game object ###
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    g1 = Game.Game(soup)
    AwayTeam = g1.away_team
    HomeTeam = g1.home_team
    GameMonth = g1.game_month
    GameDay = g1.game_day
    GameYear = g1.game_year
    
    #strings to add to bottom of csv files
    game_info_string1 = "GameMonth,GameDay,GameYear,AwayTeam,HomeTeam"
    game_info_list = [GameMonth, GameDay, GameYear, AwayTeam, HomeTeam]
    game_info_string2 = CsvStuff.make_csv_row(game_info_list)
    
    print("Game Info:")
    print(game_info_list)
    print()
    
    ### output of Game class ###
    
    lus = g1.get_lineups() #this is a dict of four lists
    #extracting lists from dict
    away_starters = lus["away_starters"]
    away_subs = lus["away_subs"]
    home_starters = lus["home_starters"]
    home_subs = lus["home_subs"]
    
    print("Away Starters: ")
    print(away_starters)
    print()
    print("Away Subs: ")
    print(away_subs)
    print()
    print("Home Starters: ")
    print(home_starters)
    print()
    print("Home Subs: ")
    print(home_subs)
    print()
    #lineups are still in original format
    
    pbps = g1.get_pbp_strings() #this is a list of half-inning strings
    #dividing half-inning strings into away and home
    away_pbps = pbps[0::2]
    #home_pbps = pbps[1::2]
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    #==========================================================================
    
    #==========================================================================
    ### Lineup Object ###
    # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
    lu1 = Lineup.Lineup(away_starters, away_subs, home_starters, home_subs)
    
    
    AwayPos,HomePos = lu1.get_pos_order() #returns dicts of positions and names
    AwaySubbed,HomeSubbed = lu1.was_subbed() #returns boolean lists in position order (indices match AwayPos and HomePos dicts)
    AwayPH,HomePH = lu1.get_pinch_hitters() #returns string lists of names
    AwayPR,HomePR = lu1.get_pinch_runners() #returns string lists of names
    AwayOrder,HomeOrder,AwayBO,HomeBO = lu1.get_batting_orders() #returns dicts of holes and names
    
    AwayRelievers,HomeRelievers = lu1.get_relievers() #returns string lists of names
    
    print("Away Pos:")
    print(AwayPos)
    print()
    print("Home Pos:")
    print(HomePos)
    print()
    
    
    print("Away Order:")
    print(AwayOrder)
    print()
    
    print("Home Order:")
    print(HomeOrder)
    print()
    
    
    
    # % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
    
    #make csv of lineup dataset
    
    #==========================================================================
    
    #==========================================================================
    ### PlayByPlay Objects ###
    # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
    #pbp object takes a single pbp string - loop to iterate through play by play string lists
    
    #create csv file for batting dataset
    BatHeaderList = ["Team","Name","Hole","CountBalls","CountStrikes","PitchString","Balls","Fouls","CalledKs","SwingKs","BIPs","Pitches","BIP","Hit","Bases","Single","Double","Triple","Homer","HitLoc","HitQual","HitType","IFH","Walk","IBB","UBB","StrikeOut","KSwing","KLook","TOC","SAC","Bunt","RBOE","FC","FieldOut","DP","HBP","UCTS","SOReach","SF","DPType","FOLocation","FOType","FOQuality","OutsAdded","BasesAdded","RunsAdded","bo_Outs","bo_OnFirst","bo_OnSecond","bo_OnThird","bo_BaseState","boBaseOutState"]
    BatHeader = CsvStuff.make_csv_header(BatHeaderList)
    fn_bat = "bat_setX.csv"
    CsvStuff.make_csv_file(fn_bat, BatHeader)
    
    #create csv file for baserunning dataset
    BRHeaderList = ["Team", "Name", "Hole", "Action", "StartBase", "EndBase", "BasesAdded", "OutsAdded", "RunsAdded", "SBA", "SB", "CS", "POA", "PO", "FPO", "WP", "PB", "AOE","bo_Outs","bo_OnFirst","bo_OnSecond","bo_OnThird","bo_BaseState","boBaseOutState"]
    BRHeader = CsvStuff.make_csv_header(BRHeaderList)
    fn_br = "br_setX.csv"
    CsvStuff.make_csv_file(fn_br, BRHeader)
    
    
    
    ### AWAY ###
    #Away play by play strings
    for s in away_pbps:
        p1 = PlayByPlay.PlayByPlay(s)
        #NumUnits = p1.num_au
        #NumBats = p1.num_bats
        #NumBRs = p1.num_brs
        #NumSubs = p1.num_subs
        
        #initializing BaseOut with default values, to pass in and out of ActionUnit methods
        BaseOutDict = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        #these methods set values self.au_types and self.au
        
        p1.get_action_units()
        p1.get_types()
        
        AUTypes = p1.au_types
        ActionUnits = p1.au
        
        
        #sort pbp strings by type and create ActionUnit objects, ouput csvs
        
        #iterate through action units and type lists
        for i,u in enumerate(ActionUnits):
            print("Type: "+AUTypes[i]+", Unit: "+u)
            print()
            
            ### Bat Type ###
            if AUTypes[i] == "bat": 
                
                
                
                #prints for testing
                print("Top of Bat")
                print(BaseOutDict)
                print()
                
                #make a BatUnit object
                bat1 = ActionUnit.BatUnit(u, "away", AwayOrder, BaseOutDict)
                
                #variables
                bat1.get_name()
                Name = bat1.batter_name
                
                
                CountBalls = bat1.count_balls
                CountStrikes = bat1.count_strikes
                
                #no arg setters
                bat1.get_hole()
                Hole = bat1.hole
                
                BIP = bat1.is_bip()
                #if BIP: location, quality, hit/out/reach, productive out
                
                
                
                #variables
                Team = AwayTeam
                PitchString = bat1.pitch_string
                PitchDict = bat1.get_pitches()
                Balls = PitchDict["Balls"] 
                Fouls = PitchDict["Fouls"]
                CalledKs = PitchDict["CalledKs"]
                SwingKs = PitchDict["SwingKs"]
                BIPs = PitchDict["BIPs"]
                Pitches = PitchDict["Pitches"]
                
                Walk = bat1.is_walk()
                BBDict = bat1.get_walk_type() 
                UBB = BBDict["UBB"]
                IBB = BBDict["IBB"]
                
                StrikeOut = bat1.is_strikeout()
                #if strikeout, type of strikeout, count balls, composition of preceding pitch string
            
                SODict = bat1.get_so_type()
                KSwing = SODict["KSwing"]
                KLook = SODict["KLook"]
                UCTS = SODict["UCTS"]
                SOReach = SODict["SOReach"]
                
                Hit = bat1.is_hit()
                #if hit: bases, is_single, is_double, is_triple, is_homerun, location, quality
                
                HDict1 = bat1.get_hit()
                Bases = HDict1["Bases"]
                Single = HDict1["Single"]
                Double = HDict1["Double"]
                Triple = HDict1["Triple"]
                Homer = HDict1["Homer"]
                    
                HDict2 = bat1.get_hit_info()
                #{"Location":loc, "Quality":qual, "BattedBallType":bb_type, "IFH":infh}
                HitLoc = HDict2["Location"]
                HitQual = HDict2["Quality"]
                HitType = HDict2["BattedBallType"]
                IFH = HDict2["IFH"]
                
                SAC = bat1.is_sac()
                SF = bat1.is_sf()
                Bunt = bat1.is_bunt()
                
                TOC = bat1.is_true_outcome()
                
                #Reach
                bat1.is_reach()
                RDict = bat1.get_reach()
                RBOE = RDict["RBOE"]
                FC = RDict["FC"]
                HBP = bat1.is_hbp() 
                
                #Field Out
                FieldOut = bat1.is_field_out()
                FODict = bat1.get_field_out()
                FOLocation = FODict["FOLocation"]
                FOType = FODict["FOType"]
                FOQuality = FODict["FOQuality"]
                
                #Double Play
                DP = bat1.is_double_play()
                DPType = bat1.get_double_play()
                
                OutsAdded = bat1.outsadded
                BasesAdded = bat1.basesadded
                RunsAdded = bat1.runsadded
                
                #catch BaseOut state after updated by BatUnit
                BaseOutDict = bat1.update_bod()
                
                #printing
                #bat1.print_stuff()
                
                bo_Outs = BaseOutDict["Outs"]
                bo_OnFirst = BaseOutDict["OnFirst"]
                bo_OnSecond = BaseOutDict["OnSecond"]
                bo_OnThird = BaseOutDict["OnThird"]
                bo_BaseState = BaseOutDict["BaseState"]
                bo_BaseOutState = BaseOutDict["BaseOutState"]
                
                #csv for bat dataset
                BatRowList = [Team, Name, Hole, CountBalls, CountStrikes, PitchString, Balls, Fouls, CalledKs, SwingKs, BIPs, Pitches, BIP, Hit, Bases, Single, Double, Triple, Homer, HitLoc, HitQual, HitType, IFH, Walk, IBB, UBB, StrikeOut, KSwing, KLook, TOC, SAC, Bunt, RBOE, FC, FieldOut, DP, HBP, UCTS, SOReach, SF, DPType, FOLocation, FOType, FOQuality, OutsAdded, BasesAdded, RunsAdded, bo_Outs, bo_OnFirst, bo_OnSecond, bo_OnThird, bo_BaseState, bo_BaseOutState]
                BatRow = CsvStuff.make_csv_row(BatRowList)
                CsvStuff.add_row_csv_file(fn_bat, BatRow)
            
            ### BR Type ###
            elif AUTypes[i] == "br":
                #prints for testing
                print("Top of BR")
                print(BaseOutDict)
                print()
                
                
                
                br1 = ActionUnit.BRUnit(u, "away", AwayOrder, BaseOutDict)
                br1.get_runner_name()
                
                br1.get_action()
                br1.get_advanced()
                br1.get_stole()
                br1.get_scored()
                br1.get_out()
                br1.is_pickoff()
                
                #variables
                Name = br1.runner_name
                
                #print for debug
                print("********************Start State:")
                print(StartStateDict)
                print("Runner Name: " + Name)
                print()
                
                #once you have runner's name, check bases for match to set start_base
                if Name == StartStateDict["OnSecond"]:
                    br1.set_start_base(2)
                elif Name == StartStateDict["OnThird"]:
                    br1.set_start_base(3)
                else:
                    br1.set_start_base(1) #first base is the default
                
                Hole = br1.hole
                
                Action = br1.action
                SBA = br1.sba
                SB = br1.sb
                CS = br1.cs
                
                POA = br1.poa
                FPO = br1.fpo
                PO = br1.po
                
                WP = br1.wp
                PB = br1.pb
                AOE = br1.aoe
                
                StartBase = br1.start_base
                EndBase = br1.end_base
                
                br1.get_bases_added()
                BasesAdded = br1.basesadded
                
                OutsAdded = br1.outsadded
                RunsAdded = br1.runsadded
                
                BaseOutDict = br1.update_bod()
                
                bo_Outs = BaseOutDict["Outs"]
                bo_OnFirst = BaseOutDict["OnFirst"]
                bo_OnSecond = BaseOutDict["OnSecond"]
                bo_OnThird = BaseOutDict["OnThird"]
                bo_BaseState = BaseOutDict["BaseState"]
                bo_BaseOutState = BaseOutDict["BaseOutState"]
                
                br1.print_stuff()
                print(BaseOutDict)
                print()
                
                BRRowList = [Team, Name, Hole, Action, StartBase, EndBase, BasesAdded, OutsAdded, RunsAdded, SBA, SB, CS, POA, PO, FPO, WP, PB, AOE, bo_Outs, bo_OnFirst ,bo_OnSecond, bo_OnThird ,bo_BaseState, bo_BaseOutState]
                BRRow = CsvStuff.make_csv_row(BRRowList)
                CsvStuff.add_row_csv_file(fn_br, BRRow)
            
            ### Sub Type ###
            else:
                sub1 = ActionUnit.SubUnit(u, "away", AwayOrder, away_subs)
                sub1.mod_batting_order()
                sub1.print_stuff()
                
                #variables
                                        
                #make csv file for sub dataset
                
    CsvStuff.add_row_csv_file(fn_bat,game_info_string1)  
    CsvStuff.add_row_csv_file(fn_bat,game_info_string2)
        
        
        
        #Home play by play strings
        
            
    
    # $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
    #==========================================================================

                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
main2()
    
        
                
    
    
    
    
    
    
    
