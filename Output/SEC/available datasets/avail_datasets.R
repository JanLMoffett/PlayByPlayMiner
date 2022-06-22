setwd("C:/Users/Jan/Desktop/Scrape/Output/SEC/available datasets/")

#batting dataset
bat <- read.csv("batting_id.csv")
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
#bat.a <- bat1[1:50,]
#br.a <- br1[1:50,]
#pa.a <- pa1[1:50,]
#m1 <- merge(pa.a, bat.a, by = "PlateAppID")
#m2 <- merge(pa.a, br.a, by="PlateAppID")

#**********************merging big datasets*************************

#dividing br dataset by base
#br1.first <- br1[which(br1$StartBase == 1), ]
#br1.second <- br1[which(br1$StartBase == 2), ]
#br1.third <- br1[which(br1$StartBase == 3), ]

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
#6886

#how many unique PlateAppID's in br set?
length(unique(br1$PlateAppID))
#5038

#number of onfirst in set
sum(br1$StartBase == 1)
#3608

#number of onsecond in set
sum(br1$StartBase == 2)
#1888

#number of onthird in set
sum(br1$StartBase == 3)
#921

#number of brunits where startbase is 0
sum(br1$StartBase == 0)
#469

3608 + 1888 + 921 + 469
#6886 - good

#subsets for each base
brfirst <- br1[which(br1$StartBase == 1),]
brsecond <- br1[which(br1$StartBase == 2),]
brthird <- br1[which(br1$StartBase == 3),]

#there shouldn't be dupe plateappid's in these datasets 
length(brfirst$PlateAppID)
#3608
length(unique(brfirst$PlateAppID))
#3608

length(brsecond$PlateAppID)
#1888
length(unique(brsecond$PlateAppID))
#1888

length(brthird$PlateAppID)
#921
length(unique(brthird$PlateAppID))
#921

#finding duplicates in onthird
#dupes <- rep(FALSE, length(brthird$PlateAppID))
#for(i in 2:length(brthird$PlateAppID)){
  
  #if plateappid matches row above, enter TRUE in dupes vector
  #if(brthird$PlateAppID[i] == brthird$PlateAppID[i-1]){
   # dupes[i] = TRUE
    #dupes[i-1] = TRUE
    
  #}
#}

#look at duped rows from dataset to see what's going on
#d3 <- brthird[which(dupes == TRUE),]

#this one is fine, just two runners with same last name


#finding duplicates in onsecond
#dupes <- rep(FALSE, length(brsecond$PlateAppID))
#for(i in 2:length(brsecond$PlateAppID)){
  
  #if plateappid matches row above, enter TRUE in dupes vector
#  if(brsecond$PlateAppID[i] == brsecond$PlateAppID[i-1]){
#    dupes[i] = TRUE 
#    dupes[i-1] = TRUE
    
#  }
#}

#look at duped rows from dataset to see what's going on
#d2 <- brsecond[which(dupes == TRUE),]



#finding duplicates in onfirst
#dupes <- rep(FALSE, length(brfirst$PlateAppID))
#for(i in 2:length(brfirst$PlateAppID)){
  
  #if plateappid matches row above, enter TRUE in dupes vector
#  if(brfirst$PlateAppID[i] == brfirst$PlateAppID[i-1]){
#    dupes[i] = TRUE 
#    dupes[i-1] = TRUE
    
#  }
#}

#look at duped rows from dataset to see what's going on
#d1 <- brfirst[which(dupes == TRUE),]

#outputting d1 to keep track of repairs
#write.csv(d1, "d1b.csv")


#merging onthird and on second
dim(brsecond) #1888, 22
dim(brthird) #921, 22

br_second_third <- merge(brsecond, brthird, by="PlateAppID", all = T)
dim(br_second_third)
#2351, 43

br_first_second_third <- merge(brfirst, br_second_third, by="PlateAppID", all = T)
dim(br_first_second_third)
#4721, 64

#any dupe plateappid's in batting dataset?
length(bat1$PlateAppID)
#16046

length(unique(bat1$PlateAppID))
#16046

#finding duplicates in bat1
#p <- rep(FALSE, length(bat1$PlateAppID))
#for(i in 2:length(bat1$PlateAppID)){

  #if plateappid matches row above, enter TRUE in dupes vector
  #if(bat1$PlateAppID[i] == bat1$PlateAppID[i-1]){
    #p[i] = TRUE 
    #p[i-1] = TRUE

  #}
#}

#sum(p)

#look at duped rows from dataset to see what's going on
#batdupes <- bat1[which(p == TRUE),]

#outputting db to keep track of repairs
#write.csv(batdupes, "batdupes.csv")

#merge batting and baserunning datasets
bat_br <- merge(bat1, br_first_second_third, by = "PlateAppID", all = T)

length(bat_br$PlateAppID)
length(unique(bat_br$PlateAppID))

#merge batting, baserunning, and pa datasets
length(pa1$PlateAppID)
length(unique(pa1$PlateAppID))

#4 pa id's without batting

big <- merge(pa1, bat_br, by = "PlateAppID", all = T)

tail(big)

#outputting big dataset
write.csv(big, "BigMerge.csv")
