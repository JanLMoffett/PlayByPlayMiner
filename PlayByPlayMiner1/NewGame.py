# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:21:53 2019

@author: Jan
"""

# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                                  Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
# a game is a single htm doc converted to a soup object with open_soup function
class Game:
    #__________________________________________________________________________
    def __init__(self, soup_obj):
        self.gamesoup = soup_obj
        #self.panel = soup_obj.find_all("section", class_="panel")[1]
        self.tablebodies = soup_obj.find_all("section", class_="panel")[1].find_all("tbody")
        
        self.gameid = "" #do i need this?  i think it's taken care of in SoupChef
        
        self.awaypositions = []
        self.homepositions = []
        self.awaynames = []
        self.homenames = []
        self.awaystartsub = []
        self.homestartsub = []
        
        self.paunits = []
        self.paside = []
        self.paunitids = []
        
        # set with get_game_info
        self.date = "" # '3/15/2019'
        self.starttime = "" # '6:02 pm'
        self.duration = "" # '2:34'
        self.attendance = "" # '3060'
        self.site = "" # 'Auburn, Ala. (Plainsman Park)'
        self.weather = "" # '61, mostly cloudy'
        self.umpires = "" # 'Home Plate: Gregory StreetFirst: Jeff GosneySecond Base: Christopher GriffinThird Base: Keith Sanders'
        
        # set with get_month_day_year using self.date
        self.month = ""
        self.day = ""
        self.year = ""
        
        # set with get_game_site
        self.city = ""
        self.state = ""
        self.park = ""
        
        #set with get_day_night
        self.daynight = "night"
        
        
    #__________________________________________________________________________    
    def get_game_info(self):
        info_table = ['Date','Start','Time','Attendance','Site','Weather','Umpires']
        info_list = ["NA", "NA", "NA", "NA", "NA", "NA", "NA"]
        
        dt1 = self.gamesoup.find("aside", class_ = "game-details").find_all("dt")
        dd1 = self.gamesoup.find("aside", class_ = "game-details").find_all("dd")
        
        dt2 = []
        dd2 = []
        
        #print("dt:")
        for d in dt1:
            dt2.append(ascii(d.string).strip("'"))
            #print(ascii(d.string).strip("'"))
            #print()
        #print()
        
        #print("dd:")
        for d in dd1:
            ts = ascii(d.string).strip("'")
            ts = ts.replace(",","")
            dd2.append(ts)
            #print(ascii(d.string).strip("'"))
            #print()
        #print()
        
        #make sure dt2 and dd2 are same length
        #if not, look for notes in dt2 and remove corresponding extra dd2 element
        while len(dt2) < len(dd2):
            for i,d in enumerate(dt2):
                if d == "Notes":
                    del dd2[i]
                    break
        
        #outer loop: info_table and info_list
        #inner loop: dt and dd tags from html file
        #['Date','Start','Time','Attendance','Site','Weather','Umpires']
        for i,v in enumerate(info_table):
            for j,t in enumerate(dt2):
                #check for match between info_table and dt2
                if t == v:
                    #put data in info_list
                    info_list[i] = dd2[j]
                    break
                
        self.date = info_list[0]
        self.starttime = info_list[1]
        self.duration = info_list[2]
        self.attendance = info_list[3]
        self.site = info_list[4]
        self.weather = info_list[5]
        self.umpires = info_list[6]
    #__________________________________________________________________________    
    def get_month_day_year(self):
        #'3/15/2019'
        self.month = self.date[0:self.date.find("/")]
        self.day = self.date[self.date.find("/")+1:self.date.find("/",self.date.find("/")+1)]
        self.year = self.date[self.date.find("/",self.date.find("/")+1)+1:]
    
    #__________________________________________________________________________    
    def get_game_site(self):
        #break site into city, state, and park
        
        city = self.site[0:self.site.rfind(" ", 0,self.site.find("(")-1)]
        city = city.strip()
        city = city.replace(".", "")
        self.city = city
        
        state = self.site[self.site.rfind(" ", 0,self.site.find("(")-1) + 1 : self.site.find("(")]
        state = state.strip()
        state = state.replace(".", "")
        self.state = state
        
        self.park = self.site[self.site.find("(")+1:self.site.find(")")]
    
    #__________________________________________________________________________    
    def get_game_duration(self):
        #convert hr:min to total min
        hr = int(self.duration[0])
        m = int(self.duration[3:])
        
        tm = hr*60 + m
        
        self.duration = str(tm)
    #__________________________________________________________________________
    def get_day_night(self):
        
        if "am" in self.starttime.lower():
            self.daynight = "day"
        elif int(self.starttime[0:self.starttime.find(":")]) < 5 or int(self.starttime[0:self.starttime.find(":")]) > 11:
            self.daynight = "day"
    
    #__________________________________________________________________________    
    def get_game_id(self):
        #need some way of getting the away team id and home team id
        
        self.gameid = self.month.zfill(2) + self.day.zfill(2) + self.year
    #__________________________________________________________________________    
    def get_lineup_positions(self):
        
        APL = []
        HPL = []
        
        away_pos_list = self.tablebodies[0].find_all("td", class_="text-uppercase hide-on-small-down")
        for n in away_pos_list:
            #print(n.string)
            APL.append(n.string)
        #print()
        
        #print("AwayPosList:")
        #print(APL)  
        
        home_pos_list = self.tablebodies[1].find_all("td", class_="text-uppercase hide-on-small-down")
        for n in home_pos_list:
            #print(n.string)
            HPL.append(n.string)
        #print()
        
        #print("HomePosList:")
        #print(HomePosList)
        
        #set game attributes   
        self.awaypositions = APL
        self.homepositions = HPL
        
    #__________________________________________________________________________
    def get_lineup_names(self):
        
        away_list1 = self.tablebodies[0].find_all("th", scope = "row")
        ANL = []
        AwayNameList = []
        AwayStarterSub = []
        
        home_list1 = self.tablebodies[1].find_all("th", scope = "row")
        HNL = []
        HomeNameList = []
        HomeStarterSub = []
        
        for n in away_list1:
            ctents = n.contents
            for c in ctents:
                if "span" in str(c):
                    continue
                else:
                    if "<" in str(c):
                        ts = str(c)
                        ANL.append(ts[ts.find(">")+1:ts.find("<",ts.find(">")+1)])
                    else:
                        ANL.append(str(c))
                
        #iterate through Away Name List
        for i,n in enumerate(ANL):
            #look for '\xa0\xa0\xa0\xa0' in previous position
            if i>0:
                #skip over blank lines
                if n == '\xa0\xa0\xa0\xa0':
                    continue
                #names after blank lines are added to sub list
                elif ANL[i-1] == '\xa0\xa0\xa0\xa0':
                    AwayStarterSub.append("sub")
                    AwayNameList.append(n)
                    continue
            #names not after blank lines are added to starter list
            AwayStarterSub.append("starter")
            AwayNameList.append(n)
          
        for n in home_list1:
            ctents = n.contents
            for c in ctents:
                if "span" in str(c):
                    continue
                else:
                    if "<" in str(c):
                        ts = str(c)
                        HNL.append(ts[ts.find(">")+1:ts.find("<",ts.find(">")+1)])
                    else:
                        HNL.append(str(c))
                
        #iterate through Home Name List
        for i,n in enumerate(HNL):
            #look for '\xa0\xa0\xa0\xa0' in previous position
            if i>0:
                #skip over blank lines
                if n == '\xa0\xa0\xa0\xa0':
                    continue
                #names after blank lines are added to sub list
                elif HNL[i-1] == '\xa0\xa0\xa0\xa0':
                    HomeStarterSub.append("sub")
                    HomeNameList.append(n)
                    continue
            #names not after blank lines are added to starter list
            HomeStarterSub.append("starter")
            HomeNameList.append(n)
        
        #set game attributes    
        self.awaynames = AwayNameList
        self.homenames = HomeNameList
        
        self.awaystartsub = AwayStarterSub
        self.homestartsub = HomeStarterSub
    #__________________________________________________________________________    
    def get_action_units(self):
        
        #find all play by play tables in html
        tb = self.gamesoup.find_all("table", class_="sidearm-table play-by-play")
        
        #whole set of play by play tables appears twice
        #find total number of tables and only store half of them
        num_half_innings = len(tb) / 2
    
        for i,t in enumerate(tb):
            
            if i >= num_half_innings:
                break
            
            th = t.find_all("th", scope = "row", string=True)
            #print("i = "+str(i))
            for j,h in enumerate(th):
                ah = ""
                if i%2 == 0:
                    ah = "AWAY"
                else:
                    ah = "HOME"
                    
                self.paside.append(ah)
                
                #print("pa_unit_id:")
                #print("PA"+ str(i+1).zfill(2) + ah +  str(j+1).zfill(2))
                
                self.paunitids.append("PA"+ str(i+1).zfill(2) + ah + str(j+1).zfill(2))
                
                un = ascii(h.string).replace("'","")
                #un = un.strip("\"")
                self.paunits.append(un)
                #print("j = "+str(j))
                #print(ascii(h.string).strip("'"))
            #print()
    #__________________________________________________________________________
    def do_stuff(self):
        self.get_game_info()
        self.get_month_day_year()
        self.get_game_id()
        self.get_game_site()
        self.get_game_duration()
        self.get_day_night()
        
        self.get_lineup_positions()
        self.get_lineup_names()
        
        self.get_action_units()
    #__________________________________________________________________________    
    def print_stuff(self):
        print("Month: " + self.month + "; Day: " + self.day + "; Year: "+self.year)
        print("Attendance: " + self.attendance + "; Start Time: " + self.starttime + "; Day/Night: " + self.daynight + "; Duration: " + self.duration)
        print("Site: " + self.site + "; Umpires: " + self.umpires + "; Weather: " + self.weather)
        print("City: "+self.city + "; State: "+self.state+"; Park: "+self.park)
        print()
        print("-------------Away Team Players-------------")
        for i,n in enumerate(self.awaynames):
            print("Name:", n, end = "; ")
            print("Position:", self.awaypositions[i], end = "; ")
            print("Starter/Sub:", self.awaystartsub[i])
        print()
        print("-------------Home Team Players-------------")
        for i,n in enumerate(self.homenames):
            print("Name:", n, end = "; ")
            print("Position:", self.homepositions[i], end = "; ")
            print("Starter/Sub:", self.homestartsub[i])
        print()
        print("Plate Appearance Units:")
        for i,u in enumerate(self.paunits):
            print("Side: " + self.paside[i] + "; PA Unit ID: " + self.paunitids[i])
            print(u)
            
    #__________________________________________________________________________


    
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
#                               Close Game Class
# % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %





