# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:15:00 2019

@author: Jan
"""
#import BeautifulSoup web scraping library
# https://www.crummy.com/software/BeautifulSoup/bs4/
from bs4 import BeautifulSoup

# Box Score/Play By Play url pattern
#https://static.ekusports.com/custompages/BB/Stats/2019/3-16-19.htm


# 1.) function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
#end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# 2.) function to return home and away teams ~~~~~~~~~~~~~~~~   
def get_home_away(soup_obj):
    gameTitle = soup_obj.title.string
    
    vs_ind = (gameTitle.find(" vs "), gameTitle.find(" vs ") + 4)
    p_ind = gameTitle.find("(") - 1
    
    away = gameTitle[0:vs_ind[0]]
    home = gameTitle[vs_ind[1]:p_ind]
    
    return home,away  
#end get_home_away function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#f 3.) unction to get opposing school name ~~~~~~~~~~~~~~~~~~  
def get_opponent(soup_obj):
    
    home,away = get_home_away(soup_obj)
    
    if home == "Eastern Kentucky":
        return away
    else:
        return home   
#end get_opponent function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
        
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
#end get_pbp_strings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 4b.) newline filter function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
#end newline filter function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 5.) Function to get strings with b tag and put into list
#Innings id's and summaries are in bold~~~~~~~~~~~~~~~~
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
#close get bold strings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 6.) Function to get list of innings summaries ~~~~~~~~~~~~~~~~~   
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
#close get_inning_summaries ~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    
    
    #enter the file name
    soup = open_soup("htm files/3-09-19.htm")
    
    oppTm = get_opponent(soup)
    print()
    print("Opposing Team: "+oppTm)
    
    homeTm, awayTm = get_home_away(soup)
    print("Home Team: "+homeTm)
    print("Away Team: "+awayTm)
    print()
    '''
    pbp_strings = get_pbp_strings(soup)
    summary_strings = get_inning_summaries(soup)
    
    #saving list of the eku player's names as they appear in the pbp strings
    Johnson = "JOHNSON, W."
    Kerr = "KERR, R."
    Howie = "HOWIE, N."
    Botsoe = "BOTSOE, C."
    Lewis = "LEWIS, A.J."
    Ludwick = "LUDWICK, C."
    Harris = "HARRIS IV, D"
    Thomason = "THOMASON, L."
    Conklin = "CONKLIN, C."
    Weaver = "WEAVER, L."
    Lucio = "LUCIO, C."
    
    eku_position_players = [Johnson, Kerr, Howie, Botsoe, Lewis, Ludwick, Harris, Thomason, Conklin, Weaver, Lucio]
    
    
    #Separate EKU strings from opponent strings
    eku_strings = []
    PA_strings = []
    
    for s in pbp_strings[::2]:
        eku_strings.append(s)
        
    for s in eku_strings:
        print(s)
        print()
        
        
    # ). is the end of a plate appearance
    # if there is a semicolon in the string, . can also be the end of a PA
    
    punct = [".", ";", ",", "(", ")"]
    
    
    for i in range(len(eku_strings)):
        
        e = eku_strings[i]
        
        for j in range(len(e)):
            if e[j] in punct:
                print(e[j], end = " ")
        print()
    print()
        
    #Finding Players
    for p in eku_position_players:
        for s in eku_strings:
            if s.find(p) != -1:
                PA_strings.append(s[s.find(p): s.find(")", s.find(p)) + 1])
                        
    print()

    print("PA Strings:")    
    for s in PA_strings:
        print(s)
        print()            
    # ,. is a name
    # () contains pitch count #-# and pitches BFKS separated by ' '   
    # ).
    # ; indicates a baserunner
    # .. indicates end of PA with baserunners OR a name with inititals
    '''
    
    lineup_strings = []
    
    lu = soup.find_all("td", align = "left")
    for s in lu:
        lineup_strings.append(str(s.string))
            
            
        
        
    for i,s in enumerate(lineup_strings):
        print(i,s,"*")
        print()
        
    print(lineup_strings[18][:-1])
    print(lineup_strings[18][:-1] == "Player")
    
    
    
    print()
    print(lineup_strings[9][3:-1])
    print(ascii(lineup_strings[9][0]))
    
    print(lineup_strings[9][0] == '\xa0')
    
    starter_names1 = []
    sub_names1 = []
    
    for s in lineup_strings:
        if s[0] != '\xa0':
            starter_names1.append(s)
        else:
            sub_names1.append(s)

        
    print("Starter names:")
    for s in starter_names1:
        
        
        print(s)
        print()
        
    print("Sub names:")
    for s in sub_names1:
        print(s)
        print()
        
    print(starter_names1[1].strip('\xa0'))
    
    
        
            
    
    
    
    
         

    
                                 
                                
        
    
    

       
    
    
    
    
        
    
        
        
            
    
        
    
    
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    
main()