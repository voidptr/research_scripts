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

names(intertwined.data)
names(intertwined.data)[1] <- "treatment"
names(intertwined.data)[2] <- "fluct_degen_sites"
names(intertwined.data)[5] <- "total_degen_sites"
names(intertwined.data)[8] <- "does_fluct_1step"
names(intertwined.data)[23] <- "does_fluct_2step"



setwd("/Volumes/rosiec/research/devolab_research/evolution_of_modularity/raw_data/082/SEPARATED/last_common_ancestor_mutation_landscapes")
## load the data into a dataframe, and reshape the data
separated.data <- read.csv("combined_degenerate_site_and_mutation_landscape_metrics__2step.csv", header=FALSE)
head(separated.data)
summary(separated.data)

names(separated.data)
names(separated.data)[1] <- "treatment"
names(separated.data)[2] <- "fluct_degen_sites"
names(separated.data)[5] <- "total_degen_sites"
names(separated.data)[8] <- "does_fluct_1step"
names(separated.data)[23] <- "does_fluct_2step"

## to be clear: 
##   V1 is the treatment
##   V2 is number of fluctuating task degenerate sites
##   V5 is total # of degenerate sites
##   V8 is the fraction of 1-step mutants that do the fluctuating task
##   V23 is the fraction of 2-step mutants that do the fluctuating task 

############### do a simple box-plot	
par(mfrow=c(2,3))
plot(fluct_degen_sites ~ treatment,
	data=intertwined.data,		
	#col=c("black","blue","red")[intertwined.data$treatment],
	ylab="Fluct Degenerate Sites",
	xlab="treatment",
	main="Intertwined Ancestor")
t.test(fluct_degen_sites ~ treatment=="noreward",
	data=intertwined.data)


plot(does_fluct_1step ~ treatment,	
	data=intertwined.data,		
	#col=c("black","blue","red")[intertwined.data$treatment],
	ylab="Fraction of 1-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Intertwined Ancestor")

plot(does_fluct_2step ~ treatment,			
	data=intertwined.data,
	#col=c("black","blue","red")[intertwined.data$treatment],
	ylab="Fraction of 2-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Intertwined Ancestor")

plot(fluct_degen_sites ~ treatment,			
	data=separated.data,
	#col=c("black","blue","red")[separated.data$treatment],
	ylab="Fluct Degenerate Sites",
	xlab="treatment",
	main="Separated Ancestor")

plot(does_fluct_1step ~ treatment,	
	data=separated.data,		
	#col=c("black","blue","red")[separated.data$treatment],
	ylab="Fraction of 1-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Separated Ancestor")

plot(does_fluct_2step ~ treatment,				
	data=separated.data,
	#col=c("black","blue","red")[separated.data$treatment],
	ylab="Fraction of 2-step Mutants that perform Fluct Task",
	xlab="treatment",
	main="Separated Ancestor")


########################## MODEL THE RELATIONSHIP BETWEEN
########################## Fluct Degenerate Sites and Fraction of 1step mutants that does Fluct Task
########################## by Treatment

par(mfrow=c(1,1))
##################### SEPARATED ANCESTOR
## do the ancova

ancova.lm.fullmodel.sep.1step.bytreatment <- lm(does_fluct_1step ~ treatment*fluct_degen_sites, data=separated.data)
summary(ancova.lm.fullmodel.sep.1step.bytreatment)

plot(does_fluct_1step ~ fluct_degen_sites,
	data=separated.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants 1step",
	main="Separated Ancestor\nDegen Sites v. Mut Lost Fluct Task")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.sep.1step.bytreatment)[1], 
	   coef(ancova.lm.fullmodel.sep.1step.bytreatment)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel.sep.1step.bytreatment)[1]+coef(ancova.lm.fullmodel.sep.1step.bytreatment)[2], 
	   coef(ancova.lm.fullmodel.sep.1step.bytreatment)[4]+coef(ancova.lm.fullmodel.sep.1step.bytreatment)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel.sep.1step.bytreatment)[1]+coef(ancova.lm.fullmodel.sep.1step.bytreatment)[2]+coef(ancova.lm.fullmodel.sep.1step.bytreatment)[3], 
	   coef(ancova.lm.fullmodel.sep.1step.bytreatment)[4]+coef(ancova.lm.fullmodel.sep.1step.bytreatment)[5]+coef(ancova.lm.fullmodel.sep.1step.bytreatment)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel.sep.1step.bytreatment)	   
	   
########### now 2-step

ancova.lm.fullmodel.sep.2step.bytreatment <- lm(does_fluct_2step ~ treatment*fluct_degen_sites, data=separated.data)
summary(ancova.lm.fullmodel.sep.2step.bytreatment)

plot(does_fluct_2step ~ fluct_degen_sites,
	data=separated.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants 2step",
	main="Separated Ancestor\nDegen Sites v. Mut Regained Fluct Task")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.sep.2step.bytreatment)[1], 
	   coef(ancova.lm.fullmodel.sep.2step.bytreatment)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel.sep.2step.bytreatment)[1]+coef(ancova.lm.fullmodel.sep.2step.bytreatment)[2], 
	   coef(ancova.lm.fullmodel.sep.2step.bytreatment)[4]+coef(ancova.lm.fullmodel.sep.2step.bytreatment)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel.sep.2step.bytreatment)[1]+coef(ancova.lm.fullmodel.sep.2step.bytreatment)[2]+coef(ancova.lm.fullmodel.sep.2step.bytreatment)[3], 
	   coef(ancova.lm.fullmodel.sep.2step.bytreatment)[4]+coef(ancova.lm.fullmodel.sep.2step.bytreatment)[5]+coef(ancova.lm.fullmodel.sep.2step.bytreatment)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel.sep.2step.bytreatment)	   

########### INTERTWINED ANCESTOR	   
	   
ancova.lm.fullmodel.int.1step.bytreatment <- lm(does_fluct_1step ~ treatment*fluct_degen_sites, data=intertwined.data)
summary(ancova.lm.fullmodel.int.1step.bytreatment)

plot(does_fluct_1step ~ fluct_degen_sites,
	data= intertwined.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants",
	main="Intertwined Ancestor\nDegen Sites v. Mut Lost Fluct Task")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.int.1step.bytreatment)[1], 
	   coef(ancova.lm.fullmodel.int.1step.bytreatment)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel.int.1step.bytreatment)[1]+coef(ancova.lm.fullmodel.int.1step.bytreatment)[2], 
	   coef(ancova.lm.fullmodel.int.1step.bytreatment)[4]+coef(ancova.lm.fullmodel.int.1step.bytreatment)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel.int.1step.bytreatment)[1]+coef(ancova.lm.fullmodel.int.1step.bytreatment)[2]+coef(ancova.lm.fullmodel.int.1step.bytreatment)[3], 
	   coef(ancova.lm.fullmodel.int.1step.bytreatment)[4]+coef(ancova.lm.fullmodel.int.1step.bytreatment)[5]+coef(ancova.lm.fullmodel.int.1step.bytreatment)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel.int.1step.bytreatment)	   
	   
	   
####### 2step	 
	 
ancova.lm.fullmodel.int.2step.bytreatment <- lm(does_fluct_2step ~ treatment*fluct_degen_sites, data=intertwined.data)
summary(ancova.lm.fullmodel.int.2step.bytreatment)

plot(does_fluct_2step ~ fluct_degen_sites,
	data= intertwined.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants",
	main="Intertwined Ancestor\nDegen Sites v. Mut Regained Fluct Task")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.int.2step.bytreatment)[1], 
	   coef(ancova.lm.fullmodel.int.2step.bytreatment)[4], col=c("black"))
	   
abline(coef(ancova.lm.fullmodel.int.2step.bytreatment)[1]+coef(ancova.lm.fullmodel.int.2step.bytreatment)[2], 
	   coef(ancova.lm.fullmodel.int.2step.bytreatment)[4]+coef(ancova.lm.fullmodel.int.2step.bytreatment)[5], col=c("blue"))
	   
abline(coef(ancova.lm.fullmodel.int.2step.bytreatment)[1]+coef(ancova.lm.fullmodel.int.2step.bytreatment)[2]+coef(ancova.lm.fullmodel.int.2step.bytreatment)[3], 
	   coef(ancova.lm.fullmodel.int.2step.bytreatment)[4]+coef(ancova.lm.fullmodel.int.2step.bytreatment)[5]+coef(ancova.lm.fullmodel.int.2step.bytreatment)[6], col=c("red"))
	   
## do a step analysis for parsimony
step(ancova.lm.fullmodel.int.2step.bytreatment)	   
	   
	   
	   
########################## MODEL THE RELATIONSHIP BETWEEN
########################## Fluct Degenerate Sites and Fraction of 1step mutants that does Fluct Task


par(mfrow=c(2,1))
##################### SEPARATED ANCESTOR
## do the ancova

ancova.lm.fullmodel.sep.1step <- lm(does_fluct_1step ~ fluct_degen_sites, data=separated.data)
summary(ancova.lm.fullmodel.sep.1step)

plot(does_fluct_1step ~ fluct_degen_sites,
	data=separated.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants 1step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.sep.1step)[1], 
	   coef(ancova.lm.fullmodel.sep.1step)[2], col=c("black"))

	   
########### now 2-step
ancova.lm.fullmodel.sep.2step <- lm(does_fluct_2step ~ fluct_degen_sites, data=separated.data)
summary(ancova.lm.fullmodel.sep.2step)

plot(does_fluct_2step ~ fluct_degen_sites,
	data=separated.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants 2step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.sep.2step)[1], 
	   coef(ancova.lm.fullmodel.sep.2step)[2], col=c("black"))


########### INTERTWINED ANCESTOR	   
## do the ancova

ancova.lm.fullmodel.int.1step <- lm(does_fluct_1step ~ fluct_degen_sites, data=separated.data)
summary(ancova.lm.fullmodel.int.1step)

plot(does_fluct_1step ~ fluct_degen_sites,
	data=intertwined.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants 1step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.int.1step)[1], 
	   coef(ancova.lm.fullmodel.int.1step)[2], col=c("black"))

	   
########### now 2-step
ancova.lm.fullmodel.int.2step <- lm(does_fluct_2step ~ fluct_degen_sites, data=separated.data)
summary(ancova.lm.fullmodel.int.2step)

plot(does_fluct_2step ~ fluct_degen_sites,
	data= intertwined.data,
	col=c("black","blue","red")[treatment],
	xlab="# degenerate sites",
	ylab="fraction of mutants 2step",
	main="Relationship of Degenerate Sites to Fraction of Mutants")
#legend(0, .96, legend=c("control","no reward","punishment"), col=c("gray","lightblue","pink"), pch=c(1,1), bg="white")
abline(coef(ancova.lm.fullmodel.int.2step)[1], 
	   coef(ancova.lm.fullmodel.int.2step)[2], col=c("black"))	   
	   
	   