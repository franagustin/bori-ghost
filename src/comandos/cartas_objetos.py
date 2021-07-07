class naipe:
	def __init__(self, palo, numero, emoji, t_posicion, e_valor):
		self.palo = palo
		self.numero = numero
		self.emoji = emoji
		self.t_posicion = t_posicion
		self.e_valor = e_valor

espada_1 = naipe("Espada", 1, "espada1", 1, 1)
basto_1 = naipe("Basto", 1, "basto1", 2, 1)
espada_7 = naipe("Espada", 7, "espada7", 3, 7)
oro_7 = naipe("Oro", 7, "oro7", 4, 7)
espada_3 = naipe("Espada", 3, "espada3", 5, 3)
basto_3 = naipe("Basto", 3, "basto3", 5, 3)
oro_3 = naipe("Oro", 3, "oro3", 5, 3)
copa_3 = naipe("Copa", 3, "copa3", 5, 3)
espada_2 = naipe("Espada", 2, "espada2", 6, 2)
basto_2 = naipe("Basto", 2, "basto2", 6, 2)
oro_2 = naipe("Oro", 2, "oro2", 6, 2)
copa_2 = naipe("Copa", 2, "copa2", 6, 2)
oro_1 = naipe("Oro", 1, "oro1", 7, 1)
copa_1 = naipe("Copa", 1, "copa1", 7, 1)
espada_rey = naipe("Espada", 12, "espadarey", 8, 10)
basto_rey = naipe("Basto", 12, "bastorey", 8, 10)
oro_rey = naipe("Oro", 12, "ororey", 8, 10)
copa_rey = naipe("Copa", 12, "coparey", 8, 10)
espada_caballo = naipe("Espada", 11, "espadacaballo", 9, 9)
basto_caballo = naipe("Basto", 11, "bastocaballo", 9, 9)
oro_caballo = naipe("Oro", 11, "orocaballo", 9, 9)
copa_caballo = naipe("Copa", 11, "copacaballo", 9, 9)
espada_sota = naipe("Espada", 10, "espadasota", 10, 8)
basto_sota = naipe("Basto", 10, "bastosota", 10, 8)
oro_sota = naipe("Oro", 10, "orosota", 10, 8)
copa_sota = naipe("Copa", 10, "copasota", 10, 8)
basto_7 = naipe("Basto", 7, "basto7", 11, 7)
copa_7 = naipe("Copa", 7, "copa7", 11, 7)
espada_6 = naipe("Espada", 6, "espada6", 12, 6)
basto_6 = naipe("Basto", 6, "basto6", 12, 6)
oro_6 = naipe("Oro", 6, "oro6", 12, 6)
copa_6 = naipe("Copa", 6, "copa6", 12, 6)
espada_5 = naipe("Espada", 5, "espada5", 13, 5)
basto_5 = naipe("Basto", 5, "basto5", 13, 5)
oro_5 = naipe("Oro", 5, "oro5", 13, 5)
copa_5 = naipe("Copa", 5, "copa5", 13, 5)
espada_4 = naipe("Espada", 4, "espada4", 14, 4)
basto_4 = naipe("Basto", 4, "basto4", 14, 4)
oro_4 = naipe("Oro", 4, "oro4", 14, 4)
copa_4 = naipe("Copa", 4, "copa4", 14, 4)

baraja = [espada_1, espada_2, espada_3, espada_4, espada_5, espada_6, espada_7, espada_sota, espada_caballo, espada_rey,
			oro_1, oro_2, oro_3, oro_4, oro_5, oro_6, oro_7, oro_sota, oro_caballo, oro_rey,
			basto_1, basto_2, basto_3, basto_4, basto_5, basto_6, basto_7, basto_sota, basto_caballo, basto_rey,
			copa_1, copa_2, copa_3, copa_4, copa_5, copa_6, copa_7, copa_sota, copa_caballo, copa_rey]
usadas = []