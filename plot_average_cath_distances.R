library(ggplot2)
library(modeest)

cath_hfamily_distances <- read.csv("/home/dbuchan/Projects/drift/average_cath_distances.csv", header=F)
colnames(cath_hfamily_distances) <- c("dist_file", "blosum_distance")
cath_hfamily_distances <- cath_hfamily_distances[-c(1883),]
mean(cath_hfamily_distances$blosum_distance)
median(cath_hfamily_distances$blosum_distance)
mode(cath_hfamily_distances$blosum_distance)
mlv(cath_hfamily_distances$blosum_distance, method = "meanshift") # 1.6

ggplot(cath_hfamily_distances, aes(x=blosum_distance)) + geom_histogram()
ggsave("/home/dbuchan/Projects/drift/plots/histogram_cath_hfamily_distances.png", dpi=100, width=800, height=600, units="px")

rep_distances <- read.csv("/home/dbuchan/Projects/drift/cath_distances/RAxML_distances.reps.dist", header=F,sep = " ")
rep_distances <- rep_distances[,-c(3)]
colnames(rep_distances) <- c("rep1", "rep2", "distance")
mean(rep_distances$distance)
median(rep_distances$distance)
nrow(rep_distances) # 21981765
sample_vec <- sample(nrow(rep_distances), 500000)
rep_sample <- rep_distances[sample_vec,]
mlv(rep_sample$distance, method = "meanshift") #3.6
ggplot(rep_distances, aes(x=distance)) + geom_histogram()
