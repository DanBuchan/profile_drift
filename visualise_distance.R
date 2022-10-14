library(ggplot2)
library(MASS)
library(dichromat)
library(RColorBrewer)

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
  write.table(as.matrix(my.dist), file=paste("./dist.txt",sep=""), row.names=FALSE, col.names=FALSE)
  
  #calculates x, y projects for the points,
  # mds%points y axis is sorted in the order of the IDs my.objects
  # build plot_df with isoMDS
  # mds = isoMDS(my.dist, k=2, maxit=1000, p=minkowski_power)
  # plot_df <- data.frame(x=mds$points[,1], y=mds$points[,2])

  # build plot_df with mdsj
  # https://www.inf.uni-konstanz.de/exalgo/software/mdsj/
  write.table(as.matrix(my.dist), file=paste("./dist.txt",sep=""), row.names=FALSE, col.names=FALSE)
  system('bash -c "java -jar /home/dbuchan/Downloads/mdsj.jar /home/dbuchan/dist.txt /home/dbuchan/dist-MDS.txt"')
  jmds <- as.matrix(read.table("/home/dbuchan/dist-MDS.txt",header=FALSE,sep=" "))
  plot_df <- data.frame(x=jmds[,1], y=jmds[,2])
  # labeling goes here, add a third colum to the mds matrix for the iteration membership

  plot_df$labels <- labels$iteration[match(strtoi(rownames(plot_df)), labels$protID)]
  plot_df[order(plot_df$labels, na.last=TRUE),]
  # plot <- ggplot(plot_df, aes(x=x, y=y)) + geom_point()
  blues20 <- colorRampPalette(brewer.pal(name="Blues", n = 9))(26)
  plot <- ggplot(plot_df, aes(x=x, y=y, color=labels)) + geom_point(aes(colour = cut(labels, c(-Inf, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, Inf))), size = 2) + scale_color_manual(values=blues20[6:26]) 

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


### Here lets map some blasts!
dist2_membership <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/distance2_membership.csv", header=F)
colnames(dist2_membership) <- c("iteration","protID")
dist2 <- read.csv("/home/dbuchan/Projects/profile_drift/RAxML_distances/distance_experiment/RAxML_distances.distance2.dist", header=F, sep = " "  )
dist2$V3 <- NULL
colnames(dist2) <- c("prot1","prot2","distance")
dist2 <- dist2[dist2$prot1 %in% dist2_membership$protID & dist2$prot2 %in% dist2_membership$protID, ]

plots <- project_distances(dist2, dist2_membership, 1)
ggsave("/home/dbuchan/Projects/profile_drift/plots/distances2_memberships.png", dpi=100, width=800, height=600, units="px")

