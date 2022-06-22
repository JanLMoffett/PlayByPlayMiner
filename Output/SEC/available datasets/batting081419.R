setwd("C:/Users/Jan/Desktop/Scrape/Output/SEC/available datasets/")
library(stringr)

#whole dataset
d <- read.csv("SEConly2019.csv")
str(d)

#batting part of dataset
b <- d[,1:55]

#how many rows with BatterID == NA?
length(which(is.na(b$BatterID))) 
#942

#removing rows with no batter
b <- b[-which(is.na(b$BatterID)),]

#variables in b dataset
names(b)
#[1] "PlateAppID"        "GameID"            "NumComponents"    
#[4] "startOuts"         "startOnFirst"      "startOnSecond"    
#[7] "startOnThird"      "startBaseState"    "startBaseOutState"
#[10] "endOuts"           "endOnFirst"        "endOnSecond"      
#[13] "endOnThird"        "endBaseState"      "FinalBaseOutState"
#[16] "TotalRPrime"       "R"                 "BatterID"         
#[19] "HomeAway.x"        "BatterName"        "BatterHole"       
#[22] "CountBalls"        "CountStrikes"      "BIP"              
#[25] "H"                 "Bases"             "Singles"          
#[28] "Doubles"           "Triples"           "HR"               
#[31] "HitLocation"       "HitQuality"        "HitType"          
#[34] "INFH"              "FieldOut"          "FOLocation"       
#[37] "FOQuality"         "FOType"            "DP"               
#[40] "DPType"            "Reach"             "RBOE"             
#[43] "FC"                "SAC"               "SF"               
#[46] "BB"                "IBB"               "UBB"              
#[49] "SO"                "KSwing"            "KLook"            
#[52] "UCTS"              "SOReach"           "HBP"              
#[55] "TrueOutcome"

unique(b$BatterID)

#sorting b by batterid
b <- b[order(b$BatterID, decreasing = F),]




