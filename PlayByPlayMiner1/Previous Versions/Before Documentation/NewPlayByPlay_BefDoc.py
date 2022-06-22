# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 15:39:05 2019

@author: Jan
"""
import math

class PlayByPlay:
    #..........................................................................
    def __init__(self, pa_unit_list, pa_side_list, pa_id_list):
        
        self.paunits = pa_unit_list
        self.pasides = pa_side_list
        self.paids = pa_id_list
        #break pa_units into bat and br action units, if pa_unit contains ";"
        #assign type to each action unit
        #assign pa id to each action unit
        
        self.actionunits = []
        self.autypes = [] #same length as actionunits, "bat", "br", "batbr", "sub"
        self.ausides = []  #same length as actionunits, "away" or "home"
        self.aupaids = [] #plate id for each action unit, unique for bat units, each br unit associated through pa_id with bat unit
        self.auhalfinnings = []     
        
    #..........................................................................
    def get_action_units(self):
        for i,u in enumerate(self.paunits):
            
            
            
            #if there is a ';' in pa unit, break into bat and br units
            if ";" in u:
                #initialize temporary string as rest of pa unit after ';'
                ts = u
                
                #while there are more semicolons in ts
                while(ts.find(";")>0):
                    #add the first part of the string to actionunits
                    self.actionunits.append(ts[0:ts.find(";")+1])
                    self.aupaids.append(self.paids[i])
                    self.ausides.append(self.pasides[i])
                    
                    #update temporary string
                    ts = ts[ts.find(";")+1:].strip()
                    
                #add the remainder to actionunits
                self.actionunits.append(ts)
                self.aupaids.append(self.paids[i])
                self.ausides.append(self.pasides[i])    
                
            else:
                #if no semicolons, add entire pa unit to action unit list
                self.actionunits.append(u)
                self.aupaids.append(self.paids[i])
                self.ausides.append(self.pasides[i])
    
    #..........................................................................
    def get_au_types(self): #run get_action_units first
        
        for u in self.actionunits:
            if ")" in u:
                if "out at" in u:
                    if "struck out" in u:
                        self.autypes.append("bat")
                    else:
                        self.autypes.append("batbr")
                elif "out on" in u:
                    self.autypes.append("batbr")
                elif "advanced" in u:
                    self.autypes.append("batbr")
                elif "stole" in u:
                    self.autypes.append("batbr")
                elif "scored" in u:
                    self.autypes.append("batbr")
                else:
                    self.autypes.append("bat")
            elif "reached" in u:
                self.autypes.append("bat")
            elif "flied" in u:
                self.autypes.append("bat")
            elif "hit by pitch" in u:
                self.autypes.append("bat")
            elif "walked" in u:
                self.autypes.append("bat")
            elif "out at" in u:     
                self.autypes.append("br")
            elif "out on" in u:
                self.autypes.append("br")
            elif "advanced" in u:
                self.autypes.append("br")
            elif "stole" in u:
                self.autypes.append("br")
            elif "scored" in u:
                self.autypes.append("br")
            elif "to" in u or "for" in u and len(u) <= 40: #this is an addition to correct logic errors
                self.autypes.append("sub")
            else:
                self.autypes.append("other") #will cause error in SoupChef
    #..........................................................................
    def get_au_types2(self): #run get_action_units first
        
        bat_verbs = ["grounded", "flied", "lined", "popped", "fouled", "walked", "intentionally walked", "hit by pitch", "reached", "struck out", "singled", "doubled", "tripled", "homered"]
        br_verbs = ["out at", "out on", "advanced", "stole", "scored"]  
        tp = ""
        
        for u in self.actionunits:
            if "reviewed" in u.lower() or "ruled" in u.lower() or "review" in u.lower():
                self.autypes.append("other")
                continue
            
            tp = "other"
            
            if "(" in u:
                tp = "bat"
                for d in br_verbs:
                    if d in u:
                        tp = "batbr"
                        break
            
            for b in bat_verbs:
                if b in u:
                    tp = "bat"
                    for v in br_verbs:
                        if v in u:
                            tp = "batbr"
                            break
                    break
                
            if tp != "other":
                self.autypes.append(tp)
                continue
            else:
                for c in br_verbs:
                    if c in u:
                        tp = "br"
                        break
                if tp != "other":
                    self.autypes.append(tp)
                    continue
                else:
                    if "pinch" in u:
                        tp = "sub"
                    elif "to" in u and "for" in u:
                        tp = "sub"
                    elif "to" in u:
                        tp = "sub"
                    self.autypes.append(tp)       
            
            
        
    #..........................................................................
    def get_au_innings(self):
        for paid in self.aupaids:
            inning = int(paid[2:4])
            
            
            self.auhalfinnings.append(inning)
                
    #..........................................................................
    def do_stuff(self):
        self.get_action_units()
        self.get_au_types2()
        self.get_au_innings()
        
    #..........................................................................
    def print_stuff(self):
        for i,u in enumerate(self.actionunits):
            print("Unit: " + u)
            print("Type: " + self.autypes[i] + "; ID: " + self.aupaids[i] + "; Side: " + self.ausides[i] + "; Inning: " + str(self.auinnings[i]))
            print()
        print()    
        
    #..........................................................................
    