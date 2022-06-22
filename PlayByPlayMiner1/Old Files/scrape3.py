# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:36:25 2019

@author: Jan
"""
#import BeautifulSoup web scraping library
# https://www.crummy.com/software/BeautifulSoup/bs4/
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# Box Score/Play By Play url pattern
#https://static.ekusports.com/custompages/BB/Stats/2019/3-16-19.htm



#function to ask user for dates ~~~~~~~~~~~~~~~~~~~~~~~~~
def ask_dates(numDates):
    #need a list of dates in "#-##-##.htm" format
    gameDatesHtm = []
    
    for i in range(numDates):
        
        m = input("Enter Month: \n")
        d = input("Enter Day: \n")
        y = input("Enter Year: \n")
        
        dateHtm = m + "-" + d + "-" + y + ".htm"
        
        gameDatesHtm.append(dateHtm)
        
    return gameDatesHtm
#end ask_dates function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
#end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#function to return home and away teams ~~~~~~~~~~~~~~~~   
def get_home_away(soup_obj):
    gameTitle = soup_obj.title.string
    
    vs_ind = (gameTitle.find(" vs "), gameTitle.find(" vs ") + 4)
    p_ind = gameTitle.find("(") - 1
    
    away = gameTitle[0:vs_ind[0]]
    home = gameTitle[vs_ind[1]:p_ind]
    
    return home,away  
#end get_home_away function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    



#function to get opposing school name ~~~~~~~~~~~~~~~~~~  
def get_opponent(soup_obj):
    
    home,away = get_home_away(soup_obj)
    
    if home == "Eastern Kentucky":
        return away
    else:
        return home   
#end get_opponent function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
      
        
    
    
#function to return T/F for EKU home game ~~~~~~~~~~~~~~
def is_home(soup_obj):
    home,away = get_home_away(soup_obj)
    if home == "Eastern Kentucky":
        return True
    else:
        return False
#end is_home function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    datesHtm = ask_dates(2)
    
    soup = open_soup(datesHtm[0])
    
    oppTm = get_opponent(soup)
    print()
    print("Opposing Team: "+oppTm)
    
    if is_home(soup):
        print("Home Game")
    else:
        print("Away or Neutral Game")
    print()
    
    """
    #prints all tags
    print("Tag names:")
    for tag in soup.find_all(True):
        print(tag.name)
    print()
    
    
    tr = soup.find_all("tr")
    print("tr:")
    for tag in tr:
        if tag.tr:
            print(tag.tr)
    print()
    
    #this prints basically everything
    p = soup.find_all("p")
    print("p:")
    for tag in p:
        if tag.p:
            print(tag.p)
    print()
    
    
    #Innings id's and summaries are in bold
    # example: 'UT Martin 8th - \n0 runs, 0 hits, 0 errors, 1 LOB.'
    b = soup.find_all("b")
    print("b:")
    for tag in b:
            print(tag.string)
    print()
    
    
    #innings summaries are in italics
    # example: '1 run, 2 hits, 1 error, 1 LOB.'
    i = soup.find_all("i")
    print("i:")
    for tag in i:
        print(tag.string)
    print()
    
    """
    font_strings = []
    pbp_strings = []
    front_off = []
    back_off = []
    
    font = soup.find_all("font", face = "verdana", size = 2, color="#000000")
    for string in font:
        font_strings.append(string)
   
    
    #for i in range(len(pbp_strings)):
    #    print(pbp_strings[i])
    #    print()
       
    
    for i in range(len(font_strings)):
        s = font_strings[i].encode("utf8")
        if len(s) > 100:
            pbp_strings.append(s)
            
    #i for each pbp string
    for s in pbp_strings:
        #j for each character in pbp string[i]
        for j in range(len(s)-14):
            #' - </b></font>'
            if str(s)[j:j+14] == ' - </b></font>':
                front_off.append(str(s)[(j+14):]) 
                
    for s in front_off:
        for j in range(len(s)-4):
            if str(s)[j:(j+4)] == "LOB.":
                back_off.append(str(s)[0:j+4])
                
                
    for s in back_off:
        print(s)
        print()
        
    #remove newline chars
    
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    
main()




