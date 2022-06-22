# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 21:32:13 2019

@author: Jan
"""

import BaseOut

def change_bo(bo_dict):
    bod = bo_dict
    
    onfirst = bod["OnFirst"]
    onsecond = bod["OnSecond"]
    onthird = bod["OnThird"]
    
    outs = bod["Outs"]
    
    
    
    bo2 = BaseOut.BaseOut()
    bo2.set_on_first(onfirst)
    bo2.set_on_second(onsecond)
    bo2.set_on_third(onthird)
    bo2.set_outs(outs)
    
    bo2.get_base_state()
    bo2.get_base_out_state()
    
    print("change_bo before")
    bo2.print_stuff()
    
    bo2.set_on_third("Jake")
    bo2.set_on_first("NA")
    bo2.set_on_second("NA")
    bo2.get_base_state()
    bo2.get_base_out_state()
    
    print("change bo after")
    bo2.print_stuff()
    
    bod2 = bo2.get_info()
    
    return bod2
    
    
    
    
    
    
    
    