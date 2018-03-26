from merkleKit import MerkleTrie

mt1 = MerkleTrie()
mt2 = MerkleTrie()
trees = [mt1, mt2]

print(mt1.get_is_ready)
mt1.insert_hash('1245789', {'greetings':'hello'})
mt1.insert_hash('124789', {'greetings':'hello'})
mt1.insert_hash('2315789', {'greetings':'hello'})
mt1.insert_hash('455789', {'greetings':'hello'})

mt2.initiate_copy(mt1)
mt.show_trie(mt.root_node, 0)

