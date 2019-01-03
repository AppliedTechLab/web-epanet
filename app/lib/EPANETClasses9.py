#EPANETClasses9.py
#2/6/18
#sets up junction, tank, pipe, coordinates,emitters, tags,patterns,options classes

def AddWhiteSpaceColon(parsedRow,colonYN):

    #this adds back in enough white space to satisfy EPANET
    #handles any mix of ints or strs in the row

    try:
        spacedRow=parsedRow[0]
    except:                     #empty row, a new line will be added at the end
        spacedRow=parsedRow
        
    spacedRow=str(spacedRow)    #incase first addition is a number
    i=1
    while i< len(parsedRow):

        white="        \t"
        try:
            spacedRow+=white+parsedRow[i] #I tested the readability of this file without the spaces and it worked
        except:
            spacedRow+=white+str(parsedRow[i])

        i+=1
    if colonYN==True:
        spacedRow+=white+";\n"
    else:
        spacedRow+="\n"
        
    return spacedRow



class Junction(object):
    
    #define class to carry all of the EPANET junction data
    kind='Junction'

    def __init__ (self, ID, Elev, Demand, Pattern, Colon):

        self.ID = str(ID)
        self.Elev= float(Elev)
        self.Demand= float(Demand)
        self.Pattern= str(Pattern)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Elevation = %.1f Demand = %.4f Pattern = %s" %(self.ID,self.Elev,self.Demand,self.Pattern)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Elev,self.Demand,self.Pattern],self.Colon)

class Tank(object):
    
    #define class to carry all of the EPANET junction data
    kind='Tank'

    def __init__ (self, ID, Elev, InitLvl, MinLvl, MaxLvl, Dia, MinVol, Colon):

        self.ID = str(ID)
        self.Elev= float(Elev)
        self.InitLvl= float(InitLvl)
        self.MinLvl= float(MinLvl)
        self.MaxLvl= float(MaxLvl)
        self.Dia= float(Dia)
        self.MinVol= float(MinVol)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Elev = %.1f InitLvl = %.2f MinLvl = %.2f MaxLvl = %.2f Dia = %.3f MinVol = %.3f" %(self.ID,self.Elev,self.InitLvl, self.MinLvl, self.MaxLvl, self.Dia, self.MinVol)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Elev,self.InitLvl, self.MinLvl, self.MaxLvl, self.Dia, self.MinVol],self.Colon)

class Pipe(object):

    #define class to carry all of the EPANET junction data
    kind='Pipe'

    def __init__ (self, ID, Node1, Node2, Length, Dia, Rough, Loss, Status, Colon):

        self.ID = str(ID)
        self.Node1= str(Node1)
        self.Node2= str(Node2)
        self.Length= float(Length)
        self.Dia= float(Dia)
        self.Rough= Rough#int(Rough) allows for non-HW friction formulations
        self.Loss= float(Loss)
        self.Status= str(Status)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        testStr = "ID= %s Node1 = %s Node2 = %s Length = %.4f Dia = %.1f Rough = %i Loss = %.1f Status = %s" %(self.ID,self.Node1,self.Node2, self.Length, self.Dia, self.Rough, self.Loss, self.Status)
        
        return testStr

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Node1,self.Node2, self.Length, self.Dia, self.Rough, self.Loss, self.Status],self.Colon)

class Coordinate(object):
    
    #define class to carry all of the EPANET junction data
    kind='Coordinates'

    def __init__ (self, ID, Xcord, Ycord,Colon):

        self.ID = str(ID)
        self.Xcord= float(Xcord)
        self.Ycord= float(Ycord)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Xcordation = %.2f Ycord = %.2f " %(self.ID,self.Xcord,self.Ycord)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Xcord,self.Ycord],self.Colon)


class Emitter(object):
    
    #define class to carry all of the EPANET junction data
    kind='Emitter'

    def __init__ (self, ID, Coef, Colon):

        self.ID = str(ID)
        self.Coef= float(Coef)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Coefficient = %.1f" %(self.ID,self.Coef)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Coef],self.Colon)
        
class Tag(object):
    
    #define class to carry all of the EPANET junction data
    kind='Tag'

    def __init__ (self, Type, ID, Value, Colon):

        self.Type = str(Type)
        self.ID = str(ID)
        self.Value= str(Value)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "Type= %s ID= %s Tag= %s" %(self.Type,self.ID,self.Value)

    def flatten(self):

        return AddWhiteSpaceColon([self.Type,self.ID,self.Value],self.Colon)
        
class DemandSpec(object):
    
    #define class to carry all of the EPANET junction data
    kind='DemandSpec'

    def __init__ (self, ID, Demand, Pattern, Colon):

        self.ID = str(ID)
        self.Demand= float(Demand)
        self.Pattern= str(Pattern)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Demand = %.4f Pattern = %s" %(self.ID,self.Demand,self.Pattern)

    def flatten(self):

        return AddWhiteSpaceColon([self.ID,self.Demand,self.Pattern],self.Colon)

class Link(object):
    
    #define class to carry which two nodes it is connected to and their indexes
    kind='Link'

    def __init__ (self, Name, ID1, ID2,i1,i2,Length,Dia):

        self.Name= str(Name)
        self.ID1 = str(ID1)
        self.ID2 = str(ID2)
        self.Length=float(Length)
        self.Dia=float(Dia)
        self.i1=int(i1)
        self.i2=int(i2)
        self.P1=[]
        self.P2=[]
        
    def __repr__(self):
        
        return "INCOMPLETE REPR FNC. ID1= %s ID2 = %s " %(self.ID1,self.ID2)

    def addPressure(self,P1,P2):

        self.P1.append(float(P1))
        self.P2.append(float(P2))
        

class DemPattern(object):
    
    #define class to carry all of the INP's option data
    kind='Pattern'

    def __init__ (self, ID, Multipliers, Colon):
        
        #print('got here')
        self.ID = str(ID)
        self.Mult= Multipliers
        self.Avg = float(sum(Multipliers))/len(Multipliers)
        self.Colon=bool(Colon)
        
    def __repr__(self):
        
        return "ID= %s Mult = %s Avg = %.3f" %(self.ID,str(self.Mult),self.Avg)

    def flatten(self):

        return AddWhiteSpaceColon(self.Mult.insert(0,self.ID),self.Colon)
    
