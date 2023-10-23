require(jsonlite)

print("reading TreeFeaturesComplete1.json...")
df1<-fromJSON("TreeFeaturesComplete1.json")

print("reading TreeFeaturesComplete2.json...")
df2<-fromJSON("TreeFeaturesComplete2.json")

print("reading TreeFeaturesComplete3.json...")
df3<-fromJSON("TreeFeaturesComplete3.json")

print("Combining dataframes...")
DF<-rbind(df1,df2,df3)
class(DF$taxid)<-"integer"
class(DF$zoom)<-"integer"
class(DF$lat)<-"numeric"
class(DF$lon)<-"numeric"

print ("Saving dataframe to binary file lmdata.Rdata...")
save(DF, file='lmdata.Rdata')

print ("Done.")



