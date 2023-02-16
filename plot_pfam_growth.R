library(ggplot2)
library(reshape2)
library(tidyr)

iteration_summary <- read.csv("/home/dbuchan/Projects/profile_drift/iteration_summary.csv", header=T)

ggplot(data=iteration_summary, aes(x=iteration, y=hit_count, fill=hit_family)) + geom_bar(stat="identity", position="dodge")

