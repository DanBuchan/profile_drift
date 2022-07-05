library(ggplot2)

average_distances <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/random_pathing/blasts/average_distances.csv", header=T)

average_distances$accumulated <- c(average_distances[1,2], 0, 0,0,0)
average_distances[2,3] <- (average_distances[1,3] + average_distances[2,2])/2
average_distances[3,3] <- (average_distances[2,3] + average_distances[3,2])/2
average_distances[4,3] <- (average_distances[3,3] + average_distances[4,2])/2
average_distances[5,3] <- (average_distances[4,3] + average_distances[5,2])/2

ggplot(average_distances, aes(x=iteration, y=ave_distance)) + geom_line() 
ggplot(average_distances, aes(x=iteration, y=accumulated)) + geom_line() 
