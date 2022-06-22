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
PA_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "reached", "struck out", "singled", "doubled", "tripled", "homered", "hit by pitch"]
hit_verbs = ["singled", "doubled", "tripled", "homered"]
on_base_verbs = ["singled", "doubled", "tripled", "homered", "walked", "intentionally walked", "reached", "hit by pitch"]
BR_verbs = ["stole", "advanced", "scored", "out"]
hit_locations = ["to pitcher", "to catcher", "to first base", "to second base", "to third base", "to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field","up the middle", "through the left side", "through the right side", "down the lf line", "down the rf line"]
out_locations = ["to p", "to c", "to 1b", "to 2b", "to 3b", "to ss", "to lf", "to cf", "to rf", "ss to 2b"]

# 1.) function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
# end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#           Functions that take soup object made by open_soup
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

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

# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#         Close functions that take soup object made by open_soup
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %


# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#       Functions that take lineup string lists made by get_lineups() 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $

# 8.) function to put starters in list in order of position
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
        
# 9.) function to tell whether or not a starter was subbed in the game
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
        
# 10.) function to get list of subs based on position
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
        
# 11.) function to get list of relief pitchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_relievers(starter_list, sub_list):
    
    rels = get_subs(starter_list, sub_list, 1)   

    return rels      
# close get_relievers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 

# 12.) function to get list of pinch hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_pinch_hitters(sub_list):
    ph = []
    
    for s in sub_list:
        if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
            ph.append(s[:s.rfind(" ")])
            
    return ph
# close get_pinch_hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
# 13.) function to get list of pinch runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_pinch_runners(sub_list):
    pr = []
    for s in sub_list:
        if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
            pr.append(s[:s.rfind(" ")])
            
    return pr
# close get_pinch_runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 14.) function to get a list of starters in batting order
def get_batting_order(starter_list): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bo = []
    
    for s in starter_list:
        if s[s.rfind(" ")+1:] != "p":
            bo.append(s[:s.rfind(" ")])
    return bo
#close get_batting_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#       Close Functions that take lineup string lists made by get_lineups() 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
# Functions that take half inning play-by-play strings made by get_pbp_strings 
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 

# 15.) function to separate substitutions from play-by-play
def sep_substitutions(pbp_string): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Stalman, L. pinch hit for Martellini,G.
    #WILLIAMS, D. to p for LASTER, N..
    subn_strings = []
    new_pbp = ""
    
    a = 0
    b = 0
    
    num_substitutions = pbp_string.count("for")
    
    #return empty list and unchanged string if there are no substitutions in hi
    if num_substitutions == 0:
        return (pbp_string, subn_strings)
    
    t = pbp_string
    for i in range(num_substitutions):
        for_i = t.find("for")
        to_i = t.rfind("to",0,for_i)
        pinch_i = t.rfind("pinch",0,for_i)
        
        if pinch_i > to_i:
            to_i = pinch_i
        
        #will begin and end after '. ' that isn't part of name
        #if substitution is first sentence in paragraph:
        if t.rfind(". ",0,to_i-2) == -1:
            a = 0
        
        else: 
            a = t.rfind(". ",0,to_i-2)+2
        
        b = t.find(". ",for_i)+2
        subn_strings.append(t[a:b-1])
        
        #add to string were subns are removed
        new_pbp += (t[:a])
        
        #update temp string
        t = t[b:]
        
    new_pbp += t
    
    return(new_pbp, subn_strings)       
# close sep substitutions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
           
# 16.) function to break pbp_strings into plate appearances ~~~~~~~~~~~~~~~~~~~
def get_PAs(pbp_string):
    
    pas = []
    ts = pbp_string
    
    i = 1
    while 0<i<len(pbp_string):
        cp = ts.find(")")
        nop = ts.find("(", cp)
        
        if cp == -1:
            break
        
        elif ts[cp+1] == ".":
            pas.append(ts[:cp+2])
            ts = ts[cp+3:]
            i = cp+3
            
        else:
            sc = cp+1
            sc = ts.rfind(";", sc, nop)
            c = ts.find(",", sc)
            p = ts.find(".", sc)
            
            while 0 < p-c <= 3:
                c = ts.find(",",c+1)
                p = ts.find(".",p+1)
                
            
            pas.append(ts[:p+2])
            ts = ts[p+2:]
            i = p+2
            
    #make sure ts is meaningful before adding to list of PA's
    #this might not be necessary at all, but I don't want to take it out rn
    if len(ts) > 12:               
        pas.append(ts)  
        
    return pas    
#close get_PAs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Close functions that take half inning play-by-play strings made by get_pbp_strings 
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 

#******************************************************************************
#              Functions dealing with Plate Appearance strings
#******************************************************************************
    


# 17.) function to get stats from plate appearances ~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_PA_stats(PA_string):
    ts = PA_string
    
    #batter = get_batter(PA_string)
    
    op = ts.find("(")
    cp = ts.find(")")
    
    parenth = ts[op+1:cp]
    
    parenth_stats = process_parenth(parenth)
    
    count_balls = parenth_stats[0]    
    count_strikes = parenth_stats[1]
    
    bs_num = parenth_stats[2]
    
    #remember to add another pitch if ball in play
    num_pitches = bs_num[0]
    
    num_balls = bs_num[1]
    num_called_k = bs_num[2]
    num_swing_k = bs_num[3]
    num_fouls = bs_num[4] 

    
    return {"count_balls":int(count_balls), "count_strikes":int(count_strikes), 
            "num_pitches":num_pitches, "num_balls":num_balls, 
            "num_called_k":num_called_k, "num_swing_k":num_swing_k, 
            "num_fouls":num_fouls}
#close get_PA_stats ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

# 17b.) function to get stats from parentheses ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_parenth(parenth_string): # ex: '3-2 KBKBBK'
    dash = parenth_string.find("-")
    sp = parenth_string.find(" ")
    
    bs = count_bs(parenth_string[sp+1:])
    
    count_b = parenth_string[dash-1]
    count_k = parenth_string[dash+1]
    
    return [count_b, count_k, bs]
#close process_parenth ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 17c.) function to count pitches, balls and strikes ~~~~~~~~~~~~~~~~~~~~~~~~~~
def count_bs(pitch_string):
    b = pitch_string.count("B")
    cs = pitch_string.count("K")
    ss = pitch_string.count("S")
    f = pitch_string.count("F")
    ps = len(pitch_string)
    
    return [ps, b, cs, ss, f]
#close count_bs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   

# 18.) function to id the batter (last, first) of a plate appearance ~~~~~~~~~~
def get_batter(PA_string):
    
    #isolating the first 12 chars of PA string.  i think the max for a name is 12 chars
    ts = PA_string[:12]
    
    #look from the right for a space followed by a lowercase letter
    rsp = ts.rfind(" ")
    if 0 < rsp < len(ts)-1 and 'a' < ts[rsp+1] < 'z':
        ts = ts[0: rsp]
    
    #finding landmarks
    comma = ts.find(",")
    sp = ts.find(" ")
    
    #determine what format name is in, could be anything
    #some possibilities:
    
    # Britton | Ramirez, III | A. Felder | LEWIS, A.J. | HARRIS IV, D | LEWIS, J.
    # Nicastro,J. | J. Shelby | Martellini,G | Dempsey, B | Frelick, S. | Bryan Wilson 
    
    #2 main categories: with comma, without comma
    if comma > 0: #there is a comma
        #sep into before=last and after=first
        last,first = ts.split(",")
        last = last.strip()
        first = first.strip()
        #print("last: " + last)
        #print("first: " + first)
        
    else: #there's no comma
        #look for a space
        if sp > 0: #there is a space
            #sep into before=last and after=first
            first,last = ts.split(" ")
            last = last.strip()
            first = first.strip()
            #print("last: " + last)
            #print("first: " + first)
        
        else: #there's no space
            last = ts
            last = last.strip()
            first = ""
            #print("last: " + last)
            #print("first: " + first)
     
    #standardizing name formats: rem punc, make title case
    first = first.strip(".")
    first = first.title()
    last = last.title()
    
    return (last,first)    
# close get_batter function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    









#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    
    
    #enter the file name
    soup = open_soup("htm files/3-19-19.htm")
    
    oppTm = get_opponent(soup)
    print()
    print("Opposing Team: "+oppTm)
    
    homeTm, awayTm = get_home_away(soup)
    print("Home Team: "+homeTm)
    print("Away Team: "+awayTm)
    print()
    
    lu = get_lineups(soup)
    
    away_starters = get_positions(lu[0])
    print("Away starters:")
    for s in away_starters:
        print(s)
        print()
        
    away_subs = lu[1]
    print("Away subs:")
    for s in away_subs:
        print(s)
        print()
        
    home_starters = get_positions(lu[2])
    print("Home starters:")
    for s in home_starters:
        print(s)
        print()
        
    home_subs = lu[3]
    print("Home subs:")
    for s in home_subs:
        print(s)
        print()
    
    pbps = get_pbp_strings(soup)
    
    print("Substitutions:")
    pbps2, subns = sep_substitutions(pbps[9])
    
    for s in subns:
        print(s)
        print()
        
    print("Play by Play string:")
    print(pbps2)
    print()
    
    print("Plate Appearances:")
    PA = get_PAs(pbps2)
    for s in PA:
        print(s[0:12])
        print()
        
    '''    
    print("PA Stats:")
    PA_stat_dict = get_PA_stats(PA[0])
    '''
    
    last_names = []
    first_names = []
    
    for s in PA:
        l,f = get_batter(s)
        last_names.append(l)
        first_names.append(f)
    
    print("last names:")    
    for s in last_names:
        print(s)
    print()

    print("first names:")
    for s in first_names:
        print(s)
    print()
    
            
    
    
    
    '''
    file = open("writetest.txt","w")
    
    file.write(str(PA_stat_dict))
    
    file.close()
    '''
    
    
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
main()