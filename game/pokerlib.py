primes = (2,3,4,7,11,13,17,19,23,29,31,37,41)

def init_deck():
	n    = 0
	suit = 0x8000
	deck = []

	for i in range(4):
		for j in range(13):
			deck.append(primes[j] | (j << 8) | suit | (1 << (16 + j)))
	
	return deck

