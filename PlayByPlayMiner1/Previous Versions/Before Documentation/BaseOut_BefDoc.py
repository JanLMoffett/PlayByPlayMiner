# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 06:36:31 2019

@author: Jan
"""

#--------------------------------------------------------------------------   
def get_base_state(on_first, on_second, on_third):
    base_state = ""
    if on_first != "NA":
        
        if on_second != "NA":
            if on_third != "NA": #bases are loaded
                base_state = "H"        
            else: #man on first and second
                base_state = "E"
                
        elif on_third != "NA": #man on first and third
            base_state = "F"
            
        else: #man on first only
            base_state = "B"
            
    elif on_second != "NA": #first is empty
        
        if on_third != "NA": #man on second and third
            base_state = "G"
            
        else: #man on second only
            base_state = "C"
            
    elif on_third != "NA": #man on third only
        base_state = "D"
    
    else: #bases are empty
        base_state = "A"
        
    return base_state
            
#--------------------------------------------------------------------------            
def get_base_out_state(outs, on_first, on_second, on_third):
    
    bs = get_base_state(on_first, on_second, on_third)
    
    return bs + str(outs)
#--------------------------------------------------------------------------    
    
def test():
    
    print(get_base_state("Jake","NA","Damon"))
    print(get_base_out_state(2, "Dustin","Danny","NA"))
   

        
        
        
        