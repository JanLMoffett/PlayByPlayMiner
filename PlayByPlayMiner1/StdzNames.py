"""Name Standardizing Module

@author: Jan L. Moffett | janlmoffett@gmail.com

This module contains the following functions:
    * last_first - returns last name, first name in proper case
    * last_only - returns last name in proper case
    * first_only - returns first name in proper case
    * lasts_firsts - returns list of last names, list of first names 
        in proper case
    * lasts_only - returns list of last names in proper case
    * firsts_only - returns list of first names in proper case
"""

def last_first(name_string):
    """processes raw name string and returns names (last, first) in proper case
    
    Args:
        name_string: a raw, unstandardized string containing a name
        
    Returns:
        ln: last name in proper case
        fn: first name in proper case
    """
    
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
    """processes raw name string and returns last name in proper case
    
    Args:
        name_string: an unstandardized string containing a name
        
    Returns:
        ln: last name in proper case
    """
    
    ln,fn = last_first(name_string)
    return ln
#------------------------------------------------------------------------------
def first_only(name_string):
    """processes raw name string and returns first name in proper case
    
    Args:
        name_string: an unstandardized string containing a name
        
    Returns:
        fn: first name in proper case
    """
    
    ln,fn = last_first(name_string)
    return fn
#------------------------------------------------------------------------------   
def lasts_firsts(name_list):
    """takes list of strings and returns lists of last names and first names in proper case
    
    Args:
        name_list: a list of raw, unstandardized strings containing names
        
    Returns:
        lns: list of last names in proper case
        fns: list of first names in proper case
    """
    
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
    """takes list of raw name strings and returns list of first names in proper case
    
    Args:
        name_list: a list of raw, unstandardized strings containing names
        
    Returns:
        lns: list of last names in proper case
    """
    
    lns,fns = lasts_firsts(name_list)
    
    return lns
#------------------------------------------------------------------------------
def firsts_only(name_list):
    """takes list of raw name strings and returns list of last names in proper case
    
    Args:
        name_list: a list of raw, unstandardized strings containing names
        
    Returns:
        fns: list of first names in proper case
    """
    
    lns,fns = lasts_firsts(name_list)
    
    return fns
#------------------------------------------------------------------------------