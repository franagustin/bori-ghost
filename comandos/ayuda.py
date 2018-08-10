import os
import discord
import re
from variables import ayuda, comandos_ayuda, descripciones_ayuda
from unicodedata import normalize

async def ayuda_general(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	if len(mensaje_separado) > 1:
		comando_separado = mensaje_separado[1].split(".")
		for elemento in descripciones_ayuda:
			nombre = re.sub(r"([^n\u0300-\u036F]|n(?!\u0303(?![\u0300-\u036F])))[\u0300-\u036F]+", r"\1", normalize("NFD",
							elemento.nombre), 0, re.I)
			nombre = normalize("NFC", nombre)
			if comando_separado[0].lower() == nombre.lower():
				i = 1
				while len(comando_separado) > i:
					for sub_elemento in elemento.subs:
						nombre = re.sub(r"([^n\u0300-\u036F]|n(?!\u0303(?![\u0300-\u036F])))[\u0300-\u036F]+", r"\1", normalize("NFD",
							elemento.nombre), 0, re.I)
						nombre = normalize("NFC", nombre)
						if comando_separado[1].lower() == nombre.lower():
							elemento = sub_elemento
					i += 1
				descripcion = elemento.descripcion
				if elemento.sintaxis[0] != None:
					if elemento.alias != None:
						descripcion += "\n**__Alias__**\n"
						for alias in elemento.alias:
							descripcion += alias+", "
					if elemento.parametros != None:
						descripcion += "\n**__Parámetros: "+str(len(elemento.parametros))+"__**\n"
						for i in range(len(elemento.parametros)):
							descripcion += str(i)+") "+elemento.parametros[i]
					descripcion += "\n**__Sintaxis__**\n"+"```{}```".format(elemento.sintaxis.format(prefijo))
					descripcion += "\n**__Ejemplo__**\n"+"```{}```".format(elemento.ejemplo.format(prefijo))
				embed = discord.Embed(title="Ayuda: "+elemento.nombre,
									description=descripcion,
									colour=0xAAAAAA)
				for i in range(len(elemento.subs)):
					if len(elemento.subs[i].subs) != 0:
						valor = elemento.subs[i].subs[0].nombre
					else:
						valor = elemento.subs[i].descripcion
					embed.add_field(name=str(i+1)+". "+elemento.subs[i].nombre,
									value=valor)
	else:
		embed = discord.Embed(title="BORI GHOST: Mensaje de Ayuda",
								description=ayuda.format(client.user.mention, prefijo, prefijo, prefijo),
								colour=0xAAAAAA)
		for mod_i in range(len(descripciones_ayuda)):
			valor = ""
			for sub_i in range(len(descripciones_ayuda[mod_i].subs)):
				valor += "**"+str(mod_i+1)+"."+str(sub_i+1)+". "+descripciones_ayuda[mod_i].subs[sub_i].nombre+"**\n"
				for i in range(len(descripciones_ayuda[mod_i].subs[sub_i].subs)):
					valor += "——"+str(mod_i+1)+"."+str(sub_i+1)+"."+str(i+1)+". "+descripciones_ayuda[mod_i].subs[sub_i].subs[i].nombre+"\n"
			embed.add_field(name=str(mod_i+1)+". "+descripciones_ayuda[mod_i].nombre,
							value=valor)
		"""mod_i = 1
		for key in comandos_ayuda:
			valor = ""
			sub_i = 1
			for sub_key in comandos_ayuda[key]:
				valor += "**"+str(mod_i)+"."+str(sub_i)+". "+sub_key+"**\n"
				for i in range(len(comandos_ayuda[key][sub_key])):
					valor += "——"+str(mod_i)+"."+str(sub_i)+"."+str(i+1)+". "+comandos_ayuda[key][sub_key][i]+"\n"
				sub_i += 1
			embed.add_field(name=str(mod_i)+". "+key,
							value=valor)
			mod_i += 1"""
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.set_footer(icon_url=avatar_autor,
					text="Este mensaje ha sido solicitado por {} ({}#{})".format(nick_autor,
							message.author.name, message.author.discriminator))
	await client.send_message(message.channel, embed=embed)