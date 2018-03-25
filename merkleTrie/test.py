from merkleKit import MerkleTrie

mt = MerkleTrie()
print(mt.get_is_ready)
mt.insert_hash('1245789')
mt.show_trie(mt.root_node, 0)
