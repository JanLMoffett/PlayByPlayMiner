# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:16:30 2019

@author: Jan
"""
import PlayByPlay
import ActionUnit

def test():
    #xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
    #                           Example Data
    #xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
    away_order = ['Avros', 'Kueber', 'Martinez', 'Spain', 'Phillips', 'Tipler', 'Joslin', 'Mcdonald', 'Head']
    away_subs = ['Hubbard', 'Campbell', 'Kouba']
    
    home_order = ['Johnson', 'Kerr', 'Howie', 'Botsoe', 'Lewis', 'Ludwick', 'Harris Iv', 'Conklin', 'Thomason']
    home_subs = ['Weaver', 'Lucio', 'Laster', 'Borek', 'Williams']
    
    pbps2 = "BOREK, N. to p for LASTER, N.. KUEBER, G. walked (3-2 KBBBFB). MARTINEZ, D. singled up the middle (2-1 BBF); KUEBER, G. advanced to third. WILLIAMS, D. to p for BOREK, N.. SPAIN, G. reached on a fielder s choice (0-2 SK); MARTINEZ, D. advanced to second; KUEBER, G. out at home 3b to c. PHILLIPS, P. struck out swinging (3-2 KBBSFBFS). TIPLER, M. reached on a fielder s choice (2-2 BFSFB); SPAIN, G. out at second 2b to ss."
    #pbps2 = "BOREK, N. to p for LASTER, N.. AVROS, X. stole second. KUEBER, G. walked (3-2 KBBBFB). KUEBER, G. stole second. MARTINEZ, D. singled up the middle (2-1 BBF); KUEBER, G. advanced to third. WILLIAMS, D. to p for BOREK, N.. SPAIN, G. reached on a fielder s choice (0-2 SK); MARTINEZ, D. advanced to second; KUEBER, G. out at home 3b to c. PHILLIPS, P. struck out swinging (3-2 KBBSFBFS). TIPLER, M. reached on a fielder s choice (2-2 BFSFB); SPAIN, G. out at second 2b to ss."
    
    #xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
    
    
    #initializing PlayByPlay object
    p1 = PlayByPlay.PlayByPlay(pbps2, away_order, away_subs, home_order, home_subs)
    #pbps = play by play string
    #away_order, home_order = list length 10 of standardized last names
    #away_subs, home_subs = list of standardized last names
    
    # PlayByPlay methods:
    p1.print_stuff()  #prints variables made by constructor
    p1.get_action_units()
    p1.get_types()
    
    a1 = p1.au
    t1 = p1.au_types
    
    
    for i,s in enumerate(a1):
        print(str(i+1)+": "+s)
        print("Type: "+t1[i])
        
        if t1[i] == "bat":
            #make a bat_unit
            b1 = ActionUnit.BatUnit(s, away_order, home_order)
            b1.print_stuff()
            print("Pitches: "+str(b1.get_pitches()))
            if b1.is_bip():
                print("Ball in Play")
                if b1.is_hit():
                    print("Hit")
                else:
                    print("Out")
            else:
                print("No Ball in Play")
            print()
            
            
        elif t1[i] == "br":
            br1 = ActionUnit.BRUnit(s, away_order, home_order)    
            br1.print_stuff()
            print()
            
        else:
            s1 = ActionUnit.SubUnit(s, away_order, away_subs, home_order, home_subs)
            s1.get_team()
            s1.print_stuff()
            print()
            
test()