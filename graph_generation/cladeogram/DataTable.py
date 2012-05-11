import cStringIO
import copy
import odict
##import restprinter as rp
import copy
import numpy as np
import types
import pdb
import gzip as gz
import datetime as dt


# This function will return a name without the format information
# The format information is stored as: Name%Format
# Where format is: %f for float, %d for int, %s for string
def tokname(descr):
   tok = descr.split('%')
   name = tok[0]
   if len(tok) > 1:
      if (tok[1] == 'f'):
         type = 'float'
      elif (tok[1] == 'd'):
         type = 'int'
      elif (tok[1] == 's'): 
         type = 'string'
      else:
         type = None
   else:
      type = None
   return name, type   
   
# This function will return the name of the column, abscent format information
def getname(descr):
   name, type = tokname(descr)
   return name

# This function will return the type of the column, abscent name
def gettype(descr):
   name, type = tokname(descr)
   return type
   
# Convert a type to a character format
def type2char(type):
   if (type == 'int'):
      c = 'd'
   elif (type == 'float'):
      c = 'f'
   elif (type == 'string'):
      c = 's'
   else:
      c = None
   return c

def SetupTable(fields):
   return SetupOutputTable(fields)

def SetupOutputTable(data):
   OUTDICT  = {}
   OUTTYPES = {}
   OUTNAMES = []
   fields = map(lambda x: x.rstrip().lstrip(), data.split(',')) if type(data) is types.StringType else data
   for x in fields:
      n,t = tokname(x)
      OUTDICT[n] = []
      OUTNAMES.append(n)
      if t is not None:
         OUTTYPES[n] = t
   return OUTDICT, OUTNAMES, OUTTYPES


class DataTable:
   
   # This function will setup a dictionary that contains the original
   # and format-absent names
   def readformat(self,tok):
      thesenames = []
      start = 0 if tok[0][0] != '#' else 1
      for x in range(start,len(tok)):
         n,t = tokname(tok[x])
         if t == None:
            continue
         else:
            self.ftypes[n] = t
            thesenames.append(n)
      if (not self.names or '__all__' in self.names):
         self.names = thesenames
         self.col = {}
         for n in thesenames:
            self.col[n] = []

      
   def __init__(self, file='', names=[], types={}, headerLines=0, sep=' ', fmnt=[], sfmnt='', **kw):
      if fmnt != []:
         trash, names, types = SetupOutputTable(fmnt)
      self.col   = odict.odict() # This will be a dictionary of numpy vectors
      self.len   = 0       # This is the length of the table
      self.names  = names  # This contains a list of ordered field names
      self.file   = file   # This is the filename
      self.types  = types  # This is an input set of field types by field name
      self.ftypes = {}     # This is a set of field types read from format information
      for n in names: 
         self.col[n] = []    #Initially, we'll read everything into lists of strings
      self.defaults = kw['defaults'] if 'defaults' in kw.keys() else {}
      self.allowedSkips = kw['allowedSkips'] if 'allowedSkips' in kw.keys() else []

      
      if (sfmnt != ''):
         self.readformat(sfmnt.split())
         self.types = copy.deepcopy(self.ftypes)

      if file=='':
         for n in self.names:
            self.col[n] = np.array([], dtype=self.types[n])
         return

      self.FORMATTAGS = ['#format:', '#format', '#fmt', '#fmt:']
      
      fid = gz.GzipFile(file)  # Open the file (all data files will be zipped)
      
      try:
         # Skip the headerlines
         self._headerlines = []
         for k in range(0,headerLines):
            self._headerlines.append(fid.readline())
         
         # For each line in the file
         for line in fid:
            if not line.strip():  # Try to remove the leading and lagging whitespace
               continue
            else:
               
               # Tokenize the lines of the file into fields
               fields = line.strip().split(sep)

               # Handled skipped fields in order specified by allowedSkips, using default values or 'nan'
               if len(fields) <= len(self.names) + len(self.allowedSkips):
                  delta = len(self.names) - len(fields)
                  if delta > len(self.allowedSkips):
                     continue;  #Nothing can be done
                  for j in range(0,delta):
                     add_skip = self.allowedSkips[j]
                     loc_field = self.names.index(add_skip)
                     default_value = self.defaults[add_skip] if add_skip in self.defaults else 'nan'
                     fields.insert(loc_field, default_value)


               # See if this line contains formatting information
               if (len(fields) > 1 and fields[0] in self.FORMATTAGS):
                  self.readformat(fields)
               # Skip the line if it doesn't contain the right number of fields or is a comment
               elif (line[0] == '#') or len(fields) != len(self.names): 
                  continue
               else: #Otherwise, store it in our temporary col dictionary
                  self.len += 1   #Increase the length of the table by one
                  for k in range(0, len(fields)):          #For each field in the line
                     self.col[self.names[k]].append(fields[k])  #Append the appropriate dictionary list

         # For each list in the dictionary
         for descr, data in self.col.items():
            try: 
               # When deciding how to format our numpy vectors, we will
               # (1) see if there is an entry in the types dictionary
               # (2) set all values to '__all__' if it is in the types dict
               # (3) otherwise, try to use the format information
               # (4) else raise an exception/tokenize

               if descr in self.types.keys():  
                  self.col[descr] = np.array(data, dtype=self.types[descr])
               elif '__all__' in self.types.keys():  
                  self.col[descr] = np.array(data, dtype=self.types['__all__'])
               elif descr in self.ftypes.keys(): 
                  self.col[descr] = np.array(data, dtype=self.ftypes[descr])
               else:
                  raise
            except:
               tt = self.types[descr] if descr in self.types.keys() else 'n/a'
               ft = self.ftypes[descr] if descr in self.ftypes.keys() else 'n/a'
               print 'Data Problem in file:%s, field:%s, types=%s, ftypes=%s, data:%s' % (file, descr, tt, ft, data)
               quit()
               
      finally:         
         fid.close()

   def __getitem__(self, name):
      return self.col[name]
      
   def table(self):
      return self.col

   def columns(self):
      return self.col.keys()
      
   def rows(self):
      return self.len

   def getHeaderlines(self):
      return self._headerlines

   def rearrange(self, ndx):
      for k,v in self.col.items():
         self.col[k] = v[ndx]
      return

   def filter(self, colname, expression, action='include'):
      if self.len == 0:
         return copy.deepcopy(self) 
      matches = np.array(map(lambda x: eval('x ' + expression), self[colname]))
      ndx = np.flatnonzero(matches) if action == 'include' else np.flatnonzero(matches ^ True)
      new_table = copy.deepcopy(self)
      new_table.col = {}
      new_table.len = len(ndx)
      for c in self.col.keys():
         new_table.col[c] = self.col[c][ndx]
      return new_table

   def asdict(self):
      ndx = np.arange(0,self.len)
      by_row = odict.odict()
      for n in ndx:
         by_row[n] = odict.odict()
      for n in by_row.keys():
         for cn in self.names:
            by_row[n][cn] = self.col[cn][n]
      return by_row
   
   def dictappendrow(self, din):
      for cn in self.names:
         self.col[cn] = np.append(self.col[cn], din[cn])
      self.len += 1

   def __repr__(self):
      by_row = self.asdict()
      buf = cStringIO.StringIO()
      #printer = rp.RST(buf)
      #printer.WriteDictAsGT(by_row, autospan=True, lpad=1, rpad=1)
      return buf.getvalue()



def WriteDataTable(file, names, data, title='', sep=' ', types={}):
   file = gz.open(file, 'w')   
   try:
      file.write("# " + title + " " +\
                 dt.datetime.today().replace(microsecond=0).isoformat(' ') + '\n')
      file.write("#format ")
      for name in names:
         if name in types:
            file.write('%s%%%s ' % (name,type2char(types[name])))
         else:
            file.write(name + " ")
      file.write('\n')
      
      rows = len(data[ names[0] ])
      
      for k in range(0,rows):
         for n in range(0,len(names)):
            file.write(str(data[ names[n] ][k]))
            if (n < len(names)-1):
               file.write(sep)
         file.write('\n')
   finally:
      file.close()



