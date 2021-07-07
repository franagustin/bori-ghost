import listas
from funciones import get_nick_avatar, get_prefijos

async def procesar_comandos(client, message):
	if message.author.bot:
		return
	comando = False
	lista_prefijos = get_prefijos(message)
	for prefijo in lista_prefijos:
		if comando == False:
			if message.content.startswith(prefijo):
				usa = prefijo
				comando = True
	if comando:
		mensaje_separado = message.content.split("\n")
		mensaje_separado = " \n ".join(mensaje_separado)
		mensaje_separado = mensaje_separado.split(" ")
		if mensaje_separado[0][len(usa)::] in listas.coms:
			nick_autor, avatar_autor = get_nick_avatar(message.author)
			await listas.coms[mensaje_separado[0][len(usa)::]](client, message, nick_autor, avatar_autor, mensaje_separado, prefijo=usa)
		elif message.content.lower()[len(usa)::] in listas.coms:
			await listas.coms['ciérrate sésamo'](client, message)
	if message.mention_everyone:
		pass
		"""
		await client.send_message(message.channel, "¿Qué te pasa, hijo de puta? ¿Por qué me mencionas? Esto es poco profesional, ya estoy harto."+
													"\nhttps://media.discordapp.net/attachments/337854421876736003/474381150245224448/9k.png")
		"""
