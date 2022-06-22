
setwd("C:/Users/Jan/Desktop/Scrape/Output/SEC/")
source("quality_to_pa.R")
#infile = "ABAM_MSST_0412201901_quality.csv" done
#infile = "ABAM_GEOR_0518201901_quality.csv" done
#infile = "ABAM_MSST_0413201901_quality.csv" done
#infile = "ABAM_MSST_0414201901_quality.csv" done
#infile = "ABAM_GEOR_0517201901_quality.csv" done
#infile = "ABAM_MSST_0412201901_quality.csv" done
#infile = "ABAM_MSST_0413201901_quality.csv" done
#infile = "ABAM_MSST_0414201901_quality.csv" done
#infile = "ABAM_OMSS_0315201901_quality.csv" done
#infile = "ABAM_OMSS_0317201901_quality.csv" done
#infile = "ABAM_OMSS_0316201901_quality.csv" #done
infile = "MIZZ_ARKS_0317201901_quality.csv"

quality_to_pa(infile)

