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

distance2_500_1000 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/average_distances2_500cluster_1000cluster.csv", header=T)
ggplot(distance2_500_1000, aes(x=iteration, y=tot_distance)) + geom_point() + geom_line()
ggplot(distance2_500_1000, aes(x=iteration, y=member_count)) + geom_point() + geom_line()
ggplot(distance2_500_1000, aes(x=iteration, y=ave_distance)) + geom_point() + geom_line()
