""" Action Unit Module

@author: Jan L. Moffett | janlmoffett@gmail.com

This module requires import of StdzNames and BaseOut modules.

This module contains the following functions:
    * get_br_data_header - returns a csv string header for baserunning dataset
    * get_bat_data_header - returns a csv string header for batting dataset
    * get_sub_data_header - returns a csv string header for substitution dataset
    
This module contains the following classes:
    * BatUnit - A string of play-by-play batting information
    * BRunit - A string of play-by-play baserunning information
    * SubUnit - A string of play-by-play substitution information    
"""

import StdzNames    
import BaseOut

#------------------------------------------------------------------------------   
def get_br_data_header():
    """returns a csv string header for baserunning dataset"""
    
    dataheader = ""
    dataheader += "HomeAway,"
    dataheader += "RunnerName,"
    dataheader += "Hole,"
    dataheader += "Action,"
    dataheader += "StartBase,"
    dataheader += "EndBase,"
    dataheader += "BasesAdded,"
    dataheader += "SB,"
    dataheader += "SBA,"
    dataheader += "OutsAdded,"
    dataheader += "Fielder1,"
    dataheader += "Fielder2,"
    dataheader += "RunsAdded,"
    dataheader += "PO,"
    dataheader += "POA,"
    dataheader += "WP,"
    dataheader += "PB,"
    dataheader += "AOE,"
    dataheader += "bostartOuts,"
    dataheader += "bostartOnFirst,"
    dataheader += "bostartOnSecond,"
    dataheader += "bostartOnThird,"
    dataheader += "bostartBaseState,"
    dataheader += "bostartBaseOutState,"
    dataheader += "boendOuts,"
    dataheader += "boendOnFirst,"
    dataheader += "boendOnSecond,"
    dataheader += "boendOnThird,"
    dataheader += "boendBaseState,"
    dataheader += "boendBaseOutState"
    
    return dataheader
#------------------------------------------------------------------------------
def get_bat_data_header():
    """returns a csv string header for batting dataset"""
    
    headstring = ""
    headstring += "HomeAway,"
    headstring += "BatterName,"
    headstring += "BatterHole,"
    headstring += "CountBalls,"
    headstring += "CountStrikes,"
    headstring += "pitchBalls,"
    headstring += "pitchFouls,"
    headstring += "pitchKSwing,"
    headstring += "pitchKLook,"
    headstring += "pitchBIPs,"
    headstring += "Pitches,"
    headstring += "BIP,"
    headstring += "H,"
    headstring += "Bases,"
    headstring += "Singles,"
    headstring += "Doubles,"
    headstring += "Triples,"
    headstring += "HR,"
    headstring += "HitLocation,"
    headstring += "HitQuality,"
    headstring += "HitType,"
    headstring += "INFH,"
    headstring += "FO,"
    headstring += "FOLocation,"
    headstring += "FOQuality,"
    headstring += "FOType,"
    headstring += "DP,"
    headstring += "DPType,"
    headstring += "Reach,"
    headstring += "RBOE,"
    headstring += "FC,"
    headstring += "SAC,"
    headstring += "SF,"
    headstring += "BB,"
    headstring += "IBB,"
    headstring += "UBB,"
    headstring += "SO,"
    headstring += "KSwing,"
    headstring += "KLook,"
    headstring += "UCTS,"
    headstring += "SOReach,"
    headstring += "HBP,"
    headstring += "TrueOutcome,"
    headstring += "BasesAdded,"
    headstring += "RunsAdded,"
    headstring += "OutsAdded,"
    headstring += "bostartOuts,"
    headstring += "bostartOnFirst,"
    headstring += "bostartOnSecond,"
    headstring += "bostartOnThird,"
    headstring += "bostartBaseState,"
    headstring += "bostartBaseOutState,"
    headstring += "boendOuts,"
    headstring += "boendOnFirst,"
    headstring += "boendOnSecond,"
    headstring += "boendOnThird,"
    headstring += "boendBaseState,"
    headstring += "boendBaseOutState"
    
    return headstring
#------------------------------------------------------------------------------
def get_sub_data_header():
    """returns a csv string header for substitution dataset"""
        
    return "SubType,PlayerOut,PlayerIn,SubbedPos"

class BatUnit:
    """A string of play-by-play batting information
    
    Attributes:
        hit_verbs: a list of verbs associated with base hits
        fo_verbs: a list of verbs associated with field outs
        fo_locations: a list of field out locations
        bip_verbs: a list of verbs associated with balls in play
        unit_string: original string of play-by-play batting information
        team: 'home' or 'away'
        bo: list containing names in batting order for specified team
        bsotstart: dict containing baseout information for start of plate appearance 
        bsotend: dict containing baseout informatino for end of plate appearance
        batter_name: last name of batter
        hole: batter place in batting order (index of bo + 1), 0 if pitcher
        count_balls: last ball count of plate appearance
        count_strikes: last strike count of plate appearance
        pitch_string: string of letters denoting balls, strikes, fouls, etc. ('BFKS')
        balls: number of 'B' in pitch_string
        fouls: number of 'F' in pitch_string
        swingingstrikes: number of 'S' in pitch_string
        calledstrikes: number of 'K' in pitch_string
        BIPs: number of pitches that put ball in play (0 or 1)
        pitches: total number of pitches based on pitch_string and if ball in play
        BIP: 1 if ball in play, 0 otherwise
        H: 1 if hit, 0 otherwise
        bases: number of bases (0, 1 for single, 2 for double,...)
        singles: 1 if single, 0 otherwise
        doubles: 1 if double, 0 otherwise
        triples: 1 if triple, 0 otherwise
        homers: 1 if home run, 0 otherwise
        hitloc: description of hit location ("right center","down the lf line",...)
        hitqual: description of hit quality ("soft","medium","hard")
        hittype: description of hit type ("ground ball","fly ball",...)
        infh: 1 in infield hit, 0 otherwise
        fieldouts: 1 if field out, 0 otherwise
        foloc: description of field out location ("rf","1b",...)
        foqual: description of field out quality ("soft","medium","hard")
        fotype: description of field out type ("ground ball","fly ball",...)
        DP: 1 if double play, 0 otherwise
        doubleplaytype: double play type ("543","63",...)
        is_rch: True if 'reach', False otherwise
        RBOE: 1 if reach base on error, 0 otherwise
        FC: 1 if fielders choice, 0 otherwise
        SAC: 1 if sacrifice bunt, 0 otherwise
        SF: 1 if sacrifice fly, 0 otherwise
        BB: 1 if walk, 0 otherwise
        IBB: 1 if intentional walk, 0 otherwise
        UBB: 1 if unintentional walk, 0 otherwise
        SO: 1 if strike out, 0 otherwise
        kswing: 1 if swinging strike out, 0 otherwise
        klook: 1 if looking strike out, 0 otherwise
        UCTS: 1 if uncaught third strike, 0 otherwise
        SOreach: 1 if reach on uncaught third strike, 0 otherwise
        trueoutcome: 1 if walk, strike out, or home run, 0 otherwise
        HBP: 1 if hit by pitch, 0 otherwise
        basesadded: number of bases added by batter (1 for single,2 for double,...)
        runsadded: number of runs scored by batter (0 or 1)
        outsadded: number of outs made by batter (0 or 1)
    """
    
    hit_verbs = ["singled", "doubled", "tripled", "homered"] #used in is_hit
    fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]#used in is_field_out
    fo_locations = ["to p", "to cf", "to 1b", "to 2b", "to 3b", "to ss", "to lf", "to c", "to rf"] #used in get_field_out
    bip_verbs = hit_verbs + fo_verbs + ["reached"]  #used in is_bip
    
    #--------------------------------------------------------------------------
    def __init__(self, bat_unit_str, team, batting_order, start_bsot):
        """Initializes BatUnit object 
        
        Args:
            bat_unit_str: string of play-by-play batting information
            team: 'away' or 'home'
            batting_order: list of names in batting order for specified team
            start_bsot: dict containing baseout state for start of plate appearance
        """
        
        self.unit_string = bat_unit_str
        self.team = team
        self.bo = batting_order
        
        self.bsotstart = start_bsot
        #end baseout state init as a copy of the start
        self.bsotend = {"Outs":start_bsot["Outs"], "OnFirst":start_bsot["OnFirst"], "OnSecond":start_bsot["OnSecond"], "OnThird":start_bsot["OnThird"], "BaseState":start_bsot["BaseState"], "BaseOutState":start_bsot["BaseOutState"]} #will be same as start until updated
        
        self.batter_name = ""
        self.hole = 0 
        
        self.count_balls = "" 
        self.count_strikes = ""
        self.pitch_string = ""
        
        self.balls = 0
        self.fouls = 0
        self.swingingstrikes = 0
        self.calledstrikes = 0
        self.BIPs = 0
        self.pitches = 0
        
        self.BIP = 0
        self.H = 0
        self.bases = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.homers = 0
        
        self.hitloc = "NA"
        self.hitqual = "NA"
        self.hittype = "NA"
        self.infh = 0
        
        self.fieldouts = 0
        self.foloc = "NA"
        self.foqual = "NA"
        self.fotype = "NA"
        
        self.DP = 0
        self.doubleplaytype = ""
        
        self.is_rch = False
        self.RBOE = 0
        self.FC = 0
        
        self.SAC = 0
        self.SF = 0
        
        self.BB = 0
        self.IBB = 0
        self.UBB = 0
        
        self.SO = 0
        self.kswing = 0
        self.klook = 0
        self.UCTS = 0
        self.SOreach = 0
        
        self.trueoutcome = 0
        
        self.HBP = 0
        
        self.basesadded = 0
        self.runsadded = 0
        self.outsadded = 0
    #--------------------------------------------------------------------------    
    def get_batter_name(self):
        """Finds batter name in unit string and sets batter_name"""
        
        ts = self.unit_string
        
        for i,n in enumerate(self.bo):
            if n.lower() in ts.lower():
                self.batter_name = n
                self.hole = i+1
                break   
        #if batter name still blank, meaning wasn't in batting order
        if self.batter_name == "":
            self.batter_name = "ERROR: name not in batting order, ts: "+ts
            
            print("!!!ERROR: BatUnit.get_batter_name, not in batting order, ts: "+ts)
    #--------------------------------------------------------------------------
    def get_count(self):
        """Finds parenth in unit string and sets count_balls, count_strikes, and pitch_string"""
        
        ts = self.unit_string
        
        #if there are no parenth, do nothing
        if ts.find("(")>0:
            self.count_balls = ts[ts.find("(")+1]
            self.count_strikes = ts[ts.find("-",ts.find("(")+1)+1]
            
            #there isn't always a pitch string included in parenth, eg: '(2-2)'
            if len(ts[ts.find("("):ts.rfind(")")+1]) > 5:
                self.pitch_string = ts[ts.find(" ", ts.find("("))+1:ts.find(")", ts.find("("))]
    #--------------------------------------------------------------------------
    def get_pitches(self):
        """Processes pitch_string and sets balls, fouls, calledstrikes,..., pitches"""
        
        ts = self.pitch_string
        tu = self.unit_string
        
        #assigning negative values to distinguish missing cases
        self.balls = -1
        self.fouls = -1
        self.calledstrikes = -1
        self.swingingstrikes = -1
        self.BIPs = -1
        self.pitches = -1
        
        if len(ts[ts.find("("):ts.rfind(")")+1]) > 5:
            self.balls = ts.count("B")
            self.fouls = ts.count("F")
            self.calledstrikes = ts.count("K")
            self.swingingstrikes = ts.count("S")
            self.BIPs = 0
            if self.BIP == 1:
                self.BIPs = 1
              
            self.pitches = sum([self.balls, self.fouls, self.calledstrikes, self.swingingstrikes, self.BIPs])
        
            if "hit by pitch" in tu:
                self.pitches += 1
                
    #--------------------------------------------------------------------------    
    def is_bip(self):
        """Determines if there is a ball in play and sets BIP."""
        
        ts = self.unit_string
        
        for s in self.bip_verbs:
            if s in ts:
                self.BIP = 1
    #--------------------------------------------------------------------------  
    def is_hit(self):
        """Determines if there is a hit and sets H."""
        
        ts = self.unit_string
        
        for s in self.hit_verbs:
            if s in ts:
                self.H = 1
    #--------------------------------------------------------------------------
    #run is_hit first
    def get_hit(self): #this function now works even if pa is not a hit
        """Determines type of base hit and sets bases, basesadded, singles,...
        
        Run is_hit before running this function.
        
        """

        ts = self.unit_string
        
        if self.H == 1:
        
            if "singled" in ts:
                self.bases = 1
                self.singles = 1
                self.basesadded = 1
            elif "doubled" in ts:
                self.bases = 2
                self.doubles = 1
                self.basesadded = 2
            elif "tripled" in ts:
                self.bases = 3
                self.triples = 1
                self.basesadded = 3
            elif "homered" in ts:
                self.bases = 4
                self.homers = 1
                self.basesadded = 4
                self.runsadded = 1
    
    #--------------------------------------------------------------------------
    def get_hit_info(self):
        """Reads unit string and sets hitloc, hitqual, hittype, and infh."""
        
        ts = self.unit_string
        #hit_locations = 
        #["to pitcher", "to catcher", "to first base", "to second base", "to third base", 
        #"to shortstop", "to left field", "to left center", "to center field", "to right center", "to right field",
        #"up the middle", "through the left side", "through the right side", 
        #"down the lf line", "down the rf line"]
        
        if self.H == 1:
            if "to" in ts:
                if "bunt" in ts:
                    if "base" in ts:
                        self.hitloc = ts[ts.find(" ",ts.find("to"))+1:ts.find("base")+4]
                    else:
                        if "shortstop" in ts:
                            self.hitloc = "shortstop"
                        else:
                            self.hitloc = "shallow infield"
                        
                    self.hitqual = "soft"
                    self.hittype = "ground ball"
                    self.infh = 1
                
                if "base" in ts:
                    self.hitloc = ts[ts.find(" ",ts.find("to"))+1:ts.find("base")+4]
                    self.hitqual = "medium"
                    self.hittype = "ground ball"
                    self.infh = 1
                
                elif "field" in ts:
                    self.hitloc = ts[ts.find(" ",ts.find("to"))+1:ts.find("field")+5]
                    self.hitqual = "hard"
                    self.hittype = "fly ball"
                    
                elif "center" in ts:
                    self.hitloc = ts[ts.find(" ", ts.find("to"))+1:ts.find("center")+6]
                    self.hitqual = "hard"
                    self.hittype = "line drive"
                else: # should be pitcher, catcher, or shortstop
                    if "shortstop" in ts:
                        self.hitloc = "shortstop"
                    else:
                        self.hitloc = "shallow infield"
                    self.hitqual = "soft"
                    self.hittype = "ground ball"
                    self.infh = 1
                    
            elif "up" in ts:
                self.hitloc = "up the middle"
                self.hitqual = "hard"
                self.hittype = "ground ball"
                    
            elif "through" in ts:
                self.hitloc = ts[ts.find(" ",ts.find("the"))+1:ts.find("side")]
                self.hitqual = "hard"
                self.hittype = "ground ball"
                
            elif "down" in ts:
                self.hitloc = ts[ts.find(" ",ts.find("the"))+1:ts.find("line")+4]
                self.hitqual = "hard"
                self.hittype = "ground ball"
                
            #MAXWELL,Bret singled, bunt (0-0).
            elif "bunt" in ts:
                self.hitloc = "shallow infield"
                self.hitqual = "soft"
                self.hittype = "ground ball"
                self.infh = 1
            
            else:
                self.hitloc = "ERROR!"  
                self.hitqual = "ERROR!"
                self.hittype = "ERROR!"
        else:
            self.hitloc = "NA"
            self.hitqual = "NA"
            self.hittype = "NA"
    #--------------------------------------------------------------------------
    def is_field_out(self):
        """Determines if there is a field out and sets fieldouts, doubleplays, and outsadded."""
        
        #fo_verbs = ["grounded", "flied", "lined", "popped", "fouled"]
        ts = self.unit_string
        
        if "hit into double play" in ts:
            self.fieldouts = 1
            self.doubleplays = 1
            self.outsadded = 1 #second out will be added with accompanying br unit
            
        for s in self.fo_verbs:
            if s in ts:
                if "out" in ts or "up" in ts:
                    self.fieldouts = 1
                    self.outsadded = 1
                elif "into" in ts:
                    self.fieldouts = 1
                    self.doubleplays = 1
                    self.outsadded = 1 #second out will be added with accompanying br unit 
    #--------------------------------------------------------------------------
    def get_field_out(self):
        """Determines type of field out and sets foqual, fotype, and foloc."""
        
        ts = self.unit_string
        
        if self.fieldouts == 1:
            for s in self.fo_verbs:
                if s in ts:
                    if s == "grounded":
                        self.foqual = "soft"
                        self.fotype = "ground ball"
                    elif s == "flied":
                        self.foqual = "medium"
                        self.fotype = "fly ball"
                    elif s == "lined":
                        self.foqual = "hard"
                        self.fotype = "line drive"
                    elif s == "popped":
                        self.foqual = "soft"
                        self.fotype = "fly ball"
                    elif s == "fouled":
                        self.foqual = "foul"
                        self.fotype = "fly ball"
                    break
             
            if self.DP == 1: #finding location different for double plays
                self.foloc = ts[ts.find("play")+5:ts.find("to",ts.find("play"))-1]
            
            else: #not a double play
                for s in self.fo_locations:
                    if s in ts:
                        self.foloc = s
                        break
    
    #--------------------------------------------------------------------------
    def get_double_play(self):
        """Determines type of double play and sets doubleplaytype."""
        
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
        self.doubleplaytype = dpt
    #--------------------------------------------------------------------------
    def is_reach(self):
        """Determines if 'reached' appears in unit string."""
        
        ts = self.unit_string
        
        if "reached" in ts:
            self.is_rch = True
    #--------------------------------------------------------------------------
    def get_reach(self):
        """Determines what type of play allowed the batter to reach base."""
        
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
                
        self.RBOE = rboe
        self.FC = fc
    #--------------------------------------------------------------------------
    def is_sac(self):
        """Determines if there is a sacrifice bunt and sets SAC."""
        ts = self.unit_string
        
        if "SAC" in ts:
            self.SAC = 1
    #--------------------------------------------------------------------------    
    def is_sf(self):
        """Determines if there is a sacrifice fly and sets SF."""
        ts = self.unit_string
        
        if "SF" in ts[0:ts.find("(")]:
            self.SF = 1
    #--------------------------------------------------------------------------
    def is_bunt(self):
        """Determines if there is a bunt and sets bunt."""
        
        ts = self.unit_string
        
        if "bunt" in ts:
            return 1
        else:
            return 0
    #--------------------------------------------------------------------------
    def is_walk(self):
        """Determines if there is a walk and sets BB, bases, and basesadded."""
        
        ts = self.unit_string
        
        if "walked" in ts:
            self.bases = 1
            self.BB = 1
            self.basesadded = 1
    #--------------------------------------------------------------------------
    def get_walk_type(self): 
        """Determines if a walk is intentional or unintentional and sets IBB and UBB."""
        
        ts = self.unit_string
        
        if self.BB == 1:
            if "intentionally" in ts:
                self.IBB = 1
            else:
                self.UBB = 1
    #--------------------------------------------------------------------------
    def is_strikeout(self):
        """Determines if there is a strike out and sets SO."""
        
        ts = self.unit_string
        
        if "struck out" in ts:
            self.SO = 1
    #--------------------------------------------------------------------------
    def get_so_type(self): # works if pa not a so
        """Determines if strike out was swinging or looking and sets kswing and klook.
        
        Also sets UCTS and SOreach.  Run is_strikeout before running this function.
        
        """
        
        ts = self.unit_string
        
        if self.SO == 1:
            
            if "reached" in ts:
                self.basesadded = 1
                self.SOreach = 1
                
                if "swinging" in ts:
                    self.kswing = 1
                    
                elif "looking" in ts:
                    self.klook = 1
                    
                
            elif "out at first" in ts:
                self.UCTS = 1
                self.outsadded = 1
                
                if "swinging" in ts:
                    self.kswing = 1
                    
                elif "looking" in ts:
                    self.klook = 1
                    
            elif "swinging" in ts:
                self.kswing = 1
                self.outsadded = 1
                
            elif "looking" in ts:
                self.klook = 1
                self.outsadded = 1
            
    #--------------------------------------------------------------------------
    #run is_walk(), is_so(), is_hit(), and get_hit() first
    def is_true_outcome(self):
        """Determines if there is a true outcome (BB, SO, or HR) and sets trueoutcome.
        
        Run is_hit, get_hit, is_walk, and is_srikeout before running this function.
        """
        
        if self.BB == 1:
            self.trueoutcome = 1
        elif self.SO == 1:
            self.trueoutcome = 1
        elif self.homers == 1:
            self.trueoutcome = 1
    #--------------------------------------------------------------------------
    def is_hbp(self):
        """Determines if batter is hit by pitch and sets hbp."""
        
        ts = self.unit_string
        
        if "hit by pitch" in ts:
            self.basesadded = 1
            self.hbp = 1
    #--------------------------------------------------------------------------
    def update_bod(self):
        """Updates information in base-out dict."""
        
        if self.basesadded == 1:
            self.bsotend["OnFirst"] = self.batter_name
            
        elif self.basesadded == 2: 
            self.bsotend["OnSecond"] = self.batter_name
            
        elif self.basesadded == 3:
            self.bsotend["OnThird"] = self.batter_name
            
        elif self.basesadded == 4:
            self.bsotend["OnFirst"] = "NA"
            self.bsotend["OnSecond"] = "NA"
            self.bsotend["OnThird"] = "NA"
        
        #check bases to make sure runner not on more than one base
        if self.bsotend["OnFirst"] == self.bsotend["OnSecond"]:
            self.bsotend["OnFirst"] = "NA"
        if self.bsotend["OnFirst"] == self.bsotend["OnThird"]:
            self.bsotend["OnFirst"] = "NA"
        if self.bsotend["OnSecond"] == self.bsotend["OnThird"]:
            self.bsotend["OnSecond"] = "NA"
        
        self.bsotend["Outs"] += self.outsadded
        
        self.bsotend["BaseState"] = BaseOut.get_base_state(self.bsotend["OnFirst"], self.bsotend["OnSecond"], self.bsotend["OnThird"])
        self.bsotend["BaseOutState"] = BaseOut.get_base_out_state(self.bsotend["Outs"], self.bsotend["OnFirst"], self.bsotend["OnSecond"], self.bsotend["OnThird"])
    
    #--------------------------------------------------------------------------
    def do_stuff(self):
        """Runs all BatUnit functions in correct order."""
        
        self.get_batter_name()
        self.is_bip()
        self.get_count()
        self.get_pitches()
        
        self.is_hit()
        self.get_hit()
        self.get_hit_info()
        self.is_field_out()
        self.get_field_out()
        self.get_double_play()
        self.is_reach()
        self.get_reach()
        self.is_sac()
        self.is_sf()
        self.is_bunt()
        self.is_walk()
        self.get_walk_type()
        self.is_strikeout()
        self.get_so_type()
        self.is_true_outcome()
        self.is_hbp()
        self.update_bod()
    #------------------------------------------------------------------------------    
    def print_stuff(self):
        """Prints all BatUnit information for testing purposes."""
        
        print("Bat Unit String: " + self.unit_string)
        print("Team: "+self.team)
        #print("Batting Order:")
        #print(self.bo)
        print()
        print("Baseout Start:")
        print(self.bsotstart)
        print()
        print("Baseout End:")
        print(self.bsotend)
        '''
        print(("Batter Name: " + self.batter_name), end = "; ")
        print(("Batter Hole: " + str(self.hole)), end = "; ")
        print(("Count Balls: " + self.count_balls), end = "; ")
        print(("Count Strikes: " + self.count_strikes), end = "; ")
        print(("Pitch String: " + self.pitch_string), end = "; ")
        print(("Balls: " + str(self.balls)), end = "; ")
        print(("Fouls: " + str(self.fouls)), end = "; ")
        print(("Sw Strikes: " + str(self.swingingstrikes)), end = "; ")
        print(("Ca Strikes: " + str(self.calledstrikes)), end = "; ")
        print(("Balls In Play: " + str(self.BIPs)), end = "; ")
        print("Pitches: " + str(self.pitches))
        print()
        print(("BIP: "+str(self.BIP)), end = "; ")
        print(("H: " + str(self.H)), end = "; ")
        print(("Bases: " + str(self.bases)), end = "; ")
        print(("Singles: " + str(self.singles)), end = "; ")
        print(("Doubles: " + str(self.doubles)), end = "; ")
        print(("Triples: " + str(self.triples)), end = "; ")
        print("HR: " + str(self.homers))
        print()
        print(("Hit Location: "+self.hitloc), end = "; ")
        print(("Hit Quality: "+self.hitqual), end = "; ")
        print(("Hit Type: "+self.hittype), end = "; ")
        print("Infield hit: "+str(self.infh))
        print()
        
        print(("FO: "+str(self.fieldouts)), end = "; ")
        print(("FO Location: "+str(self.foloc)), end = "; ")
        print(("FO Quality: "+self.foqual), end = "; ")
        print(("FO Type: "+self.fotype), end = "; ")
        print(("DP: " + str(self.DP)), end = "; ")
        print("DP Type: "+self.doubleplaytype)
        print()
        print(("Reach: "+str(self.is_rch)), end = "; ")
        print(("RBOE: "+str(self.RBOE)), end = "; ")
        print(("FC: "+str(self.FC)), end = "; ")
        print(("SAC: "+str(self.SAC)), end = "; ")
        print("SF: "+str(self.SF))
        print()
        print(("BB: "+str(self.BB)), end = "; ")
        print(("IBB: "+str(self.IBB)), end = "; ")
        print(("UBB: "+str(self.UBB)), end = "; ")
        print(("SO: "+str(self.SO)), end = "; ")
        print(("KSwing: "+str(self.kswing)), end = "; ")
        print(("KLook: "+str(self.klook)), end = "; ")
        print(("UCTS: "+str(self.UCTS)), end = "; ")
        print(("SOReach: "+str(self.SOreach)), end = "; ")
        print(("HBP: "+str(self.HBP)), end = "; ")
        print("True Outcome: " + str(self.trueoutcome))
        print()
        print(("Bases Added: "+str(self.basesadded)), end = "; ")
        print(("Runs Added: "+str(self.runsadded)), end = "; ")
        print("Outs Added: "+str(self.outsadded))
        print()
        '''
    #------------------------------------------------------------------------------    
    def get_baseout_end(self):
        """Returns updated dict of base-out information."""
        
        return self.bsotend
        
        
    #------------------------------------------------------------------------------    
    def get_data_string(self):
        """Returns csv string of all variables generated by BatUnit class."""
        
        rowstring = ""
        rowstring += self.team
        rowstring += (","+self.batter_name)
        rowstring += (","+str(self.hole))
        rowstring += (","+self.count_balls)
        rowstring += (","+self.count_strikes)
        rowstring += (","+str(self.balls))
        rowstring += (","+str(self.fouls))
        rowstring += (","+str(self.swingingstrikes))
        rowstring += (","+str(self.calledstrikes))
        rowstring += (","+str(self.BIPs))
        rowstring += (","+str(self.pitches))
        rowstring += (","+str(self.BIP))
        rowstring += (","+str(self.H))
        rowstring += (","+str(self.bases))
        rowstring += (","+str(self.singles))
        rowstring += (","+str(self.doubles))
        rowstring += (","+str(self.triples))
        rowstring += (","+str(self.homers))
        rowstring += (","+self.hitloc)
        rowstring += (","+self.hitqual)
        rowstring += (","+self.hittype)
        rowstring += (","+str(self.infh))
        rowstring += (","+str(self.fieldouts))
        rowstring += (","+str(self.foloc))
        rowstring += (","+self.foqual)
        rowstring += (","+self.fotype)
        rowstring += (","+str(self.DP))
        rowstring += (","+self.doubleplaytype)
        rowstring += (","+str(self.is_rch))
        rowstring += (","+str(self.RBOE))
        rowstring += (","+str(self.FC))
        rowstring += (","+str(self.SAC))
        rowstring += (","+str(self.SF))
        rowstring += (","+str(self.BB))
        rowstring += (","+str(self.IBB))
        rowstring += (","+str(self.UBB))
        rowstring += (","+str(self.SO))
        rowstring += (","+str(self.kswing))
        rowstring += (","+str(self.klook))
        rowstring += (","+str(self.UCTS))
        rowstring += (","+str(self.SOreach))
        rowstring += (","+str(self.HBP))
        rowstring += (","+str(self.trueoutcome))
        rowstring += (","+str(self.basesadded))
        rowstring += (","+str(self.runsadded))
        rowstring += (","+str(self.outsadded))
        
        sbo = self.bsotstart
        sOuts = str(sbo["Outs"])
        sOF = sbo["OnFirst"]
        sOS = sbo["OnSecond"]
        sOT = sbo["OnThird"]
        sBS = sbo["BaseState"]
        sBOS = sbo["BaseOutState"]
        
        ebo = self.bsotend
        eOuts = str(ebo["Outs"])
        eOF = ebo["OnFirst"]
        eOS = ebo["OnSecond"]
        eOT = ebo["OnThird"]
        eBS = ebo["BaseState"]
        eBOS = ebo["BaseOutState"]
        
        rowstring += ("," + sOuts)
        rowstring += ("," + sOF)
        rowstring += ("," + sOS)
        rowstring += ("," + sOT)
        rowstring += ("," + sBS)
        rowstring += ("," + sBOS)
        rowstring += ("," + eOuts)
        rowstring += ("," + eOF)
        rowstring += ("," + eOS)
        rowstring += ("," + eOT)
        rowstring += ("," + eBS)
        rowstring += ("," + eBOS)
        
        return rowstring
    #--------------------------------------------------------------------------       
#//\\//\\//\\//\\//\\//\\Baserunning Unit Class//\\//\\//\\//\\//\\//\\//\\//\\ 
class BRUnit:
    """A string of play-by-play baserunning information
    
    Attributes:
        unitstring: original string of play-by-play baserunning information
        side: 'home' or 'away'
        bo: list of last names in batting order for specified team
        bsotstart: dict containing baseout information for start of plate appearance
        bsotend: dict containing baseout information for end of plate appearance
        action: what baserunner did ("advanced","stole","scored",...)
        runnername: last name of baserunner
        hole: baserunner place in batting order 
        advanced: True if runner advanced, False otherwise
        stole: True if runner stole a base, False otherwise
        scored: True if runner scored, False otherwise
        out: True if runner was out, False otherwise
        fielder1: position of first fielder involved in runner out ("1b","ss",...)
        fielder2: position of second fielder involved in runner out ("2b","3b",...)
        startbase: base occupied by runner at start of plate appearance (0,1,...,4)
        endbase: base occupied by runner at end of plate appearance (0,1,...,4)
        basesadded: number of bases gained by runner (endbase - startbase)
        outsadded: 1 if runner out, 0 otherwise
        runsadded: 1 if runner scored, 0 otherwise
        sba: 1 if stolen base attempt, 0 otherwise
        sb: 1 if stolen base, 0 otherwise
        poa: 1 if pickoff attempt, 0 otherwise
        fpo: 1 if failed pickoff attempt, 0 otherwise
        po: 1 if pickoff, 0 otherwise
        cs: 1 if caught stealing, 0 otherwise
        wp: 1 if wild pitch, 0 otherwise
        pb: 1 if passed ball, 0 otherwise
        aoe: 1 if runner advanced on error, 0 otherwise
        outatbase: base where runner called out
        
    """
    
    
    #--------------------------------------------------------------------------
    def __init__(self, unit_str, team, batting_order, start_bsot, end_bsot):
        """Initializes BRUnit object.
        
        Args:
            unit_str: original baserunning unit string
            team: 'away' or 'home'
            batting_order: list of names in batting order for specified team
            start_bsot: dict of base-out information for start of plate appearance
            end_bsot: dict of base-out information for end of plate appearance
        """
        
        self.unitstring = unit_str
        self.side = team
        self.bo = batting_order
        
        self.bsotstart = start_bsot
        self.bsotend = end_bsot
        
        self.action = "NA"
        self.runnername = "NA"
        self.hole = 0
        
        self.advanced = False
        self.stole = False
        self.scored = False
        self.out = False
        
        self.fielder1 = "NA"
        self.fielder2 = "NA"
        
        self.startbase = 0
        self.endbase = 0
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
        self.outatbase = 0
    #--------------------------------------------------------------------------    
            
    def get_runner_name(self):
        """Finds runner name in unit string and sets runnername and hole."""
        
        ts = self.unitstring
        
        for i,n in enumerate(self.bo):
            if n.lower() in ts.lower():
                self.runnername = n
                self.hole = i+1
                break          
    
    #--------------------------------------------------------------------------
    def get_start_base(self):
        """Determines base occupied by runner at start of plate appearance."""
       
        if self.runnername == self.bsotstart["OnFirst"]:
            self.startbase = 1
        elif self.runnername == self.bsotstart["OnSecond"]:
            self.startbase = 2
        elif self.runnername == self.bsotstart["OnThird"]:
            self.startbase = 3
        else:
            print("!!!ERROR: BRUnit.get_start_base; " + self.unitstring)
            
    def get_start_base_batbr(self):
        """Determines base occupied by batter-runner after reaching initially."""
        
        #treat the batunit and brunit as separate
        #look at the end baseout in stead of the start baseout for batter-runner's start base
        
        if self.runnername == self.bsotend["OnFirst"]:
            self.startbase = 1
            self.bsotend["OnFirst"] = "NA"
        elif self.runnername == self.bsotend["OnSecond"]:
            self.startbase = 2
            self.bsotend["OnSecond"] = "NA"
        elif self.runnername == self.bsotend["OnThird"]:
            self.startbase = 3
            self.bsotend["OnThird"] = "NA"
        else:
            print("!!!ERROR: BRUnit.get_start_base_batbr; " + self.unitstring)
            
        
    #--------------------------------------------------------------------------
    def get_action(self):
        """Determines action performed by baserunner and sets action, advanced, stole, scored, and out."""
        
        ts = self.unitstring
        
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
            print("!!!ERROR: BRUnit.get_action, ts: "+ts)
            print()
    
    #--------------------------------------------------------------------------
    def is_pickoff(self):
        """Determines if there is a pickoff and sets poa and po."""
        
        #run set_start_base first
        ts = self.unitstring
        
        if "caught stealing" in ts:
            self.sba = 1
            self.cs = 1
            self.outsadded = 1
            self.endbase = 0
            
        elif "failed pickoff" in ts:
            self.poa = 1
            self.fpo = 1 #end_base will be updated in get_advanced
            
        if "picked off" in ts:
            self.poa = 1
            self.po = 1
            self.outsadded = 1
            self.endbase = 0
            
        
    #--------------------------------------------------------------------------
    def get_advanced(self):
        """Determines where and why runner advanced, sets endbase, wp, pb, and aoe."""
        
        ts = self.unitstring
        
        if self.advanced:
            if "advanced to" in ts:
                if "to second" in ts:
                    self.endbase = 2
                elif "to third" in ts:
                    self.endbase = 3
                else:
                    print("!!!ERROR: BRUnit.get_advanced, ts: "+ts)
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
        """Determines what base runner stole and sets sba, sb, and endbase."""
        
        ts = self.unitstring
        
        if self.stole:
            if "second" in ts:
                self.sba = 1
                self.sb = 1
                self.endbase = 2
            elif "third" in ts:
                self.sba = 1
                self.sb = 1
                self.endbase = 3
            else: 
                print("ERROR!!!: BRUnit.get_stole, ts: "+ts)
    #--------------------------------------------------------------------------            
    def get_scored(self):
        """Sets endbase and runsadded and sets wp, pb, and aoe if applicable."""
        
        ts = self.unitstring
        
        if self.scored:
            self.endbase = 4
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
        """Determines where runner was called out and what fielders made the play."""
        
        ts = self.unitstring
        bi = -1
        
        if self.out:
            
            if "out at" in ts:    
        
                if "first" in ts:
                    self.outatbase = 1
                    bi = ts.rfind("first")
                elif "second" in ts:
                    self.outatbase = 2
                    bi = ts.rfind("second")
                elif "third" in ts:
                    self.outatbase = 3
                    bi = ts.rfind("third")
                elif "home" in ts:
                    self.outatbase = 4
                    bi = ts.rfind("home")
                    
                self.fielder1 = ts[ts.find(" ",bi)+1:ts.find("to",bi)-1]
                self.fielder2 = ts[ts.find("to",bi)+3:ts.find("to",bi)+5]
            
            #make sure it wasn't an uncaught third strike, in which case out was added in batting unit
            if "struck out" in ts:
                self.outsadded = 0
            else:
                self.outsadded = 1
            
            self.endbase = 0
        
    #--------------------------------------------------------------------------
    def update_bsot(self):
        """Updates information in base-out dict."""
        
        if self.endbase == 0:
            #if runner was out, erase from bases
            if self.bsotend["OnFirst"] == self.runnername:
                self.bsotend["OnFirst"] = "NA"
            if self.bsotend["OnSecond"] == self.runnername:
                self.bsotend["OnSecond"] = "NA"
            if self.bsotend["OnThird"] == self.runnername:
                self.bsotend["OnThird"] = "NA"
        elif self.endbase == 2:
            self.bsotend["OnSecond"] = self.runnername
        elif self.endbase == 3:
            self.bsotend["OnThird"] = self.runnername
        elif self.endbase == 4:
            #if runner scored, erase from bases
            if self.bsotend["OnFirst"] == self.runnername:
                self.bsotend["OnFirst"] = "NA"
            if self.bsotend["OnSecond"] == self.runnername:
                self.bsotend["OnSecond"] = "NA"
            if self.bsotend["OnThird"] == self.runnername:
                self.bsotend["OnThird"] = "NA"
        
        #keep outs between 0 and 3
        self.bsotend["Outs"] += self.outsadded
        
        #check bases to make sure runner not on more than one base
        if self.bsotend["OnFirst"] == self.bsotend["OnSecond"]:
            self.bsotend["OnFirst"] = "NA"
        if self.bsotend["OnFirst"] == self.bsotend["OnThird"]:
            self.bsotend["OnFirst"] = "NA"
        if self.bsotend["OnSecond"] == self.bsotend["OnThird"]:
            self.bsotend["OnSecond"] = "NA"
        
        self.bsotend["BaseState"] = BaseOut.get_base_state(self.bsotend["OnFirst"],self.bsotend["OnSecond"],self.bsotend["OnThird"])
        self.bsotend["BaseOutState"] = self.bsotend["BaseState"]+str(self.bsotend["Outs"])
    #--------------------------------------------------------------------------
    def get_bases_added(self):  
        """Determines bases added by baserunner during plate appearance (endbase - startbase)."""
        
        self.basesadded = self.endbase - self.startbase 
        
    #--------------------------------------------------------------------------
    def do_stuff(self):
        """Runs all BRUnit functions in correct order."""
        
        self.get_runner_name()
        self.get_start_base()
        self.get_action()
        self.is_pickoff()
        self.get_advanced()
        self.get_stole()
        self.get_scored()
        self.get_out()
        self.update_bsot()
        self.get_bases_added()
    #--------------------------------------------------------------------------    
    def do_stuff_batbr(self):
        """Runs all BRUnit functions for batter-runner case in correct order."""
        
        self.get_runner_name()
        self.get_start_base_batbr()
        self.get_action()
        self.is_pickoff()
        self.get_advanced()
        self.get_stole()
        self.get_scored()
        self.get_out()
        self.update_bsot()
        self.get_bases_added()
    
    #--------------------------------------------------------------------------
    def print_stuff(self):
        """Prints all BRUnit information for testing purposes."""
        
        print("Runner Name: " + self.runnername)
        print("Hole: " + str(self.hole))
        print("Action: "+ self.action)
        print("Start Base: "+ str(self.startbase))
        print("End Base: " + str(self.endbase))
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
        print("Start BaseOut:")
        print(self.bsotstart)
        print("End BaseOut:")
        print(self.bsotend)
        print()
    #--------------------------------------------------------------------------
    def get_baseout_end(self):
        """Returns updated dict of base-out information."""
        
        return self.bsotend
    
    #--------------------------------------------------------------------------   
    def get_data_string(self):
        """Returns csv string of all variables generated by BRUnit class."""
        
        datastring = ""
        datastring += (self.side+",")
        datastring += (self.runnername+",")
        datastring += (str(self.hole)+",")
        datastring += (self.action+",")
        datastring += (str(self.startbase)+",")
        datastring += (str(self.endbase)+",")
        datastring += (str(self.basesadded)+",")
        datastring += (str(self.sb)+",")
        datastring += (str(self.sba)+",")
        datastring += (str(self.outsadded)+",")
        datastring += (self.fielder1+",")
        datastring += (self.fielder2+",")
        datastring += (str(self.runsadded)+",")
        datastring += (str(self.po)+",")
        datastring += (str(self.poa)+",")
        datastring += (str(self.wp)+",")
        datastring += (str(self.pb)+",")
        datastring += (str(self.aoe)+",")
        
        sbo = self.bsotstart
        sOuts = str(sbo["Outs"])
        sOF = sbo["OnFirst"]
        sOS = sbo["OnSecond"]
        sOT = sbo["OnThird"]
        sBS = sbo["BaseState"]
        sBOS = sbo["BaseOutState"]
        
        ebo = self.bsotend
        eOuts = str(ebo["Outs"])
        eOF = ebo["OnFirst"]
        eOS = ebo["OnSecond"]
        eOT = ebo["OnThird"]
        eBS = ebo["BaseState"]
        eBOS = ebo["BaseOutState"]
        
        datastring += (sOuts+",")
        datastring += (sOF+",")
        datastring += (sOS+",")
        datastring += (sOT+",")
        datastring += (sBS+",")
        datastring += (sBOS+",")
        datastring += (eOuts+",")
        datastring += (eOF+",")
        datastring += (eOS+",")
        datastring += (eOT+",")
        datastring += (eBS+",")
        datastring += eBOS
        
        return datastring
        
#//\\//\\//\\//\\//\\//\\Substitution Unit Class//\\//\\//\\//\\//\\//\\//\\//\\ 
#list of positions

       
class SubUnit:
    """A string of play-by-play substitution information
    
    Attributes:
        off_pos = a list of positions in format used by websites ("dh","p",...)
        unitstring: original substitution string
        side: 'home' or 'away'
        ogawaybattingorder: original batting order for away team, a list of last names
        oghomebattingorder: original batting order for home team, a list of last names
        awaybattingorder: batting order for away team after substitution
        homebattingorder: batting order for home team after substitution
        awayoffsubs: offensive subs for away team, a list of last names
        homeoffsubs: offensive subs for home team, a list of last names
        awayrelievers: list of relief pitchers for away team
        homerelievers: list of relief pitchers for home team
        offense: False for pitchers and sub units without ' for ' in unitstring
            True causes update to batting order
        playerin: last name of player subbing in
        playerout: last name of player coming out or 'NA' if none
        subpos: position being subbed ("rf","p",...)
        subhole: subbed player's place in batting order (list index + 1)
    """
    
    off_pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]
    #--------------------------------------------------------------------------
    def __init__(self, sub_unit_str, team, away_batting_order, away_off_subs, away_relievers, home_batting_order, home_off_subs, home_relievers):
        """Initializes SubUnit object.
        
        Args:
            sub_unit_str: original play-by-play string of substitution information
            team: 'away' or 'home'
            away_batting_order: list of names in batting order for away team
            away_off_subs: list offensive subs for away team
            away_relievers: list of relief pitchers for away team
            home_batting_order: list of names in batting order for home team
            home_off_subs: list of offensive subs for home team
            home_relievers: list of relief pitchers for home team
            
        """
        
        self.unitstring = sub_unit_str
        self.side = team # 'home' or 'away'
        self.ogawaybattingorder = away_batting_order
        self.oghomebattingorder = home_batting_order
        self.awaybattingorder = []
        self.homebattingorder = []
        self.awayoffsubs = away_off_subs
        self.homeoffsubs = home_off_subs
        self.awayrelievers = away_relievers
        self.homerelievers = home_relievers
        
        self.offense = False #False for pitchers and sub units without ' for '
        
        self.playerin = "NA"
        self.playerout = "NA" #there may not always be a playerout
        
        self.subpos = "NA"
        self.subhole = 0
    #--------------------------------------------------------------------------    
    
    def get_players(self):
        """Finds player names in unit string and sets playerout and playerin."""
        
        ts = self.unitstring
        
        #if 'for' in string, playerout is name after it
        if 'for' in ts:
            self.playerout = StdzNames.last_only(ts[ts.find(' for ')+5:])
        if 'pinch' in ts: 
            self.playerin = StdzNames.last_only(ts[:ts.find("pinch")])
        elif 'to' in ts:
            self.playerin = StdzNames.last_only(ts[:ts.find(" to ")])
        else:
            self.playerin = "ERROR: SubUnit.get_players, ts: " + ts
    
    
    #--------------------------------------------------------------------------    
    def get_pos(self):
        """Determines position that is being substituted."""
        
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
    def get_offense(self): #run get_players and get_pos first
        """Determines if substitution requires change to a batting order."""
        
        if self.playerout != "NA":
            if self.subpos != 'p':
                self.offense = True
                
    
    def get_hole(self): #run get_offense first
        """Determines subbed player's place in batting order."""
        
        if self.offense:
            
            found = False #keep track of whether or not name was found, either team can sub any time
             
            if self.side == "away":
                for i,b in enumerate(self.ogawaybattingorder):
                    if self.playerout == b:
                        self.subhole = i+1
                        found = True
                        break
                 
                if not found:
                    for i,b in enumerate(self.oghomebattingorder):
                        if self.playerout == b:
                            self.subhole = i+1
                            self.side = "home"
                            found = True
                            break
                
                if not found:
                    print("Error: Subunit.get_hole; Name not found in batting orders")
            elif self.side == "home":
                for i,b in enumerate(self.oghomebattingorder):
                    if self.playerout == b:
                        self.subhole = i+1
                        found = True
                        break
                    
                if not found:
                    for i,b in enumerate(self.ogawaybattingorder):
                        if self.playerout == b:
                            self.subhole = i+1
                            self.side = "away"
                            found = True
                            break
                if not found:
                    print("Error: Subunit.get_hole; Name not found in batting orders")
            else:
                print("!!!Error: SubUnit.get_hole: self.side not 'home' or 'away'")
    
    #--------------------------------------------------------------------------    
    #Need function to return modified batting order when pos player is subbed
    def mod_batting_order(self):
        """Modifies batting order based on substitution."""
        
        #run other methods first
        if self.offense: #if substitution isn't defensive only
            
            if self.side == "away":
                for i,p in enumerate(self.ogawaybattingorder):
                    if i == self.subhole-1:
                        self.awaybattingorder.append(self.playerin)
                    else:
                        self.awaybattingorder.append(p)
                self.homebattingorder = self.oghomebattingorder
                
            elif self.side == "home":
                for i,p in enumerate(self.oghomebattingorder):
                    if i == self.subhole-1:
                        self.homebattingorder.append(self.playerin)
                    else:
                        self.homebattingorder.append(p)
                self.awaybattingorder = self.ogawaybattingorder
            else:
                print("Error: SubUnit.mod_batting_order: self.side not 'home' or 'away'")
            
        else:    
            self.awaybattingorder = self.ogawaybattingorder
            self.homebattingorder = self.oghomebattingorder
            
            
    #--------------------------------------------------------------------------  
    def do_stuff(self):
        """Runs all SubUnit functions in the correct order."""
        
        self.get_players()
        self.get_pos()
        self.get_offense()
        self.get_hole()
        self.mod_batting_order()
        
    #--------------------------------------------------------------------------    
    def get_updated_bo(self):
        """Returns post-substitution batting order lists for both teams."""
        
        return self.awaybattingorder, self.homebattingorder
    
    #--------------------------------------------------------------------------
    def print_stuff(self):
        """Prints all SubUnit information for testing purposes."""
        
        print("Original Batting Orders:")
        print(self.ogawaybattingorder)
        print(self.oghomebattingorder)
        print("Updated Batting Order:")
        print(self.awaybattingorder)
        print(self.homebattingorder)
        print()
        print("Offensive Subs:")
        print(self.awayoffsubs)
        print(self.homeoffsubs)
        
        print()
        print("Unit String: " + self.unitstring)
        print("Player Out: " + self.playerout + "; Player In: "+self.playerin + "; Subbed Pos: "+self.subpos + "; Hole: "+str(self.subhole))
        print()
        
    #--------------------------------------------------------------------------    
    def get_data_string(self):
        """Returns csv string of all variables generated by SubUnit class."""
        
        return self.playerout + "," + self.playerin + "," + self.subpos
        

        
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
#------------------------------------------------------------------------------    
def br_test():
    
    #dummy data:
    #bas1 = "LEWIS, A.J. hit by pitch (0-0)."
    #bsotstart should be: 0,NA,NA,NA,A,A0
    #bsotend should be: 0,Lewis,NA,NA,B,B0
    
    #bas2 = "LUDWICK, C. singled down the lf line (3-2 KBKBFB);" 
    #bsotstart should be: 0,Lewis,NA,NA,B,B0
    #bsotend should be: 0,Ludwick,NA,NA,B,B0
    
    brs3 = "LEWIS, A.J. advanced to second."
    #bsotstart should be: 0,Lewis,NA,NA,B,B0
    #bsotsend should be: 0,Ludwick,Lewis,NA,C,C0
    
    AwayBO = ['Johnson', 'Kerr', 'Howie', 'Botsoe', 'Lewis', 'Ludwick', 'Harris', 'Thomason', 'Conklin']
    bst = BaseOut.get_base_state("Lewis","NA","NA")
    bost = BaseOut.get_base_out_state(0,"Lewis","NA","NA")
    bods = {"Outs":0, "OnFirst":"Lewis", "OnSecond":"NA", "OnThird":"NA", "BaseState":bst, "BaseOutState":bost}
    bode = {"Outs":0, "OnFirst":"Ludwick", "OnSecond":"NA", "OnThird":"NA", "BaseState":bst, "BaseOutState":bost}
    
    
    br1 = BRUnit(brs3, "away", 1, AwayBO, bods, bode)
    br1.do_stuff()
    br1.print_stuff()
    
    print(br1.get_data_header())
    print()
    print(br1.get_data_string())    
    print()
#------------------------------------------------------------------------------    
def bat_test():
    
    startbo = {"Outs":0, "OnFirst":"Lewis", "OnSecond":"NA", "OnThird":"NA", "BaseState":"B", "BaseOutState":"B0"}
    batus1 = "LUDWICK, C. singled down the lf line (3-2 KBKBFB);"
    batus2 = "LEWIS, A.J. flied out to cf (3-2)."
    
    AwayBO = ['Johnson', 'Kerr', 'Howie', 'Botsoe', 'Lewis', 'Ludwick', 'Harris', 'Thomason', 'Conklin']
    
    
    bt1 = BatUnit(batus1,"away",AwayBO,startbo)
    bt1.do_stuff()
    bt1.print_stuff()
    print()
    dh = get_bat_data_header()
    ds = bt1.get_data_string()
    print(dh)
    print(ds)
    print()
    
    bt2 = BatUnit(batus2, "away", AwayBO, {"Outs":0, "OnFirst":"NA","OnSecond":"NA", "OnThird":"NA","BaseState":"A", "BaseOutState":"A0"})
    bt2.do_stuff()
    bt2.print_stuff()
    print()
    dh = get_bat_data_header()
    ds = bt2.get_data_string()
    print(dh)
    print(ds)
    print()
    
def batbr_test():
    
    bts1 = "TOPPEL walked (3-1 BBBKB);"
    brs2 = "PENA advanced to second."
    bbrs3 = "SWEENEY singled through the left side, advanced to second on the throw, RBI (3-1 BBKB);"
    brs4 = "TOPPEL advanced to third;"
    brs5 = "PENA scored."
    bts6 = "TESMOND flied out to lf (0-0)."
    
    #SWEENEY singled through the left side, advanced to second on the throw, RBI (3-1 BBKB); 
    HomeBO = ['Kerrigan', 'Emme', 'Morris', 'Govern', 'Pena', 'Knernschield', 'Toppel', 'Sweeney', 'Tesmond']
   
    #bbr1s = "SWEENEY singled through the left side, advanced to second on the throw, RBI (3-1 BBKB);"
    
    startbo = {"Outs":2, "OnFirst":"Pena","OnSecond":"NA","OnThird":"NA","BaseState":"B","BaseOutState":"B2"}
    
    bt1 = BatUnit(bts1,"home",HomeBO,startbo)
    bt1.do_stuff()
    bt1.print_stuff()
    
    endbo = bt1.get_baseout_end()
    
    br2 = BRUnit(brs2,"home",HomeBO,startbo,endbo)
    br2.do_stuff()
    br2.print_stuff()
    endbo = br2.get_baseout_end()
    
    startbo = endbo
    
    bbr3a = BatUnit(bbrs3,"home",HomeBO,startbo)
    bbr3a.do_stuff()
    bbr3a.print_stuff()
    endbo = bbr3a.get_baseout_end()
    
    bbr3b = BRUnit(bbrs3,"home",HomeBO,startbo,endbo)
    bbr3b.do_stuff_batbr()
    bbr3b.print_stuff()
    endbo = bbr3b.get_baseout_end()
    
    br4 = BRUnit(brs4,"home",HomeBO,startbo,endbo)
    br4.do_stuff()
    br4.print_stuff()
    endbo = br4.get_baseout_end()
    
    br5 = BRUnit(brs5,"home",HomeBO,startbo,endbo)
    br5.do_stuff()
    br5.print_stuff()
    endbo = br5.get_baseout_end()
    
    startbo = endbo
    
    bt6 = BatUnit(bts6,"home",HomeBO,startbo)
    bt6.do_stuff()
    bt6.print_stuff()
    