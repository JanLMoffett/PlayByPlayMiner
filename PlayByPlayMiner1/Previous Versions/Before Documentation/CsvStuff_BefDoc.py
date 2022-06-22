# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:18:31 2019

@author: Jan
"""

# function to take a list and print elements as row of csv ~~~~~~~~~~~~~~~~~~~~   
def csv_print(some_list):
    r = ""
    for i,a in enumerate(some_list):
        if i == len(some_list)-1:
            s = str(a)
            r += (s)
            break
            
        s = str(a)
        r += (s + ",")
        
        
    print(r)
# close csv_print function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------
# function to make a csv header ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#takes list of variable names and returns string in csv format
def make_csv_header(var_list):
    r = ""
    
    for i,s in enumerate(var_list):
        if i == len(var_list)-1:
            r += s
            break
        r += (s + ",")
    
    return r    
# close make_csv_header ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------   
# function to take a list and return string with elements as row of csv ~~~~~~~
def make_csv_row(data_list):
    r = ""

    for i,a in enumerate(data_list):
        if i == len(data_list)-1:
            r += str(a)
            break
        r += (str(a) + ",")
        
    return r
# close make_csv_row function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#------------------------------------------------------------------------------       
#this function creates a new csv file and writes the header of variable names to it
def make_csv_file(file_name, header_string):
    file = open(file_name,"w")
    file.write(header_string + "\n")
    file.close()
#------------------------------------------------------------------------------
#this function adds a row of data to an existing csv file       
def add_row_csv_file(file_name, csv_row_string):
    file = open(file_name,"a")
    file.write(csv_row_string + "\n")
    file.close()
#------------------------------------------------------------------------------   
    
    
def test():
    
    header1 = "Name,Team,Balls,Strikes,Hit,Walk,K"
    name1 = "test060219.csv"
    obs_list1 = ["Cargo","Away","3","1","0","1","0"]
    obs_list2 = ["Bongo","Away","2","2","1","0","0"]
    obs_list3 = ["Jim","Home","0","2","0","0","1"]
    
    make_csv_file(name1, header1)
    csv_row1 = csv_string(obs_list1)
    csv_row2 = csv_string(obs_list2)
    csv_row3 = csv_string(obs_list3)
    add_row_csv_file(name1,csv_row1)
    add_row_csv_file(name1,csv_row2)
    add_row_csv_file(name1,csv_row3)
   
    
