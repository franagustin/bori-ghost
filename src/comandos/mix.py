from funciones import lista_a_cadena, get_nick_avatar, borrar_repetidos
from random import randint
from discord import Embed

async def reverso(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	mensaje_sin_comando = lista_a_cadena(mensaje_separado, 1)
	await client.send_message(message.channel, mensaje_sin_comando[::-1])

async def decir(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	mensaje_sin_comando = lista_a_cadena(mensaje_separado, 1)
	if mensaje_sin_comando != "":
		await client.send_typing(message.channel)
		await client.delete_message(message)
		await client.send_message(message.channel, mensaje_sin_comando)

async def elegir(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	mensaje_sin_comando = lista_a_cadena(mensaje_separado, 1)
	if ";" in mensaje_sin_comando:
		mensaje_separado = mensaje_sin_comando.split(";")
	else:
		mensaje_separado = mensaje_sin_comando.split("|")
	if len(mensaje_separado) == 1:
		await client.send_message(message.channel, "Creo que eligiré... ``"+mensaje_separado[0]+
									"`` \nNo me tomes el pelo e_e **¡TIENES QUE DARME MÁS DE UNA OPCIÓN!**")
	else:
		opcion = randint(0, len(mensaje_separado)-1)
		await client.send_message(message.channel, mensaje_separado[opcion])

async def obtener_avatar(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	if len(message.mentions) == 0:
		avatar_embed = Embed(title="Avatar de {} ({}#{})".format(nick_autor, message.author.name, message.author.discriminator))
		avatar_embed.set_image(url=avatar_autor)
		avatar_embed.set_footer(text="Tú mismo lo pediste", icon_url=avatar_autor)
		await client.send_message(message.channel, embed=avatar_embed)
	else:
		for miembro in message.mentions:
			nick, avatar = get_nick_avatar(miembro)
			avatar_embed = Embed(title="Avatar de {} ({}#{})".format(nick, miembro.name, miembro.discriminator))
			avatar_embed.set_image(url=avatar)
			avatar_embed.set_footer(text="Este avatar fue pedido por {} ({}#{})".format(nick_autor,
									message.author.name, message.author.discriminator),
									icon_url=avatar_autor)
			await client.send_message(message.channel, embed=avatar_embed)