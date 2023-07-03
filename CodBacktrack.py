#Cristian, Guido e João Pedro Padoan

#Resolve Cacheiro viajante sem se preocupar com a distância, logo se passar um objetivo que não seja ele mesmo vai percorrer todos os grafos mesmo assim

class Estado:
  def __init__(self,nome, ind):#mDist
    self.nome = nome
    #self.mDist = mDist
    self.filhos = []
    self.ind = ind
  def darLuz(self,filhos):
    self.filhos = filhos


A = Estado('A',0)#[-1, 100, 125, 100, 75]
B = Estado('B',1)#[100, -1, 50, 75, 125]
C = Estado('C',2)#[125, 50, -1, 100, 125],
D = Estado('D',3)#[100, 75, 100, -1, 50],
E = Estado('E',4)#[75, 125, 125, 50, -1],

A.darLuz([B,C,D,E])
B.darLuz([A,C,D,E])
C.darLuz([A,B,D,E])
D.darLuz([A,B,C,E])
E.darLuz([A,B,C,D])

#Checa se passou por todos os elementos
def caminhoCheio(lv,tam):
  if len(lv) < 5:
    return False
  return True

#checa se filhos estão no LNE
def ntfilhos(f,le):
  cont = 0
  for i in f:
    if i not in le:
      continue
    else:
      cont+=1
  if cont == len(f):
    return True
  return False

def Busca_Retrocesso(G,Inicial,Obj):
  tam = len(G)
  loop = False
  if Obj == Inicial:
    loop = True

  LE = [Inicial]
  LNE = [Inicial]
  BSS = []
  EC = Inicial

  #Enquanto LNE não está vazio
  while(LNE):
    #Termina programa caso todos caminhos tenham sido percorridos e 
    if loop and caminhoCheio(LE,tam) and Obj in EC.filhos:
      LE.insert(0,Obj)
      return LE
    elif not loop and EC == Obj: 
      return LE
    print(ntfilhos(EC.filhos,LE))
    if not EC.filhos or ntfilhos(EC.filhos,LE):
      while ((LE) and EC == LE[0]):
        print('AAAAA')
        #Marca caminho removido como usado
        #used[EC.ind] = True
        BSS.insert(0,EC)
        LE.pop(0)
        LNE.pop(0)
        if LNE:
          EC = LNE[0]
      LE.insert(0,EC)
    else:
      #LNE.pop(0)
      #for i in range(max, 0, -1):
      for h in range(len(EC.filhos)-1,-1,-1):
        j = EC.filhos[h]
        #Caso filho não estejea no caminho atual vai coloca-lo no começo de LNE
        if j in LNE and (j not in LE):
          LNE.remove(j)
        if (j not in LE) and (j not in LNE) and (j not in BSS):
              LNE.insert(0,j)
    
      for h in LNE:
        print(h.nome)
      EC = LNE[0]
      LE.insert(0,EC)
  return False



#Parametros
Gs = [A,B,C,D,E]
ini = A
Obj = C

#Resposta
R = Busca_Retrocesso(Gs,ini,Obj)
print("RESPOSTA FINAL PRO COMECO::")
if R != False:
  for i in R:
    print(i.nome)
else:
  print(R)