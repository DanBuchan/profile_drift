library(ggplot2)
library(reshape2)

average_distances <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/random_pathing/blasts/average_distances.csv", header=T)

average_distances$accumulated <- c(average_distances[1,2], 0, 0,0,0)
average_distances[2,3] <- (average_distances[1,3] + average_distances[2,2])/2
average_distances[3,3] <- (average_distances[2,3] + average_distances[3,2])/2
average_distances[4,3] <- (average_distances[3,3] + average_distances[4,2])/2
average_distances[5,3] <- (average_distances[4,3] + average_distances[5,2])/2

ggplot(average_distances, aes(x=iteration, y=ave_distance)) + geom_line() 
ggplot(average_distances, aes(x=iteration, y=accumulated)) + geom_line() 

###

distances2 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances2.csv", header=T)
distances5 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances5.csv", header=T)
distances10 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances10.csv", header=T)
distances20 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances20.csv", header=T)

all_distances <- data.frame(iteration=distances2$iteration, dist2=distances2$ave_distance, dist5=distances5$ave_distance, dist10=distances10$ave_distance, dist20=distances20$ave_distance)
plot_df <- melt(all_distances, id.vars="iteration")

ggplot(plot_df, aes(x=iteration, y=value, col=variable)) + geom_point() + geom_line()
ggsave("/home/dbuchan/Projects/profile_drift/plots/family_growth_at_distances.png", dpi=100, width=800, height=600, units="px")
