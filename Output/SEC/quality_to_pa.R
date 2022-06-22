

quality_to_pa <- function(infile_name){

require(stringr)

#bring in csv quality file
q <- read.csv(infile_name, quote = "", fill = FALSE)
# =========== ENTER FILENAME ABOVE ^^^^^^^^^^^^^

#remove rows labeled "sub" and "other"
if("sub" %in% q$AUType){
  q <- q[-which(q$AUType == "sub"),]
}
if("other" %in% q$AUType){
  q <- q[-which(q$AUType == "other"),]
}  
  
#delete unneeded columns
q <- q[,-4:-3]


#column names
#names(q)
#[1] "GameID"            "PlateAppID"        "startOuts"        
#[4] "startOnFirst"      "startOnSecond"     "startOnThird"     
#[7] "startBaseState"    "startBaseOutState" "endOuts"          
#[10] "endOnFirst"        "endOnSecond"       "endOnThird"       
#[13] "endBaseState"      "endBaseOutState"   "RPrime"        

#make a vector of unique PlateAppID's
PlateAppID <- unique(as.character(q$PlateAppID))
#w has a row for each unique PA in w dataframe
numrows <- length(PlateAppID)

#vectors for w
GameID <- rep(q$GameID[1],numrows)
startOuts <- rep(NA,numrows)
startOnFirst <- rep("NA",numrows)
startOnSecond <- rep("NA",numrows)
startOnThird <- rep("NA",numrows)
startBaseState <- rep("NA",numrows)
startBaseOutState <- rep("NA",numrows)
endOuts <- rep(NA,numrows)
endOnFirst <- rep("NA",numrows)
endOnSecond <- rep("NA",numrows)
endOnThird <- rep("NA",numrows)
endBaseState <- rep("NA",numrows)
FinalBaseOutState <- rep("NA",numrows)
#needs to be calculated:
TotalRPrime <- rep(NA,numrows)

#add these columns after w is finished:
Sequence <- rep(NA,numrows)         #
#fill Sequence vector               #
for(i in seq_along(Sequence)){      #
  Sequence[i] = i                   #        
}                                   #
                                    #
R <- rep(NA,numrows)                #
#####################################

#iterate through unique pa vector and count num components for each value
NumComponents <- rep(NA,numrows)
for (i in seq_along(PlateAppID)){
  NumComponents[i] = length(which(q$PlateAppID == PlateAppID[i]))
}

#create new data frame for plate_appearances table in database
w <- data.frame(GameID,PlateAppID,NumComponents)

#iterate through w looking at NumComponents
for(i in seq_along(w$PlateAppID)){
#for(i in seq_len(5)){ #first 5 only for testing
  paid <- w$PlateAppID[i]
  
  #when 1 component, copy info to w vectors
  if(w$NumComponents[i] == 1){
    t <- q[which(q$PlateAppID == as.character(paid)),]
    
    TotalRPrime[i] <- t$RPrime[1]
    
    #store startOuts, startOnFirst, startOnSecond, ... from first row in temp df
    startOuts[i] <- t$startOuts[1]
    startOnFirst[i] <- as.character(t$startOnFirst[1])
    startOnSecond[i] <- as.character(t$startOnSecond[1])
    startOnThird[i] <- as.character(t$startOnThird[1])
    startBaseState[i] <- as.character(t$startBaseState[1])
    startBaseOutState[i] <- as.character(t$startBaseOutState[1])
    
    #store endOuts, endOnFirst, endOnSecond, ... from last row in temp df
    endOuts[i] <- t$endOuts[1]
    endOnFirst[i] <- as.character(t$endOnFirst[1])
    endOnSecond[i] <- as.character(t$endOnSecond[1])
    endOnThird[i] <- as.character(t$endOnThird[1])
    endBaseState[i] <- as.character(t$endBaseState[1])
    #store endBaseOutState from last row of temp df as FinalBaseOutState for that paid
    FinalBaseOutState[i] <- as.character(t$endBaseOutState[1])
  
  #when more than 1 component, get rows from q and store in temp df  
  }else if(w$NumComponents[i] > 1){
    
    t <- q[which(q$PlateAppID == as.character(paid)),]
    #add up RPrime amounts and store in TotalRPrime for that paid
    TotalRPrime[i] <- sum(t$RPrime)
    
    #store startOuts, startOnFirst, startOnSecond, ... from first row in temp df
    startOuts[i] <- t$startOuts[1]
    startOnFirst[i] <- as.character(t$startOnFirst[1])
    startOnSecond[i] <- as.character(t$startOnSecond[1])
    startOnThird[i] <- as.character(t$startOnThird[1])
    startBaseState[i] <- as.character(t$startBaseState[1])
    startBaseOutState[i] <- as.character(t$startBaseOutState[1])
    
    #store endOuts, endOnFirst, endOnSecond, ... from last row in temp df
    endOuts[i] <- t$endOuts[NumComponents[i]]
    endOnFirst[i] <- as.character(t$endOnFirst[NumComponents[i]])
    endOnSecond[i] <- as.character(t$endOnSecond[NumComponents[i]])
    endOnThird[i] <- as.character(t$endOnThird[NumComponents[i]])
    endBaseState[i] <- as.character(t$endBaseState[NumComponents[i]])
    #store endBaseOutState from last row of temp df as FinalBaseOutState for that paid
    FinalBaseOutState[i] <- as.character(t$endBaseOutState[NumComponents[i]])
  }
  
}

#add vectors to w df
w <- data.frame(Sequence,w,startOuts,startOnFirst,startOnSecond,startOnThird,startBaseState,startBaseOutState,
                endOuts,endOnFirst,endOnSecond,endOnThird,endBaseState,FinalBaseOutState,TotalRPrime,R)


#fill R vector

#get inning, find all rows for inning

#------empty vectors to store inning and total runs for inning (actually a half inning)
w_inning = vector("numeric") #iterates with w

tRuns = vector("numeric") #will be length of num of half innings


for(i in seq_along(w$PlateAppID)){
  #------locate inning in w$PlateAppID[i] and add to vector
  w_inning = append(w_inning, as.numeric(str_sub(w$PlateAppID[i], start = 24, end = 25)))
}

#vector of half innings
inning = unique(w_inning) #iterates with rRuns

#------iterate through unique innings, summing TotalRPrime values
for (i in inning){
  #------find rows in inning which match i, find total runs for inning
  tRuns[i] = sum(w$TotalRPrime[which(w_inning==i)])
}

#iterate through w rows, storing R from tRuns, then subtracting TotalRPrime from R for next row
for(i in seq(numrows)){
  if(i == 1){  #if first row
    print(tRuns[i])
    w$R[i] = tRuns[i]            
  }else if(w_inning[i] != w_inning[i-1]){  #if inning has changed
    w$R[i] = tRuns[w_inning[i]]    
  }else{                                   #if within inning
    w$R[i] = w$R[i-1] - w$TotalRPrime[i-1]  
  }
}

outfile_name = paste0(w$GameID[1],"_paR.csv")

write.csv(w,file = outfile_name,row.names = F)

}

