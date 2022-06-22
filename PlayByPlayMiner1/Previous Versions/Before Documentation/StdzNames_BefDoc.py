# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:11:18 2019

@author: Jan
"""

def last_first(name_string):
    name_string = name_string.strip()
    spaces = name_string.count(" ")
    #print("spaces: "+str(spaces)) #test
    ln = ""
    fn = ""
    
    if spaces == 0:
        if "," in name_string:
            ln = name_string[0:name_string.find(",")].title()
            ln = ln.replace(".","") #remove punc
            fn = name_string[name_string.find(",")+1:]
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
        else:
            ln = name_string.title()
            ln = ln.replace(".","") #remove punc
    elif spaces == 1:
        #check for punctuation
        if "," in name_string:  #assuming last, first
            ln = name_string[0:name_string.find(",")].title()
            ln = ln.replace(".","") #remove punc
            fn = name_string[name_string.find(",")+1:]
            fn = fn.strip() #remove spaces
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
        else: #assuming first last
            fn = name_string[0:name_string.find(" ")]
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
            ln = name_string[name_string.find(" ")+1:].title()
            ln = ln.replace(".","") #remove punc
    elif spaces == 2:
        if "," in name_string:
            ln = name_string[0:name_string.find(",")].title()
            ln = ln.replace(".","") #remove punc
            fn = name_string[name_string.find(",")+1:name_string.rfind(" ")]
            fn = fn.strip()
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
        else:
            fn = name_string[0:name_string.find(" ")]
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
            ln = name_string[name_string.find(" ")+1:name_string.rfind(" ")].title()
            ln = ln.replace(".","") #remove punc
    elif spaces == 3:
        if "," in name_string:
            ln = name_string[0:name_string.find(",")]
            ln = ln.strip()
            ln = ln.replace(".","") #remove punc
            if " " in ln:
                ln_front = ln[0:ln.find(" ")]
                ln_back = ln[ln.find(" ")+1:]
                if len(ln_back) < 4:
                    ln = ln_front.title()
                else:
                    ln = ln.strip(" ")
                    ln = ln.title()
            fn = name_string[name_string.find(",")+1: name_string.rfind(" ")]
            fn = fn.strip()
            fn = fn.title()
        else:
            print("!!!ERROR: stdz_name, too many spaces")
            print("Invalid Entry: " + name_string)
            ln = "ERROR: " + name_string
            fn = "ERROR: " + name_string
            
    else:   
        print("!!!ERROR: stdz_name, too many spaces") 
        print("Invalid Entry: " + name_string)
        ln = "ERROR: " + name_string
        fn = "ERROR: " + name_string
        
    return ln, fn
#------------------------------------------------------------------------------
def last_only(name_string):
    ln,fn = last_first(name_string)
    return ln
#------------------------------------------------------------------------------
def first_only(name_string):
    ln,fn = last_first(name_string)
    return fn
#------------------------------------------------------------------------------   
def lasts_firsts(name_list): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #check for comma to determine order (last, First vs. First Last)
    fns = []
    lns = []
    
    for n in name_list:
        l, f = last_first(n)
        lns.append(l)
        fns.append(f)
        
    return lns, fns   

#------------------------------------------------------------------------------
def lasts_only(name_list):
    lns,fns = lasts_firsts(name_list)
    
    return lns
#------------------------------------------------------------------------------
def firsts_only(name_list):
    lns,fns = lasts_firsts(name_list)
    
    return fns
#------------------------------------------------------------------------------
def test():
    n_list = ['KERRIGAN, Keith', 'EMME, Grant', 'MORRIS, Hunter', 'GOVERN, Jimmy', 'PENA, Christian', 'KNERNSCHIELD, Ryan', 'WAZNIS. Matt', 'SWEENEY, Trey', 'TESMOND, Tyler', 'DEXTER, Spenser']
    
    print(last_first("MORRIS, Hunter"))
    print(last_first("MORRIS, Hunter 2b"))
    print(last_first("Hunter Morris"))
    print(last_first("Hunter Morris "))
    print(last_first("MORRIS, H. a"))
    print(last_first("MORRIS,H."))
    print(last_first("H. Morris"))
    print(last_first("MORRIS"))
    print(last_first("MORRIS "))
    print()
    print(last_first("morris day and the time"))
    print()
    
    lasts, firsts = lasts_firsts(n_list)
    
    for i,ln in enumerate(lasts):
        print("Last Name: "+ln + "; First Name: "+firsts[i])
    print()
    
    lastsonly = lasts_only(n_list)
    
    for ln in lastsonly:
        print(ln)
    print()
    
    firstsonly = firsts_only(n_list)
    
    for fn in firstsonly:
        print(fn)
    print()
  
