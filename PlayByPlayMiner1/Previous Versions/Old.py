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

#//////////////////////////// STATIC FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# function to open htm doc ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def open_soup(htm_string):
    #opening the htm file from eku baseball website
    with open(htm_string) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
# end open_soup function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
# function to take a list of names in unknown format and output list of 
# standardized last names    
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
#------------------------------------------------------------------------------
# function to take a list and print elements as row of csv ~~~~~~~~~~~~~~~~~~~~   
def csv_print(some_list):
    r = ""
    for i,a in enumerate(some_list):
        if i == len(some_list)-1:
            s = str(a)
            r += (s)
            break
            
        s = str(a)
        r += (s + ",")
        
        
    print(r)
# close csv_print function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------
# function to make a csv header from user input ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def make_csv_header(num_vars):
    r = ""
    
    for i in range(num_vars):
        #get input
        u = input("Enter Variable Name:\n")
        r += (u + ",")
    
    print(r)
    return r    
# close make_csv_header ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------   
# function to take a list and return string with elements as row of csv ~~~~~~~
def csv_string(some_list):
    r = ""

    for i,a in enumerate(some_list):
        if i == len(some_list)-1:
            s = str(a)
            r += (s)
            break
        s = str(a)
        r += (s + ",")
        
    return r
# close csv_string function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      
# //////////////////////// CLOSE STATIC FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\  



# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                                  Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
# a game is a single htm doc converted to a soup object with open_soup function
class Game:
    #--------------------------------------------------------------------------
    def __init__(self, soup_obj):
        self.game_soup = soup_obj
        self.game_title = soup_obj.title.string
        self.away_team = self.game_title[0:self.game_title.find(" vs ")]
        self.home_team = self.game_title[self.game_title.find(" vs ") + 4:self.game_title.find("(") - 1]
    #--------------------------------------------------------------------------    
    def get_pbp_strings(self):
        font_strings = []
        pbp_strings = []
        front_off = []
        back_off = []
        
        font = self.game_soup.find_all("font", face = "verdana", size = 2, color="#000000")
        for string in font:
            font_strings.append(string)
          
        for s in font_strings:
            s2 = s.encode("utf8")
            if len(s2) > 100:
                pbp_strings.append(str(s2))
                
        for s in pbp_strings:
            #j for each character in s
            for j in range(len(s)-14):
                #' - </b></font>'
                if s[j:j+14] == ' - </b></font>':
                    front_off.append(s[(j+14) : ]) 
                    
        for s in front_off:
            #j for each character in s
            for j in range(len(s)-4):
                if s[j:(j+6)] == "<i><b>":
                    back_off.append(s[0 : (j-1)])
        
        
        #newline filter
        return_list = newline_filter(back_off)
        return return_list
    # end get_pbp_strings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #--------------------------------------------------------------------------
    # function to get names and positions in lineups, and differentiate between teams, 
    # then between starts and subs
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
    # close get_lineups~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                               Close Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %



# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                                 Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
class Lineup:
    #--------------------------------------------------------------------------
    def __init__(self, away_starter_list, away_sub_list, home_starter_list, home_sub_list):
        self.away_starters = away_starter_list
        self.away_subs = away_sub_list
        self.home_starters = home_starter_list
        self.home_subs = home_sub_list
    #--------------------------------------------------------------------------
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
    #--------------------------------------------------------------------------        
    # function to tell whether or not a starter was subbed in the game
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
    # close was subbed function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    #--------------------------------------------------------------------------        
    # function to get list of subs based on position
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
    #close get_subs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    #--------------------------------------------------------------------------        
    # 11.) function to get list of relief pitchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_relievers(self):
        
        away_relievers, home_relievers = self.get_subs(1)   
    
        return away_relievers, home_relievers      
    # close get_relievers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 
    #--------------------------------------------------------------------------
    # function to get list of pinch hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    #--------------------------------------------------------------------------    
    # function to get list of pinch runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    #--------------------------------------------------------------------------
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
    #--------------------------------------------------------------------------
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                            Close Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $



#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
#                            Play by Play Class 
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
class PlayByPlay:
    #--------------------------------------------------------------------------
    def __init__(self, pbp_string):
        self.original_pbp_string = pbp_string
    #--------------------------------------------------------------------------    
    def get_action_units(self):
        #this method is a replacement for sep_substitions
        #builds an array of each discrete unit that contains a name and an action
        #sorts them into batting, baserunning, and substitutions later
        ts = self.original_pbp_string
        
        au = []
        aus = ""
        
        i = 0
        while i < (len(ts)):
            #find landmarks
            ppi = ts.find(").",i) #indicates end of batting unit that has no br
            psci = ts.find(");", i) #indicates end of batting unit that has assoc br
            sci = ts.find(";",i) #indicates end of br unit
            pi = ts.find(".",i) #indicates end of substituition or br unit if abs(pi - ci) > 5
            
            lm = [ppi, psci, sci, pi]
            
            #changing negative indices to 99999 so they don't interfere with finding min
            for j in range(len(lm)):
                if lm[j] == -1:
                    lm[j] = 99999
            
            #k is the min index
            k = min(lm)
            
            if k == ppi:
                aus += ts[i:k+2]
                #print(aus.strip())
                au.append(aus.strip())
                aus = ""
                i = k+2
                
            elif k == psci:
                aus += ts[i:k+2]
                #print(aus.strip())
                au.append(aus.strip())
                aus = ""
                i = k+2
                
            elif k == sci:
                aus += ts[i:k+1]
                #print(aus.strip())
                au.append(aus.strip())
                aus = ""
                i = k+1
                
            elif k == pi:
                ci = ts.rfind(",",0,k)
                if 0 <= pi-ci <= 5:
                    aus += ts[i:k+1]
                    i = k+1
                else:
                    aus += ts[i:k+1]
                    #print(aus.strip())
                    au.append(aus.strip())
                    aus = ""
                    i = k+1
            else:
                break
            
        return au    
    #close get_action_units ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #--------------------------------------------------------------------------    
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           Close Play by Play Class 
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||



# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
#                               Action Unit Class  
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @    
class ActionUnit:
    csv_header = ["SeqOrder","Name","Team","Type"]
    #--------------------------------------------------------------------------
    def __init__(self, action_unit_string, place_in_seq, away_batting_order, home_batting_order, away_subs, home_subs):
        self.au_string = action_unit_string
        self.place_in_seq = place_in_seq
        self.away_bo = away_batting_order
        self.home_bo = home_batting_order
        self.au_type = ""
        self.au_player = ""
        self.au_team = ""
        self.return_stats = ["NA"]*4
    #--------------------------------------------------------------------------
    def get_type(self):
        ts = self.au_string
        if ts.find(")") != -1:
            self.au_type = "bat"
        elif ts.find("for") != -1:
            self.au_type = "sub"
        else:
            self.au_type = "br"
    #--------------------------------------------------------------------------
    def get_name(self):
        ts = self.au_string
        
        #check away bo
        for s in self.away_bo:
            if s == ts[0:len(s)].title():
                self.au_player = s
                self.au_team = "away"
         
        if len(self.au_player) < 1:
            #check home bo
            for s in self.home_bo:
                if s == ts[0:len(s)].title():
                    self.au_player = s
                    self.au_team = "home"
    #--------------------------------------------------------------------------
    
# @ @ @ @ @ @ @ @ @ @ @ @ @ Bat Unit Class @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
class BatUnit(ActionUnit):
    bat_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "hit by pitch", "reached", "struck out", "singled", "doubled", "tripled", "homered"]
    hit_verbs = ["singled", "doubled", "tripled", "homered"]
    hit_locations = ["to pitcher", "to catcher", "to first base", "to second base", "to third base", "to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field","up the middle", "through the left side", "through the right side", "down the lf line", "down the rf line"]
    fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]
    fo_locations = ["to p", "to c", "to 1b", "to 2b", "to 3b", "to ss", "to lf", "to cf", "to rf", "ss to 2b"]
    bip_verbs = hit_verbs + fo_verbs + ["reached"]  
    bip_locations = hit_locations + fo_locations
    on_base_verbs = ["singled", "doubled", "tripled", "homered", "walked", "intentionally walked", "reached", "hit by pitch"]
    
    def is_bip(self):
        ts = self.au_string
        
        for b in self.bip_verbs:
            if b in ts:
                return True
        return False
    #--------------------------------------------------------------------------
    def get_bip_location(self):
        ts = self.au_string
        
        for l in self.bip_locations:
            if l in ts:
                return l
        return "NA"
    #--------------------------------------------------------------------------
    def is_hit(self):
        ts = self.au_string
        
        for v in self.hit_verbs:
            if v in ts:
                return True
        return False
    #--------------------------------------------------------------------------
    def get_hit_location(self):
        ts = self.au_string
        
        for l in self.hit_locations:
            if l in ts:
                return l
        return "NA"
    #--------------------------------------------------------------------------
    def is_field_out(self):
        ts = self.au_string
        
        for v in self.fo_verbs:
            if v in ts:
                return True
        return False
    #--------------------------------------------------------------------------
    def get_out_location(self):
        ts = self.au_string
        
        for l in self.fo_locations:
            if l in ts:
                return l
        return "NA"
    #--------------------------------------------------------------------------
    def is_on_base(self):
        ts = self.au_string
        
        for v in self.on_base_verbs:
            if v in ts:
                return True
        return False
    #--------------------------------------------------------------------------
    def get_base(self):
        ts = self.au_string
        
        for v in self.on_base_verbs:
            if v in ts:
                if v == "doubled":
                    return "2"
                elif v == "tripled":
                    return "3"
                elif v == "homered":
                    return "4"
                else:
                    return "1"
        return "0"
    #--------------------------------------------------------------------------     
    
# @ @ @ @ @ @ @ @ @ @ @ @ Baserunning Unit Class @ @ @ @ @ @ @ @ @ @ @ @ @ @ @  

class BRUnit(ActionUnit):
    br_verbs = ["stole", "advanced", "scored", "out at"]     
    
# @ @ @ @ @ @ @ @ @ @ @ @ Substitution Unit Class @ @ @ @ @ @ @ @ @ @ @ @ @ @ @

class SubUnit(ActionUnit):
    #--------------------------------------------------------------------------
    def get_sub_info(self):    
        ts = self.au_string
        #get name of player coming in
        fi = ts.find("for")
        ti = ts.rfind("to",0,fi-1)
        pos = ts[ti+3:fi-1]
        p_in = ts[0:ti-1]
        p_out = ts[fi+4:]
        
        nms = stdz_names([p_out, p_in])
        
        return (nms[0], nms[1], pos)

    '''   
    #--------------------------------------------------------------------------
    #modify the batting order 
    def mod_bo(self):
        if self.team == "away":
            bo = self.away_bo
        else:
            bo = self.home_bo
            
            #need stdz list of subs names
    #--------------------------------------------------------------------------
    '''
    #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
#                          Close Action Unit Class  
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # MAIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():    
    #enter the file name
    soup = open_soup("htm files/4-05-19.htm")
    
    # Game object
    g1 = Game(soup)
    print("Away Team: "+g1.away_team)
    print("Home Team: "+g1.home_team)
    print()
    
    lus = g1.get_lineups() #this is a dict with four elements
    
    away_starters = lus["away_starters"]
    away_subs = lus["away_subs"]
    home_starters = lus["home_starters"]
    home_subs = lus["home_subs"]
    
    pbps = g1.get_pbp_strings()
    
    away_pbps = pbps[0::2]
    home_pbps = pbps[1::2]
    
    lu1 = Lineup(away_starters, away_subs, home_starters, home_subs)
    
    away_po, home_po = lu1.get_pos_order()
    away_subbed, home_subbed = lu1.was_subbed()
    
    away_batting_order, home_batting_order = lu1.get_batting_orders()
    
    stdz_away_bo = stdz_names(away_batting_order)
    stdz_home_bo = stdz_names(home_batting_order)
    stdz_away_subs = stdz_names(away_subs)
    stdz_home_subs = stdz_names(home_subs)
    
    
    print("Away Batting Order:")
    print(stdz_away_bo)
    
    
    print("Away Substitute Players:")
    print(stdz_away_subs)
        
    
    print("Home Batting Order:")
    print(stdz_home_bo)
        
    
    print("Home Substitute Players:")
    print(stdz_home_subs)
    
    '''
    
    print("Away Play by Play strings:")
    for i,s in enumerate(away_pbps):
        print("Away Inning " + str(i+1) + ": " + s)
    print()
    
    print("Home Play by Play strings:")
    for i,s in enumerate(home_pbps):
        print("Home Inning " + str(i+1) + ": " + s)
    print()
    '''
   
    for i in range(len(away_pbps)):
        #making a pbp object and making sure it works
        print("Away Play by Play String "+str(i)+":")
        print(away_pbps[i])
        print()
    
        pbp1 = PlayByPlay(away_pbps[i])
        aau = pbp1.get_action_units()
        
        print("Action Units:")
        for s in aau:
            print(s)
        print()
        
        '''
        print("Action Units:")
        for j,s in enumerate(aau):
            print(s)
            tau = ActionUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
            tau.assign_type()
            
            if tau.au_type == "bat":
                bau = BatUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
                #put in BatUnit methods
                
            elif tau.au_type == "br":
                brau = BRUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
                #put in BRUnit methods
            
            else: #substitution
                sau = SubUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
                sau.get_name()
                print("au_player: " + sau.au_player)
                print("au_team:   " + sau.au_team)
                sau.get_type()
                print("au_type:   " + sau.au_type)
                sub_info = sau.get_sub_info()
                print("player_out, player_in, position:")
                for s in sub_info:
                    print(s)
                print()
                #put in SubUnit methods
            
        print()
    
    for i in range(len(home_pbps)):
        print("Home Play by Play String "+str(i)+":")
        print(home_pbps[i])
        print()
        pbp2 = PlayByPlay(home_pbps[i])
        hau = pbp2.get_action_units()
        
        print("Action Units:")
        for j,s in enumerate(hau):
            tau = ActionUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
            tau.assign_type()
            
            if tau.au_type == "bat":
                bau = BatUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
                #put in BatUnit methods
                
            elif tau.au_type == "br":
                brau = BRUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
                #put in BRUnit methods
            
            else: #substitution
                sau = SubUnit(s,j,stdz_away_bo,stdz_home_bo,stdz_away_subs,stdz_home_subs)
                #put in SubUnit methods
            
            
        print()
    
    
    
    print("Action Unit Class:")
    
    #header1 = make_csv_header(4)
    header1 = ["Seq","Name","Team","Type","BIP","BIP Location","Hit","Hit Location","Field Out","Out Location","On Base","Bases"]
    csv_print(header1)
    for j in range(len(a0au)):
        tau = ActionUnit(a0au[j], j, stdz_away_bo, stdz_home_bo)
        
        tau.assign_type()
        
        if tau.au_type == "bat":
            bau = BatUnit(a0au[j], j, stdz_away_bo, stdz_home_bo)
            
        elif tau.au_type == "br":
            brau = BRUnit(a0au[j], j, stdz_away_bo, stdz_home_bo)
            
        else: #substition
            sau = SubUnit(a0au[j], j, stdz_away_bo, stdz_home_bo)
            
            
            
        
        
        
        
        csv_print(tl)
    
    
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