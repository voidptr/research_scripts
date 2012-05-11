import pdb
import numpy as np
import gzip

class clade:
   def __init__(self, id, cdata, popsize):
      self.id = id
      self.cdata = cdata
      self.popsize = popsize
      self.InitPolygon()

   def InitPolygon(self):
      num = self.cdata.shape[0]
      num_pts = num*2
      self.polyY = np.zeros(num_pts)
      self.polyX = np.zeros(num_pts)
      for n in range(0,num):
         self.polyY[n]           = self.popsize/2.0 - self.cdata[n,1]/2.0
         self.polyX[n]           = self.cdata[n,0] 
         self.polyY[num_pts-n-1] = self.popsize/2.0 + self.cdata[n,1]/2.0
         self.polyX[num_pts-n-1] = self.cdata[n,0]
      self.birth = np.min(self.cdata[:,0])
      self.death = np.max(self.cdata[:,0])
      return

   def AddChild(self,child):
      if child.birth < self.death and child.birth > self.birth:
         overlap = np.intersect1d(self.cdata[:,0], child.cdata[:,0])
         for o in overlap:
            ndx = np.ravel(np.nonzero(self.polyX == o))
            ndxL = min(ndx)
            ndxU = max(ndx)
            ndxC = np.ravel(np.nonzero(child.cdata[:,0] == o))
            try:
               self.polyY[ndxL] = self.polyY[ndxL] - 0.5 * child.cdata[ndxC,1]
               self.polyY[ndxU] = self.polyY[ndxU] + 0.5 * child.cdata[ndxC,1]
            except:
               pdb.set_trace()

class cladeogram:
   def __init__(self, file, popsize):
      self.popsize = popsize
      self.InputFromFile(file)
      self.AdjustClades()
      return

   def GetClades(self):
      return self.CLADES

   def AdjustClades(self):
      ids = np.sort(self.CLADES.keys())[::-1]
      for c in range(0,len(ids)):
         for p in range(c+1,len(ids)):
            childID = ids[c]
            parentID = ids[p]
            self.CLADES[parentID].AddChild(self.CLADES[childID])
      return

   def InputFromFile(self, ccld_path):
      self.CLADES = {}
      data = {}
      fin = gzip.open(ccld_path)
      for line in fin.readlines():
         line = line.strip()
         if line is '' or line[0] == '#':
            continue
         toks = line.split(' ')
         update = int(toks[0])
         numgen = int(toks[1])
         for g in range(0,numgen):
            id  = int(toks[2+2*g])
            num = int(toks[3+2*g])
            if id not in data:
               data[id] = [[update, num]]
            else:
               data[id].append([update,num])
      for k,v in data.items():
         self.CLADES[k] = clade(k, np.array(v), self.popsize)
      return


