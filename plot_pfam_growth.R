library(ggplot2)
library(reshape2)
library(tidyr)
library(tidyverse)

print_chart <- function(groupdata) {
  ggplot(data=groupdata, aes(x=iteration, y=hit_count, fill=hit_family)) + geom_bar(stat="identity", position=position_dodge2(preserve = "single")) + labs(title=groupdata$rep_family)
}

iteration_summary <- read.csv("/home/dbuchan/Projects/profile_drift/iteration_summary.csv", header=T)
testdf <- head(iteration_summary, 2000)

testdf %>% group_by(rep) %>% group_map(~ print_chart(.x))

# ggplot(data=iteration_summary, aes(x=iteration, y=hit_count, fill=hit_family)) + geom_bar(stat="identity", position="dodge")
