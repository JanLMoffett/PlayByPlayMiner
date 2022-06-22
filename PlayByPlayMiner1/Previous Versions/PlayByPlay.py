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
        
        self.num_subs = 0
        self.num_bats = 0
        self.num_brs = 0
        self.num_au = 0
        
        self.au = []
        self.au_types = []
    
    #--------------------------------------------------------------------------
    def get_action_units(self):
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
                aus += ts[i:]
                #print(aus.strip())
                au.append(aus.strip())
                break
        self.au = au    
            
    
    
    #--------------------------------------------------------------------------
    def get_types(self):
        #types
        t = []
        aus = self.au
        
        for u in aus:
            if ")" in u:
                if "out at" in u:
                    if "struck out" in u:
                        t.append("bat")
                    else:
                        t.append("batbr")
                elif "out on" in u:
                    t.append("batbr")
                elif "advanced" in u:
                    t.append("batbr")
                elif "stole" in u:
                    t.append("batbr")
                elif "scored" in u:
                    t.append("batbr")
                else:
                    t.append("bat")
            elif "reached" in u:
                t.append("bat")
            elif "hit by pitch" in u:
                t.append("bat")
            elif "walked" in u:
                t.append("bat")
            
            elif "out at" in u:     
                t.append("br")
            elif "out on" in u:
                t.append("br")
            elif "advanced" in u:
                t.append("br")
            elif "stole" in u:
                t.append("br")
            elif "scored" in u:
                t.append("br")
            else:
                t.append("sub")
                
        self.au_types = t
    #--------------------------------------------------------------------------
    def get_au_nums(self):
        t = self.au_types
        
        self.num_batbrs = t.count("batbr")
        self.num_bats = t.count("bat")
        self.num_brs = t.count("br")
        self.num_subs = t.count("sub")
        self.num_au = self.num_bats + self.num_brs + self.num_subs
    #--------------------------------------------------------------------------
    def do_stuff(self):
        self.get_action_units()
        self.get_types()
        self.get_au_nums()
    #--------------------------------------------------------------------------
    def print_stuff(self):
        print("original pbp string:") 
        print(self.original_pbp_string)
        print()
        
        print("num bat_units: " + str(self.num_bats))
        print("num batbr_units: "+str(self.num_batbrs))
        print("num br_units:  " + str(self.num_brs))
        print("num sub_units: " + str(self.num_subs))
        print("total:        " + str(self.num_au))
        print()
        
        for i,s in enumerate(self.au):
            print(self.au_types[i])
            print(s)
        print()
        
    #--------------------------------------------------------------------------    
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           Close Play by Play Class 
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    
def test():
    
    
    pbpx = "LEWIS, A.J. hit by pitch (0-0). LUDWICK, C. singled down the lf line (3-2 KBKBFB); LEWIS, A.J. advanced to second. WEAVER, L. pinch ran for LUDWICK, C.. HARRIS IV, D singled to third base, bunt (0-0); WEAVER, L. advanced to second; LEWIS, A.J. advanced to third. THOMASON, L. flied out to cf, SF, RBI (3-2 FFBBB); WEAVER, L. advanced to third; LEWIS, A.J. scored. CONKLIN, C. grounded out to p, SAC, bunt, RBI (0-0); HARRIS IV, D advanced to second; WEAVER, L. scored. JOHNSON, W. struck out swinging (0-2 SKFS)."
    P1 = PlayByPlay(pbpx)
    
    P1.do_stuff()
    P1.print_stuff()
    
    '''
    apx1 = "JOHNSON, W. flied out to cf to left center (3-1 BBBK). KERR, R. flied out to cf (0-2 SFFFFF). HOWIE, N. singled up the middle (0-1 S). BOTSOE, C. fouled out to 1b (1-2 KBK)."
    apx2 = "LEWIS, A.J. flied out to cf (3-2 FBKFFBB). LUDWICK, C. lined out to 3b (0-1 F). HARRIS IV, D struck out looking (0-2 FFFK)."
    apx3 = "THOMASON, L. singled through the right side (1-1 BK). CONKLIN, C. grounded out to p, SAC, bunt (0-1 F); THOMASON, L. advanced to second. THOMASON, L. advanced to third on a passed ball. JOHNSON, W. struck out swinging (1-2 KSBS). KERR, R. flied out to rf (0-0)."
    apx4 = "HOWIE, N. flied out to rf to right center (2-2 FFBB). BOTSOE, C. flied out to cf to right center (0-0). LEWIS, A.J. doubled down the lf line (2-1 KBB). LUDWICK, C. flied out to cf to right center (3-2 FBBKB)."
    apx5 = "HARRIS IV, D doubled to left center (1-2 KFB). HARRIS IV, D out at second p to ss, picked off. THOMASON, L. singled to shortstop (2-1 KBB). CONKLIN, C. struck out swinging (0-2 KKS). JOHNSON, W. grounded out to 3b (0-0)."
    apx6 = "KERR, R. flied out to cf (0-0). HOWIE, N. struck out looking (1-2 BFFK). BOTSOE, C. struck out swinging (1-2 KKBFS)."
    apx7 = "LEWIS, A.J. hit by pitch (0-0). LUDWICK, C. singled down the lf line (3-2 KBKBFB); LEWIS, A.J. advanced to second. WEAVER, L. pinch ran for LUDWICK, C.. HARRIS IV, D singled to third base, bunt (0-0); WEAVER, L. advanced to second; LEWIS, A.J. advanced to third. THOMASON, L. flied out to cf, SF, RBI (3-2 FFBBB); WEAVER, L. advanced to third; LEWIS, A.J. scored. CONKLIN, C. grounded out to p, SAC, bunt, RBI (0-0); HARRIS IV, D advanced to second; WEAVER, L. scored. JOHNSON, W. struck out swinging (0-2 SKFS)."
    apx8 = "STEVENSON to p for DEXTER. KERR, R. popped up to 3b (3-2 BBBFF). HOWIE, N. grounded out to ss (2-2 BKKFB). BOTSOE, C. struck out swinging (1-2 BKFS)."
    apx9 = "LEWIS, A.J. singled to right field (0-0). WEAVER, L. to dh. WEAVER, L. grounded out to p unassisted, SAC, bunt (2-1 BBK); LEWIS, A.J. advanced to second. HARRIS IV, D fouled out to 1b (1-1 KB). THOMASON, L. walked (3-1 BBBKB). CONKLIN, C. tripled to right center, 2 RBI (0-0); THOMASON, L. scored; LEWIS, A.J. scored. JOHNSON, W. walked (3-2 FBKFBBB). KERR, R. flied out to lf (1-2 BFFFFF)."
    
    apxlist = [apx1, apx2, apx3, apx4, apx5, apx6, apx7, apx8, apx9]
    
    for x in apxlist:
        pbp = PlayByPlay(x)
        pbp.do_stuff()
        pbp.print_stuff()
    '''

    
    