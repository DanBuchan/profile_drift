library(ggplot2)

cath_hfamily_distances <- read.csv("/home/dbuchan/Projects/drift/average_cath_distances.csv", header=F)
colnames(cath_hfamily_distances) <- c("dist_file", "blosum_distance")
cath_hfamily_distances <- cath_hfamily_distances[-c(1883),]
mean(cath_hfamily_distances$blosum_distance)

ggplot(cath_hfamily_distances, aes(x=blosum_distance)) + geom_histogram()
ggsave("/home/dbuchan/Projects/drift/plots/histogram_cath_hfamily_distances.png", dpi=100, width=800, height=600, units="px")
