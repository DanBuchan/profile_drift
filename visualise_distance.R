library(ggplot2)
library(MASS)

# Distance matrix assembly after: https://stackoverflow.com/questions/12274967/csv-of-distances-to-dist-object-r

project_distances <- function(data){
  print(paste("Mean: ", mean(data$distance)))
  print(paste("SD: ", sd(data$distance)))
  my.objects <- sort(unique(c(as.character(data$prot1), as.character(data$prot2))))
  data$prot1 <- match(data$prot1, my.objects)
  data$prot2 <- match(data$prot2, my.objects)
  
  n <- length(my.objects)
  dist_mat <- matrix(NA, n, n)
  i <- as.matrix(data[-3])
  dist_mat[i] <- dist_mat[i[,2:1]] <- data$distance
  my.dist <- as.dist(dist_mat)
  
  mds = isoMDS(my.dist, k=2)
  plot_df <- data.frame(x=mds$points[,1], y=mds$points[,2])
  plot <- ggplot(plot_df, aes(x=x, y=y)) + geom_point()
  return(plot)
}

distances_csv <- read.csv("/home/dbuchan/Projects/drift/pairwise_distance_substitution.csv", header=T)
plot <- project_distances(distances_csv)
plot
ggsave("/home/dbuchan/Projects/drift/plots/100_subsitution_points.png", dpi=100, width=800, height=600, units="px")

breadth_distances_csv <- read.csv("/home/dbuchan/Projects/drift/pairwise_distance_substitution_breadth.csv", header=T)
plot <- project_distances(breadth_distances_csv)
plot
ggsave("/home/dbuchan/Projects/drift/plots/100_subsitution_points_breadth.png", dpi=100, width=800, height=600, units="px")

