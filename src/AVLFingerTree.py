# No imports.
# AVLFingerTree:
# - Inserts always start searching from max_node (finger).
# - Adds insertion_sort(arr) that:
#     1) inserts the numbers in the given order (like insertion sort process),
#     2) does an in-order scan to output the sorted array,
#     3) returns (sorted_array, rebalance_ops, search_ops)
#
# Definitions requested:
# - search_ops: each time we "go over" (visit/inspect) a node during the insert search,
#               count +1 (this includes the start node, any nodes climbed, and any nodes descended).
# - rebalance_ops: count ONLY "height change events" during rebalancing walk upward
#                  (do NOT count rotations themselves; do NOT count height updates inside rotation helpers).
#
# Notes:
# - Duplicates are supported: we store a frequency counter in node.value (an int),
#   and output duplicates accordingly in the sorted array.

class AVLNode:
    __slots__ = ("key", "value", "left", "right", "parent", "height")

    def __init__(self, key, value=1, parent=None):
        self.key = key
        self.value = value  # frequency for duplicates
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1

    def __repr__(self):
        return "AVLNode(key=%r, h=%r, freq=%r)" % (self.key, self.height, self.value)


class AVLFingerTree:
    def __init__(self):
        self.root = None
        self.min_node = None
        self.max_node = None
        self.size = 0  # number of distinct keys (nodes)

        # stats (used by insertion_sort)
        self._search_ops = 0
        self._rebalance_ops = 0

    # ----------------------------
    # PUBLIC: insertion_sort
    # ----------------------------
    def insertion_sort(self, arr):
        """
        Insert numbers in the given order (like insertion sort processing),
        then in-order traverse to produce the sorted array.

        Returns:
            (sorted_array, rebalance_ops, search_ops)
        """
        # reset tree + stats
        self.root = None
        self.min_node = None
        self.max_node = None
        self.size = 0
        self._search_ops = 0
        self._rebalance_ops = 0

        # Insert each item (in the same order as insertion sort would process)
        for x in arr:
            self._insert_with_stats(x)

        # In-order scan => sorted
        out = []
        self._inorder_to_list(self.root, out)

        return (out, self._rebalance_ops, self._search_ops)

    # ----------------------------
    # INSERT (with stats)
    # ----------------------------
    def _insert_with_stats(self, key):
        if self.root is None:
            n = AVLNode(key, 1, parent=None)
            self.root = n
            self.min_node = n
            self.max_node = n
            self.size = 1
            return n

        start = self.max_node  # always start from max finger

        parent, direction, existing = self._find_parent_for_insert_from_max(start, key)
        if existing is not None:
            existing.value += 1  # duplicate
            return existing

        new_node = AVLNode(key, 1, parent=parent)
        if direction < 0:
            parent.left = new_node
        else:
            parent.right = new_node

        self.size += 1
        self._update_min_max_on_insert(new_node)

        # rebalance upward from parent
        self._rebalance_from(parent)
        return new_node

    def _update_min_max_on_insert(self, node):
        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node
        if self.max_node is None or node.key > self.max_node.key:
            self.max_node = node

    # ----------------------------
    # SEARCH from max finger (counts node visits)
    # ----------------------------
    def _find_parent_for_insert_from_max(self, start, key):
        """
        Returns (parent, direction, existing_node_or_None)
        direction: -1 => left, +1 => right

        Counts "search_ops" as number of nodes inspected:
          - start node counts
          - each climbed ancestor counts
          - each descended node counts
        """
        # visit start
        self._search_ops += 1

        # Fast path: append after current max
        if key > start.key:
            return (start, +1, None)

        if key == start.key:
            return (start, 0, start)

        # climb up from max until root (count every node we step onto)
        a = start
        while a.parent is not None and key < a.parent.key:
            a = a.parent
            self._search_ops += 1

        # now descend BST-search from 'a' (count every visited node)
        node = a
        parent = None
        direction = 0

        while node is not None:
            # node is being inspected
            # (If node==a, it was already counted above only if we climbed onto it;
            #  to keep consistent, count it here as well ONLY if it's not already counted.
            #  Simpler: always count inspections in this loop; but avoid double-count of 'a'
            #  by counting 'a' here only if 'a' != start and we didn't just count it.
            #  We'll implement a clean rule:
            #    - We count nodes when we ENTER them.
            #    - We already counted 'a' if it was reached by climbing OR if a==start.
            #    - So count here except for the first iteration.
            if node is not a:
                self._search_ops += 1

            parent = node
            if key == node.key:
                return (node, 0, node)
            elif key < node.key:
                direction = -1
                node = node.left
            else:
                direction = +1
                node = node.right

            # when we move to a child, that child will be counted when inspected;
            # we already handle counting upon entering (next loop iteration).

        return (parent, direction, None)

    # ----------------------------
    # AVL utilities
    # ----------------------------
    def _h(self, node):
        return node.height if node is not None else 0

    def _update_height_conditionally(self, node):
        """
        Update height of node.
        Count +1 iff:
         - height actually changes
         - |balance_factor(node)| < 2  (no rotation case)
        """
        old_h = node.height

        hl = self._h(node.left)
        hr = self._h(node.right)
        new_h = 1 + (hl if hl > hr else hr)

        bf = hl - hr

        if new_h != old_h and abs(bf) < 2:
            self._rebalance_ops += 1

        node.height = new_h


    def _update_height_no_count(self, node):
        """
        Update height but DO NOT count (used inside rotations).
        """
        hl = self._h(node.left)
        hr = self._h(node.right)
        node.height = 1 + (hl if hl > hr else hr)

    def _balance_factor(self, node):
        return self._h(node.left) - self._h(node.right)

    # ----------------------------
    # Rotations (do NOT count height changes here)
    # ----------------------------
    def _rotate_left(self, x):
        y = x.right
        if y is None:
            return x

        T2 = y.left

        # rotate
        y.left = x
        x.right = T2

        # parents
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x is x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

        x.parent = y
        if T2 is not None:
            T2.parent = x

        # update heights (no counting here)
        self._update_height_no_count(x)
        self._update_height_no_count(y)
        return y

    def _rotate_right(self, y):
        x = y.left
        if x is None:
            return y

        T2 = x.right

        # rotate
        x.right = y
        y.left = T2

        # parents
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        else:
            if y is y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x

        y.parent = x
        if T2 is not None:
            T2.parent = y

        # update heights (no counting here)
        self._update_height_no_count(y)
        self._update_height_no_count(x)
        return x

    # ----------------------------
    # Rebalancing after insert (count height changes only here)
    # ----------------------------
    def _rebalance_from(self, node):
        cur = node
        while cur is not None:
            # update height + conditional counting
            self._update_height_conditionally(cur)

            bf = self._balance_factor(cur)

            # rotations (NOT counted)
            if bf > 1:
                if self._balance_factor(cur.left) < 0:
                    self._rotate_left(cur.left)
                self._rotate_right(cur)

            elif bf < -1:
                if self._balance_factor(cur.right) > 0:
                    self._rotate_right(cur.right)
                self._rotate_left(cur)

            cur = cur.parent


    # ----------------------------
    # In-order traversal to list (handles duplicates via node.value)
    # ----------------------------
    def _inorder_to_list(self, node, out):
        if node is None:
            return
        self._inorder_to_list(node.left, out)
        # append duplicates
        freq = node.value
        while freq > 0:
            out.append(node.key)
            freq -= 1
        self._inorder_to_list(node.right, out)
