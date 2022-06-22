
setwd("C:/Users/Jan/Desktop/Scrape/Output/SEC/available datasets/")

#batting dataset
bat <- read.csv("batting_w_id.csv")
#fixing column name
names(bat)[1] <- "PlayerID"
#columns names
names(bat)

#baserunning dataset
br <- read.csv("baserunning_w_id.csv")
#fixing column names
names(br)[1] <- "PlayerID"
#column names
names(br)

#plate appearances dataset
pa <- read.csv("plate_appearances.csv")
#fixing column name
names(pa)[1] <- "Sequence"
#column names
names(pa)

#?merge

#sorting datasets by PlateAppID
bat1 <- bat[order(bat$PlateAppID),]
br1 <- br[order(br$PlateAppID),]
pa1 <- pa[order(pa$PlateAppID),]

#**********************merging mini datasets*************************
#making mini datasets to test merging code, using first 50 rows of datasets
bat.a <- bat1[1:50,]
br.a <- br1[1:50,]
pa.a <- pa1[1:50,]
m1 <- merge(pa.a, bat.a, by = "PlateAppID")
m2 <- merge(pa.a, br.a, by="PlateAppID")

#**********************merging big datasets*************************

#dividing br dataset by base
br1.first <- br1[which(br1$StartBase == 1), ]
br1.second <- br1[which(br1$StartBase == 2), ]
br1.third <- br1[which(br1$StartBase == 3), ]

#merging baserunning sets
#br1.second_third <- merge(br1.second, br1.third, by = "PlateAppID", all = TRUE)
#br1.first_second_third <- merge(br1.first, br1.second_third, by = "PlateAppID", all = TRUE)

#bat1.br <- merge(bat1, br1.first_second_third, by = "PlateAppID", all = TRUE)
#pa.batbr <- merge(pa1, bat1.br, by = "PlateAppID", all = TRUE)

#ouputting csv of big merged dataset
#write.csv(pa.batbr, "bigMerge1.csv")

#things were a little weird, need to be more careful when merging
#**********************merging big datasets*************************
#are there any duplicate PlateAppID's in pa dataset?
length(pa1$PlateAppID)
#16986
length(unique(pa1$PlateAppID))
#16986

#how many brunits in set?
length(br1$PlateAppID)
#6903

#how many unique PlateAppID's in br set?
length(unique(br1$PlateAppID))
#5038

#number of onfirst in set
sum(br1$StartBase == 1)
#3692

#number of onsecond in set
sum(br1$StartBase == 2)
#1901

#number of onthird in set
sum(br1$StartBase == 3)
#916

3692 + 1901 + 916
#6509

#number of brunits where startbase is 0
sum(br1$StartBase == 0)
#394

6903 - 6509 
#394

#subsets for each base
brfirst <- br1[which(br1$StartBase == 1),]
brsecond <- br1[which(br1$StartBase == 2),]
brthird <- br1[which(br1$StartBase == 3),]

#there shouldn't be dupe plateappid's in these datasets 
length(brfirst$PlateAppID)
#3692
length(unique(brfirst$PlateAppID))
#3606

3692-3606 #86

length(brsecond$PlateAppID)
#1901
length(unique(brsecond$PlateAppID))
#1887

1901-1887 #14

length(brthird$PlateAppID)
#916
length(unique(brthird$PlateAppID))
#915



#finding duplicates in onthird
dupes <- rep(FALSE, length(brthird$PlateAppID))
for(i in 2:length(brthird$PlateAppID)){
  
  #if plateappid matches row above, enter TRUE in dupes vector
  if(brthird$PlateAppID[i] == brthird$PlateAppID[i-1]){
    dupes[i] = TRUE
    dupes[i-1] = TRUE
    
  }
}

#look at duped rows from dataset to see what's going on
d3 <- brthird[which(dupes == TRUE),]

#this one is fine, just two runners with same last name


#finding duplicates in onsecond
dupes <- rep(FALSE, length(brsecond$PlateAppID))
for(i in 2:length(brsecond$PlateAppID)){
  
  #if plateappid matches row above, enter TRUE in dupes vector
  if(brsecond$PlateAppID[i] == brsecond$PlateAppID[i-1]){
    dupes[i] = TRUE 
    dupes[i-1] = TRUE
    
  }
}

#look at duped rows from dataset to see what's going on
d2 <- brsecond[which(dupes == TRUE),]



#finding duplicates in onfirst
dupes <- rep(FALSE, length(brfirst$PlateAppID))
for(i in 2:length(brfirst$PlateAppID)){
  
  #if plateappid matches row above, enter TRUE in dupes vector
  if(brfirst$PlateAppID[i] == brfirst$PlateAppID[i-1]){
    dupes[i] = TRUE 
    dupes[i-1] = TRUE
    
  }
}

#look at duped rows from dataset to see what's going on
d1 <- brfirst[which(dupes == TRUE),]



