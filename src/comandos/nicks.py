import re
from funciones import borrar_repetidos

async def manejar_apodos(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	if message.author in message.mentions and message.author.server_permissions.change_nickname:
		mencion = re.search("<@!?{}>".format(message.author.id), message.content)
		i = mensaje_separado.index(mencion.group())+1
		nuevo_apodo = ""
		while i < len(mensaje_separado):
			if not re.search("<@!?[0-9]+>", mensaje_separado[i]):
				nuevo_apodo += " "+mensaje_separado[i]
				i += 1
			else:
				i = len(mensaje_separado)
		nuevo_apodo = borrar_repetidos(nuevo_apodo, " ")
		if nuevo_apodo == "":
			nuevo_apodo = None
		elif len(nuevo_apodo) > 32:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, "¡Tu nuevo apodo es demasiado largo! Debe tener **32 carácteres** o menos.")
			return
		await cambiar_apodo(client, message, message.author, nuevo_apodo)
	if message.author.server_permissions.manage_nicknames:
		for miembro in message.mentions:
			mencion = re.search("<@!?{}>".format(miembro.id), message.content)
			i = mensaje_separado.index(mencion.group())+1
			nuevo_apodo = ""
			while i < len(mensaje_separado):
				if not re.search("<@!?[0-9]+>",mensaje_separado[i]):
					nuevo_apodo += " "+mensaje_separado[i]
					i += 1
				else:
					i = len(mensaje_separado)
			nuevo_apodo = borrar_repetidos(nuevo_apodo, " ")
			if nuevo_apodo == "":
				nuevo_apodo = None
			elif len(nuevo_apodo) > 32:
				await client.send_typing(message.channel)
				await client.send_message(message.channel, "¡El nuevo apodo es demasiado largo! Debe tener **32 carácteres** o menos.")
				return
			await cambiar_apodo(client, message, miembro, nuevo_apodo)
	elif not message.author.server_permissions.manage_nicknames:
		mensaje_permisos = """"Dame un momento... ¡Listo!\n...\n...\n JA JA JA Ni lo creas, no tienes los permisos suficientes para cambiar apodos. Fue un buen intento, igualmente, {}. ¡Ánimo!"""
		await client.send_typing(message.channel)
		await client.send_message(message.channel, mensaje_permisos.format(message.author.mention))

async def cambiar_apodo(client, message, miembro, apodo):
	mensaje = "El nuevo apodo para *{}#{}* es **{}**"
	await client.change_nickname(miembro, apodo)
	await client.send_typing(message.channel)
	await client.send_message(message.channel, mensaje.format(miembro.name, miembro.discriminator, miembro.display_name))