#id1: 316175827
#name1: Maayan Oz
#username1: maayanoz
#id2: 211627658
#name2: Amir Arbiv
#username2: amirarbiv1


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value, is_virtual=False):
		self.key = key
		self.value = value
		self.left = AVLNode(-1, "", True) #virtual nodes
		self.right = AVLNode(-1, "", True) #like they asked in the instructions
		self.parent = None
		self.height = -1
		"""Indicates whether the node is a virtual node
		@type: bool
		"""
		self.is_virtual = is_virtual

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return not self.is_virtual


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self.size = 0 #added fields
#		self.lst = [] #list of max nodes for finger search
#		self.max_node = self.lst[0] if self.lst else None
#		self.min_node = self.lst[-1] if self.lst else None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		if self.root is None:
			return None, -1
		#if key > self.max_node.key or key < self.min_node.key: #check if key is out of bounds
		#	return None, -1
		count = 0
		curr = self.root
		while curr.key != key: #regular BST search
			if key > curr.key:
				if curr.right.is_real_node():
					curr = curr.right
					count += 1
				else:
					return None, -1
			else: #key < curr.key
				if curr.left.is_real_node():
					curr = curr.left
					count += 1
				else:
					return None, -1
			
		return curr, count+1




	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key): 
		if self.root is None: #check if tree is empty
			return None, -1
		#if key > self.max_node.key or key < self.min_node.key: #check if key is out of bounds
			#return None, -1

		count = 0
		curr = self.max_node
		while curr.key > key: #move up until we find the correct subtree
			curr = curr.parent
			count += 1
		(found, edges) = self.search(key) #search from the found subtree
		if found is not None:
			return found, edges + count

		return None, -1


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		return self.insert_from_node(self, key, val, self.root)




	"""inserts a new node into the dictionary with corresponding key and value, starting at a given node
	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@type start_node: AVLNode
	@param start_node: the node from which the insertion starts
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
"""

	def insert_from_node(self, key, val, start_node):
		edges = 0
		new_node = AVLNode(key, val)
		curr = start_node
		if self.root is None: #check if tree is empty
			self.root = new_node
			self.size += 1
			return new_node, edges, rotations

		while True: #regular BST insert
			if key < curr.key:
				if curr.left.is_real_node():
					curr = curr.left
					edges += 1
				else:
					curr.left = new_node
					new_node.parent = curr
					edges += 1
					break
			else: #key > curr.key
				if curr.right.is_real_node():
					curr = curr.right
					edges += 1
				else:
					curr.right = new_node
					new_node.parent = curr
					edges += 1
					break
		self.size += 1
		rotations = self.rebalance_after_insert(key, new_node)
		
		return new_node, edges, rotations
    




    
""" rotates and rebalances the tree after insertion

	@type key: int
	@param key: key of the newly inserted node
	@type node: AVLNode
	@param node: the newly inserted node
	@rtype: int
	@returns: number of rotations performed during rebalancing
"""

	def rebalance_after_insert(self, key, node): #rebalancing and updating heights going up from the inserted node
		curr = node.parent
		rotations = 0
		while curr is not None:
			left_height = curr.left.height if curr.left.is_real_node() else -1
			right_height = curr.right.height if curr.right.is_real_node() else -1
			curr.height = 1 + max(left_height, right_height)

			balance_factor = left_height - right_height

			if balance_factor > 1: #left heavy
				if key < curr.left.key: #left-left case
					self.rotate_right(curr)
					rotations += 1
				else: #left-right case
					self.rotate_left(curr.left)
					self.rotate_right(curr)
					rotations += 2
			elif balance_factor < -1: #right heavy
				if key > curr.right.key: #right-right case
					self.rotate_left(curr)
					rotations += 1
				else: #right-left case
					self.rotate_right(curr.right)
					self.rotate_left(curr)
					rotations += 2

			curr = curr.parent
		return rotations




	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self): #recursive inorder traversal
		if self.root is None: #check if tree is empty
			return []
		res = []
		def inorder(curr): #inorder traversal
			if curr.is_real_node():
				inorder(curr.left)
				res.append((curr.key, curr.value))
				inorder(curr.right)
		inorder(self.root)
		return res


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		if self.root is None: #check if tree is empty
			return None
		curr = self.root
		while curr.right.is_real_node(): #go right until we reach the max
			curr = curr.right
		return curr

	"""returns the node with the minimal key in the dictionary

	@rtype: AVLNode
	@returns: the minimal node, None if the dictionary is empty
	"""
	def min_node(self):
		if self.root is None: #check if tree is empty
			return None
		curr = self.root
		while curr.left.is_real_node(): #go left until we reach the min
			curr = curr.left
		return curr

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self): #simple
		return self.size	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self): #simple
		if self.root is not None:
			return self.root
		return None
