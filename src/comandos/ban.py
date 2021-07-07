import discord
import re
from variables import pie_texto, unban_titulo, del_descripcion, ban_kick_color, unban_color, frown_usuario, un_usuario
from funciones import get_mute_role, crear_embed, borrar_repetidos
from discord import Forbidden

async def ban(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	"""Comando "ban" y "kick". Bannea o expulsa a uno o más usuarios especificando una razón (individual para cada uno).
		Envía un mensaje al servidor por cada usuario baneado o kickeado y, también, uno a cada usuario avisándole
		e incluyendo el motivo (si fue especificado).
		Parámetros:
			-Usuario (mención): miembro del servidor que se quiere bannear/kickear.
			-Razón: razón por la cual se lo excluye del servidor.
		Sintaxis:
			usuario (razón usuario razón usuario razón usuario razón usuario razón)*
			* = opcionales."""
	if message.mention_everyone == False: #Evita banear a todos los usuarios
		if not message.author.server_permissions.ban_members:
			return
		for miembro in message.mentions:
			if message.author.top_role.position > miembro.top_role.position:
				razon = ""
				mencion = re.search("<@!?{}>".format(miembro.id), message.content)
				i = mensaje_separado.index(mencion.group())+1
				while i < len(mensaje_separado):
					if discord.utils.get(message.mentions, id = mensaje_separado[i][2:len(mensaje_separado[i])-1:]) == None:
						razon += " "+mensaje_separado[i]
						i += 1
					else:
						i = len(mensaje_separado)
				razon = borrar_repetidos(razon, " ")
				if razon == "":
					razon = "No se ha especificado ninguna razón."
				if message.content.startswith("ban",len(prefijo),len(prefijo)+4) or message.content.startswith("banear",
					len(prefijo),len(prefijo)+7):
					ban_kick="baneado"
					emoji=u"\U0000274E"
					puede = message.author.server_permissions.ban_members
				else:
					ban_kick="expulsado"
					emoji=u"\U0001F462"
					puede = message.author.server_permissions.kick_members
				if puede == False:
					await client.send_typing(message.channel)
					await client.send_message(message.channel, "No tienes los permisos necesarios.")
					return
				pie_embed = pie_texto.format(ban_kick,nick_autor,message.author.name,message.author.discriminator)
				ban_embed = crear_embed(client,(emoji,ban_kick), del_descripcion, ban_kick_color, miembro, message.author,
										message.server, razon, frown_usuario, miniatura="avatar", pie=pie_embed,
										ed=(ban_kick,"de",""))
				if len(ban_embed) == 2:
					try:
						await client.send_typing(miembro)
						await client.send_message(miembro, embed=ban_embed[1])
					except Forbidden: pass
				if ban_kick == "baneado":
					await client.ban(miembro, delete_message_days=0)
				else:
					await client.kick(miembro)
				await client.send_typing(message.channel)
				await client.send_message(message.channel, embed=ban_embed[0])
			else:
				await client.send_typing(message.channel)
				await client.send_message(message.channel, "{} es más profesional que tú, {}".format(miembro.display_name,
																							message.author.display_name))

async def unban(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	"""Comando "unban". Desbanea a un usuario del servidor pudiendo especificar una razón para ello.
		Envía un mensaje en el servidor y puede, opcionalmente, enviar uno al usuario (si éste los permite)
		donde figura quién lo desbaneó y la razón (si fue especificada).
		Parámetros:
			-Usuario: Nombre de usuario de quien se pretende desbanear.
			-Razón: (Opcional) Motivo por el que se lo quiere desbanear.
			-Mensaje SI o NO: (Opcional) Si existe tercer parámetro, se envía un mensaje al usuario.
		Sintaxis:
			1) usuario | razón | Extra
			2) usuario; razón; extra
		Notas:
			1) En contraste con el comando "ban", no se puede desbanear a múltiples usuarios de una vez.
			2) El tercer parámetro puede ser uno o más carácteres cualquiera.
			3) Puede o no haber espacio entre los parámetros y los separadores.
			4) Los separadores pueden ser "|" o ";"."""
	if not message.author.server_permissions.ban_members:
		return
	lista = await client.get_bans(message.server)
	if ";" in message.content:
		mensaje_separado = message.content.split(";")
	else:
		mensaje_separado = message.content.split("|")
	empieza = 5+len(prefijo)
	while mensaje_separado[0][empieza] == " ":
		mensaje_separado[0] = mensaje_separado[0][0:empieza:] + mensaje_separado[0][empieza+1::]
	while mensaje_separado[0].endswith(" "):
		mensaje_separado[0] = mensaje_separado[0][0:len(mensaje_separado[0])-1:]
	if len(mensaje_separado) >= 2:
		while mensaje_separado[1].startswith(" "):
			mensaje_separado[1] = mensaje_separado[1][1::]
		while mensaje_separado[1].endswith(" "):
			mensaje_separado[1] = mensaje_separado[1][0:len(mensaje_separado[1])-1:]
		razon = mensaje_separado[1]
	else:
		razon = "No se ha especificado ninguna razón"
	miembro = None
	for user in lista:
		if user.name.lower().startswith(mensaje_separado[0][empieza::]):
			miembro = user
	if miembro != None:
		pie_embed = pie_texto.format("desbaneado",nick_autor,message.author.name,message.author.discriminator)
		unban_embed = crear_embed(client,unban_titulo, del_descripcion, unban_color, miembro, message.author,
								 message.server, razon, un_usuario, miniatura="avatar", pie=pie_embed,
								 ed=("desbaneado","de",""))
		await client.unban(message.server, miembro)
		await client.send_typing(message.channel)
		await client.send_message(message.channel, embed=unban_embed[0])
		if len(mensaje_separado) >= 3 and len(unban_embed) == 2:
			try:
				await client.send_typing(message.channel)
				await client.send_message(miembro, embed=unban_embed[1])
			except Forbidden: pass