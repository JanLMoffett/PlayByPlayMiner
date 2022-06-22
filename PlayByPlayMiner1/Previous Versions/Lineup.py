# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:25:11 2019
@author: Jan
"""
import StdzNames
import CsvStuff
pos = ["dh","p","c","1b","2b","3b","ss","lf","cf","rf"]
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                                 Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
class Lineup:
    #--------------------------------------------------------------------------
    def __init__(self, away_starter_list, away_sub_list, home_starter_list, home_sub_list, game_id):
        self.gameid = game_id
        self.awaystarters = away_starter_list
        self.awaysubs = away_sub_list
        self.homestarters = home_starter_list
        self.homesubs = home_sub_list
        
        self.awaylastnames = []
        self.awayfirstnames = []
        self.homelastnames = []
        self.homefirstnames = []
        
        self.awayposorder = []
        self.homeposorder = []
        
        self.homeoffsubs = [] #substitute position players
        self.homerelievers = []
        
        self.awayoffsubs = [] #substitute position players
        self.awayrelievers = []
        
    #--------------------------------------------------------------------------
    # function to put starters in list in order of position
    def get_pos_order(self):
        #takes a list of strings in format: KERR, Ryland 2b
        #returns list of ten names
        
        away_pos_order = [""]*10 # 0 will be DH
        home_pos_order = [""]*10 # 0 will be DH
        
        #read last two chars in string
        for i,s in enumerate(self.awaystarters):
            for j,t in enumerate(pos):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                    last_name = StdzNames.last_only(s)
                    away_pos_order[j] = last_name
                    
        #read last two chars in string
        for i,s in enumerate(self.homestarters):
            for j,t in enumerate(pos):
                if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[j]:
                    last_name = StdzNames.last_only(s)
                    home_pos_order[j] = last_name
                    
        away_pos_dict = {"DesignatedHitter":away_pos_order[0],"StartingPitcher":away_pos_order[1],"Catcher":away_pos_order[2],"FirstBaseman":away_pos_order[3],"SecondBaseman":away_pos_order[4],"ThirdBaseman":away_pos_order[5],"ShortStop":away_pos_order[6],"LeftFielder":away_pos_order[7],"CenterFielder":away_pos_order[8],"RightFielder":away_pos_order[9]}
        home_pos_dict = {"DesignatedHitter":home_pos_order[0],"StartingPitcher":home_pos_order[1],"Catcher":home_pos_order[2],"FirstBaseman":home_pos_order[3],"SecondBaseman":home_pos_order[4],"ThirdBaseman":home_pos_order[5],"ShortStop":home_pos_order[6],"LeftFielder":home_pos_order[7],"CenterFielder":home_pos_order[8],"RightFielder":home_pos_order[9]}        
        
        self.awayposorder = away_pos_order
        self.homeposorder = home_pos_order
        
        return away_pos_dict, home_pos_dict
    
    #--------------------------------------------------------------------------        
    #--------------------------------------------------------------------------
    def get_all_names(self):
        awaynames = self.awaystarters + self.awaysubs
        homenames = self.homestarters + self.homesubs
        
        self.awaylastnames, self.awayfirstnames = StdzNames.lasts_firsts(awaynames)
        self.homelastnames, self.homefirstnames = StdzNames.lasts_firsts(homenames)
    #--------------------------------------------------------------------------        
    def get_subs(self, pos_num):
        asl = self.awaysubs
        hsl = self.homesubs
        
        a_pos_subs = []
        h_pos_subs = []
        
        #check for starter with a / in the string
        for s in self.awaystarters:
            if s.find('/') != -1:
                asl.append(s)    
            
        for s in asl:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[pos_num]:
                a_pos_subs.append(s)
                
        #check for starter with a / in the string
        for s in self.homestarters:
            if s.find('/') != -1:
                hsl.append(s)    
            
        for s in hsl:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == pos[pos_num]:
                h_pos_subs.append(s)
                
        aps = StdzNames.lasts_only(a_pos_subs)
        hps = StdzNames.lasts_only(h_pos_subs)
        
                
        return aps, hps
    #close get_subs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    #--------------------------------------------------------------------------        
    # function to get list of relief pitchers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_relievers(self):
        
        away_relievers, home_relievers = self.get_subs(1)   
    
        return away_relievers, home_relievers      
    # close get_relievers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 
    #--------------------------------------------------------------------------
    
    # function to get list of pinch hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_pinch_hitters(self):
        away_pinch_hitters = []
        home_pinch_hitters = []
        
        for s in self.awaysubs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
                away_pinch_hitters.append(s)
                
        for s in self.homesubs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "ph":
                home_pinch_hitters.append(s)
                
        aph = StdzNames.lasts_only(away_pinch_hitters)
        hph = StdzNames.lasts_only(home_pinch_hitters)
                
        return aph, hph
    # close get_pinch_hitters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #--------------------------------------------------------------------------    
    # function to get list of pinch runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_pinch_runners(self):
        
        away_pinch_runners = []
        home_pinch_runners = []
        
        for s in self.awaysubs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
                away_pinch_runners.append(s)
                
        for s in self.homesubs:
            if s[s.rfind(" ")+1:s.rfind(" ")+3] == "pr":
                home_pinch_runners.append(s)
                
        apr = StdzNames.lasts_only(away_pinch_runners)
        hpr = StdzNames.lasts_only(home_pinch_runners)
                
        return apr, hpr
    # close get_pinch_runners ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_off_subs(self):
        aos = []
        hos = []
        for s in self.awaysubs:
            if s[s.rfind(" ")+1:] != "p":
                aos.append(StdzNames.last_only(s))
        for s in self.homesubs:
            if s[s.rfind(" ")+1:] != "p":
                hos.append(StdzNames.last_only(s))
        
        return aos,hos
    #--------------------------------------------------------------------------
    # function to get a list of starters in batting order
    def get_batting_orders(self): #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        away_bo = []
        home_bo = []
        
        for s in self.awaystarters:
            if s[s.rfind(" ")+1:] != "p":
                away_bo.append(StdzNames.last_only(s))
                
        for s in self.homestarters:
            if s[s.rfind(" ")+1:] != "p":
                home_bo.append(StdzNames.last_only(s))
        
        return away_bo, home_bo
    #close get_batting_order ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    
    #want dataset to contain: GameID, Home/Away, last name, first name, pos1, pos2, starter/sub
    def get_lineup_data(self):
        
        gid = self.gameid
        finame = "C:/Users/Jan/Desktop/Scrape/Output/G"+gid+"_lineup.csv"
        header = "GameID,AwayHome,LastName,FirstName,Pos1,Pos2,StarterSub"
        CsvStuff.make_csv_file(finame, header)
        
        #away team
        for s in self.awaystarters:
            lnm, fnm = StdzNames.last_first(s)
            pos = s[s.rfind(" ")+1:]
            #if there is a slash in the position
            if pos.find('/')>0:
                pos1 = pos[:pos.find('/')]
                pos2 = pos[pos.find('/')+1:]
            else:
                pos1 = pos
                pos2 = "NA"
            rowlist = [gid,"away",lnm,fnm,pos1,pos2,"starter"]
            rowstr = CsvStuff.make_csv_row(rowlist)
            CsvStuff.add_row_csv_file(finame,rowstr)
        for s in self.awaysubs:
            lnm, fnm = StdzNames.last_first(s)
            pos = s[s.rfind(" ")+1:]
            #if there is a slash in the position
            if pos.find('/')>0:
                pos1 = pos[:pos.find('/')]
                pos2 = pos[pos.find('/')+1:]
            else:
                pos1 = pos
                pos2 = "NA"
            rowlist = [gid,"away",lnm,fnm,pos1,pos2,"sub"]
            rowstr = CsvStuff.make_csv_row(rowlist)
            CsvStuff.add_row_csv_file(finame,rowstr)
        
        #home team
        for s in self.homestarters:
            lnm, fnm = StdzNames.last_first(s)
            pos = s[s.rfind(" ")+1:]
            #if there is a slash in the position
            if pos.find('/')>0:
                pos1 = pos[:pos.find('/')]
                pos2 = pos[pos.find('/')+1:]
            else:
                pos1 = pos
                pos2 = "NA"
            rowlist = [gid,"home",lnm,fnm,pos1,pos2,"starter"]
            rowstr = CsvStuff.make_csv_row(rowlist)
            CsvStuff.add_row_csv_file(finame,rowstr)
        for s in self.homesubs:
            lnm, fnm = StdzNames.last_first(s)
            pos = s[s.rfind(" ")+1:]
            #if there is a slash in the position
            if pos.find('/')>0:
                pos1 = pos[:pos.find('/')]
                pos2 = pos[pos.find('/')+1:]
            else:
                pos1 = pos
                pos2 = "NA"
            rowlist = [gid,"home",lnm,fnm,pos1,pos2,"sub"]
            rowstr = CsvStuff.make_csv_row(rowlist)
            CsvStuff.add_row_csv_file(finame,rowstr)
        
        
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
#                            Close Lineup Class 
# $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
        
def test():
    #dummy data
    AwayStarters = ['JOHNSON, Will lf', 'KERR, Ryland 2b', 'HOWIE, Nick rf', 'BOTSOE, Chris cf', 'LEWIS, A.J. c', 'LUDWICK, Charles dh', 'HARRIS IV, Daniel ss', 'THOMASON, Logan 3b', 'CONKLIN, Corey 1b', 'TEAGUE, Logan p']
    AwaySubs = ['WEAVER, Lyndon pr/dh', 'WILLIAMS, Darren p', 'OCHSENBEIN, Aaron p']
    HomeStarters = ['KERRIGAN, Keith lf', 'EMME, Grant cf', 'MORRIS, Hunter 1b', 'GOVERN, Jimmy 2b', 'PENA, Christian 3b', 'KNERNSCHIELD, Ryan c', 'WAZNIS, Matt dh', 'SWEENEY, Trey ss', 'TESMOND, Tyler rf', 'DEXTER, Spenser p']
    HomeSubs = ['TOPPEL, Dane ph', 'STEVENSON, Alex p']
    
    lu = Lineup(AwayStarters, AwaySubs, HomeStarters, HomeSubs, "20190412")
    
    #Position Dicts
    print("============ Positions ==============")
    print()
    apd, hpd = lu.get_pos_order()
    for i,t in enumerate(apd.items()):
        print(t)
    print()
    for i,t in enumerate(hpd.items()):
        print(t)
    print()
    
    #All Names
    print("============ All Names ==============")
    print()
    lu.get_all_names()
    
    aln = lu.awaylastnames
    afn = lu.awayfirstnames
    
    hln = lu.homelastnames
    hfn = lu.homefirstnames
    
    print("____Away Names: ")
    for i,n in enumerate(aln):
        print(afn[i] + " " + n)
    print()
    
    print("____Home Names: ")
    for i,n in enumerate(hln):
        print(hfn[i] + " " + n)
    print()
    
    print("============ Batting Orders ==============")
    print()
    #Batting Orders
    abo,hbo = lu.get_batting_orders()
    print("____Away Batting Order:")
    print(abo)
    print()
    print("____Home Batting Order:")
    print(hbo)
    print()
    
    print("============ Get Relievers ==============")
    print()    
    arel,hrel = lu.get_relievers()
    print("Away Relievers:")
    print(arel)
    print()
    print("Home Relievers:")
    print(hrel)
    print()
    
    print("============ Get Offensive Subs ==============")
    awaos,homos = lu.get_off_subs()
    print("Away Offensive Subs:")
    print(awaos)
    print()
    print("Home Offensive Subs:")
    print(homos)
    print()
    lu.get_lineup_data()
    
