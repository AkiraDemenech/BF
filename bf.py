


EXPAND = 'expand'
BLOCK = 'block'
CICLE = 'cicle'
CICLE_EXPAND = CICLE + EXPAND
ONCE = 'once'
BLOCK_ONCE = BLOCK + ONCE

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
		
	def __lshift__ (self, left = True, cicle = None, block = None, once = None, expand = None):
		if left < 0:
			self.__rshift__(-left, cicle, block, once, expand)
			return
			
		self.pointer -= left 
		
		if self.pointer < 0:
		
			if circle == None:
				circle = self.min_cicle
				
		
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
			
			if circle == None:
				circle = self.max_cicle
				
		
			max = (1 + cicle) * len(self.cells) 
		
			if self.pointer >= max:				
				if block == None:
					block = self.max_block
				if expand == None:
					expand = self.max_expand				
				
				if expand:
					while self.pointer % (len(self.cells) - 1) != 0:
						if block and len(self.cells) >= self.max: 							
							break
						self.cells.append(self.default)
					else:	
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