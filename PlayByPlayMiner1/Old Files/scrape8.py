# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:15:00 2019

@author: Jan
"""
# import BeautifulSoup web scraping library
# https://www.crummy.com/software/BeautifulSoup/bs4/
from bs4 import BeautifulSoup

# Box Score/Play By Play url pattern
# https://static.ekusports.com/custompages/BB/Stats/2019/3-16-19.htm

#constants
pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]
PA_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "reached", "struck", "singled", "doubled", "tripled", "homered", "hit"]
hit_verbs = ["singled", "doubled", "tripled", "homered"]
on_base_verbs = ["singled", "doubled", "tripled", "homered", "walked", "reached", "hit"]
BR_verbs = ["stole", "advanced", "scored", "out"]
hit_locations = ["to pitcher", "to catcher", "to first base", "to second base", "to third base", "to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field","up the middle", "through the left side", "through the right side", "down the lf line", "down the rf line"]

# 1.) function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
# end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# 2.) function to return home and away teams ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
def get_home_away(soup_obj):
    gameTitle = soup_obj.title.string
    
    vs_ind = (gameTitle.find(" vs "), gameTitle.find(" vs ") + 4)
    p_ind = gameTitle.find("(") - 1
    
    away = gameTitle[0:vs_ind[0]]
    home = gameTitle[vs_ind[1]:p_ind]
    
    return home,away  
# end get_home_away function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
# 3.) function to get opposing school name ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_opponent(soup_obj):
    
    home,away = get_home_away(soup_obj)
    
    if home == "Eastern Kentucky":
        return away
    else:
        return home   
# end get_opponent function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
        
# 4.) function to get a list of pbp strings and remove \n chars
#example of pbp string w/out newlines removed:
#LOVELL, B. to c. BODINE, C. to dh.\nELDRIDGE, Cr struck out swinging (3-2 BFFBBS). DIXSON, Sean flied out to cf to\nright center (3-2 BFBKB). DANIELS, Bla grounded out to ss (1-2 KBF). <i><b>0\nruns, 0 hits, 0 errors, 0 LOB.
def get_pbp_strings(soup_obj):
    font_strings = []
    pbp_strings = []
    front_off = []
    back_off = []
    
    font = soup_obj.find_all("font", face = "verdana", size = 2, color="#000000")
    for string in font:
        font_strings.append(string)
   
    #for i in range(len(pbp_strings)):
    #    print(pbp_strings[i])
    #    print()
      
    for s in font_strings:
        s2 = s.encode("utf8")
        if len(s2) > 100:
            pbp_strings.append(str(s2))
            
    #i for each pbp string
    for s in pbp_strings:
        #j for each character in pbp string[i]
        for j in range(len(s)-14):
            #' - </b></font>'
            if s[j:j+14] == ' - </b></font>':
                front_off.append(s[(j+14) : ]) 
                
    for s in front_off:
        for j in range(len(s)-4):
            if s[j:(j+6)] == "<i><b>":
                back_off.append(s[0 : (j-1)])
    
    
    #newline filter
    return_list = newline_filter(back_off)
    return return_list
# end get_pbp_strings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 4b.) newline filter function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def newline_filter(string_list):
    
    
    no_nl = []
    for i,s in enumerate(string_list):
        ts = ""
        for j in range(0, len(s)):
            
            if s[j] == '\\':
                ts += ' '
            elif j>0 and s[j-1] == '\\':
                continue
            else:
                ts += s[j]
        no_nl.append(ts)
        
    #build return_list
    return no_nl
# end newline filter function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 5.) Function to get strings with b tag and put into list
#Innings id's and summaries are in bold ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_bold_strings(soup_obj):
    # example: 'UT Martin 8th - \n0 runs, 0 hits, 0 errors, 1 LOB.'
    bold = []
    bs = []
    
    b = soup_obj.find_all("b")
    
    for tag in b:
        bold.append(str(tag.string))
     
    for s in bold:
        bs.append(str(s.encode("utf8")))
        
    bs_new = newline_filter(bs)
    
    return bs_new
# close get bold strings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 6.) Function to get list of innings summaries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
#innings summaries are in italics
# example: '1 run, 2 hits, 1 error, 1 LOB.'
def get_inning_summaries(soup_obj):
    raw_summaries = []
    rs = []
    
    it = soup_obj.find_all("i")
    
    for tag in it:
        raw_summaries.append(tag.string)   
    for s in raw_summaries:
        rs.append(str(s.encode("utf8")))
        
    rs = newline_filter(rs)
    
    return rs
# close get_inning_summaries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#7.) function to get names and positions in lineups, and differentiate between teams, then between starts and subs
def get_lineups(soup_obj):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #will return list of away starters and home starters
    lineup_strings = []
    
    lu = soup_obj.find_all("td", align = "left")
    
    for s in lu:
        lineup_strings.append(str(s.string))

    #away team is listed first
    #each team starts with "player" and ends with "totals"
    away = []
    home = []
    
    i = 0
    while lineup_strings[i] != 'Totals\xa0':
        if lineup_strings[i] != 'Player\xa0':
            away.append(lineup_strings[i])
        i += 1
            
    i += 1
    while lineup_strings[i] != 'Totals\xa0':
        if lineup_strings[i] != 'Player\xa0' and lineup_strings[i] != '\xa0\xa0':
            home.append(lineup_strings[i])
        i += 1
    
    away_st = []
    away_su = []
    
    for s in away:
        if s[0] != '\xa0':
            away_st.append(s[:-1])
        else:
            away_su.append(s[3:-1])
    
    home_st = []
    home_su = []
    
    for s in home:
        if s[0] != '\xa0':
            home_st.append(s[:-1])
        else:
            home_su.append(s[3:-1])
    
    return (away_st, away_su, home_st, home_su) 
# close get_lineups~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    
# function to put starters in list in order of position
def get_positions(lineup_list):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #takes a list of strings in format: KERR, Ryland 2b
    #returns list of ten names
    
    pos_order = [""]*10 # 0 will be DH
    
    #read last two chars in string
    for i,s in enumerate(lineup_list):
        for j,t in enumerate(pos):
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                pos_order[j] = s[:s.rfind(" ")]
                
    return pos_order    
# close pos_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
# function to tell whether or not a starter was subbed in the game
# takes lineup lists of subs of variable length, returns boolean list, len = 10 
def was_subbed(sub_list):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    subbed = [False]*10
    
    for i,p in enumerate(pos):
        for j,s in enumerate(sub_list):
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == p:
                subbed[i] = True
                break
           
    return subbed
# close was subbed function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
        
# function to get list of subs based on position
def get_subs(starter_list, sub_list, pos_num):
    sl = sub_list
    pos_subs = []
    
    #check for starter with a / in the string
    for s in starter_list:
        if s.find('/') != -1:
            sl.append(s)    
        
    for s in sl:
        if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[pos_num]:
            pos_subs.append(s[:s.rfind(" ")])
            
    return pos_subs
#close get_subs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
        
# function to get list of relief pitchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_relievers(starter_list, sub_list):
    
    rels = get_subs(starter_list, sub_list, 1)   

    return rels      
# close get_relievers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 

def get_pinch_hitters(sub_list):
    ph = []
    
    for s in sub_list:
        if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
            ph.append(s[:s.rfind(" ")])
            
    return ph
# close get_pinch_hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

def get_pinch_runners(sub_list):
    pr = []
    for s in sub_list:
        if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
            pr.append(s[:s.rfind(" ")])
            
    return pr
# close get_pinch_hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_batting_order(starter_list): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bo = []
    
    for s in starter_list:
        if s[s.rfind(" ")+1:] != "p":
            bo.append(s[:s.rfind(" ")])
    return bo
#close get_batting_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    
#function to break pbp_strings into plate appearances ~~~~~~~~~~~~~~~~~~~~~~~~~
def get_PAs(pbp_string):
    pa = []
    
    #Player[space]PA_verb[space]<Location>
    i = 0
    while i < len(pbp_string):
        t = i
        
        if pbp_string.find(")",i) == -1:
            pa.append(pbp_string[i+1:])
            break
        
        #find the first closing parenth
        i = pbp_string.find(")",i)+2
        #if there is a period after the )
        if pbp_string[i-1] == ".":
            pa.append(pbp_string[t:i])
            i += 1
        else:
            #there are baserunners
            for b in BR_verbs:
                if pbp_string.find(b,i)!= -1:
                    i = pbp_string.find(".", pbp_string.rfind(b,i))+1
                    pa.append(pbp_string[t:i])
                    i += 1
                    break
                    
        
        
    
    
    return pa
#close get_PAs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    
    
            
            
            
            
        
        
        
        
    
    
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    
    
    #enter the file name
    soup = open_soup("htm files/3-02-19b.htm")
    
    oppTm = get_opponent(soup)
    print()
    print("Opposing Team: "+oppTm)
    
    homeTm, awayTm = get_home_away(soup)
    print("Home Team: "+homeTm)
    print("Away Team: "+awayTm)
    print()
    
    #lineups is a list of four lists
    lineups = get_lineups(soup)
    
    #use the lists you get from get_lineups and run them through get_positions
    #to put starters in order by position and was_subbed to determine if the starters
    #were subbed at some point
    home_starters_names = get_positions(lineups[0]) 
    home_subbed = was_subbed(lineups[1])
    away_starters_names = get_positions(lineups[2])
    away_subbed = was_subbed(lineups[3])
    home_relievers = get_relievers(lineups[0], lineups[1])
    home_ph = get_pinch_hitters(lineups[1])
    away_ph = get_pinch_hitters(lineups[3])
    home_pr = get_pinch_runners(lineups[1])
    away_pr = get_pinch_runners(lineups[3])
    
    home_bo = get_batting_order(lineups[0])
    away_bo = get_batting_order(lineups[2])
    
    '''
    
    print("Home starters names:")
    for i,s in enumerate(home_starters_names):
        print(s)
        print(home_subbed[i])
        print()
        
    print("Away starters names:")
    for i,s in enumerate(away_starters_names):
        print(s)
        print(away_subbed[i])
        print()
        
    
    print("Home Relief Pitchers:")
    for s in home_relievers:
        print(s)
        print()
    
    print("Away Relief Pitchers:")    
    away_relievers = get_relievers(lineups[2], lineups[3])
    for s in away_relievers:
        print(s)
        print()
        
    print("Home pinch hitters:")
    for s in home_ph:
        print(s)
        print()
    
    print("Home pinch runners:")
    for s in home_pr:
        print(s)
        print()
        
    print("Away pinch hitters:")
    for s in away_ph:
        print(s)
        print()
        
    print("Away pinch runners:")
    for s in away_pr:
        print(s)
        print()
    '''
    print("Home Batting Order:")
    for s in home_bo:
        print(s)
        print()
        
    print("Away Batting Order:")
    for s in away_bo:
        print(s)
        print()
    
    pbp = get_pbp_strings(soup)
    
    for s in pbp:
        print(s)
        print()
      
    home_pa = get_PAs(pbp[16])
    
    for s in home_pa:
        print(s)
        print()
        
    

    
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    
main()