data=read.csv("data.data",sep="\t")
term<-unique(data$term)
alg<-unique(data$alg)
color<-seq(2,1+length(term)*length(alg)/2)
color<-c(color,color)

par(mfrow=c(2,2))
boxplot(data$timeSec~data$term*data$alg,horizontal=TRUE,col=color,
      main="Time in Seconds",ylab="terms.alg")
boxplot(data$bottleLengthSST~data$term*data$alg,horizontal=TRUE,col=color,
      main="Bottleneck Length for Steinerized Tree",ylab="terms.alg")
boxplot(data$totalLength~data$term*data$alg,horizontal=TRUE,col=color,
      main="Spanning Tree Total Length",ylab="terms.alg")
boxplot(data$bottleLength~data$term*data$alg,horizontal=TRUE,col=color,
      main="Bottleneck Length for Spanning Tree",ylab="terms.alg")


par(mfrow=c(1,2))
steinerMST=data$steiner[which(data$alg=="MST")]
steinerMSTterm=data$term[which(data$alg=="MST")]
boxplot(steinerMST~steinerMSTterm,col=color,
      main="Steiner Points MST",xlab="terms",ylab="steiners")

data$steiner[which(data$alg=="SMT")]=2*data$steiner[which(data$alg=="SMT")]
steinerSMT=data$steiner[which(data$alg=="SMT")]
steinerSMTterm=data$term[which(data$alg=="SMT")]
boxplot(steinerSMT~steinerSMTterm,col=color,
      main="Steiner Points SMT",xlab="terms",ylab="steiners")


par(mfrow=c(1,1))
boxplot(data$timeHour~data$term*data$alg,horizontal=TRUE,col=color,
      main="Time in Hours",ylab="terms.alg")
