# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:11:18 2019

@author: Jan
"""

def stdz_name(name_string):
    name_string = name_string.strip()
    spaces = name_string.count(" ")
    #print("spaces: "+str(spaces)) #test
    ln = ""
    fn = ""
    
    if spaces == 0:
        if "," in name_string:
            ln = name_string[0:name_string.find(",")].title()
            fn = name_string[name_string.find(",")+1:]
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
        else:
            ln = name_string.title()
    elif spaces == 1:
        #check for punctuation
        if "," in name_string:  #assuming last, first
            ln = name_string[0:name_string.find(",")].title()
            fn = name_string[name_string.find(",")+1:]
            fn = fn.strip() #remove spaces
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
        else: #assuming first last
            fn = name_string[0:name_string.find(" ")]
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
            ln = name_string[name_string.find(" ")+1:].title()
    elif spaces == 2:
        if "," in name_string:
            ln = name_string[0:name_string.find(",")].title()
            fn = name_string[name_string.find(",")+1:name_string.rfind(" ")]
            fn = fn.strip()
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
        else:
            fn = name_string[0:name_string.find(" ")]
            fn = fn.replace(".","") #remove punc
            fn = fn.title()
            ln = name_string[name_string.find(" ")+1:name_string.rfind(" ")].title()
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
            
    else:   
        print("!!!ERROR: stdz_name, too many spaces")     
        
    return ln, fn

# standardized list of last names    
def stdz_names(name_list): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #check for comma to determine order (last, First vs. First Last)
    fns = []
    lns = []
    
    for n in name_list:
        l, f = stdz_name(n)
        lns.append(l)
        fns.append(f)
        
    return lns, fns   
# close stdz_names ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------

def test():
    n_list = ['KERRIGAN, Keith', 'EMME, Grant', 'MORRIS, Hunter', 'GOVERN, Jimmy', 'PENA, Christian', 'KNERNSCHIELD, Ryan', 'WAZNIS. Matt', 'SWEENEY, Trey', 'TESMOND, Tyler', 'DEXTER, Spenser']
    
    
    '''
    print(stdz_name("MORRIS, Hunter"))
    print(stdz_name("MORRIS, Hunter 2b"))
    print(stdz_name("Hunter Morris"))
    print(stdz_name("Hunter Morris "))
    print(stdz_name("MORRIS, H. a"))
    print(stdz_name("MORRIS,H."))
    print(stdz_name("H. Morris"))
    print(stdz_name("MORRIS"))
    print(stdz_name("MORRIS "))
    '''
    
    lasts, firsts = stdz_names(n_list)
    
    for i,ln in enumerate(lasts):
        print("Last Name: "+ln + "; First Name: "+firsts[i])
    
    print(stdz_name("HARRIS IV, Daniel ss"))
    aj = "A.J. Lewis"
    print(aj.strip("."))
    print(aj.replace(".",""))
