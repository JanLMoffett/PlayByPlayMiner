# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:12:23 2019

@author: Jan
"""

#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//  
#                             Action Unit Classes    
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//
import StdzNames    
import BaseOut

#//\\//\\//\\//\\//\\//\\//\\Batting Unit Class//\\//\\//\\//\\//\\//\\//\\//\\
class BatUnit:
    bat_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "hit by pitch", "reached", "struck out", "singled", "doubled", "tripled", "homered"]
    hit_verbs = ["singled", "doubled", "tripled", "homered"]
    hit_locations = ["to pitcher", "to catcher", "to first base", "to second base", "to third base", "to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field","up the middle", "through the left side", "through the right side", "down the lf line", "down the rf line"]
    
    true_oc_verbs = ["walked", "homered", "struck out"]
    
    fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]
    fo_locations = ["to p", "to cf", "to 1b", "to 2b", "to 3b", "to ss", "to lf", "to c", "to rf"]
    bip_verbs = hit_verbs + fo_verbs + ["reached"]  
    bip_locations = hit_locations + fo_locations
    on_base_verbs = ["singled", "doubled", "tripled", "homered", "walked", "intentionally walked", "reached", "hit by pitch"]
    new_br_verbs = ["singled", "doubled", "tripled", "walked", "intentionally walked", "reached", "hit by pitch"]
    
    
    #--------------------------------------------------------------------------
    def __init__(self, bat_unit_str, team, batting_order, bsot_dict):
        self.unit_string = bat_unit_str
        self.team = team
        self.bo = batting_order
        
        self.bsotdict = bsot_dict
        
        self.batter_name = ""
        self.count_balls = bat_unit_str[bat_unit_str.find("(")+1]
        self.count_strikes = bat_unit_str[bat_unit_str.find("(")+3]
        if "(0-0)" in bat_unit_str:
            self.pitch_string = ""
        else:
            self.pitch_string = bat_unit_str[bat_unit_str.rfind(" ",0,bat_unit_str.find(")"))+1:bat_unit_str.find(")")]
        self.hole = 0 
        
        self.is_h = False
        self.is_bb = False
        self.is_so = False
        self.is_hr = False
        self.is_fo = False
        self.is_inplay = False
        self.is_true_oc = False
        self.is_rch = False
        self.is_dp = False
        self.rbi = 0
        self.bases = 0 #this is for hits only.  basesadded includes walks, etc as well as hits
        
        self.basesadded = 0
        self.runsadded = 0
        self.outsadded = 0
        
        
    #--------------------------------------------------------------------------    
    def get_name(self):
        ts = self.unit_string
        
        for n in self.bo:
            if n.lower() in ts.lower():
                self.batter_name = n
                break            
    #--------------------------------------------------------------------------  
    def print_stuff(self):
        print("Unit String: " + self.unit_string)
        print("Batter Name: " + self.batter_name)  
        print("Count Balls: " + self.count_balls)
        print("Count Strikes: " + self.count_strikes)
        print("Pitch String: " + self.pitch_string)
        print("Batter Team: " + self.team)
        print("Place in Order: " + str(self.hole))
        
    #--------------------------------------------------------------------------  
    
    #--------------------------------------------------------------------------  
    def get_hole(self):
        if self.team == "away":
            for i,p in enumerate(self.bo):
                if self.batter_name == p:
                    self.hole = i+1
                    
        elif self.team == "home":
            for i,p in enumerate(self.home_bo):
                if self.batter_name == p:
                    self.hole = i+1
                    
            
    #--------------------------------------------------------------------------
    def is_bip(self):
        ts = self.unit_string
        
        for s in self.bip_verbs:
            if s in ts:
                self.is_inplay = True
                return 1
        return 0
    #--------------------------------------------------------------------------
    def get_pitches(self):
        ts = self.pitch_string
        tu = self.unit_string
        num_pitches = 0
        
        num_balls = ts.count("B")
        num_fouls = ts.count("F")
        num_called_k = ts.count("K")
        num_swing_k = ts.count("S")
        num_in_play = 0
        if self.is_inplay:
            num_in_play = 1
          
        num_pitches = sum([num_balls,num_fouls,num_called_k,num_swing_k,num_in_play])
        
        if "hit by pitch" in tu:
            num_pitches += 1
            
        return {"Balls":num_balls, "Fouls":num_fouls, "CalledKs":num_called_k, "SwingKs":num_swing_k, "BIPs":num_in_play, "Pitches":num_pitches}
    #--------------------------------------------------------------------------    
    def is_hit(self):
        ts = self.unit_string
        
        for s in self.hit_verbs:
            if s in ts:
                self.is_h = True
                return 1
                
        return 0   
    #--------------------------------------------------------------------------
    #run is_hit first
    def get_hit(self): #this function now works even if pa is not a hit
        
        singles = 0
        doubles = 0
        triples = 0
        homers = 0
        
        ts = self.unit_string
        
        if self.is_h:
        
            if "singled" in ts:
                self.bases = 1
                singles = 1
                self.basesadded = 1
            elif "doubled" in ts:
                self.bases = 2
                doubles = 1
                self.basesadded = 2
            elif "tripled" in ts:
                self.bases = 3
                triples = 1
                self.basesadded = 3
            elif "homered" in ts:
                self.bases = 4
                homers = 1
                self.is_hr = True
                self.basesadded = 4
                self.runsadded = 1
                
                
        bases = self.bases
            
        return {"Bases":bases, "Single":singles, "Double":doubles, "Triple":triples, "Homer":homers}
    
    #--------------------------------------------------------------------------
    def get_hit_info(self):
        loc = ""
        qual = ""
        bb_type = ""
        infh = 0
        ts = self.unit_string
        #hit_locations = 
        #["to pitcher", "to catcher", "to first base", "to second base", "to third base", 
        #"to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field",
        #"up the middle", "through the left side", "through the right side", 
        #"down the lf line", "down the rf line"]
        
        if self.is_h:
            if "to" in ts:
                if "bunt" in ts:
                    if "base" in ts:
                        loc = ts[ts.find(" ",ts.find("to"))+1:ts.find("base")+4]
                    else:
                        if "shortstop" in ts:
                            loc = "shortstop"
                        else:
                            loc = "shallow infield"
                        
                    qual = "soft"
                    bb_type = "ground ball"
                    infh = 1
                
                if "base" in ts:
                    loc = ts[ts.find(" ",ts.find("to"))+1:ts.find("base")+4]
                    qual = "medium"
                    bb_type = "ground ball"
                    infh = 1
                
                elif "field" in ts:
                    loc = ts[ts.find(" ",ts.find("to"))+1:ts.find("field")+5]
                    qual = "hard"
                    bb_type = "fly ball"
                    
                elif "center" in ts:
                    loc = ts[ts.find(" ", ts.find("to"))+1:ts.find("center")+6]
                    qual = "hard"
                    bb_type = "line drive"
                else: # should be pitcher, catcher, or shortstop
                    if "shortstop" in ts:
                        loc = "shortstop"
                    else:
                        loc = "shallow infield"
                    qual = "soft"
                    bb_type = "ground ball"
                    infh = 1
                    
            elif "up" in ts:
                loc = "up the middle"
                qual = "hard"
                bb_type = "ground ball"
                    
            elif "through" in ts:
                loc = ts[ts.find(" ",ts.find("the"))+1:ts.find("side")]
                qual = "hard"
                bb_type = "ground ball"
                
            elif "down" in ts:
                loc = ts[ts.find(" ",ts.find("the"))+1:ts.find("line")+4]
                qual = "hard"
                bb_type = "ground ball"
                
            #MAXWELL,Bret singled, bunt (0-0).
            elif "bunt" in ts:
                loc = "shallow infield"
                qual = "soft"
                bb_type = "ground ball"
                infh = 1
            
            else:
                loc = "ERROR!"  
                qual = "ERROR!"
                bb_type = "ERROR!"
        else:
            loc = "NA"
            qual = "NA"
            bb_type = "NA"
            
        return {"Location":loc, "Quality":qual, "BattedBallType":bb_type, "IFH":infh}
    #--------------------------------------------------------------------------
    def is_field_out(self):
        
        #fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]
        ts = self.unit_string
        
        if "hit into double play" in ts:
            self.is_fo = True
            self.is_dp = True
            self.outsadded = 1 #second out will be added with accompanying br unit
            return 1
        
        for s in self.fo_verbs:
            if s in ts:
                if "out" in ts or "up" in ts:
                    self.is_fo = True 
                    self.outsadded = 1
                elif "into" in ts:
                    self.is_fo = True
                    self.is_dp = True
                    self.outsadded = 1 #second out will be added with accompanying br unit
                return 1
        return 0   
    #--------------------------------------------------------------------------
    def get_field_out(self):
        ts = self.unit_string
        fol = "NA" #field out location
        fot = "NA" #field out type
        foq = "NA" #quality of batted ball
        
        if self.is_fo:
            for s in self.fo_verbs:
                if s in ts:
                    if s == "grounded":
                        foq = "soft"
                        fot = "ground ball"
                    elif s == "flied":
                        foq = "medium"
                        fot = "fly ball"
                    elif s == "lined":
                        foq = "hard"
                        fot = "line drive"
                    elif s == "popped":
                        foq = "soft"
                        fot = "fly ball"
                    elif s == "fouled":
                        foq = "foul"
                        fot = "fly ball"
                    break
             
            if self.is_dp: #finding location different for double plays
                fol = ts[ts.find("play")+5:ts.find("to",ts.find("play"))-1]
            
            else: #not a double play
                for s in self.fo_locations:
                    if s in ts:
                        fol = s
                        break
                    
        return {"FOLocation":fol, "FOType":fot, "FOQuality":foq}    
    
    #--------------------------------------------------------------------------
    def is_double_play(self):
        if self.is_dp:
            return 1
        return 0
    #--------------------------------------------------------------------------
    def get_double_play(self):
        ts = self.unit_string
        dpt = ""
        to_cnt = 0 
        ti1 = -1
        ti2 = -1
        p1 = ""
        p2 = ""
        p3 = ""
        
        if "double play" in ts:
        
            to_cnt = ts.count("to",ts.find("into")+4)
            
            if "unassisted" in ts:
                p1 = ts[ts.rfind("play")+5:ts.find("unassisted")-1]
            
            if to_cnt > 0:
                ti1 = ts.find("to",ts.find("into")+4)
                
                p1 = ts[ts.find("play")+5:ts.find("to",ts.find("play"))-1]
                
                if to_cnt > 1:
                    ti2 = ts.find("to",ti1+3)
                    p2 = ts[ti1+3:ti2-1]
            
            if p1 != "":
                if p1 == "2b":
                    dpt += "4"
                elif p1 == "3b":
                    dpt += "5"
                elif p1 == "ss":
                    dpt += "6"
                elif p1 == "p":
                    dpt += "1"
                elif p1 == "1b":
                    dpt += "3"
                elif p1 == "c":
                    dpt += "2"
                elif p1 == "lf":
                    dpt += "7"
                elif p1 == "cf":
                    dpt += "8"
                elif p1 == "rf":
                    dpt += "9"
            else:
                print("!!!ERROR in get_double_play.  No p1")
            
            if p2 != "":
                if p2 == "p":
                    dpt += "1"
                elif p2 == "c":
                    dpt += "2"
                elif p2 == "1b":
                    dpt += "3"
                elif p2 == "2b":
                    dpt += "4"
                elif p2 == "3b":
                    dpt += "5"
                elif p2 == "ss":
                    dpt += "6"
                elif p2 == "lf":
                    dpt += "7"
                elif p2 == "cf":
                    dpt += "8"
                elif p2 == "rf":
                    dpt += "9"
            
            if p3 != "":
                if p3 == "p":
                    dpt += "1"
                elif p3 == "c":
                    dpt += "2"
                elif p3 == "1b":
                    dpt += "3"
                elif p3 == "2b":
                    dpt += "4"
                elif p3 == "3b":
                    dpt += "5"
                elif p3 == "ss":
                    dpt += "6"
                elif p3 == "lf":
                    dpt += "7"
                elif p3 == "cf":
                    dpt += "8"
                elif p3 == "rf":
                    dpt += "9"
        
        else:
            dpt = "NA"
        return dpt
    
    #--------------------------------------------------------------------------
    def is_reach(self):
        ts = self.unit_string
        
        if "reached" in ts:
            self.is_rch = True
            
    #--------------------------------------------------------------------------
    #what are the types of reaches?  RBOE, FC...
    def get_reach(self):
        rboe = 0
        fc = 0
        
        ts = self.unit_string
        
        if self.is_rch:
            self.basesadded = 1
            
            if "error" in ts:
                rboe = 1
                
            if "dropped" in ts:
                rboe = 1
                
            if "choice" in ts:
                fc = 1
                
            if "wild" in ts:
                rboe = 1
                
            if "interference" in ts:
                rboe = 1
                
        return {"RBOE":rboe, "FC":fc}
    
    #--------------------------------------------------------------------------
    def is_sac(self):
        ts = self.unit_string
        
        if "SAC" in ts:
            self.outsadded = 1
            return 1
        else:
            return 0
    
    #--------------------------------------------------------------------------    
    def is_sf(self):
        ts = self.unit_string
        
        if "SF" in ts[0:ts.find("(")]:
            self.outsadded = 1
            return 1
        else:
            return 0
        
    #--------------------------------------------------------------------------
    def is_bunt(self):
        ts = self.unit_string
        
        if "bunt" in ts:
            return 1
        else:
            return 0
        
    #--------------------------------------------------------------------------
    def is_walk(self):
        ts = self.unit_string
        
        if "walked" in ts:
            self.bases = 1
            self.is_bb = True
            self.basesadded = 1
            return 1
        else:
            return 0
        
    #--------------------------------------------------------------------------
    #run is_walk first
    def get_walk_type(self): #now works if pa isn't a walk
        ibb = 0
        ubb = 0
        ts = self.unit_string
        
        if self.is_bb:
            if "intentionally" in ts:
                ibb = 1
            else:
                ubb = 1
            
        return {"UBB":ubb, "IBB":ibb}
            
            
    #--------------------------------------------------------------------------
    def is_strikeout(self):
        ts = self.unit_string
        
        if "struck out" in ts:
            self.is_so = True
            return 1
        else:
            return 0
        
    #--------------------------------------------------------------------------
    #run is_strikeout first
    def get_so_type(self): # works if pa not a so
        s_k = 0
        uc = 0
        sor = 0
        c_k = 0
        
        ts = self.unit_string
        
        if self.is_so:
        
            if "swinging" in ts:
                s_k = 1
                
                if "reached first" in ts:
                    self.basesadded = 1
                    sor = 1
                
                else:
                    if "out at first c to 1b" in ts:
                        uc = 1
                    self.outsadded = 1
            else:
                self.outsadded = 1
                c_k = 1
            
        return {"KSwing":s_k, "KLook":c_k, "UCTS":uc, "SOReach":sor}
            
            
    #--------------------------------------------------------------------------
    #run is_walk(), is_so(), is_hit(), and get_hit() first
    def is_true_outcome(self):
        toc = 0
        
        
        if self.is_bb or self.is_so or self.is_hr:
            toc = 1
            self.is_true_oc = True
          
        return toc
        
    #--------------------------------------------------------------------------
    def is_hbp(self):
        ts = self.unit_string
        
        if "hit by pitch" in ts:
            self.basesadded = 1
            return 1
        else:
            return 0 
        
    #--------------------------------------------------------------------------
    def update_bod(self):
        d = self.bsotdict
        
        
        if self.basesadded == 1:
            d["OnFirst"] = self.batter_name
            d["OnSecond"] = "NA" #clear bases ahead of current runner
            d["OnThird"] = "NA" #they will be updated in br class
            
        elif self.basesadded == 2: 
            d["OnSecond"] = self.batter_name
            d["OnThird"] = "NA"
            
        elif self.basesadded == 3:
            d["OnThird"] = self.batter_name
            
        elif self.basesadded == 4:
            d["OnFirst"] = "NA"
            d["OnSecond"] = "NA"
            d["OnThird"] = "NA"
            
        d["Outs"] += self.outsadded
        
        #initalize a BaseOut object using info from unit
        b = BaseOut.BaseOut(d["Outs"], d["OnFirst"], d["OnSecond"], d["OnThird"])
        
        b.get_base_state()
        b.get_base_out_state()
        
        d["BaseState"] = b.base_state
        d["BaseOutState"] = b.base_out_state
        
        return d
    
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    
    
#//\\//\\//\\//\\//\\//\\Baserunning Unit Class//\\//\\//\\//\\//\\//\\//\\//\\ 
class BRUnit:
    def __init__(self, br_unit_str, team, batting_order, bsot_dict):
        
        self.bsotdict = bsot_dict
        
        
        self.unit_string = br_unit_str
        self.bo = batting_order
        self.team = team
        
        self.action = "NA"
        self.runner_name = "NA"
        self.hole = 0
        
        self.advanced = False
        self.stole = False
        self.scored = False
        self.out = False
        
        self.fielder1 = "NA"
        self.fielder2 = "NA"
        
        self.start_base = 0
        self.end_base = 0
        self.basesadded = 0
        
        self.outsadded = 0
        self.runsadded = 0
        
        self.sba = 0 #stolen base attempts
        self.sb = 0 #stolen bases
        self.poa = 0 #pickoff attempts
        self.fpo = 0 #failed pickoff attempts
        self.po = 0 #successful pickoff
        self.cs = 0 #caught stealing
        self.wp = 0 #wild pitch
        self.pb = 0 #passed ball
        self.aoe = 0 #advanced on error
        
        self.bases = 0
        self.out_at_base = 0
    #--------------------------------------------------------------------------    
    def get_action(self):
        ts = self.unit_string
        
        if "out at" in ts:     #outs trump other actions, in case "advanced...out" in same string
            self.out = True
            self.action = "out"
        elif "out on" in ts:
            self.out = True
            self.action = "out"
        elif "advanced" in ts:
            self.advanced = True
            self.action = "advanced"
        elif "stole" in ts:
            self.stole = True
            self.action = "stole"
        elif "scored" in ts:
            self.scored = True
            self.action = "scored"
        
        else:
            print("!!!Error: BRUnit.get_action")
            print()
   
    #--------------------------------------------------------------------------        
    def get_runner_name(self):
        ts = self.unit_string
        
        for i,n in enumerate(self.bo):
            if n.lower() in ts.lower():
                self.runner_name = n
                self.hole = i+1
                break          
    
    #--------------------------------------------------------------------------
    #change this to get_start_base, and get it from the start_state parameter
    def set_start_base(self, strtbase):
        self.start_base = strtbase
    
    

    
    #--------------------------------------------------------------------------
    def is_pickoff(self):
        #run set_start_base first
        ts = self.unit_string
        
        if "caught stealing" in ts:
            self.sba = 1
            self.cs = 1
            self.outsadded = 1
            self.end_base = 0
            
        elif "failed pickoff" in ts:
            self.poa = 1
            self.fpo = 1 #end_base will be updated in get_advanced
            
        if "picked off" in ts:
            self.poa = 1
            self.po = 1
            self.outsadded = 1
            self.end_base = 0
            
        
    #--------------------------------------------------------------------------
    def get_advanced(self):
        ts = self.unit_string
        
        if self.advanced:
            if "advanced to" in ts:
                if "to second" in ts:
                    self.end_base = 2
                elif "to third" in ts:
                    self.end_base = 3
                else:
                    print("!!!Error: BRUnit.get_advanced")
                    print()
            if "on" in ts[ts.find("advanced"):]:
                if "wild pitch" in ts:
                    self.wp = 1
                elif "passed ball" in ts:
                    self.pb = 1
                elif "error" in ts:
                    self.aoe = 1
                elif "interference" in ts:
                    self.aoe = 1
                
        
    #--------------------------------------------------------------------------
    def get_stole(self):
        ts = self.unit_string
        
        #i don't know what it looks like if someone steals home, does it say "stole home" or "scored"?
        
        if self.stole:
            if "second" in ts:
                self.sba = 1
                self.sb = 1
                self.end_base = 2
            elif "third" in ts:
                self.sba = 1
                self.sb = 1
                self.end_base = 3
            elif "home" in ts:
                self.sba = 1
                self.sb = 1
                self.end_base = 4
    #--------------------------------------------------------------------------            
    def get_scored(self):
        ts = self.unit_string
        
        if self.scored:
            self.end_base = 4
            self.runsadded += 1
            
            if "on" in ts[ts.find("advanced"):]:
                if "wild pitch" in ts:
                    self.wp = 1
                elif "passed ball" in ts:
                    self.pb = 1
                elif "error" in ts:
                    self.aoe = 1
                elif "interference" in ts:
                    self.aoe = 1
    #--------------------------------------------------------------------------        
    def get_out(self):
        ts = self.unit_string
        bi = -1
        
        if self.out:
            
            if "out at" in ts:    
        
                if "first" in ts:
                    self.out_at_base = 1
                    bi = ts.rfind("first")
                elif "second" in ts:
                    self.out_at_base = 2
                    bi = ts.rfind("second")
                elif "third" in ts:
                    self.out_at_base = 3
                    bi = ts.rfind("third")
                elif "home" in ts:
                    self.out_at_base = 4
                    bi = ts.rfind("home")
                    
                self.fielder1 = ts[ts.find(" ",bi)+1:ts.find("to",bi)-1]
                self.fielder2 = ts[ts.find("to",bi)+3:ts.find("to",bi)+5]
            
            
            
            self.outsadded += 1
            self.end_base = 0
            
    #--------------------------------------------------------------------------
    def get_bases_added(self):  #run near end
        self.basesadded = self.end_base - self.start_base    
        
    #--------------------------------------------------------------------------
    def update_bod(self):
        d = self.bsotdict
        
        if self.end_base == 2:
            d["OnSecond"] = self.runner_name
            
            #check first base and update if needed
            if d["OnFirst"] == self.runner_name:
                d["OnFirst"] = "NA"
            
        elif self.end_base == 3:
            d["OnThird"] = self.runner_name
            
            #check first and second base and update if needed
            if d["OnFirst"] == self.runner_name:
                d["OnFirst"] = "NA"
            if d["OnSecond"] == self.runner_name:
                d["OnSecond"] = "NA"
                
        #if runner scored make sure he's not listed on base
        elif self.end_base == 4:
            if d["OnFirst"] == self.runner_name:
                d["OnFirst"] = "NA"
            if d["OnSecond"] == self.runner_name:
                d["OnSecond"] = "NA"
            if d["OnThird"] == self.runner_name:
                d["OnThird"] = "NA"
            
        #if runner was out, remove from bases
        else:
            if d["OnFirst"] == self.runner_name:
                d["OnFirst"] = "NA"
                
            if d["OnSecond"] == self.runner_name:
                d["OnSecond"] = "NA"
                
            if d["OnThird"] == self.runner_name:
                d["OnThird"] = "NA"
                
        #reset outs if they're already at 3
        if d["Outs"] > 2:
            d["Outs"] = 0
        
        
        d["Outs"] += self.outsadded
        
        #initalize a BaseOut object using info from unit
        b = BaseOut.BaseOut(d["Outs"], d["OnFirst"], d["OnSecond"], d["OnThird"])
        
        b.get_base_state()
        b.get_base_out_state()
        
        d["BaseState"] = b.base_state
        d["BaseOutState"] = b.base_out_state
        
        return d
    
    #--------------------------------------------------------------------------
    def print_stuff(self):
        print("Unit String: " + self.unit_string)
        print("Runner Name: " + self.runner_name)
        print("Hole: " + str(self.hole))
        print("Action: "+ self.action)
        print("Start Base: "+ str(self.start_base))
        print("End Base: " + str(self.end_base))
        print("Bases Added: " + str(self.basesadded))
        
        print("Stolen Bases: " + str(self.sb) + "/" + str(self.sba))
        print("Outs Added: " + str(self.outsadded))
        print("Fielder 1: " + self.fielder1)
        print("Fielder 2: "+ self.fielder2)
        
        print("Runs Added: " + str(self.runsadded))
        print("Pick Offs: " + str(self.po) + "/" + str(self.poa))
        
        print("Wild Pitch: "+str(self.wp))
        print("Passed Ball: "+str(self.pb))
        print("Adv on Error: "+str(self.aoe))
        print()
        
    #--------------------------------------------------------------------------

    






#//\\//\\//\\//\\//\\//\\Substitution Unit Class//\\//\\//\\//\\//\\//\\//\\//\\ 
#list of positions

       
class SubUnit:
    off_pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]
    #--------------------------------------------------------------------------
    def __init__(self, sub_unit_str, team, batting_order, off_subs, opp_relievers):
        self.unitstring = sub_unit_str
        self.side = team # 'home' or 'away'
        self.ogbattingorder = batting_order
        self.battingorder = []
        self.offsubs = off_subs
        self.opprels = opp_relievers
        
        self.subtype = "NA" #will be off or def
        
        self.playerin = "NA"
        self.playerout = "NA" #there may not always be a playerout
        
        self.subpos = "NA"
        self.subhole = 0
    #--------------------------------------------------------------------------    
    def get_players(self):
        ts = self.unitstring
        
        #if 'for' in string, playerout is name after it
        if 'for' in ts:
            self.playerout = StdzNames.last_only(ts[ts.find('for')+4:])
                
        if 'to' in ts:
            self.playerin = StdzNames.last_only(ts[:ts.find("to")])
        elif 'pinch' in ts:
            self.playerin = StdzNames.last_only(ts[:ts.find("pinch")])
                
        else:
            self.playerin = "ERROR: SubUnit.get_players, ts: "+ts
            
    #--------------------------------------------------------------------------
    def get_type(self): #defensive or offensive substitution (or both)
        ts = self.unitstring
        #if substitution doesn't contain 'for', strictly defensive
        if "for" not in ts:
            self.subtype = "def"
        else:
            if "to p for" in ts:
                self.subtype = "def"
            elif "pinch ran" in ts:
                self.subtype = "off"
            elif "pinch hit" in ts:
                self.subtype = "off"
            else:
                self.subtype = "off"
         
    #--------------------------------------------------------------------------
    def get_hole(self):
        if self.subtype == "off":
            for i,b in enumerate(self.ogbattingorder):
                if self.playerout == b:
                    self.subhole = i+1
                    break
    #--------------------------------------------------------------------------    
    def get_pos(self):
        ts = self.unitstring
        
        if "pinch hit" in ts:
            self.subpos = "ph"
        elif "pinch ran" in ts:
            self.subpos = "pr"   
        else:
            for p in self.off_pos:
                if p in ts[ts.find("to")+3:]:
                    self.subpos = p
                    break
                
        #else remains "NA" 
    #--------------------------------------------------------------------------    
    #Need function to return modified batting order when pos player is subbed
    def mod_batting_order(self):
        #run other methods first
        if self.subtype == "off": #if substitution isn't defensive only
            
            bo = self.ogbattingorder
            
            for i,p in enumerate(bo):
                if i == self.subhole-1:
                    self.battingorder.append(self.playerin)
                    continue
                self.battingorder.append(p)
            
        else:
            self.battingorder = self.ogbattingorder    
    #--------------------------------------------------------------------------    
    #do stuff methods will run all no-arg, no return setters in proper order
    def do_stuff(self):
        self.get_players()
        self.get_type()
        self.get_hole()
        self.get_pos()
        self.mod_batting_order()
        
    #--------------------------------------------------------------------------    
    def get_updated_bo(self):
        return self.battingorder    
    
    
    #--------------------------------------------------------------------------
    def print_stuff(self):
        print("Original Batting Order:")
        print(self.ogbattingorder)
        print()
        print("Updated Batting Order:")
        print(self.battingorder)
        print()
        
        print("Offensive Subs:")
        print(self.offsubs)
        print("Opposing Relievers:")
        print(self.opprels)
        print()
        print("Unit String: " + self.unitstring)
        print("Sub Type: " + self.subtype)
        print()
        print("Player Out: "+self.playerout)
        print("Player In: "+self.playerin)
        print("Subbed Pos: "+self.subpos)
        print()
        
    #--------------------------------------------------------------------------    
            
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//  
#                        CLose Action Unit Classes    
#//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//  
#--------------------------------------------------------------------------
def sub_test():
    
    #dummy data:
    AwayBO = ['Johnson', 'Kerr', 'Howie', 'Botsoe', 'Lewis', 'Ludwick', 'Harris', 'Thomason', 'Conklin']
    HomeBO = ['Kerrigan', 'Emme', 'Morris', 'Govern', 'Pena', 'Knernschield', 'Waznis', 'Sweeney', 'Tesmond']
    AwayRels = ['Williams', 'Ochsenbein']
    HomeRels = ['Stevenson']
    AwayOffs = ['Weaver']
    HomeOffs = ['Toppel']
    
    us1 = "WEAVER, L. pinch ran for LUDWICK, C.."
    us2 = "STEVENSON to p for DEXTER."
    us3 = "WEAVER, L. to dh."
    
    su1 = SubUnit(us1,"away",AwayBO,AwayOffs,HomeRels)
    su1.do_stuff()
    su1.print_stuff()
    
    su2 = SubUnit(us2,"away",AwayBO,AwayOffs,HomeRels)
    su2.do_stuff()
    su2.print_stuff()
    
    su3 = SubUnit(us3,"away",AwayBO,AwayOffs,HomeRels)
    su3.do_stuff()
    su3.print_stuff()
#--------------------------------------------------------------------------    
    
    
    
    
    
   
