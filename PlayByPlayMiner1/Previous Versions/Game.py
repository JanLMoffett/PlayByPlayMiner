# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:21:53 2019

@author: Jan
"""
#------------------------------------------------------------------------------
# function to filter newline chars out of a list of strings
def newline_filter(string_list):
    no_nl = []
    for i,s in enumerate(string_list):
        ts = ""
        for j in range(0, len(s)):
            
            if s[j] == '\\':
                ts += ' '
            elif j>0 and s[j-1] == '\\':
                continue
            else:
                ts += s[j]
        no_nl.append(ts)
        
    #build return_list
    return no_nl
#------------------------------------------------------------------------------
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                                  Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
# a game is a single htm doc converted to a soup object with open_soup function
class Game:
    #--------------------------------------------------------------------------
    def __init__(self, soup_obj):
        self.game_soup = soup_obj
        self.game_title = soup_obj.title.string
        self.away_team = self.game_title[0:self.game_title.find(" vs ")]
        self.home_team = self.game_title[self.game_title.find(" vs ") + 4:self.game_title.find("(") - 1]
        self.game_month = self.game_title[self.game_title.find("(")+1:self.game_title.find(" ",self.game_title.find("(")+1)]
        self.game_day = self.game_title[self.game_title.find(" ",self.game_title.find("("))+1:self.game_title.find(",")]
        self.game_year = self.game_title[self.game_title.find(",")+2:self.game_title.find(")")]
    
    #--------------------------------------------------------------------------    
    def get_pbp_strings(self):
        font_strings = []
        pbp_strings = []
        front_off = []
        back_off = []
        
        font = self.game_soup.find_all("font", face = "verdana", size = 2, color="#000000")
        for string in font:
            font_strings.append(string)
          
        for s in font_strings:
            s2 = s.encode("utf8")
            if len(s2) > 100:
                pbp_strings.append(str(s2))
                
        for s in pbp_strings:
            #j for each character in s
            for j in range(len(s)-14):
                #' - </b></font>'
                if s[j:j+14] == ' - </b></font>':
                    front_off.append(s[(j+14) : ]) 
                    
        for s in front_off:
            #j for each character in s
            for j in range(len(s)-4):
                if s[j:(j+6)] == "<i><b>":
                    back_off.append(s[0 : (j-1)])
        
        
        #newline filter
        return_list = newline_filter(back_off)
        return return_list
    
    #--------------------------------------------------------------------------
    # function to get names and positions in lineups, and differentiate between teams, 
    # then between starts and subs
    def get_lineups(self):
        #will return list of away starters and home starters
        lineup_strings = []
        
        lu = self.game_soup.find_all("td", align = "left")
        
        for s in lu:
            lineup_strings.append(str(s.string))
    
        #away team is listed first
        #each team starts with "player" and ends with "totals"
        away = []
        home = []
        
        i = 0
        while lineup_strings[i] != 'Totals\xa0':
            if lineup_strings[i] != 'Player\xa0':
                away.append(lineup_strings[i])
            i += 1
                
        i += 1
        while lineup_strings[i] != 'Totals\xa0':
            if lineup_strings[i] != 'Player\xa0' and lineup_strings[i] != '\xa0\xa0':
                home.append(lineup_strings[i])
            i += 1
        
        away_st = []
        away_su = []
        
        for s in away:
            if s[0] != '\xa0':
                away_st.append(s[:-1])
            else:
                away_su.append(s[3:-1])
        
        home_st = []
        home_su = []
        
        for s in home:
            if s[0] != '\xa0':
                home_st.append(s[:-1])
            else:
                home_su.append(s[3:-1])
        
        return {"away_starters":away_st, "away_subs":away_su, "home_starters":home_st, "home_subs":home_su}
    #--------------------------------------------------------------------------
        
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                               Close Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
