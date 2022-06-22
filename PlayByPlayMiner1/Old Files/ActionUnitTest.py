# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:57:57 2019

@author: Jan
"""

pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]

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
def main():
    #action_unit_string, place_in_seq, away_batting_order, home_batting_order, away_subs, home_subs
    aux1 = "LASTER, N. to p for LEWIS, J.."
    aux2 = "TIPLER, M. advanced to second."
    aux3 = "JOSLIN, M. walked (3-2 BFBKBB);"
    
    #list of action units
    aux = [aux1, aux2, aux3]
    
    seq_num = 4
    away_bo = ['Avros', 'Kueber', 'Martinez', 'Spain', 'Phillips', 'Tipler', 'Joslin', 'Mcdonald', 'Head']
    away_subs = ['Hubbard', 'Campbell', 'Kouba']
    
    home_bo = ['Johnson', 'Kerr', 'Howie', 'Botsoe', 'Lewis', 'Ludwick', 'Harris Iv', 'Conklin', 'Thomason']
    home_subs = ['Weaver', 'Lucio', 'Laster', 'Borek', 'Williams']
    
    a1 = ActionUnit(aux1, seq_num, away_bo, home_bo, away_subs, home_subs)
    a1.get_name()
    a1.get_type()
    
    print("Action Unit String:")
    print(a1.au_string)
    print()
    
    print("Name:", end = " ")
    print(a1.au_player)
    
    print()
    print(a1.au_team)
    
main()
