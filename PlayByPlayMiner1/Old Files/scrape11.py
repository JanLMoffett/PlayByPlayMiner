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

pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]

# function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
# end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# function to filter newline chars out of a list of strings ~~~~~~~~~~~~~~~~~~~
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

# function to take a list of names in unknown format and output list of standardized last names    
def stdz_names(name_list): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #check for comma to determine order (last, First vs. First Last)
    lns = []
    for s in name_list:
        if s.find(",")>0: #there is a comma
            lns.append(s[0:s.find(",")].title())    
        else: #there's no comma
            lns.append(s[s.find(" ")+1:].title())
    return lns    
# close stdz_names ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                                  Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

# a game is a single htm doc converted to a soup object with open_soup function
class Game:
    def __init__(self, soup_obj):
        self.game_soup = soup_obj
        self.game_title = soup_obj.title.string
        self.away_team = self.game_title[0:self.game_title.find(" vs ")]
        self.home_team = self.game_title[self.game_title.find(" vs ") + 4:self.game_title.find("(") - 1]
        
    # 4.) function to get a list of pbp strings and remove \n chars
    # example of pbp string w/out newlines removed:
    # LOVELL, B. to c. BODINE, C. to dh.\nELDRIDGE, Cr struck out swinging (3-2 BFFBBS). DIXSON, Sean flied out to cf to\nright center (3-2 BFBKB). DANIELS, Bla grounded out to ss (1-2 KBF). <i><b>0\nruns, 0 hits, 0 errors, 0 LOB.
    def get_pbp_strings(self):
        font_strings = []
        pbp_strings = []
        front_off = []
        back_off = []
        
        font = self.game_soup.find_all("font", face = "verdana", size = 2, color="#000000")
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
    
    # 5.) Function to get strings with b tag and put into list
    #Innings id's and summaries are in bold ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_bold_strings(self):
        # example: 'UT Martin 8th - \n0 runs, 0 hits, 0 errors, 1 LOB.'
        bold = []
        bs = []
        
        b = self.game_soup.find_all("b")
        
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
    def get_inning_summaries(self):
        raw_summaries = []
        rs = []
        
        it = self.game_soup.find_all("i")
        
        for tag in it:
            raw_summaries.append(tag.string)   
        for s in raw_summaries:
            rs.append(str(s.encode("utf8")))
            
        rs = newline_filter(rs)
        
        return rs
    # close get_inning_summaries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #7.) function to get names and positions in lineups, and differentiate between teams, then between starts and subs
    def get_lineups(self):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #will return list of away starters and home starters
        lineup_strings = []
        
        lu = self.game_soup.find_all("td", align = "left")
        
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
        
        return {"away_starters":away_st, "away_subs":away_su, "home_starters":home_st, "home_subs":home_su}
    # close get_lineups~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                               Close Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                                 Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $

class Lineup:
    def __init__(self, away_starter_list, away_sub_list, home_starter_list, home_sub_list):
        self.away_starters = away_starter_list
        self.away_subs = away_sub_list
        self.home_starters = home_starter_list
        self.home_subs = home_sub_list
    
    # 8.) function to put starters in list in order of position
    def get_pos_order(self):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #takes a list of strings in format: KERR, Ryland 2b
        #returns list of ten names
        
        away_pos_order = [""]*10 # 0 will be DH
        home_pos_order = [""]*10 # 0 will be DH
        
        #read last two chars in string
        for i,s in enumerate(self.away_starters):
            for j,t in enumerate(pos):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                    away_pos_order[j] = s[:s.rfind(" ")]
                    
        #read last two chars in string
        for i,s in enumerate(self.home_starters):
            for j,t in enumerate(pos):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                    home_pos_order[j] = s[:s.rfind(" ")]
                    
        return away_pos_order, home_pos_order
    # close pos_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
    # 9.) function to tell whether or not a starter was subbed in the game
    # takes lineup lists of subs of variable length, returns boolean list, len = 10 in pos order
    def was_subbed(self):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        away_subbed = [False]*10
        home_subbed = [False]*10
        
        for i,p in enumerate(pos):
            for j,s in enumerate(self.away_subs):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == p:
                    away_subbed[i] = True
                    break
                
        for i,p in enumerate(pos):
            for j,s in enumerate(self.home_subs):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == p:
                    home_subbed[i] = True
                    break
               
        return away_subbed, home_subbed
    # close was subbed function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
            
    # 10.) function to get list of subs based on position
    def get_subs(self, pos_num):
        asl = self.away_subs
        hsl = self.home_subs
        
        a_pos_subs = []
        h_pos_subs = []
        
        #check for starter with a / in the string
        for s in self.away_starters:
            if s.find('/') != -1:
                asl.append(s)    
            
        for s in asl:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[pos_num]:
                a_pos_subs.append(s[:s.rfind(" ")])
                
        #check for starter with a / in the string
        for s in self.home_starters:
            if s.find('/') != -1:
                hsl.append(s)    
            
        for s in hsl:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[pos_num]:
                h_pos_subs.append(s[:s.rfind(" ")])
                
        return a_pos_subs, h_pos_subs
    #close get_subs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
            
    # 11.) function to get list of relief pitchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_relievers(self):
        
        away_relievers, home_relievers = self.get_subs(1)   
    
        return away_relievers, home_relievers      
    # close get_relievers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 
    
    # 12.) function to get list of pinch hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_pinch_hitters(self):
        away_pinch_hitters = []
        home_pinch_hitters = []
        
        for s in self.away_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
                away_pinch_hitters.append(s[:s.rfind(" ")])
                
        for s in self.home_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
                home_pinch_hitters.append(s[:s.rfind(" ")])
                
        return away_pinch_hitters, home_pinch_hitters
    # close get_pinch_hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    # 13.) function to get list of pinch runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_pinch_runners(self):
        
        away_pinch_runners = []
        home_pinch_runners = []
        
        for s in self.away_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
                away_pinch_runners.append(s[:s.rfind(" ")])
                
        for s in self.home_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
                home_pinch_runners.append(s[:s.rfind(" ")])
                
        return away_pinch_runners, home_pinch_runners
    # close get_pinch_runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # 14.) function to get a list of starters in batting order
    def get_batting_orders(self): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        away_bo = []
        home_bo = []
        
        for s in self.away_starters:
            if s[s.rfind(" ")+1:] != "p":
                away_bo.append(s[:s.rfind(" ")])
                
        for s in self.home_starters:
            if s[s.rfind(" ")+1:] != "p":
                home_bo.append(s[:s.rfind(" ")])
                
        return away_bo, home_bo
    #close get_batting_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                            Close Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
#                            Play by Play Class 
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 

class PlayByPlay:
    def __init__(self, pbp_string):
        self.original_pbp_string = pbp_string
        self.new_pbp_string = ""
        self.substitutions = ""
        

    # 15.) function to separate substitutions from play-by-play
    def sep_substitutions(self): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Stalman, L. pinch hit for Martellini,G.
        #WILLIAMS, D. to p for LASTER, N..
        subn_strings = []
        new_pbp = ""
        
        a = 0
        b = 0
        
        num_substitutions = self.pbp_string.count("for")
        
        #return empty list and unchanged string if there are no substitutions in hi
        if num_substitutions == 0:
            return (self.pbp_string, subn_strings)
        
        t = self.original_pbp_string
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
        
        self.new_pbp = new_pbp
        self.substitutions = subn_strings
        
    # close sep substitutions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
               
    # 16.) function to break pbp_strings into plate appearances ~~~~~~~~~~~~~~~
    def get_PAs(self):
        
        pas = []
        ts = self.new_pbp
        
        i = 1
        while 0<i<len(self.new_pbp):
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
    #close get_PAs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           Close Play by Play Class 
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

#******************************************************************************
#                               PlateApp Class
#******************************************************************************
    
class PlateApp:
    #constants
    
    PA_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "reached", "struck out", "singled", "doubled", "tripled", "homered", "hit by pitch"]
    
    hit_verbs = ["singled", "doubled", "tripled", "homered"]
    hit_locations = ["to pitcher", "to catcher", "to first base", "to second base", "to third base", "to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field","up the middle", "through the left side", "through the right side", "down the lf line", "down the rf line"]
    
    bip_verbs = ["grounded", "flied", "lined", "popped", "fouled", "singled", "doubled", "tripled", "homered"]
    
    fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]
    out_locations = ["to p", "to c", "to 1b", "to 2b", "to 3b", "to ss", "to lf", "to cf", "to rf", "ss to 2b"]
    
    on_base_verbs = ["singled", "doubled", "tripled", "homered", "walked", "intentionally walked", "reached", "hit by pitch"]
    BR_verbs = ["stole", "advanced", "scored", "out"]
    
    #constructor
    def __init__(self, PA_string):
        self.original_string = PA_string
        self.parenth = PA_string[PA_string.find("(")+1:PA_string.find(")")]
        self.pitch_string = self.parenth[self.parenth.find(" ")+1:]
        self.count_balls = self.parenth[self.parenth.find("-")-1]
        self.count_strikes = self.parenth[self.parenth.find("-")+1]
        self.balls = self.pitch_string.count("B")
        self.fouls = self.pitch_string.count("F")
        self.called_strikes = self.pitch_string.count("K")
        self.swing_strikes = self.pitch_string.count("S")
        
    def get_num_pitches(self):
        np = len(self.pitch_string)
        for s in self.bip_verbs:
            if s in self.original_string:
                np += 1
                break
    
    # 18.) function to id the batter (last, first) of a plate appearance ~~~~~~~~~~
    def get_batter(self):
        #isolating the first 12 chars of PA string.  i think the max for a name is 12 chars
        ts = self.original_string[:12]
        
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
    
    # Game object
    g1 = Game(soup)
    print("Away Team: "+g1.away_team)
    print("Home Team: "+g1.home_team)
    print()
    
    '''
    inn_sums = g1.get_inning_summaries()
    print("Inning summaries:")
    for s in inn_sums:
        print(s)
    print() 
    '''
    
    lus = g1.get_lineups() #this is a dict with four elements
    
    away_starters = lus["away_starters"]
    away_subs = lus["away_subs"]
    home_starters = lus["home_starters"]
    home_subs = lus["home_subs"]
    
    
    
    '''
    boldstrings = g1.get_bold_strings()
    print("Bold strings:")
    for s in boldstrings:
        print(s)
    print()
    '''
    
    pbps = g1.get_pbp_strings()
    
    away_pbps = pbps[0::2]
    home_pbps = pbps[1::2]
    
    lu1 = Lineup(away_starters, away_subs, home_starters, home_subs)
    
    away_po, home_po = lu1.get_pos_order()
    away_subbed, home_subbed = lu1.was_subbed()
    
    away_batting_order, home_batting_order = lu1.get_batting_orders()
    
    stdz_away_bo = stdz_names(away_batting_order)
    stdz_home_bo = stdz_names(home_batting_order)
    
    print("Away Batting Order:")
    for i,s in enumerate(stdz_away_bo):
        print(str(i+1) + " " + s)
    print()
    
    print("Home Batting Order:")
    for i,s in enumerate(stdz_home_bo):
        print(str(i+1) + " " + s)
    print()
    
    print("Away Play by Play strings:")
    for i,s in enumerate(away_pbps):
        print("Away Inning " + str(i+1) + ": " + s)
    print()
    
    print("Home Play by Play strings:")
    for i,s in enumerate(home_pbps):
        print("Home Inning " + str(i+1) + ": " + s)
    print()
    
    '''
    print("Away starters:")
    for s in away_starters:
        print(s)
    print()
      
    print("Away subs:")
    for s in away_subs:
        print(s)
    print()
    
    print("Home starters:")
    for s in home_starters:
        print(s)
    print()
    
    print("Home subs:")
    for s in home_subs:
        print(s)
    print()
    
    print("Away Position Order:")
    for i,s in enumerate(away_po):
        print(s + " | Subbed: " + str(away_subbed[i]))
    print()
    
    print("Home Position Order:")
    for i,s in enumerate(home_po):
        print(s + " | Subbed: " + str(home_subbed[i]))
    print()
    
    file = open("writetest.txt","w")
    
    file.write(str(PA_stat_dict))
    
    file.close()
    '''
    
    
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # end MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
main()