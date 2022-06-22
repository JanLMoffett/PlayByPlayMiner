setwd("C://Users/Jan/Desktop/Scrape/Old Files/")
library(stringr)

au_lines = readLines("action_units.txt")

au_type = rep("NA", length(au_lines))
au_string = rep("NA",length(au_lines))


for(i in 1:length(au_lines)){
  loc = str_locate(au_lines[i],",")
  
  a = loc[1]
  au_type[i] <- str_sub(au_lines[i], start=1, end=a-1)
  
  au_string[i] <- str_sub(au_lines[i], start = a+1, end = str_length(au_lines[i]))
}

error = rep(F, length(au_lines)) #column to keep track of error in unit

error[1:196] <- T #first game in directory is messed up

audf <- data.frame(au_string, au_type, error) #adding error column to data frame
audf <- audf[-1,] #chop off first row

#look for units that are too short, mark as error 
audf[which(str_length(audf$au_string)<11),3] <- T

#dataframe with errors (i found so far) removed
audf2 <- audf[which(audf$error==F),]

head(audf2[str_which(audf2$au_string, "struck"),1])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Strike outs
k <- audf2[str_which(audf2$au_string, "struck"),1]

kswing <- k[str_which(k, "swinging")]
klook <- k[str_which(k, "looking")]

num_kswing <- length(kswing)
num_klook <- length(klook)

barplot(c(num_kswing, num_klook), names.arg = c("Swinging","Looking"), main = "Strike Outs")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#strike outs removed
audf3 <- audf2[-str_which(audf2$au_string, "struck"),1]

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Advancing
advanced <- audf3[str_which(audf3, "advanced")]

length(advanced)

advanced_to_second <- advanced[str_which(advanced,"advanced to second")]
num_adv_to_second <- length(advanced_to_second)

advanced_to_third <- advanced[str_which(advanced,"advanced to third")]
num_adv_to_third <- length(advanced_to_third)

advanced_to_both <- advanced_to_second[str_which(advanced_to_second, "advanced to third")]
num_adv_to_both <- length(advanced_to_both)


#looking for rbi
rbi <- audf2$au_string[str_which(audf2$au_string, "RBI")]
head(rbi)

#looking for outs
out <- audf2$au_string[str_which(audf2$au_string, "out")]
head(out,25)

#looking for ground outs
go <- audf2$au_string[str_which(audf2$au_string, "grounded out")]
head(go, 120)
gdp <- audf2$au_string[str_which(audf2$au_string, "grounded into")]
head(gdp, 100)

#other types of double plays?
dp <- audf2$au_string[str_which(audf2$au_string, "double play")]
#unassisted dps?
udp <- dp[str_which(dp, "unassisted")] 

#what is the average length of an action unit?
mean(nchar(as.character(audf2$au_string)))
#37.05322
#what is the standard deviation?
sd(nchar(as.character(audf2$au_string)))
#11.59909

#how is the num of chars distributed?
hist(nchar(as.character(audf2$au_string)))


#set w/in 2 sd of mean
au2sd <- audf2$au_string[which((37.05322 - 2*11.59909) <= nchar(as.character(audf2$au_string)) & nchar(as.character(audf2$au_string)) <= (37.05322 + 2*11.59909))]

au_tails <- audf2$au_string[-(which((37.05322 - 2*11.59909) <= nchar(as.character(audf2$au_string)) & nchar(as.character(audf2$au_string)) <= (37.05322 + 2*11.59909)))]

au_tails

br1 <- as.character(audf2$au_string[str_which(audf2$au_string, "out at")])

outon <- as.character(audf2$au_string[str_which(audf2$au_string, "out on")])

br2 <- as.character(audf2$au_string[str_which(audf2$au_string, "advanced")])
scored <- as.character(audf2$au_string[str_which(audf2$au_string, "scored")])
br4 <- as.character(audf2$au_string[str_which(audf2$au_string, "stole")])

balk <- as.character(audf2$au_string[str_which(audf2$au_string, "balk")])

br <- c(br1,br2,br3,br4)

interference <- as.character(audf2$au_string[str_which(audf2$au_string, "interference")])
advanced <- as.character(audf2$au_string[str_which(audf2$au_string, "advanced")])
unearned <- as.character(audf2$au_string[str_which(audf2$au_string, "unearned")])
pickedoff <- as.character(audf2$au_string[str_which(audf2$au_string, "picked off")])
wildpitch <- as.character(audf2$au_string[str_which(audf2$au_string, "wild pitch")])
failed <- as.character(audf2$au_string[str_which(audf2$au_string, "failed")])

SAC <- as.character(audf2$au_string[str_which(audf2$au_string, "SAC")])
SF <- as.character(audf2$au_string[str_which(audf2$au_string, "SF")])
SAC
SF
