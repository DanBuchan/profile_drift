library(ggplot2)
library(reshape2)
library(tidyr)

setwd("/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/")
files <- Sys.glob("distance10*.membercount")

draw_member_chart <- function(file){
  member_count <- read.csv(file, header=T)
  long_counts <- gather(member_count, class, count, background:first:second, factor_key=TRUE)
  ggplot(data=long_counts, aes(x=iteration, y=count, fill=class)) + geom_bar(stat="identity", position="dodge")+labs(title=file)
}

lapply(files, draw_member_chart)

