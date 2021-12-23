


EXPAND = 'expand'
BLOCK = 'block'
CICLE = 'cicle'
CICLE_EXPAND = CICLE + EXPAND
ONCE = 'once'
BLOCK_ONCE = BLOCK + ONCE

ADD = '+'
SUB = '-'
INC = '>'
DEC = '<'

WHILE = '['
END = ']'

PRINT = '.'
INPUT = ','

BF = {ADD: lambda bf: bf.__add__(), SUB: lambda bf: bf.__sub__(), 
INC: lambda bf: bf.__rshift__(),	DEC: lambda bf: bf.__lshift__(), 
WHILE: lambda bf: bf.loop_open(), END: lambda bf: bf.loop_close(),
INPUT: lambda bf: bf.input(),	PRINT: lambda bf: bf.print()}

class Brainfuck:
	
	def __init__ (self, init = 0, cells = None, default = False, overflow = True, mod = 256, max = 30000, max_action = EXPAND, neg_action = CICLE_EXPAND):
		if cells == None:
			cells = []
		if not len(cells):	
			cells.append(default)
		
		self.cells = cells	
		
		self.default = default 
		
		self.overflow = overflow
		self.mod = mod
		
		self.pointer = init 
		
		self.min_action = str(neg_action).lower()		
		self.max_action = str(max_action).lower() 
		self.max = max
		
		
		self.max_cicle = CICLE in self.max_action
		self.max_expand = EXPAND in self.max_action
		self.max_block = BLOCK in self.max_action or not (self.max_cicle or self.max_expand)  
		self.max_once = self.max_block and ONCE in self.max_action		
		
		
		self.min_cicle = CICLE in self.min_action
		self.min_expand = EXPAND in self.min_action
		self.min_block = BLOCK in self.min_action or not (self.min_cicle or self.min_expand)
		self.min_once = self.min_block and ONCE in self.min_action  

		self.loop_stack = self.progr = self.buffer = []
		self.instruction = False 
		
		
	def __lshift__ (self, left = True, cicle = None, block = None, once = None, expand = None):
		if left < 0:
			self.__rshift__(-left, cicle, block, once, expand)
			return
			
		self.pointer -= left 
		
		if self.pointer < 0:
		
			if cicle == None:
				cicle = self.min_cicle
				
		
			min = - cicle * len(self.cells) 
			
			if self.pointer < min:
			
				if block == None:
					block = self.min_block
				if expand == None:
					expand = self.min_expand				
				
				if expand:
					while self.pointer % len(self.cells) != 0:
						if block and len(self.cells) >= self.max: 							
							break
						self.cells.insert(0, self.default)
					else:	
						return
				
				if block:	
					if once == None:
						once = self.min_once
					self.pointer = min * once
				else:		
					self.pointer %= len(self.cells)
					 	
				
	def __rshift__ (self, right = True, cicle = None, block = None, once = None, expand = None):
		if right < 0:
			self.__lshift__(-right, cicle, block, once, expand)
			return
			
		self.pointer += right			
		
		if self.pointer >= len(self.cells):	
			
			if cicle == None:
				cicle = self.max_cicle
				
		
			max = (1 + cicle) * len(self.cells) 
		
			if self.pointer >= max:				
				if block == None:
					block = self.max_block
				if expand == None:
					expand = self.max_expand				
				
				if expand:
					while len(self.cells) < self.max or not block:
						self.cells.append(self.default)						
						if self.pointer % (len(self.cells) - 1) == 0: 							
							return						
						
				
				if block:		
					if once == None:
						once = self.max_once
					self.pointer = (max - 1) * once
				else:	
					self.pointer %= len(self.cells)
			 			
	def __add__ (self, incr = True, index = None, overflow = None, mod = None):			
		v = self.__getitem__(index) + incr
		if overflow == None:
			overflow = self.overflow
		if overflow:	
			if mod == None:
				mod = self.mod
			v %= mod	
		self.__setitem__(value = v)		
		return v 
		
	def __sub__ (self, decr = True, index = None, overflow = None, mod = None):					
		return self.__add__(-decr, index, overflow, mod)	
		
	def __isub__ (self, decr = True, index = None, overflow = None, mod = None):	
		return self.__sub__(decr, index, overflow, mod)
		
	def __iadd__ (self, incr = True, index = None, overflow = None, mod = None):	
		return self.__add__(incr, index, overflow, mod)		
		
	def __getitem__ (self, index = None):			
		if type(index) != int:
			index = self.pointer
		
		return self.cells[index % len(self.cells)]	
		
	def __setitem__ (self, index = None, value = None):	
		if type(index) != int:
			index = self.pointer
		if value == None:
			value = self.default	
		
		self.cells[index % len(self.cells)] = value	

	def loop_close (self):
		try:
			self.instruction = self.loop_stack.pop()
		except IndexError:	
			return

	def loop_open (self, open = WHILE, close = END):

		i = not self.__getitem__()
		if i:				
			if type(close) == int:		
				self.instruction = close
			else:	
				while i:
					self.instruction += 1

					c = self.instruction % len(self.progr)
					if c == 0:
						break 

					i += 1 if (self.progr[c] == open) else -(self.progr[c] == close) 							
			
			return  
		self.loop_stack.append(self.instruction)



	def start (self, progr, init = False):	
		self.progr = progr
		self.loop_stack.clear()
		self.instruction = init 

	def step (self):	
		if self.instruction >= len(self.progr):
			raise StopIteration(f'{self.instruction} >= {len(self.progr)}')
		return self.__next__()

	 

	def __next__ (self, progr = None, i = None, brainfuck = BF):
		if i == None:
			i = self.instruction
		if progr == None:	
			progr = self.progr

		try:
			brainfuck[progr[i%len(progr)]](self)	
		except KeyError:	
			pass
		self.instruction = i + 1 

		return self.instruction 



	def __iter__ (self, brainfuck = BF):	
		

		while self.instruction < len(self.progr):	
			yield self.__next__(brainfuck=brainfuck) 

	#	self.loop_stack = self.instruction = None


	def print (self):
		print(end = chr(self.__getitem__()))

	def input (self):	
		if not len(self.buffer): 
			self.buffer = list(input())
			self.buffer.append('\n')
		self.__setitem__(value = ord(self.buffer.pop(0)))	





		