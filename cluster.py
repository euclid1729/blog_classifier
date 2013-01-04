def readfile(filename):
 lines=[line for line in file('blogdata.ods')]
 colnames=lines[0].strip().split()[1:]
 rownames=[]
 data=[]
 for line in lines[1:]:
  p=line.strip().split('\t')
  rownames.append(p[0])
  data.append([float(x) for x in p[1:]])
 return rownames,colnames,data

from math import sqrt
import random
def pearson(v1,v2):
# Simple sums
 sum1=sum(v1)
 sum2=sum(v2)
# Sums of the squares
 sum1Sq=sum([pow(v,2) for v in v1])
 sum2Sq=sum([pow(v,2) for v in v2])
# Sum of the products
 pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
# Calculate r (Pearson score)
 num=pSum-(sum1*sum2/len(v1))
 den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
 if den==0: return 0
 return 1.0-num/den

class bicluster:
 def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
  self.left=left
  self.right=right
  self.vec=vec
  self.id=id
  self.distance=distance

def hclusters(rows,distance=pearson):
 distances={}
 currentclusterid=-1
 
 clust=[bicluster(rows[i],id=i) for i in range(len(rows))]
 while len(clust)>1:
  closest=distance(clust[0].vec,clust[1].vec)
  for i in range(len(clust)):
   for j in range(len(clust)):
    if(clust[i].id,clust[j].id) not in distances:
     distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust  [j].vec)
     d=distances[(clust[i].id,clust[j].id)]
     if d<closest:
      closest=d
      lowestpair=(i,j)
# calculate the average of the two clusters
   mergevec=[(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
   newcluster=bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=closest,id=currentclustid)
   currentclusterid-=1
   del clust[lowestpair[1]]
   del clust[lowestpair[0]]
   clust.append(newcluster)
 return clust[0]

def kcluster(rows,distance=pearson,k=4):
 #preparing the range for cluster points
 ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
 #make clusters with len(row[0]) dimentions 
 clusters=[[random.random() *(ranges[j][1]-ranges[j][0])+ranges[j][0] for j in range(len(rows[0]))] for i in range(k)]
 lastmatches=None
 for t in range(100):
  print 'iteration %d' % t
  bestmatches=[[] for i in range(k)]
  #assigning rows to clusters 
  for j in range(len(rows)):
   row=rows[j]
   bestmatch=0
   for i in range(k):
    d=distance(clusters[i],row)
    if d < distance(clusters[bestmatch],row): bestmatch=i
   bestmatches[bestmatch].append(j)
  if bestmatches == lastmatches: break
  lastmatches=bestmatches
  #move clusters 
  for i in range(k):
   avgs=[0.0]*len(rows[0])
   if len(bestmatches[i])>0:
    for rowid in bestmatches[i]:
     for m in range(len(rows[rowid])):
      avgs[m]+=rows[rowid][m]
    for j in range(len(avgs)):
     avgs[j]/=len(bestmatches[i])
    clusters[i]=avgs
 return bestmatches
if __name__ == "__main__": 
 blognames,words,data=readfile('blogdata.ods')
 kclust=kcluster(data,k=3)
 for c in kclust:
  for rowid in c:
   print blognames[rowid]
  print "\n\n"
