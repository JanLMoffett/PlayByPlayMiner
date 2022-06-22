library(stringr)

#setting working directory
setwd("C:/Users/Jan/Desktop/Scrape/Analysis/")
#importing data
b1 <- read.csv("Datasets/BattingRunExpValues2.csv")
#fixing column names
names(b1)[1] <- "PlateAppID"

names(b1)
#variable names:
# [1] "PlateAppID"                 "startBaseOutState"          "FinalBaseOutState" 
# [4] "PA_EndValue_ExpectedRuns"   "PA_StartValue_ExpectedRuns" "TotalRPrime"              
# [7] "R"                          "ChangeExpRuns"              "BatterID"                     
#[10] "Singles"                    "Doubles"                    "Triples"                
#[13] "HR"                         "BB"                         "SO"                   
#[16] "FO"     

#subset of singles
b1_1b <- b1[which(b1$Singles==1),1:9]
#E(R) for singles
avg_R_1b <- mean(b1_1b$R)

avg_R_1b_A0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'A0')])
avg_R_1b_A1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'A1')])
avg_R_1b_A2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'A2')])

avg_R_1b_B0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'B0')])
avg_R_1b_B1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'B1')])
avg_R_1b_B2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'B2')])

avg_R_1b_C0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'C0')])
avg_R_1b_C1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'C1')])
avg_R_1b_C2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'C2')])

avg_R_1b_D0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'D0')])
avg_R_1b_D1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'D1')])
avg_R_1b_D2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'D2')])

avg_R_1b_E0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'E0')])
avg_R_1b_E1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'E1')])
avg_R_1b_E2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'E2')])

avg_R_1b_F0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'F0')])
avg_R_1b_F1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'F1')])
avg_R_1b_F2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'F2')])

avg_R_1b_G0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'G0')])
avg_R_1b_G1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'G1')])
avg_R_1b_G2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'G2')])

avg_R_1b_H0 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'H0')])
avg_R_1b_H1 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'H1')])
avg_R_1b_H2 <- mean(b1_1b$R[str_which(string = b1_1b$startBaseOutState, pattern = 'H2')])

#vector of RE values for singles
RE_1b <- c(avg_R_1b_A0,avg_R_1b_A1,avg_R_1b_A2,avg_R_1b_B0,avg_R_1b_B1,avg_R_1b_B2,
           avg_R_1b_C0,avg_R_1b_C1,avg_R_1b_C2,avg_R_1b_D0,avg_R_1b_D1,avg_R_1b_D2,
           avg_R_1b_E0,avg_R_1b_E1,avg_R_1b_E2,avg_R_1b_F0,avg_R_1b_F1,avg_R_1b_F2,
           avg_R_1b_G0,avg_R_1b_G1,avg_R_1b_G2,avg_R_1b_H0,avg_R_1b_H1,avg_R_1b_H2)

#subset of doubles
b1_2b <- b1[which(b1$Doubles==1),1:9]

avg_R_2b_A0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'A0')])
avg_R_2b_A1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'A1')])
avg_R_2b_A2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'A2')])

avg_R_2b_B0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'B0')])
avg_R_2b_B1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'B1')])
avg_R_2b_B2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'B2')])

avg_R_2b_C0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'C0')])
avg_R_2b_C1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'C1')])
avg_R_2b_C2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'C2')])

avg_R_2b_D0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'D0')])
avg_R_2b_D1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'D1')])
avg_R_2b_D2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'D2')])

avg_R_2b_E0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'E0')])
avg_R_2b_E1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'E1')])
avg_R_2b_E2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'E2')])

avg_R_2b_F0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'F0')])
avg_R_2b_F1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'F1')])
avg_R_2b_F2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'F2')])

avg_R_2b_G0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'G0')])
avg_R_2b_G1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'G1')])
avg_R_2b_G2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'G2')])

avg_R_2b_H0 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'H0')])
avg_R_2b_H1 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'H1')])
avg_R_2b_H2 <- mean(b1_2b$R[str_which(string = b1_2b$startBaseOutState, pattern = 'H2')])

#vector of RE values for doubles
RE_2b <- c(avg_R_2b_A0,avg_R_2b_A1,avg_R_2b_A2,avg_R_2b_B0,avg_R_2b_B1,avg_R_2b_B2,
           avg_R_2b_C0,avg_R_2b_C1,avg_R_2b_C2,avg_R_2b_D0,avg_R_2b_D1,avg_R_2b_D2,
           avg_R_2b_E0,avg_R_2b_E1,avg_R_2b_E2,avg_R_2b_F0,avg_R_2b_F1,avg_R_2b_F2,
           avg_R_2b_G0,avg_R_2b_G1,avg_R_2b_G2,avg_R_2b_H0,avg_R_2b_H1,avg_R_2b_H2)

#subset of triples - not enough observations for these
b1_3b <- b1[which(b1$Triples==1),1:9]

avg_R_3b_A0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'A0')])
avg_R_3b_A1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'A1')])
avg_R_3b_A2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'A2')])

avg_R_3b_B0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'B0')])
avg_R_3b_B1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'B1')])
avg_R_3b_B2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'B2')])

avg_R_3b_C0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'C0')])
avg_R_3b_C1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'C1')])
avg_R_3b_C2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'C2')])

avg_R_3b_D0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'D0')])
avg_R_3b_D1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'D1')])
avg_R_3b_D2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'D2')])

avg_R_3b_E0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'E0')])
avg_R_3b_E1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'E1')])
avg_R_3b_E2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'E2')])

avg_R_3b_F0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'F0')])
avg_R_3b_F1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'F1')])
avg_R_3b_F2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'F2')])

avg_R_3b_G0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'G0')])
avg_R_3b_G1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'G1')])
avg_R_3b_G2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'G2')])

avg_R_3b_H0 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'H0')])
avg_R_3b_H1 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'H1')])
avg_R_3b_H2 <- mean(b1_3b$R[str_which(string = b1_3b$startBaseOutState, pattern = 'H2')])

#vector of RE values for triples
RE_3b <- c(avg_R_3b_A0,avg_R_3b_A1,avg_R_3b_A2,avg_R_3b_B0,avg_R_3b_B1,avg_R_3b_B2,
           avg_R_3b_C0,avg_R_3b_C1,avg_R_3b_C2,avg_R_3b_D0,avg_R_3b_D1,avg_R_3b_D2,
           avg_R_3b_E0,avg_R_3b_E1,avg_R_3b_E2,avg_R_3b_F0,avg_R_3b_F1,avg_R_3b_F2,
           avg_R_3b_G0,avg_R_3b_G1,avg_R_3b_G2,avg_R_3b_H0,avg_R_3b_H1,avg_R_3b_H2)

#subset of home runs
b1_HR <- b1[which(b1$HR==1),1:9]

avg_R_HR_A0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'A0')])
avg_R_HR_A1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'A1')])
avg_R_HR_A2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'A2')])

avg_R_HR_B0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'B0')])
avg_R_HR_B1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'B1')])
avg_R_HR_B2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'B2')])

avg_R_HR_C0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'C0')])
avg_R_HR_C1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'C1')])
avg_R_HR_C2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'C2')])

avg_R_HR_D0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'D0')])
avg_R_HR_D1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'D1')])
avg_R_HR_D2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'D2')])

avg_R_HR_E0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'E0')])
avg_R_HR_E1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'E1')])
avg_R_HR_E2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'E2')])

avg_R_HR_F0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'F0')])
avg_R_HR_F1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'F1')])
avg_R_HR_F2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'F2')])

avg_R_HR_G0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'G0')])
avg_R_HR_G1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'G1')])
avg_R_HR_G2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'G2')])

avg_R_HR_H0 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'H0')])
avg_R_HR_H1 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'H1')])
avg_R_HR_H2 <- mean(b1_HR$R[str_which(string = b1_HR$startBaseOutState, pattern = 'H2')])

#vector of RE values for HR
RE_HR <- c(avg_R_HR_A0,avg_R_HR_A1,avg_R_HR_A2,avg_R_HR_B0,avg_R_HR_B1,avg_R_HR_B2,
           avg_R_HR_C0,avg_R_HR_C1,avg_R_HR_C2,avg_R_HR_D0,avg_R_HR_D1,avg_R_HR_D2,
           avg_R_HR_E0,avg_R_HR_E1,avg_R_HR_E2,avg_R_HR_F0,avg_R_HR_F1,avg_R_HR_F2,
           avg_R_HR_G0,avg_R_HR_G1,avg_R_HR_G2,avg_R_HR_H0,avg_R_HR_H1,avg_R_HR_H2)

#subset of walks
b1_BB <- b1[which(b1$BB==1),1:9]

#subset of strike outs
b1_SO <- b1[which(b1$SO==1),1:9]

#subset of field outs
b1_FO <- b1[which(b1$FO==1),1:9]


