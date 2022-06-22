# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:25:11 2019

@author: Jan
"""
import StdzNames
pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]
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
    # function to put starters in list in order of position
    def get_pos_order(self):#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #takes a list of strings in format: KERR, Ryland 2b
        #returns list of ten names
        
        away_pos_order = [""]*10 # 0 will be DH
        home_pos_order = [""]*10 # 0 will be DH
        
        #read last two chars in string
        for i,s in enumerate(self.away_starters):
            for j,t in enumerate(pos):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                    away_pos_order[j] = StdzNames.stdz_name(s[:s.rfind(" ")])
                    
        #read last two chars in string
        for i,s in enumerate(self.home_starters):
            for j,t in enumerate(pos):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                    home_pos_order[j] = StdzNames.stdz_name(s[:s.rfind(" ")])
                    
        away_pos_dict = {"DesignatedHitter":away_pos_order[0],"StartingPitcher":away_pos_order[1],"Catcher":away_pos_order[2],"FirstBaseman":away_pos_order[3],"SecondBaseman":away_pos_order[4],"ThirdBaseman":away_pos_order[5],"ShortStop":away_pos_order[6],"LeftFielder":away_pos_order[7],"CenterFielder":away_pos_order[8],"RightFielder":away_pos_order[9]}
        home_pos_dict = {"DesignatedHitter":home_pos_order[0],"StartingPitcher":home_pos_order[1],"Catcher":home_pos_order[2],"FirstBaseman":home_pos_order[3],"SecondBaseman":home_pos_order[4],"ThirdBaseman":home_pos_order[5],"ShortStop":home_pos_order[6],"LeftFielder":home_pos_order[7],"CenterFielder":home_pos_order[8],"RightFielder":home_pos_order[9]}        
           
        return away_pos_dict, home_pos_dict
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
                
        aps = StdzNames.stdz_names(a_pos_subs)
        hps = StdzNames.stdz_names(h_pos_subs)
        
                
        return aps, hps
    #close get_subs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    #--------------------------------------------------------------------------        
    # function to get list of relief pitchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_relievers(self):
        
        away_relievers, home_relievers = self.get_subs(1)   
    
        return away_relievers, home_relievers      
    # close get_relievers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 
    #--------------------------------------------------------------------------
    # function to get list of pinch hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_pinch_hitters(self):
        away_pinch_hitters = []
        home_pinch_hitters = []
        
        for s in self.away_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
                away_pinch_hitters.append(s[:s.rfind(" ")])
                
        for s in self.home_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
                home_pinch_hitters.append(s[:s.rfind(" ")])
                
        aph = StdzNames.stdz_names(away_pinch_hitters)
        hph = StdzNames.stdz_names(home_pinch_hitters)
                
        return aph, hph
    # close get_pinch_hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #--------------------------------------------------------------------------    
    # function to get list of pinch runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_pinch_runners(self):
        
        away_pinch_runners = []
        home_pinch_runners = []
        
        for s in self.away_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
                away_pinch_runners.append(s[:s.rfind(" ")])
                
        for s in self.home_subs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
                home_pinch_runners.append(s[:s.rfind(" ")])
                
        apr = StdzNames.stdz_names(away_pinch_runners)
        hpr = StdzNames.stdz_names(home_pinch_runners)
                
        return apr, hpr
    # close get_pinch_runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #--------------------------------------------------------------------------
    # 14.) function to get a list of starters in batting order
    def get_batting_orders(self): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        away_bo = []
        home_bo = []
        
        for s in self.away_starters:
            if s[s.rfind(" ")+1:] != "p":
                away_bo.append(StdzNames.stdz_name(s[:s.rfind(" ")]))
                
        for s in self.home_starters:
            if s[s.rfind(" ")+1:] != "p":
                home_bo.append(StdzNames.stdz_name(s[:s.rfind(" ")]))
                
        away_bo_names = {"OneHole":away_bo[0],"TwoHole":away_bo[1], "ThreeHole":away_bo[2], "FourHole":away_bo[3], "FiveHole":away_bo[4], "SixHole":away_bo[5], "SevenHole":away_bo[6], "EightHole":away_bo[7], "NineHole":away_bo[8]}
        home_bo_names = {"OneHole":home_bo[0],"TwoHole":home_bo[1], "ThreeHole":home_bo[2], "FourHole":home_bo[3], "FiveHole":home_bo[4], "SixHole":home_bo[5], "SevenHole":home_bo[6], "EightHole":home_bo[7], "NineHole":home_bo[8]}
        
        return away_bo, home_bo, away_bo_names, home_bo_names
    #close get_batting_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    #--------------------------------------------------------------------------
    
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                            Close Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
        
