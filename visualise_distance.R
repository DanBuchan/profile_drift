library(ggplot2)
library(MASS)

# Distance matrix assembly after: https://stackoverflow.com/questions/12274967/csv-of-distances-to-dist-object-r

project_distances <- function(data, labels, minkowski_power){
  print(paste("Mean: ", mean(data$distance)))
  print(paste("SD: ", sd(data$distance)))

  # a list of the prot names in sorted order
  my.objects <- sort(unique(c(as.character(data$prot1), as.character(data$prot2))))

  # number the IDs in the original data frame if there are character names
  data$prot1 <- match(data$prot1, my.objects)
  data$prot2 <- match(data$prot2, my.objects)

  # Make a matrix of the right dimensions
  n <- length(my.objects)
  dist_mat <- matrix(NA, n, n)
  # make a matrix of the IDs
  i <- as.matrix(data[-3])

  # cast the distances to the matrix
  dist_mat[i] <- dist_mat[i[,2:1]] <- data$distance
  #cast the matrix as a distance matrix
  my.dist <- as.dist(dist_mat)

  #calculates x, y projects for the points,
  # mds%points y axis is sorted in the order of the IDs my.objects
  mds = isoMDS(my.dist, k=2, maxit=1000, p=minkowski_power)
  # labeling goes here, add a third colum to the mds matrix for the iteration membership

  plot_df <- data.frame(x=mds$points[,1], y=mds$points[,2])
  plot_df$labels <- labels$iteration[match(strtoi(rownames(plot_df)), labels$protID)]
  plot_df[order(plot_df$labels, na.last=TRUE),]
  # plot <- ggplot(plot_df, aes(x=x, y=y)) + geom_point()
  plot <- ggplot(plot_df, aes(x=x, y=y, color=labels)) + geom_point(aes(colour = cut(labels, c(-Inf, 0, 1, 2, 3, 4, Inf))), size = 2) + scale_color_brewer(type = 'div', palette='Set1',direction = 1) 

  return(plot)
}

distances_csv <- read.csv("/home/dbuchan/Projects/profile_drift/pairwise_distance_substitution.csv", header=T)
plot <- project_distances(distances_csv)
plot
ggsave("/home/dbuchan/Projects/drift/plots/100_subsitution_points.png", dpi=100, width=800, height=600, units="px")

breadth_distances_csv <- read.csv("/home/dbuchan/Projects/profile_drift/pairwise_distance_substitution_breadth.csv", header=T)
plot <- project_distances(breadth_distances_csv)
plot
ggsave("/home/dbuchan/Projects/drift/plots/100_subsitution_points_breadth.png", dpi=100, width=800, height=600, units="px")


### RAxML

distances_10000 <- read.csv("/home/dbuchan/Projects/drift/RAxML_distances/step_size_2/RAxML_distances.1000_by_10_step_2_random_walk_distances.csv", header=F, sep = " "  )
distances_10000$V3 <- NULL
colnames(distances_10000) <- c("prot1","prot2","distance")

plot <- project_distances(distances_10000, 1)
plot
ggsave("/home/dbuchan/Projects/profile_drift/plots/100_subsitution_points_breadth.png", dpi=100, width=800, height=600, units="px")

### cath fanned data

cath_iteration_labels <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/cath_fanning_distance_3_walks_step_2/cath_blasts/iteration_labels.csv", header=F)
colnames(cath_iteration_labels) <- c("iteration","protID")
cath_distances <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/cath_fanning_distance_3_walks_step_2/RAxML_distances.full_relabelled.dist", header=F, sep = " "  )
cath_distances$V3 <- NULL
colnames(cath_distances) <- c("prot1","prot2","distance")
cath_distances <- cath_distances[cath_distances$prot1 %in% cath_iteration_labels$protID, ]
cath_distances <- cath_distances[cath_distances$prot2 %in% cath_iteration_labels$protID, ]

plots <- project_distances(cath_distances, cath_iteration_labels, 1)
ggsave("/home/dbuchan/Projects/profile_drift/plots/fanning_cath.png", dpi=100, width=800, height=600, units="px")


### 
rand_iteration_labels <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/random_pathing/blasts/random_membership.csv", header=F)
colnames(rand_iteration_labels) <- c("iteration","protID")
rand_distances <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/random_pathing/RAxML_distances.full_db.dist", header=F, sep = " "  )
rand_distances$V3 <- NULL
colnames(rand_distances) <- c("prot1","prot2","distance")
rand_distances <- rand_distances[rand_distances$prot1 %in% rand_iteration_labels$protID, ]
rand_distances <- rand_distances[rand_distances$prot2 %in% rand_iteration_labels$protID, ]

plots <- project_distances(rand_distances, rand_iteration_labels, 1)
ggsave("/home/dbuchan/Projects/profile_drift/plots/random_distances.png", dpi=100, width=800, height=600, units="px")
