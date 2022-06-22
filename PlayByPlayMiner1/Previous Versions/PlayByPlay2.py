# -*- coding: utf-8 -*-
"""
Created on Thu May 30 17:00:58 2019

@author: Jan
"""

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
#                            Play by Play Class 
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 
class PlayByPlay:
    #--------------------------------------------------------------------------
    def __init__(self, pbp_string):
        self.original_pbp_string = pbp_string
        
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
                if "intentionally" in u:
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
            pi = ts.find(". ",i) #indicates end of substituition or br unit if abs(pi - ci) > 5
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
                if ts[ci+2:pi+1] == "A.J.":
                    aus += ts[i:k+1]
                    i = k+1
                elif (0 <= pi-ci <= 3): #if period is near a comma, indicating part of a name
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