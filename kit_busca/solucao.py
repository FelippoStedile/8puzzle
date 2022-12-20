from collections import deque
from queue import PriorityQueue as pqueue

OBJETIVO = '12345678_'

class Nodo:
	"""
	Implemente a classe Nodo com os atributos descritos na funcao init
	"""
	def __init__(self, estado, pai, acao, custo):
		"""
		Inicializa o nodo com os atributos recebidos
		:param estado:str, representacao do estado do 8-puzzle
		:param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
		:param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
		:param custo:int, custo do caminho da raiz até este nó
		"""
		self.estado = estado
		self.pai = pai
		self.acao = acao
		self.custo = custo

	def __repr__(self) -> str:
		return repr(self.estado + ' ' + str(self.custo))


def moveEspaco(acao, estado, pos):
	if acao == 'acima':
		estado = estado[:pos] + estado[pos-3] + estado[pos+1:]
		estado = estado[:pos-3] + '_' + estado[pos-2:]
	elif acao == 'abaixo':
		estado = estado[:pos] + estado[pos+3] + estado[pos+1:]
		estado = estado[:pos+3] + '_' + estado[pos+4:]
	elif acao == 'esquerda':
		estado = estado[:pos] + estado[pos-1] + estado[pos+1:]
		estado = estado[:pos-1] + '_' + estado[pos:]
	else:
		estado = estado[:pos] + estado[pos+1] + estado[pos+1:]
		estado = estado[:pos+1] + '_' + estado[pos+2:]

	return (acao, estado)
		

def sucessor(estado):
	"""
	Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
	para cada ação possível no estado recebido.
	Tanto a ação quanto o estado atingido são strings também.
	:param estado:
	:return:
	"""
	pos = estado.rfind('_')
	estados = []
	if pos < 0:
		raise IndexError
	if pos not in [2, 5, 8]:
		# pode ir para a direita
		estados.append(moveEspaco('direita', estado, pos))	
	if pos < 6:
		# pode ir para baixo
		estados.append(moveEspaco('abaixo', estado, pos))	
	if pos > 2:
		# pode ir para cima
		estados.append(moveEspaco('acima', estado, pos))
	if pos not in [0, 3, 6]:
		# pode ir para a esquerda
		estados.append(moveEspaco('esquerda', estado, pos))
	return estados


def expande(nodo):
	"""
	Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
	Cada nodo do iterable é contém um estado sucessor do nó recebido.
	:param nodo: objeto da classe Nodo
	:return:
	"""
	filhos = []
	for index, tupla in enumerate(sucessor(nodo.estado)):
		filhos.append(Nodo(tupla[1], nodo, tupla[0], nodo.custo+1))
	return filhos

def search(explorados, fronteira, filho):

	for i in range(len(fronteira)):
		if fronteira[i].estado == filho.estado:
			return True
	for j in range(len(explorados)):
		if explorados[j].estado == filho.estado:
			return True
	return False

def searchHam(explorados, fronteira, filho):

	for i in range(fronteira.qsize()):
		if fronteira[i].estado == filho.estado:
			return True
	for j in range(len(explorados)):
		if explorados[j].estado == filho.estado:
			return True
	return False

def sobePais(nodo):
	caminho = deque([])
	while nodo.pai != None:
		caminho.appendleft(nodo.acao)
		nodo = nodo.pai
	caminho = list(caminho)
	return caminho

def bfs(estado):
	"""
	Recebe um estado (string), executa a busca em LARGURA e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	explorado = []
	fronteira = deque([])
	nodo = Nodo(estado, None, None, 0)
	fronteira.append(nodo)
	while len(fronteira):
		nodo = fronteira.popleft()
		explorado.append(nodo)
		if(nodo.estado == OBJETIVO):
			caminho = sobePais(nodo)
			return caminho
		else:
			filhos = deque(expande(nodo))
			while len(filhos):
				filho = filhos.popleft()
				if search(explorado, fronteira, filho)==False:
					fronteira.append(filho)
	return None


def dfs(estado):
	"""
	Recebe um estado (string), executa a busca em PROFUNDIDADE e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	explorado = []
	fronteira = deque([])
	nodo = Nodo(estado, None, None, 0)
	fronteira.append(nodo)
	while len(fronteira):
		nodo = fronteira.pop()
		explorado.append(nodo)
		if(nodo.estado == OBJETIVO):
			caminho = sobePais(nodo)
			return caminho
		else:
			filhos = deque(expande(nodo))
			while len(filhos):
				filho = filhos.pop()
				if search(explorado, fronteira, filho)==False:
					fronteira.append(filho)
	return None


def hamming(estado):
	contador = 0
	for i, j in zip(estado, OBJETIVO):
		if i != j:
			contador += 1
	return contador


def astar_hamming(estado):
	"""
	Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	explorado = []
	fronteira = pqueue()
	fronteira.put((hamming(estado), Nodo(estado, None, None, 0)))
	while fronteira.qsize():
		nodo = fronteira.get()
		explorado.append(nodo[1])
		if(nodo[1].estado == OBJETIVO):
			caminho = sobePais(nodo[1])
			return caminho
		else:
			filhos = deque(expande(nodo[1]))
			while len(filhos):
				filho = filhos.pop()
				if searchHam(explorado, fronteira, filho)==False:
					fronteira.put((hamming(filho.estado), filho))
	return None


def manhattan(estado):
	contador = 0
	for index, char in enumerate(estado):
		contador += abs(index - OBJETIVO.index(char))
	return contador


def astar_manhattan(estado):
	"""
	Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	explorado = []
	fronteira = pqueue()
	fronteira.put((manhattan(estado), Nodo(estado, None, None, 0)))
	while fronteira.qsize():
		nodo = fronteira.get()
		explorado += nodo
		if(nodo.estado == OBJETIVO):
			return explorado
		else:
			fronteira.put((manhattan(nodo.estado), nodo))
	return None
