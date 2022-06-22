# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 21:32:11 2019

@author: Jan
"""

import BaseOut
import bo_test2

bo1 = BaseOut.BaseOut()

bo1.print_stuff()

bo1.set_on_first("Jake")
bo1.set_on_second("Ryland")
bo1.set_on_third("Howie")

bo1.get_base_state()
bo1.get_base_out_state()

bo1.print_stuff()
bod = bo1.get_info()

print(bod)
print()

newbod = bo_test2.change_bo(bod)

print("newbod")
print(newbod)






