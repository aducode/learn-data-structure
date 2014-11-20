#!/usr/bin/python
#-*- coding:utf-8 -*-
import random
import types
class Node(object):
	def __init__(self, key=None, value=None, next=None):
		self.key=key
		self.value=value
		self.next=next

class SkipList(object):
	def __init__(self, level=0):
		self.level = level
		self.tail = Node()
		self.head = Node()
		self.head.next = list()
		self.head.next.append(self.tail) #作为tail

	def build(self, iterator):
		if iterator is types.DictType:
			for k, v in iterator.items():
				self.set(k,v)
		elif hasattr(iterator, '__iter__') or isinstance(iterator, (types.StringTypes, types.UnicodeType)):
			i=0
			for v in iterator:
				self.set(i,v)
				i += 1
			
	def get(self, key):	
		node = self._get_node(key)
		if node is None:
			return None
		return node.value

	def _get_node(self, key):
		level = self.level
		top_head = self.head.next[level]
		pre_top_head = self.head
		while True:
			if top_head == self.tail or top_head.key > key:
				level -= 1
				if level < 0:
					return None
				top_head = pre_top_head.next[level]
			elif top_head.key == key:
				return top_head
			else:
				pre_top_head = top_head
				top_head = top_head.next[level]

	def set(self, key, value):
		#先查找
		update = list()
		level = self._random_level()
		for i in xrange(level+1):
			if i <= self.level:
				p = self.head
				while p.next[i].key is not None:
					if p.next[i].key == key:
						p.next[i].value = value
						return False
					elif p.next[i].key < key:
						p = p.next[i]
					else:
						break
				update.append(p)
			else:
				self.level = level
				self.head.next.append(self.tail)
				update.append(self.head)
		
		new_node = Node(key, value, [])
		for  i in xrange(level+1):
			p = update[i]
			new_node.next.append(p.next[i])
			p.next[i] = new_node
		
		return True

			
	def remove(self, key):
		for i in xrange(self.level-1, -1, -1):
			h = self.head
			while h.next[i].key is not None:
				if h.next[i].key < key:
					h = h.next[i]
				elif h.next[i].key == key:
					found_node = h.next[i]
					h.next[i] = h.next[i].next[i]
					del found_node.next[i]
				else:
					break

	def _random_level(self):
		rl = 0
		while random.randint(0,1):
			rl += 1
		if rl > self.level + 1:
			rl = self.level + 1
		return rl

	def visit(self, level=0):
		head = self.head
		while head.next[level].key is not None:
			yield (head.next[level].key, head.next[level].value)
			head = head.next[level]
	def all(self):
		return self.visit()
	
	def top(self):
		return self.visit(self.level)

if __name__ == '__main__':
	print 'Test SKIP LIST'
	skip_list = SkipList()
	skip_list.build('abcdefghigklmnopqrstuvwxyz0123456789')	
	skip_list.set(1110,'abc')
	skip_list.set(11111,'cde')
	skip_list.set(2234,'123')
	skip_list.set(31451,'000')
	skip_list.set(1000,10000)
	for l in xrange(skip_list.level, -1 , -1):
		print 'LEVEL[%d] items are:' % l
		for k,v in skip_list.visit(l):
			print '%s=%s' % (k, v)
	print skip_list.get(31451)
	print 'BEFORE DELETE ...'
	print skip_list.get(1000)
	skip_list.remove(1000)
	print 'AFTER DELETE ...'
	print skip_list.get(1000)
	for k, v in skip_list.all():
		print '%s=%s' % (k, v)
