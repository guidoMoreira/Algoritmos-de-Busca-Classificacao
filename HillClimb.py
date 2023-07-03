#Cristian, Guido e João Padoan


globalid = 1

#Heuristica
def heuristica(e,obj):
  h = 0
  for i in range(0,3):
    for j in range(0,3):
          if e.m[i][j] == obj[i][j]:
            h+=1
  return h


#Retorna linha e coluna do elemento x na matriz m
def findx(x,m):
  j = 0
  for y in m:
    try:
      i = y.index(x)
      return [j,i]
    except:
      j+=1
  return False

#Cria cópia da matriz
def cpM(m):
  nm = []
  for i in m:
    nm.append(list(i))
  return nm

#Compara duas matrizes
def compM(m1,m2):
  count = 0
  for i in range(0,3):
    for j in range(0,3):
          if m1[i][j] == m2[i][j]:
            count+=1
  if count >=9:
    return True
  else:
    return False

#Printa matriz
def printm(m):
  for i in m:
    print(i)

#Classe dos estados com seu id, matriz, pai e filhos
class EstadoProff:
  def __init__(self,pai,matriz):
    self.m = matriz
    self.filhos = []
    self.pai = pai #EstadoProff()
    self.id = -1
    #profundidade
    self.prof=0
    self.h = -1

  def setId(self):
    global globalid
    self.id = globalid
    globalid+=1
  
  #Adiciona filho criado na lista
  def checaF(self, f, Tudosf):
    if self.pai == None or not compM(f.m,self.pai.m):
      Tudosf.append(f)
    

  #Gera filho com movimento a esquerda
  def geraEsq(self,pos):
    #print("Gera Esq")
    nM = cpM(self.m)
    nM[pos[0]][pos[1]] = nM[pos[0]][pos[1]-1]
    nM[pos[0]][pos[1]-1] = '#'
    return EstadoProff(self,nM)

  #Gera filho com movimento a direita
  def geraDir(self,pos):
    #print("Gera Dir")
    nM = cpM(self.m)
    nM[pos[0]][pos[1]] = nM[pos[0]][pos[1]+1]
    nM[pos[0]][pos[1]+1] = '#'
    return EstadoProff(self,nM)

  #Gera filho com movimento a Cima
  def geraCim(self,pos):
    #print("Gera Cim")
    nM = cpM(self.m)
    nM[pos[0]][pos[1]] = nM[pos[0]-1][pos[1]]
    nM[pos[0]-1][pos[1]] = '#'
    return EstadoProff(self,nM)

  #Gera filho com movimento a Baixo
  def geraBax(self,pos):
    #print("Gera Bax")
    nM = cpM(self.m)
    nM[pos[0]][pos[1]] = nM[pos[0]+1][pos[1]]
    nM[pos[0]+1][pos[1]] = '#'
    return EstadoProff(self,nM)

  #Checa posição do espaço vazio para criar filhos com movimentos possíveis
  def darLuz(self):
    Tudosf = []
    pos = findx('#',self.m)
    posx = pos[1]
    posy = pos[0]
    if posy == 0:
      f = self.geraBax(pos)
      self.checaF(f,Tudosf)
    elif posy == 1:
      f1 = self.geraBax(pos)
      self.checaF(f1,Tudosf)
      f2 = self.geraCim(pos)
      self.checaF(f2,Tudosf)
    else:
      f = self.geraCim(pos)
      self.checaF(f,Tudosf)
    if posx == 0:
      f = self.geraDir(pos)
      self.checaF(f,Tudosf)
    elif posx == 1:
      f1 = self.geraEsq(pos)
      self.checaF(f1,Tudosf)
      f2 = self.geraDir(pos)
      self.checaF(f2,Tudosf)
    else:
      f = self.geraEsq(pos)
      self.checaF(f,Tudosf)
    self.filhos = Tudosf

    #salva profundidade dos filhos
    for f in self.filhos:
      f.prof = getProf(f)
    
    return Tudosf
    

#Checa se chegou ao limitegetProf
def profLim(f,lim):
  prof = getProf(f)
  
  if prof > lim:
    return True
  else:
    return False

#Calcula profundiade do filho
def getProf(f):
  count = 0
  aux = f
  while(aux.pai != None):
    aux = aux.pai
    count+=1
  return count
  
def printR(r):
  aux = r
  print("Resultado: "+ str(aux.id)+"\nProfundidade: " + str(getProf(aux)))
  
  printm(aux.m)
  while(aux.pai != None):
    aux = aux.pai
    print("filho de " + str(aux.id))
    printm(aux.m)

#Hill climbing
def HC(mInicial, mObjetivo):
  global globalid
  globalid = 1
  Inicial = EstadoProff(None, mInicial)
  Inicial.setId()
  X = Inicial
  while not compM(X.m, mObjetivo):
    filhos = X.darLuz()

    maxh = 0
    mf = filhos[0]
    for i in filhos:
      h = heuristica(i,mObjetivo)
      if h>maxh:
        maxh = h
        mf = i
    X = mf
    X.setId()
  
  print("==Hill Climbing==")
  printR(X)
  return True

#Busca Melhor Escolha
def BME(mInicial,mObjetivo,lim): 
  global globalid
  globalid = 1
  Inicial = EstadoProff(None,mInicial) 
  Inicial.setId()
  Aberto = [Inicial]
  Fechado = []
  
  while Aberto:
    
    X = Aberto[0]
    Aberto.pop(0)
    if compM(X.m ,mObjetivo):
      print("==Busca melhor Escolha==")
      printR(X)
      return True
    else:
     
      filhos = X.darLuz()

      for i in filhos[:]:
        inf = False
        inA = False
        for fe in Fechado[:]:
          if compM(i.m,fe.m):
            inf = True
        for fa in Aberto[:]:
          if compM(i.m,fa.m):
            inA = True
        if not inA and not inf:
          i.h = heuristica(i,mObjetivo)
          Aberto.append(i)
          
      for i in filhos[:]:
        for fa in Aberto[:]:
          if compM(i.m,fa.m):
            if getProf(i) < getProf(fa):
              #muda estado na posição do antigo
              Aberto[Aberto.getIndex(fa)] = i

      
      for i in filhos[:]:
        for fe in Fechado[:]:
          if compM(i.m,fe.m):
            if getProf(i) < getProf(fe):
              Fechado.remove(fe)
              Aberto.append(i)

      for i in filhos:
        i.setId()

    Fechado.insert(0,X)
    Aberto = sorted(Aberto, key=lambda x:x.h, reverse=True)
  return False
   

#Matriz inicial
m = [[2,8,3],[1,6,4],[7,'#',5]]

#Objetivo
obj = [[1,2,3],[8,'#',4],[7,6,5]]

#Hill climb
R = HC(m, obj)

#Busca melhor Escolha
R = BME(m, obj,5)