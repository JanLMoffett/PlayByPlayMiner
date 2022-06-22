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
import re


# Box Score/Play By Play url pattern
# https://static.ekusports.com/custompages/BB/Stats/2019/3-16-19.htm



#//////////////////////////// STATIC FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


#////////////////////////// CLOSE STATIC FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\ 
  #45,72,146,161,167
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN1 - iterates through a folder of files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main1():
    #folder of html files 
    #file_list = os.listdir(path = "C:/Users/Jan/Desktop/Scrape/htm files/EKU/")
    
    #create csv for dataset of games and gameid's
    gdfn = "C:/Users/Jan/Desktop/Scrape/Output/GameData.csv"
    gh = "GameID,AwayTeam,HomeTeam,Weekday,GameMonth,GameDay,GameYear,DH,GameofDay"
    CsvStuff.make_csv_file(gdfn,gh)
    
    #html file name
    f1 = "ARIZ_UCLA_03241901.html"
    f2 = "TENN_AUBN_03151901.htm"
    
    
    #enter the htm file name
    filename = "C:/Users/Jan/Desktop/Scrape/htm files/TEST/" + f2
    soup = open_soup(filename)
    
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Title:")
    print(soup.title)
    print()
    '''
    <title>
        Baseball vs Tennessee on 3/15/2019 - Box Score - Auburn University Athletics
    </title>
    '''
    print("___________________________________")
    
    spaces = "&nbsp;&nbsp;&nbsp;&nbsp;"
    subs = []
    panels = soup.find_all("section", class_="panel")
    
    '''
    print("Panels:")
    for p in panels:
        b = p.find("tbody")
        
        print("Table Body:")
        
            
        th = b.find_all("th", scope="row")
        
        print("Table Body Contents:")
        for t in th:
            for c in t.contents:
                print(c)
            print()
        print()
                    
        print("===================================")  
    '''
        
    #panel 2, tbody 1, all contents
    #this gives the opposing lineup
    
    #__________________________________________________________________________
    #panel2 contains tables with lineups
    panel2 = panels[1]
    #table bodies from panel2
    tbodies = panel2.find_all("tbody")
    #__________________________________________________________________________
    
    #raw lu lists contain all contents of the table bodies
    
    #website team
    web_raw_lu_list = tbodies[0].contents
    #opposing team 
    opp_raw_lu_list = tbodies[1].contents
    
    
    #__________________________________________________________________________
    
    #list of positions
    
    web_pos_list = tbodies[0].find_all("td", class_="text-uppercase hide-on-small-down")
    WebPosList = []
    for n in web_pos_list:
        #print(n.string)
        WebPosList.append(n.string)
    #print()
    
    print("WebPosList:")
    print(WebPosList)  
    
    opp_pos_list = tbodies[1].find_all("td", class_="text-uppercase hide-on-small-down")
    OppPosList = []
    for n in opp_pos_list:
        #print(n.string)
        OppPosList.append(n.string)
    #print()
    
    print("OppPosList:")
    print(OppPosList)
            
    #__________________________________________________________________________    
        
        
        
    print()
    
    
    
    
    
    '''
    #This delivers all the unit strings grouped by half-inning, with some extra crap
    us = soup.find_all("table", class_ = "sidearm-table")
    for u in us:
        th = u.find_all("th", scope = "row", string = True)
        for t in th:
            if "." in t.string:
                print(t.string)
        print()
    print("___________________________________")
    '''
    
    
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#______________________________________________________________________________
#==============================================================================
#                                 static methods
#______________________________________________________________________________
#==============================================================================
    
#______________________________________________________________________________
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup   
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
    
        
               
    
    
    
    
    
    
    
