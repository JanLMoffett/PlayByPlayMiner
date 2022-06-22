# -*- coding: utf-8 -*-
"""
Created on Thu May 30 17:00:58 2019

@author: Jan
"""
# standardized list of last names    
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
# standardized last name    
def stdz_name(name_string): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #check for comma to determine order (last, First vs. First Last)
    if name_string.find(",")>0: #there is a comma
        return name_string[0:name_string.find(",")].title()    
    else: #there's no comma
        return name_string[name_string.find(" ")+1:].title()
# close stdz_name ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------


#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
#                            Play by Play Class 
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
class PlayByPlay:
    #--------------------------------------------------------------------------
    def __init__(self, pbp_string, away_batting_order, away_subs, home_batting_order, home_subs):
        self.original_pbp_string = pbp_string
        self.away_bo = away_batting_order
        self.away_sl = away_subs
        self.home_bo = home_batting_order
        self.home_sl = home_subs
        
        self.num_subs = pbp_string.count("for")
        self.num_bats = pbp_string.count(")")
        self.num_brs = pbp_string.count(";")
        self.num_au = self.num_subs + self.num_bats + self.num_brs
        
        self.au = []
        self.au_types = []
    #--------------------------------------------------------------------------
    def print_stuff(self):
        print("original pbp string:") 
        print(self.original_pbp_string)
        print()
        print("num sub_units: " + str(self.num_subs))
        print("num bat_units: " + str(self.num_bats))
        print("num br_units:  " + str(self.num_brs))
        print("total:        " + str(self.num_au))
        print()
        
    #--------------------------------------------------------------------------
    def get_types(self):
        #types
        t = []
        aus = self.au
        
        for u in aus:
            if "for" in u:
                t.append("sub")
            elif ")" in u:
                t.append("bat")
            else:
                t.append("br")
                
        self.au_types = t
        
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
            dp = ts.find("..",i)
            
            lm = [ppi, psci, sci, pi, dp]
            
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
                
            elif k == dp: #if there is a double period
                    aus += ts[i:k+2]
                    #print(aus.strip())
                    au.append(aus.strip())
                    aus = ""
                    i = k+2   
                
            elif k == pi:
                ci = ts.rfind(",",0,k)
                if 0 <= pi-ci <= 5: #if period is near a comma, indicating part of a name
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
        self.au = au    
            
    #close get_action_units ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #--------------------------------------------------------------------------
    
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           Close Play by Play Class 
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//  
#                             Action Unit Classes    
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//    

#//\\//\\//\\//\\//\\//\\//\\Batting Unit Class//\\//\\//\\//\\//\\//\\//\\//\\
class BatUnit:
    bat_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "hit by pitch", "reached", "struck out", "singled", "doubled", "tripled", "homered"]
    hit_verbs = ["singled", "doubled", "tripled", "homered"]
    hit_locations = ["to pitcher", "to catcher", "to first base", "to second base", "to third base", "to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field","up the middle", "through the left side", "through the right side", "down the lf line", "down the rf line"]
    
    true_oc_verbs = ["walked", "homered", "struck out"]
    
    fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]
    fo_locations = ["to p", "to c", "to 1b", "to 2b", "to 3b", "to ss", "to lf", "to cf", "to rf", "ss to 2b"]
    bip_verbs = hit_verbs + fo_verbs + ["reached"]  
    bip_locations = hit_locations + fo_locations
    on_base_verbs = ["singled", "doubled", "tripled", "homered", "walked", "intentionally walked", "reached", "hit by pitch"]
    
    
    def __init__(self, bat_unit_str, away_bo, home_bo):
        self.unit_string = bat_unit_str
        self.away_bo = away_bo
        self.home_bo = home_bo
        self.batter_name = stdz_name(bat_unit_str[:12])
        self.count_balls = bat_unit_str[bat_unit_str.find("(")+1]
        self.count_strikes = bat_unit_str[bat_unit_str.find("(")+3]
        self.pitch_string = bat_unit_str[bat_unit_str.rfind(" ",0,bat_unit_str.find(")"))+1:bat_unit_str.find(")")]
        
    #--------------------------------------------------------------------------  
    def print_stuff(self):
        print("Unit String: " + self.unit_string)
        print("Batter Name: " + self.batter_name)  
        print("Count Balls: " + self.count_balls)
        print("Count Strikes: " + self.count_strikes)
        print("Pitch String: " + self.pitch_string)
    #--------------------------------------------------------------------------     
    def is_bip(self):
        ts = self.unit_string
        
        for s in self.bip_verbs:
            if s in ts:
                return True
        return False
    #--------------------------------------------------------------------------
    def get_pitches(self):
        ts = self.pitch_string
        num_balls = ts.count("B")
        num_fouls = ts.count("F")
        num_called_k = ts.count("K")
        num_swing_k = ts.count("S")
        num_in_play = 0
        if self.is_bip():
            num_in_play = 1
        num_pitches = sum([num_balls,num_fouls,num_called_k,num_swing_k,num_in_play])
        return {"Balls":num_balls, "Fouls":num_fouls, "CalledKs":num_called_k, "SwingKs":num_swing_k, "BIPs":num_in_play, "Pitches":num_pitches}
    #--------------------------------------------------------------------------    
    def is_hit(self):
        ts = self.unit_string
        
        for s in self.hit_verbs:
            if s in ts:
                return True
        return False   
    #--------------------------------------------------------------------------
    def is_true_oc(self):
        ts = self.unit_string
        
        for s in self.true_oc_verbs:
            for s in ts:
                return True
        return False
    #--------------------------------------------------------------------------
    
    
    #--------------------------------------------------------------------------
#//\\//\\//\\//\\//\\//\\Baserunning Unit Class//\\//\\//\\//\\//\\//\\//\\//\\ 
class BRUnit:
    def __init__(self, br_unit_str, away_bo, home_bo):
        self.unit_string = br_unit_str
        self.away_bo = away_bo
        self.home_bo = home_bo
        self.runner_name = stdz_name(br_unit_str[:12])
    #--------------------------------------------------------------------------  
    def print_stuff(self):
        print("Unit String: " + self.unit_string)
        print("Runner Name: " + self.runner_name)
    
    #--------------------------------------------------------------------------
#//\\//\\//\\//\\//\\//\\Substitution Unit Class//\\//\\//\\//\\//\\//\\//\\//\\        
class SubUnit:
    def __init__(self, sub_unit_str, away_bo, away_subs, home_bo, home_subs):
        self.unit_string = sub_unit_str
        self.away_bo = away_bo
        self.away_subs = away_subs
        self.home_bo = home_bo
        self.home_subs = home_subs
        self.for_i =  sub_unit_str.find("for")
        self.to_i = sub_unit_str.rfind("to", 0, self.for_i)
        self.player_in = stdz_name(self.unit_string[0:self.to_i-1])
        self.player_out = stdz_name(self.unit_string[self.for_i+4:])
        self.sub_pos = self.unit_string[self.to_i+3:self.for_i-1]
        self.team = ""
    #--------------------------------------------------------------------------    
    def print_stuff(self):
        print("Unit String: "+self.unit_string)
        print("Player in: "+self.player_in)
        print("Player out: "+self.player_out)
        print("Position: "+self.sub_pos)
        print("Team: "+self.team)
        
    #--------------------------------------------------------------------------    
    def get_team(self):
        if self.player_in in self.away_subs:
            self.team = "away"
        else:
            self.team = "home"
        
    #--------------------------------------------------------------------------    

    #Need function that modifies batting order when pos player is subbed
    
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//  
#                        CLose Action Unit Classes    
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//  

def test():
    #xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
    #                           Example Data
    #xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
    away_order = ['Avros', 'Kueber', 'Martinez', 'Spain', 'Phillips', 'Tipler', 'Joslin', 'Mcdonald', 'Head']
    away_subs = ['Hubbard', 'Campbell', 'Kouba']
    
    home_order = ['Johnson', 'Kerr', 'Howie', 'Botsoe', 'Lewis', 'Ludwick', 'Harris Iv', 'Conklin', 'Thomason']
    home_subs = ['Weaver', 'Lucio', 'Laster', 'Borek', 'Williams']
    
    pbps2 = "BOREK, N. to p for LASTER, N.. KUEBER, G. walked (3-2 KBBBFB). MARTINEZ, D. singled up the middle (2-1 BBF); KUEBER, G. advanced to third. WILLIAMS, D. to p for BOREK, N.. SPAIN, G. reached on a fielder s choice (0-2 SK); MARTINEZ, D. advanced to second; KUEBER, G. out at home 3b to c. PHILLIPS, P. struck out swinging (3-2 KBBSFBFS). TIPLER, M. reached on a fielder s choice (2-2 BFSFB); SPAIN, G. out at second 2b to ss."
    #pbps2 = "BOREK, N. to p for LASTER, N.. AVROS, X. stole second. KUEBER, G. walked (3-2 KBBBFB). KUEBER, G. stole second. MARTINEZ, D. singled up the middle (2-1 BBF); KUEBER, G. advanced to third. WILLIAMS, D. to p for BOREK, N.. SPAIN, G. reached on a fielder s choice (0-2 SK); MARTINEZ, D. advanced to second; KUEBER, G. out at home 3b to c. PHILLIPS, P. struck out swinging (3-2 KBBSFBFS). TIPLER, M. reached on a fielder s choice (2-2 BFSFB); SPAIN, G. out at second 2b to ss."
    
    #xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
    
    
    #initializing PlayByPlay object
    p1 = PlayByPlay(pbps2, away_order, away_subs, home_order, home_subs)
    #pbps = play by play string
    #away_order, home_order = list length 10 of standardized last names
    #away_subs, home_subs = list of standardized last names
    
    # PlayByPlay methods:
    p1.print_stuff()  #prints variables made by constructor
    p1.get_action_units()
    p1.get_types()
    
    a1 = p1.au
    t1 = p1.au_types
    
    
    for i,s in enumerate(a1):
        print(str(i+1)+": "+s)
        print("Type: "+t1[i])
        
        if t1[i] == "bat":
            #make a bat_unit
            b1 = BatUnit(s, away_order, home_order)
            b1.print_stuff()
            print("Pitches: "+str(b1.get_pitches()))
            if b1.is_bip():
                print("Ball in Play")
                if b1.is_hit():
                    print("Hit")
                else:
                    print("Out")
            else:
                print("No Ball in Play")
            print()
            
            
        elif t1[i] == "br":
            br1 = BRUnit(s, away_order, home_order)    
            br1.print_stuff()
            print()
            
        else:
            s1 = SubUnit(s, away_order, away_subs, home_order, home_subs)
            s1.get_team()
            s1.print_stuff()
            print()
            
test()