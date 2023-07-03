#Cristian, Guido e João Padoan


globalid = 1

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

  def setId(self):
    global globalid
    self.id = globalid
    globalid+=1
  
  #Adiciona filho criado na lista
  def checaF(self, f, Tudosf):
    #global globalid
    #if self.pai == None or not compM(f.m,self.pai.m):
    Tudosf.append(f)
    #else:
      #globalid-=1

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
    self.filhos = Tudosf
    return Tudosf
    
  
#Busca em Largura
def bfs(mInicial,mObjetivo):
  global globalid
  globalid = 1
  Inicial = EstadoProff(None,mInicial)
  Inicial.setId()
  Aberto = [Inicial]
  Fechado = []
  while Aberto:
    X = Aberto[0]
    Aberto.pop(0)
    #print("ABRINDO "+str(X.id)+":")
    #printm(X.m)
    if compM(X.m ,mObjetivo):
      print("==BUSCA LARGURA==")
      printR(X)
      return True
    else:
     
      filhos = X.darLuz()
      
      Fechado.insert(0,X)
      
      for i in filhos[:]:
        for fe in Fechado[:]:
          if compM(i.m,fe.m):
            filhos.remove(i)
      for i in filhos[:]:
        for fa in Aberto[:]:
          if compM(i.m,fa.m):
            filhos.remove(i)

      #Caso algum filho tenha sido removido por estar duplicado atualiza o indice dos filhos criados antes
      for i in filhos:
        i.setId()

      ##Caso a busca seja pelo lado esquerdo esse é usado
      filhos.reverse()
      
      for i in filhos:
        Aberto.append(i)
        #print(i.id)
        #printm(i.m)
      
  return False

#Checa se chegou ao limite
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
  print("Resultado: "+ str(aux.id)+"\nProfundidade: "+str(getProf(aux)))
  
  printm(aux.m)
  while(aux.pai != None):
    aux = aux.pai
    print("filho de " + str(aux.id))
    printm(aux.m)

#Busca em Profundidade
def DFS(mInicial,mObjetivo,lim): 
  global globalid
  globalid = 1
  Inicial = EstadoProff(None,mInicial) 
  Inicial.setId()
  Aberto = [Inicial]
  Fechado = []
  
  while Aberto:
    
    X = Aberto[0]
    while profLim(X,lim):
      Aberto.pop(0)
      X = Aberto[0]
    Aberto.pop(0)
    #rint("ABRINDO "+str(X.id)+":")
    #printm(X.m)
    if compM(X.m ,mObjetivo):
      print("==BUSCA PROFUNDIDADE==")
      printR(X)
      return True
    else:
     
      filhos = X.darLuz()
      
      Fechado.insert(0,X)

      for i in filhos[:]:
        for fe in Fechado[:]:
          if compM(i.m,fe.m):
            filhos.remove(i)
      for i in filhos[:]:
        for fa in Aberto[:]:
          if compM(i.m,fa.m):
            filhos.remove(i)

      #Caso algum filho tenha sido removido por estar duplicado atualiza o indice dos filhos criados antes
      for i in filhos:
        i.setId()

      ##Caso a busca seja pelo lado esquerdo esse é usado
      #filhos.reverse()

      #Adiciona filhos aa aberto e printa seu id e matriz
      for i in filhos:
        Aberto.insert(0,i)
        #print(i.id)
        #printm(i.m)
      
  return False
   

#Matriz inicial
m = [[2,8,3],[1,6,4],[7,'#',5]]

#Objetivo
obj = [[1,2,3],[8,'#',4],[7,6,5]]

#Profundidade
R = DFS(m, obj,5)

#Largura
R = bfs(m, obj)