"""Base-out Coding Module

@author: Jan L. Moffett | janlmoffett@gmail.com

This module contains the following functions:
    * get_base_state - returns alpha code for baserunning configuration
    * get_base_out_state - returns alpha-numeric code for baserunning and outs
"""

#--------------------------------------------------------------------------   
def get_base_state(on_first, on_second, on_third):
    """Returns alpha code for base state given runners
    
    Codes and corresponding base configurations:
    'A' = ___; 'B' = __1; 'C' = _2_; 'D' = 3__; 
    'E' = _21; 'F' = 3_1; 'G' = 32_; 'H' = 321
    
    Args:
        on_first: a string indicating runner name or NA if base is empty
        on_second: a string indicating runner name or NA if base is empty
        on_third: a string indicating runner name or NA if base is empty
        
    Returns:
        A string of length 1 in the range {'A','B','C',...,'H'}
    """
    
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
    """Returns alpha-numeric code for base-out state given runners and outs
    
    Codes and corresponding base configurations:
    'A0', 'A1', 'A2', 'A3' = ___ | 0, 1, 2, 3 outs
    'B0', 'B1', 'B2', 'B3' = __1 | 0, 1, 2, 3 outs
    'C0', 'C1', 'C2', 'C3' = _2_ | 0, 1, 2, 3 outs
    'D0', 'D1', 'D2', 'D3' = 3__ | 0, 1, 2, 3 outs
    'E0', 'E1', 'E2', 'E3' = _21 | 0, 1, 2, 3 outs
    'F0', 'F1', 'F2', 'F3' = 3_1 | 0, 1, 2, 3 outs
    'G0', 'G1', 'G2', 'G3' = 32_ | 0, 1, 2, 3 outs
    'H0', 'H1', 'H2', 'H3' = 321 | 0, 1, 2, 3 outs
    
    Args:
        outs: an int or a string in range [0,3] indicating number of outs
        on_first: a string indicating runner name or 'NA' if base is empty
        on_second: a string indicating runner name or 'NA' if base is empty
        on_third: a string indicating runner name or 'NA' if base is empty
        
    Returns:
        A string of length 2 in the range {'A0',...,'A3',...,'H0',...,'H3'}
    """
    
    bs = get_base_state(on_first, on_second, on_third)
    
    return bs + str(outs)
#--------------------------------------------------------------------------
        
        
        