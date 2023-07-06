library(ggplot2)
library(reshape2)

average_distances <- read.csv("/home/dbuchan/Projects/profile_drift/old_RAxML_distances/random_pathing/blasts/average_distances.csv", header=T)

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
distances30 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances30.csv", header=T)
distances40 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances40.csv", header=T)
distances50 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/average_distances50.csv", header=T)

all_distances <- data.frame(iteration=distances2$iteration, dist2=distances2$ave_distance, dist5=distances5$ave_distance, dist10=distances10$ave_distance, dist20=distances20$ave_distance, dist30=distances30$ave_distance, dist40=distances40$ave_distance, dist50=distances50$ave_distance)
plot_df <- melt(all_distances, id.vars="iteration")
ggplot(plot_df, aes(x=iteration, y=value, col=variable)) + geom_point() + geom_line()
ggsave("/home/dbuchan/Projects/profile_drift/plots/family_growth_at_ave_distances.png", dpi=100, width=800, height=600, units="px")

tot_distances <- data.frame(iteration=distances2$iteration, tot2=distances2$tot_distance, tot5=distances5$tot_distance, tot10=distances10$tot_distance, tot20=distances20$tot_distance, tot30=distances30$tot_distance, tot40=distances40$tot_distance, tot50=distances50$tot_distance)
plot_df <- melt(tot_distances, id.vars="iteration")
ggplot(plot_df, aes(x=iteration, y=value, col=variable)) + geom_point() + geom_line()
ggsave("/home/dbuchan/Projects/profile_drift/plots/family_growth_at_tot_distances.png", dpi=100, width=800, height=600, units="px")

members <- data.frame(iteration=distances2$iteration, memb2=distances2$member_count, memb5=distances5$member_count, memb10=distances10$member_count, memb20=distances20$member_count, memb30=distances30$member_count, memb40=distances40$member_count, memb50=distances50$member_count)
plot_df <- melt(members, id.vars="iteration")
ggplot(plot_df, aes(x=iteration, y=value, col=variable)) + geom_point() + geom_line()
ggsave("/home/dbuchan/Projects/profile_drift/plots/members_growth_at_iteration.png", dpi=100, width=800, height=600, units="px")


###

distance2_500_1000 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/average_distances10_22cluster_58cluster.csv", header=T)
ggplot(distance2_500_1000, aes(x=iteration, y=tot_distance)) + geom_point() + geom_line()
ggplot(distance2_500_1000, aes(x=iteration, y=member_count)) + geom_point() + geom_line()
ggplot(distance2_500_1000, aes(x=iteration, y=ave_distance)) + geom_point() + geom_line()

distance2_500_1000 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/average_distances40_6cluster_39cluster.csv", header=T)
ggplot(distance2_500_1000, aes(x=iteration, y=tot_distance)) + geom_point() + geom_line()
ggplot(distance2_500_1000, aes(x=iteration, y=member_count)) + geom_point() + geom_line()
ggplot(distance2_500_1000, aes(x=iteration, y=ave_distance)) + geom_point() + geom_line()

path <- "/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/"
files <- Sys.glob(paste(path, "average_distances10*", sep=""))
ldf <- lapply(files, read.csv)
ldf[[1]]$dist <- 118
ldf[[2]]$dist <- 129
ldf[[3]]$dist <- 139
ldf[[4]]$dist <- 158
ldf[[5]]$dist <- 58
ldf[[6]]$dist <- 98
ten_distances <- rbind(ldf[[5]], ldf[[6]], ldf[[1]], ldf[[2]], ldf[[3]], ldf[[4]])
ten_distances$dist <- as.factor(ten_distances$dist) 
ggplot(ten_distances, aes(x=iteration, y=member_count, group=dist, colour=dist))+ geom_point() + geom_line()

files <- Sys.glob(paste(path, "average_distances20*", sep=""))
ldf <- lapply(files, read.csv)
ldf[[1]]$dist <- 101
ldf[[2]]$dist <- 29
ldf[[3]]$dist <- 46
ldf[[4]]$dist <- 51
ldf[[5]]$dist <- 63
ldf[[6]]$dist <- 67
ldf[[7]]$dist <- 82
ldf[[8]]$dist <- 88
ldf[[9]]$dist <- 92
twenty_distances <- rbind(ldf[[2]], ldf[[3]], ldf[[4]], ldf[[5]], ldf[[6]], ldf[[7]], ldf[[8]], ldf[[9]], ldf[[1]])
twenty_distances$dist <- as.factor(twenty_distances$dist) 
ggplot(twenty_distances, aes(x=iteration, y=member_count, group=dist, colour=dist))+ geom_point() + geom_line()

files <- Sys.glob(paste(path, "average_distances30*", sep=""))
ldf <- lapply(files, read.csv)
ldf[[1]]$dist <- 17
ldf[[2]]$dist <- 26
ldf[[3]]$dist <- 31
ldf[[4]]$dist <- 32
ldf[[5]]$dist <- 38
ldf[[6]]$dist <- 44
thirty_distances <- rbind(ldf[[1]], ldf[[2]], ldf[[3]], ldf[[4]], ldf[[5]], ldf[[6]])
thirty_distances$dist <- as.factor(thirty_distances$dist) 
ggplot(thirty_distances, aes(x=iteration, y=member_count, group=dist, colour=dist))+ geom_point() + geom_line()


files <- Sys.glob(paste(path, "average_distances40*", sep=""))
ldf <- lapply(files, read.csv)
ldf[[1]]$dist <- 12
ldf[[2]]$dist <- 17
ldf[[3]]$dist <- 21
ldf[[4]]$dist <- 27
ldf[[5]]$dist <- 31
ldf[[6]]$dist <- 36
ldf[[7]]$dist <- 39
forty_distances <- rbind(ldf[[1]], ldf[[2]], ldf[[3]], ldf[[4]], ldf[[5]], ldf[[6]], ldf[[7]])
forty_distances$dist <- as.factor(forty_distances$dist) 
ggplot(forty_distances, aes(x=iteration, y=member_count, group=dist, colour=dist))+ geom_point() + geom_line()


files <- Sys.glob(paste(path, "average_distances50*", sep=""))
ldf <- lapply(files, read.csv)
ldf[[1]]$dist <- 12
ldf[[2]]$dist <- 17
ldf[[3]]$dist <- 20
ldf[[4]]$dist <- 24
ldf[[5]]$dist <- 26
ldf[[6]]$dist <- 28
ldf[[7]]$dist <- 29
ldf[[8]]$dist <- 8
fifty_distances <- rbind(ldf[[8]], ldf[[1]], ldf[[2]], ldf[[3]], ldf[[4]], ldf[[5]], ldf[[6]], ldf[[7]])
fifty_distances$dist <- as.factor(fifty_distances$dist) 
ggplot(fifty_distances, aes(x=iteration, y=member_count, group=dist, colour=dist))+ geom_point() + geom_line()
