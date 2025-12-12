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
		if is_virtual:
			self.left = None
			self.right = None
		else:
			self.left = AVLNode(-1, "", True)
			self.right = AVLNode(-1, "", True)
		self.parent = None
		self.height = 0 if not is_virtual else -1
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
		self._size = 0 #added field


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
		return self.search_from_node(key, self.root)
		

	def search_from_node(self, key, start_node): #helping func for search
		count = 0
		curr = start_node
		while curr.key != key: #regular BST search
			if not curr.is_real_node():
				return None, -1
			if key > curr.key:
				curr = curr.right
				count += 1
			else: #key < curr.key
				curr = curr.left
				count += 1
			
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
		curr = self.max_node()
		while curr.key > key: #move up until we find the correct subtree
			if curr.parent is None:
				break
			curr = curr.parent
			count += 1
		(found, edges) = self.search_from_node(key, curr) #search from the found subtree
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
		return self.insert_from_node(key, val, self.root)




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

	def insert_from_node(self, key, val, start_node): #helping func for insertions
		edges = 0
		new_node = AVLNode(key, val)
		curr = start_node
		if self.root is None: #check if tree is empty
			self.root = new_node
			self._size += 1
			return new_node, 0, 0

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
		self._size += 1
		self.update_heights(new_node) #fix heights after insertion
		rotations = self.rebalance_after_insert(key, new_node)
		
		return new_node, edges, rotations
    

	""" updates heights going up from the inserted node
	@type node: AVLNode
	@param node: the newly inserted node
	"""
	def update_heights(self, node):
		curr = node.parent
		while curr is not None:
			curr.height = 1 + max(curr.right.height, curr.left.height)
			curr = curr.parent
		return None


    
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
					#rotations += 2 what they said not to count
			elif balance_factor < -1: #right heavy
				if key > curr.right.key: #right-right case
					self.rotate_left(curr)
					rotations += 1
				else: #right-left case
					self.rotate_right(curr.right)
					self.rotate_left(curr)
					#rotations += 2 what they said not to count

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
		if self.root is None: #check if tree is empty
			new_node = AVLNode(key, val)
			self.root = new_node
			self._size += 1
			return new_node, 0, 0
		edges = 0
		curr = self.max_node()
		while curr.key > key: #move up until we find the correct subtree
			if curr.parent is None:
				break
			curr = curr.parent
			edges += 1
		(new_node, search_edges, rotations) = self.insert_from_node(key, val, curr) #insert from the found subtree
		edges += search_edges
		self.update_heights(new_node)
		return new_node, edges, rotations




	"""performs a rotation on the given unbalanced node
	@type node: AVLNode
	@param node: the unbalanced node
"""
	def rotate_left(self, node): #node is the unbalanced node 
		temp = node
		node = node.right
		node.parent = temp.parent
		temp.right = node.left
		if temp.right.is_real_node():
			temp.right.parent = temp
		node.left = temp
		if temp.parent is not None: #check if temp is not root
			if temp.parent.right == temp:
				temp.parent.right = node
			else:
				temp.parent.left = node
		else:
			self.root = node
		temp.parent = node
		self.update_heights(temp) #update heights starting from temp
		self.update_heights(node)#switch heights
		return None
#need to fix heights after rotation
	def rotate_right(self, node): #code is similar to rotate_left
		temp = node
		node = node.left
		node.parent = temp.parent
		temp.left = node.right
		if temp.left.is_real_node():
			temp.left.parent = temp
		node.right = temp
		if temp.parent is not None:
			if temp.parent.right == temp:
				temp.parent.right = node
			else:
				temp.parent.left = node
		else:
			self.root = node
		temp.parent = node
		self.update_heights(temp) #update heights starting from temp
		self.update_heights(node) #switch heights
		return None



	def update_heights_after_rotation(self, node): #updating heights after rotation using update_heights
		node.right.height = 1 + max(node.left.height, node.right.height)
		node.left.height = 1 + max(node.left.height, node.right.height)
		node.height = 1 + max(node.left.height, node.right.height)
		return None
				

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
		#handle edge cases
		if tree2._size + self._size == 0: #both trees are empty
			new_node = AVLNode(key, val)
			self.root = new_node
			self._size = 1
			return
		if self._size == 0: #self is empty
			tree2.insert(key, val)
			self.root = tree2.root
			self._size = tree2._size
			return
		if tree2._size == 0: #tree2 is empty
			self.insert(key, val)
			return

		new_node = AVLNode(key, val)
		#check which tree is bigger
		#start from the root of the bigger tree and go down the left/right spine until heights are equal
		#then insert new_node there and attach the smaller tree
		if self._size >= tree2._size: #self is bigger
			if key < self.root.key: #self's keys are larger
    
				curr = self.root 
				#go left until we find the correct spot to insert new_node
				while curr.left.height > tree2.root.height:
					curr = curr.left
				new_node.right = curr.left
				if new_node.right.is_real_node():
					new_node.right.parent = new_node
				new_node.left = tree2.root
				tree2.root.parent = new_node
				update_heights(new_node)
				new_node.parent = curr
				curr.left = new_node
				self._size += tree2._size + 1
    
			else: #tree2's keys are larger
				curr = self.root 
				#go right until we find the correct spot to insert new_node
				while curr.right.height > self.root.height:
					curr = curr.right
				new_node.left = curr.right
				if new_node.left.is_real_node():
					new_node.left.parent = new_node
				new_node.right = self.root
				self.root.parent = new_node
				update_heights(new_node)
				new_node.parent = curr
				curr.right = new_node
				tree2._size += self._size + 1

		else: #tree2 is bigger
			if key < tree2.root.key: #self's keys are larger				

				curr = tree2.root 
				#go left until we find the correct spot to insert new_node
				while curr.left.height > tree2.root.height:
					curr = curr.left
				new_node.right = curr.left
				if new_node.right.is_real_node():
					new_node.right.parent = new_node
				new_node.left = tree2.root
				tree2.root.parent = new_node
				update_heights(new_node)
				new_node.parent = curr
				curr.left = new_node
				self._size += tree2._size + 1


			else: #tree2's keys are larger
				
				curr = self.root 
				#go left until we find the correct spot to insert new_node
				while curr.right.height > self.root.height:
					curr = curr.right
				new_node.left = curr.right
				if new_node.left.is_real_node():
					new_node.left.parent = new_node
				new_node.right = self.root
				self.root.parent = new_node
				update_heights(new_node)
				new_node.parent = curr
				curr.right = new_node
				tree2._size += self._size + 1

			update_heights(new_node.parent)
			#rebalancing from new_node
			self.rebalance_after_insert(key, new_node)
			return


		# #help junc goes down the left/right spine and inserts new_node
		# def join_helper(small, big, new_node, side1, side2):
		# 	curr = small.root 
		# 	#go left until we find the correct spot to insert new_node
		# 	while curr.side1.height > small.root.height:
		# 		curr = curr.side1
		# 	new_node.side2 = curr.side1
		# 	if new_node.side2.is_real_node():
		# 		new_node.side2.parent = new_node
		# 	new_node.side1 = small.root
		# 	small.root.parent = new_node
		# 	update_heights(new_node)
		# 	new_node.parent = curr
		# 	curr.side1 = new_node
		# 	big._size += small._size + 1
		# 	return
			


	# def merge (self , tree2, curr, new_node): #helper function for join
	# 	while curr.left.height > new_node.left.height: #find the correct spot to insert new_node
	# 		curr = curr.left
	# 	new_node.right = curr
	# 	update_heights(new_node)
	# 	new_node.parent = curr.parent
	# 	curr.parent.left = new_node
	# 	curr.parent = new_node
	# 	self._size += tree2._size + 1
	# 	update_heights(new_node.parent)
	# 	return self


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node): #split using join and delete recursively
		return self.split_rec(self.root, node.key)

			

	def split_rec(self, node, key): #helper function for split
		if not node.is_real_node():
			return AVLTree(), AVLTree()
		if node.key < key:
			left, right = self.split_rec(node.right, key)
			t_org_l = AVLTree()
			t_org_l.root = node.left
			if node.is_real_node():
				self.join(t_org_l, left, node.key, node.value)
			return node, right
		elif node.key > key:
			left, right = self.split_rec(node.left, key)
			t_org_r = AVLTree()
			t_org_r.root = node.right
			if node.is_real_node():
				self.join(t_org_r, right, node.key, node.value)
			return left, node
		else: #node.key == key
			tree_small = AVLTree()
			tree_small.root = node.left
			if node.left:
				node.left.parent = None
				pass
			tree_big = AVLTree()
			tree_big.root = node.right
			if node.right:
				node.right.parent = None
				pass
			return tree_small, tree_big
	

	# def successor(self, node):
	# 	if node.right.is_real_node(): #go right once and then left until we reach the min
	# 		curr = node.right
	# 		while curr.left.is_real_node():
	# 			curr = curr.left
	# 		return curr
	# 	curr = node
	# 	while curr.parent is not None and curr.parent.right == curr: #go up until we find a parent that is a left child
	# 		curr = curr.parent
	# 	return curr.parent #could be None if no successor exists

	# def predecessor(self, node):
	# 	if node.left.is_real_node(): #go left once and then right until we reach the max
	# 		curr = node.left
	# 		while curr.right.is_real_node():
	# 			curr = curr.right
	# 		return curr
	# 	curr = node
	# 	while curr.parent is not None and curr.parent.left == curr: #go up until we find a parent that is a right child
	# 		curr = curr.parent
	# 	return curr.parent #could be None if no predecessor exists

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
		return self._size	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self): #simple
		return self.root #None if empty