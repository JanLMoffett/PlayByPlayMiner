# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 14:13:38 2019

@author: Jan
"""
import BaseOut

class GameState:
    def __init__(self):
        
        self.baseoutstate = {"Outs":0, "OnFirst":"NA", "OnSecond":"NA", "OnThird":"NA", "BaseState":"A", "BaseOutState":"A0"}
        self.fieldstate = {"atDH":"NA", "atP":"NA", "atC":"NA", "at1B":"NA", "at2B":"NA","at3B":"NA", "atSS":"NA", "atLF":"NA", "atCF":"NA", "atRF":"NA"}
        
        self.outs = 0
        self.onfirst = "NA"
        self.onsecond = "NA"
        self.onthird = "NA"
        self.basestate = "A"
        self.baseoutstate = "A0"
        
    def update_outs(self, num_outs):
        
        
        
        
        
        
        