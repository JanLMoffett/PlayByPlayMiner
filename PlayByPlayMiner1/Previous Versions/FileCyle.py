# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:22:53 2019

@author: Jan
"""

list1 = ['Johnson', 'Kerr', 'Howie', 'Lewis', 'Harris Iv', 'Lucio', 'Botsoe', 'Conklin', 'Weaver']
list2 = ['Dunn', 'Snider', 'Fitzgerald', 'Kerr', 'Britton', 'Stringer', 'Campbell', 'Lavey', 'Davis']


match = False

for i in list1:
    for j in list2:
        
        if i == j:
            match = True
            
print(match)