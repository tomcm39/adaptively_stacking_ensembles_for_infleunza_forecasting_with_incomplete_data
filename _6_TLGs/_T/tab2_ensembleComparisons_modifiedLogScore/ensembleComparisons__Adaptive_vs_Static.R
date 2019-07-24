#mcandrew
require(lme4)
require(lmPerm)


rename <- function(d,old,new){
    names(d)[names(d)==old] <- new
    return(d)
}


computeEstimates <- function(model){
    
    cf <- coef(model)
    means <- do.call(rbind.data.frame, cf)

    re <- ranef(model, condVar=TRUE)

    ses <- arm::se.coef(model)
    InterceptVariability <- ses$fixef
    ses$fixef <- NULL
    
    ses <- sapply( ses, function(x){sqrt(x^2+InterceptVariability^2)})
    
    sds   <- do.call(rbind.data.frame, ses)

    e95target <- cf$target+1.96*ses$target
    e95season <- cf$season+1.96*ses$season
    e95region <- cf$region+1.96*ses$region
    uppers <- list("region" = e95region, "season" = e95season, "target" = e95target)
    upperCnf <- do.call(rbind.data.frame, uppers)
    
    e5target <- cf$target-1.96*ses$target
    e5season <- cf$season-1.96*ses$season
    e5region <- cf$region-1.96*ses$region
    lowers <- list("region" = e5region, "season" = e5season, "target" = e5target)
    lowerCnf <- do.call(rbind.data.frame, lowers)
    
    pvTarget <- data.frame("(Intercept)" = apply(cbind(cf$target,ses$target),1, function(x){2*(1 - pnorm(abs(x[1]),0,x[2]))}))
    pvSeason <- data.frame("(Intercept)" = apply(cbind(cf$season,ses$season),1, function(x){2*(1 - pnorm(abs(x[1]),0,x[2]))}))
    pvRegion <- data.frame("(Intercept)" = apply(cbind(cf$region,ses$region),1, function(x){2*(1 - pnorm(abs(x[1]),0,x[2]))}))
    ps <- list("region" = pvRegion, "season" = pvSeason, "target" = pvTarget)
    pvalues <- do.call(rbind.data.frame, ps)


    outputCoef <- function(model,type,specificType){
        dta <- eval(parse(text=paste0("coef(model)$",type)))
        return( dta[row.names(dta)==specificType,"(Intercept)"])
    }
    bootStrapPvalues <- data.frame(rep(0,length(row.names(pvalues))))
    row.names(bootStrapPvalues) = row.names(pvalues)
    names(bootStrapPvalues) = c('Intercept')

    print('bootstrapping')
    for (i in 1:dim(bootStrapPvalues)[1]){
        print(i)
        type_sType <- row.names(bootStrapPvalues)[i]
        type <- strsplit(type_sType,'[.]')[[1]][1]
        stype <- strsplit(type_sType,'[.]')[[1]][2]
        
        rslts <- as.matrix(as.data.frame(bootMer(x=model, function(x){outputCoef(x,type,stype)}, nsim=1000)))
        rslts <- rslts-mean(rslts) # center
        statistic <-means[type_sType,'(Intercept)']
        pvalue <- mean(abs(rslts) > statistic)
        bootStrapPvalues[type_sType,"(Intercept)"] <- pvalue
    }
    
    rslts <- cbind(means,sds,lowerCnf,upperCnf,pvalues,bootStrapPvalues)
    names(rslts) <- c("means","se","lowerCI","upperCI","p",'bootP')
    return(rslts)
}


#------------------------------------------

d <- read.csv('../../../_5_compute_and_score__ensembles/analysisData/allEnsembleScores.csv')

dynamic <- d[d$modelType=='dynamic',]
dynamic08 <- dynamic[dynamic$prior==0.08,]
dynamic08 <- rename(dynamic08,'logScore5','logScoreDynamic5')

static  <- d[d$modelType=='static',]
static00 <- static[static$prior==0.00,]
static00 <- rename(static00,'logScore5','logScoreStatic5')

DSE <- merge(dynamic08,static00,by = c('region','target','EWNum'))

DSE['difDE'] <- DSE$logScoreDynamic - DSE$logScoreEqual
DSE['difDS'] <- DSE$logScoreDynamic - DSE$logScoreStatic

DSE['year'] <- substr(DSE$EWNum,1,4)
DSE['week'] <- substr(DSE$EWNum,5,6)

computeSeason <- function(x){
    year <- strtoi(x['year'])
    nextYear <- year+1
    pastYear <- year-1
    return(ifelse(x['week'] <53 & x['week'] >=40 , paste0(year,'/',nextYear) , paste0(pastYear,'/',year)))
}
DSE['season'] <- apply(DSE,1,computeSeason)

dsRslts <- lmer( difDS~(1|season) + (1|target) + (1|region), data = DSE)
dsRslts <- computeEstimates(dsRslts)
write.csv(dsRslts,"tableData/dsRslts.csv")

#buildTables
require(xtable)

print("Adaptive vs Static")
dsRslts <- round(dsRslts,2)
dsRslts$EffectSize <- paste0(dsRslts$means," (",dsRslts$lowerCI,", ",dsRslts$upperCI,")")
dsRslts <- dsRslts[, c("EffectSize",'p') ]
dsRslts$p <- sapply(dsRslts$p,function(x){ifelse(x==0,"<0.01",x)})
xtable(dsRslts)
