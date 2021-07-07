from variables import whitelist

async def cerrar(client, message, *resto, prefijo=None):
	"""Comando "cerrar". Se encarga de cerrar el bot."""
	if message.author.id in whitelist:
		await client.send_typing(message.channel)
		await client.send_message(message.channel, "Bot cerrado.")
		await client.close()