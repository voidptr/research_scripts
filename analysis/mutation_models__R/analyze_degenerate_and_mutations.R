## Rosangela Canino-Koning
## Evolution of Modularity
## Analyzing Degenerate Sites and Mutation Landscape - May 13, 2011
##
## MacOS X 10.6.7
## R 1.40-devel 64-bit

################## data loading and setup

require(arm)
require(car)
require(rgl)
setwd("/Volumes/rosiec/research/devolab_research/evolution_of_modularity/raw_data/082/INTERTWINED/last_common_ancestor_mutation_landscapes")
## load the data into a dataframe, and reshape the data
intertwined.data <- read.csv("combined_degenerate_site_and_mutation_landscape_metrics__2step.csv", header=FALSE)
head(intertwined.data)
summary(intertwined.data)


setwd("/Volumes/rosiec/research/devolab_research/evolution_of_modularity/raw_data/082/SEPARATED/last_common_ancestor_mutation_landscapes")
## load the data into a dataframe, and reshape the data
separated.data <- read.csv("combined_degenerate_site_and_mutation_landscape_metrics__2step.csv", header=FALSE)
head(separated.data)
summary(separated.data)

## to be clear: 
##   V1 is the treatment
##   V5 is total # of degenerate sites
##   V8 is the fraction of 1-step mutants that do the fluctuating task
##   V23 is the fraction of 2-step mutants that do the fluctuating task 

############### do a simple box-plot	
par(mfrow=c(2,3))
plot(intertwined.data$V5 ~ intertwined.data$V1,			
	ylab="Total Degenerate Sites",
	xlab="treatment",
	main="Intertwined Ancestor")

plot(intertwined.data$V8 ~ intertwined.data$V1,			
	ylab="Fraction of 1-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Intertwined Ancestor")

plot(intertwined.data$V23 ~ intertwined.data$V1,			
	ylab="Fraction of 2-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Intertwined Ancestor")


plot(separated.data$V5 ~ separated.data$V1,			
	ylab="Total Degenerate Sites",
	xlab="treatment",
	main="Separated Ancestor")

plot(separated.data$V8 ~ separated.data$V1,			
	ylab="Fraction of 1-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Separated Ancestor")

plot(separated.data$V23 ~ separated.data$V1,			
	ylab="Fraction of 2-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Separated Ancestor")


## to be clear: 
##   V1 is the treatment
##   V5 is total # of degenerate sites
##   V8 is the fraction of 1-step mutants that do the fluctuating task



par(mfrow=c(2,4))
##################### SEPARATED ANCESTOR
## do the ancova

ancova.lm.fullmodel <- lm(V8 ~ V1*V5, data=separated.data)
summary(ancova.lm.fullmodel)

plot(V8 ~ V5,
	data=separated.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants 1step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel)[1], 
	   coef(ancova.lm.fullmodel)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2]+coef(ancova.lm.fullmodel)[3], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5]+coef(ancova.lm.fullmodel)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel)	   
	   
## step it down
ancova.lm.nointeractions <- lm(V8 ~ V1*V5, data=separated.data)
summary(ancova.lm.nointeractions)

plot(V8 ~ V5,
	data=separated.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants 1step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.nointeractions)[1], 
	   coef(ancova.lm.nointeractions)[4], col=c("black"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2], 
	   coef(ancova.lm.nointeractions)[4], col=c("blue"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2]+coef(ancova.lm.nointeractions)[3], 
	   coef(ancova.lm.nointeractions)[4], col=c("red"))	   

########### now 2-step

ancova.lm.fullmodel <- lm(V23 ~ V1*V5, data=separated.data)
summary(ancova.lm.fullmodel)

plot(V23 ~ V5,
	data=separated.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants 2step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel)[1], 
	   coef(ancova.lm.fullmodel)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2]+coef(ancova.lm.fullmodel)[3], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5]+coef(ancova.lm.fullmodel)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel)	   
	   
## step it down
ancova.lm.nointeractions <- lm(V23 ~ V1*V5, data=separated.data)
summary(ancova.lm.nointeractions)

plot(V23 ~ V5,
	data=separated.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants 2step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.nointeractions)[1], 
	   coef(ancova.lm.nointeractions)[4], col=c("black"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2], 
	   coef(ancova.lm.nointeractions)[4], col=c("blue"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2]+coef(ancova.lm.nointeractions)[3], 
	   coef(ancova.lm.nointeractions)[4], col=c("red"))	  








########### INTERTWINED ANCESTOR	   
	   
ancova.lm.fullmodel <- lm(V8 ~ V1*V5, data=intertwined.data)
summary(ancova.lm.fullmodel)

plot(V8 ~ V5,
	data= intertwined.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel)[1], 
	   coef(ancova.lm.fullmodel)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2]+coef(ancova.lm.fullmodel)[3], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5]+coef(ancova.lm.fullmodel)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel)	   
	   
## step it down
ancova.lm.nointeractions <- lm(V8 ~ V1*V5, data= intertwined.data)
summary(ancova.lm.nointeractions)

plot(V8 ~ V5,
	data=intertwined.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.nointeractions)[1], 
	   coef(ancova.lm.nointeractions)[4], col=c("black"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2], 
	   coef(ancova.lm.nointeractions)[4], col=c("blue"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2]+coef(ancova.lm.nointeractions)[3], 
	   coef(ancova.lm.nointeractions)[4], col=c("red"))	   
	   
	   
####### 2step	 
	 
ancova.lm.fullmodel <- lm(V23 ~ V1*V5, data=intertwined.data)
summary(ancova.lm.fullmodel)

plot(V23 ~ V5,
	data= intertwined.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel)[1], 
	   coef(ancova.lm.fullmodel)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel)[1]+coef(ancova.lm.fullmodel)[2]+coef(ancova.lm.fullmodel)[3], 
	   coef(ancova.lm.fullmodel)[4]+coef(ancova.lm.fullmodel)[5]+coef(ancova.lm.fullmodel)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel)	   
	   
## step it down
ancova.lm.nointeractions <- lm(V23 ~ V1*V5, data= intertwined.data)
summary(ancova.lm.nointeractions)

plot(V23 ~ V5,
	data=intertwined.data,
	col=c("gray","lightblue","pink")[V1],
	xlab="# degenerate sites",
	ylab="fraction of mutants",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.nointeractions)[1], 
	   coef(ancova.lm.nointeractions)[4], col=c("black"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2], 
	   coef(ancova.lm.nointeractions)[4], col=c("blue"))
	   
abline(coef(ancova.lm.nointeractions)[1]+coef(ancova.lm.nointeractions)[2]+coef(ancova.lm.nointeractions)[3], 
	   coef(ancova.lm.nointeractions)[4], col=c("red"))	   
	   	   	   
	   
	   
	   
	   
	   
	   