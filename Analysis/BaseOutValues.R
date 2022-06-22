
setwd("C:/Users/Jan/Desktop/Scrape/Analysis/")

#importing dataset
p1 <- read.csv("Datasets/PAandBaseOutStates.csv")
#fixing column name
names(p1)[1] <- "PlateAppID"

names(p1)
#variables
#[1] "PlateAppID"        "startBaseState"    "startBaseOutState"
#[4] "endBaseState"      "FinalBaseOutState" "TotalRPrime"      
#[7] "R" 

#finding expected run values for each base-out state
ER_A0 <- mean(p1[which(p1$startBaseOutState == "A0"),7])
ER_A1 <- mean(p1[which(p1$startBaseOutState == "A1"),7])
ER_A2 <- mean(p1[which(p1$startBaseOutState == "A2"),7])

ER_B0 <- mean(p1[which(p1$startBaseOutState == "B0"),7])
ER_B1 <- mean(p1[which(p1$startBaseOutState == "B1"),7])
ER_B2 <- mean(p1[which(p1$startBaseOutState == "B2"),7])

ER_C0 <- mean(p1[which(p1$startBaseOutState == "C0"),7])
ER_C1 <- mean(p1[which(p1$startBaseOutState == "C1"),7])
ER_C2 <- mean(p1[which(p1$startBaseOutState == "C2"),7])

ER_D0 <- mean(p1[which(p1$startBaseOutState == "D0"),7])
ER_D1 <- mean(p1[which(p1$startBaseOutState == "D1"),7])
ER_D2 <- mean(p1[which(p1$startBaseOutState == "D2"),7])

ER_E0 <- mean(p1[which(p1$startBaseOutState == "E0"),7])
ER_E1 <- mean(p1[which(p1$startBaseOutState == "E1"),7])
ER_E2 <- mean(p1[which(p1$startBaseOutState == "E2"),7])

ER_F0 <- mean(p1[which(p1$startBaseOutState == "F0"),7])
ER_F1 <- mean(p1[which(p1$startBaseOutState == "F1"),7])
ER_F2 <- mean(p1[which(p1$startBaseOutState == "F2"),7])

ER_G0 <- mean(p1[which(p1$startBaseOutState == "G0"),7])
ER_G1 <- mean(p1[which(p1$startBaseOutState == "G1"),7])
ER_G2 <- mean(p1[which(p1$startBaseOutState == "G2"),7])

ER_H0 <- mean(p1[which(p1$startBaseOutState == "H0"),7])
ER_H1 <- mean(p1[which(p1$startBaseOutState == "H1"),7])
ER_H2 <- mean(p1[which(p1$startBaseOutState == "H2"),7])

#vector of expected run values
ERxBO <- c(ER_A0, ER_A1, ER_A2, ER_B0, ER_B1, ER_B2, ER_C0, ER_C1, ER_C2,
           ER_D0, ER_D1, ER_D2, ER_E0, ER_E1, ER_E2, ER_F0, ER_F1, ER_F2,
           ER_G0, ER_G1, ER_G2, ER_H0, ER_H1, ER_H2)

#vector of base-out state labels
boStates <- c("A0", "A1", "A2", "B0", "B1", "B2", "C0", "C1", "C2",
              "D0", "D1", "D2", "E0", "E1", "E2", "F0", "F1", "F2",
              "G0", "G1", "G2", "H0", "H1", "H2")

#barplot of expected run values by base-out state
barplot(ERxBO, names.arg= boStates)

#dataframe of base-out states and their expected run values
er_values <- data.frame(boStates, ERxBO)

#saving a csv of expected run values
write.csv(er_values, "Datasets/er_values.csv")



