library(plyr) # ldply
library(dplyr)
library(mice) # pmm
library(naniar) # var_miss
library(data.table) # fread
library(tidyr) # gather - plot_missing
library(dplyr) # group_by - plot_missing
library(ggplot2) # plot_missing
library(imputeTS) # LOCF

# Feature extraction
features = c('HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp', 'EtCO2',
             'Glucose', 'Gender', 'ICULOS', 'SepsisLabel')

# checking no of zeros and ones in every psv files
setwd('C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\training')
files <- list.files() 
v0 <- c(); v1 <- c()
for(i in 1:length(files)) {
  temp <- as.data.frame(fread(files[i], sep = '|', header = T))[, features]
  z = 0; o = 0
  for(j in temp$SepsisLabel) {
    if(j == 0) z = z + 1
    else o = o + 1
  }
  v0 <- c(v0, z); v1  <- c(v1, o)
}

v <- abs(v0 - v1)
v <- sort(v)

# do the same as above for training set_B

# Perfoming downsampling in traingin set_A
setwd('C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\training')
zeros1 = 0; ones1 = 0; ct = 0
files <- list.files()
for(i in 1:length(files)) {
  temp <- as.data.frame(fread(files[i], sep = '|', header = T))[, features]
  z = 0; o = 0
  for(j in temp$SepsisLabel) {
    if(j == 0) z = z + 1
    else o = o + 1
  }
  if(abs(o - z) <= 11) {
    zeros1 = zeros1 + z; ones1 = ones1 + o
    s <- paste0("C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\train\\p" , ct , ".csv")
    write.csv(temp, s)
    ct = ct + 1
  }
}
abs(zeros1 - ones1)

# Perfoming downsampling in traingin set_B
zeros2 = 0; ones2 = 0; ct = 0
setwd('C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\training_setB')
files <- list.files() 
for(i in 1:length(files)) {
  temp <- as.data.frame(fread(files[i], sep = '|', header = T))[, features]
  z = 0; o = 0
  for(j in temp$SepsisLabel) {
    if(j == 0) z = z + 1
    else o = o + 1
  }
  if(abs(o - z) <= 11) {
    zeros2 = zeros2 + z; ones2 = ones2 + o
    s <- paste0("C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\trainB\\p" , ct , ".csv")
    write.csv(temp, s)
    ct = ct + 1
  }
}

abs(zeros2 - ones2)

# Combining downsampled data of training set_A and training set_B
setwd('C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\train')
df1 <- ldply(list.files(), read.csv, header=TRUE)
setwd('C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\trainB')
df2 <- ldply(list.files(), read.csv, header=TRUE)
df <- rbind(df1, df2)
setwd('C:\\Users\\DELL\\Desktop\\Sepsis\\Data')

# Ploting Imbalance
a <- table(df$SepsisLabel)
rownames(a)[1] <- "Non Sepsis"; rownames(a)[2] <- "Sepsis";
barplot(a,
        xlab = "Patients",
        ylab = "Count",
        col = c("Red","navy"),
        main = "Data Imbalance")

# plotting imbalance using pie
table(df$SepsisLabel)
pie(c(12962, 12257), c('Non Sepsis', 'Sepsis'), main = "Data Imbalance", col = c('red', 'navy'))


# Imputing missing values using PMM (MICE package) 
imputed_Data <- mice(df, m=3, maxit = 25, method = 'pmm', seed = 500)
summary(imputed_Data)

# Storing final csv file
completeData <- complete(imputed_Data, 2)
summary(completeData)
write.csv(completeData, 'C:\\Users\\DELL\\Desktop\\Sepsis\\Data\\Cleaned\\completeClean.csv')