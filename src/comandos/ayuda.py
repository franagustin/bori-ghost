import os
import discord
import re
from variables import ayuda, descripciones_ayuda
from unicodedata import normalize

async def ayuda_manejador(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	if len(mensaje_separado) > 1:
		comando_separado = mensaje_separado[1].split(".")
		elem = None
		for elemento in descripciones_ayuda:
			if comando_separado[0].lower() == elemento.ident.lower():
				i = 1
				while len(comando_separado) > i:
					for sub_elemento in elemento.subs:
						if comando_separado[i].lower() == sub_elemento.ident.lower():
							elemento = sub_elemento
					i += 1
				if elem == None:
					elem = elemento
		if elem == None:
			numeros = []
			for parte in comando_separado:
				try:
					numeros.append(int(parte))
				except ValueError:
					pass
			if len(numeros) >= 1 and numeros[0]-1 in range(len(descripciones_ayuda)):
				elem = descripciones_ayuda[numeros[0]-1]
			for i in range(1,len(numeros)):
				if numeros[i]-1 in range(len(elem.subs)):
					elem = elem.subs[numeros[i]-1]
		if elem != None:
			await ayuda_especifica(client, message, elem, nick_autor, avatar_autor, prefijo)
		else:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, "ERROR: No has especificado un módulo válido.")
	else:
		await ayuda_general(client, message, nick_autor, avatar_autor, prefijo)

async def ayuda_especifica(client, message, elemento, nick_autor, avatar_autor, prefijo):
	descripcion = elemento.descripcion
	if elemento.sintaxis != None:
		if elemento.alias != None:
			descripcion += "\n**__Alias__**\n"
			for i in range(len(elemento.alias)):
				descripcion += "*"+elemento.alias[i]+"*"
				if i < len(elemento.alias)-1:
					descripcion += ", "
		if elemento.parametros != None:
			descripcion += "\n**__Parámetros:__ "
			for i in range(len(elemento.parametros)):
				if elemento.parametros[i] == None:
					descripcion += "NO**"
				else:
					if i == 0:
						descripcion += str(len(elemento.parametros))+"**"
					descripcion += "\n**"+str(i+1)+")** "+elemento.parametros[i]
		descripcion += "\n**__Sintaxis__**\n"+"```{}```".format(elemento.sintaxis.format(prefijo))
		descripcion += "\n Los símbolos < y > y todo lo que esté entre paréntesis **no** debe escribirse."
		descripcion += "\n**__Ejemplo__**\n"+"```{}```".format(elemento.ejemplo.format(prefijo))
	embed = discord.Embed(title=u"\U0001F527"+" Ayuda: "+elemento.nombre,
						description=descripcion,
						colour=0x2464CC)
	for i in range(len(elemento.subs)):
		valor = elemento.subs[i].descripcion+"\n"
		if len(elemento.subs[i].subs) != 0:
			for indice in range(len(elemento.subs[i].subs)):
				valor += "——"+str(i+1)+"."+str(indice+1)+". "+elemento.subs[i].subs[indice].nombre+"\n"
		embed.add_field(name=u"\U0001F47B"+" "+str(i+1)+". "+elemento.subs[i].nombre,
						value=valor)
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.set_footer(icon_url=avatar_autor,
					text="Este mensaje ha sido solicitado por {} ({}#{})".format(nick_autor,
							message.author.name, message.author.discriminator))
	try:
		await client.send_typing(message.author)
		await client.send_message(message.author, embed=embed)
		await client.send_typing(message.channel)
		await client.send_message(message.channel, u"\U0001F5A5"+" Revisa tu MAC, súbdito. "+u"\U0001F4BB"+"\n"+
									u"\U0001F4E9"+" Te he enviado un mensaje privado. "+u"\U0001F4E8")
	except discord.errors.Forbidden:
		await client.send_typing(message.channel)
		await client.send_message(message.channel, embed=embed)


async def ayuda_general(client, message, nick_autor, avatar_autor, prefijo):
	embed = discord.Embed(title=u"\U0001F916"+" BORI GHOST: Mensaje de Ayuda",
							description=ayuda.format(client.user.mention, prefijo, prefijo, prefijo),
							colour=0x2464CC)
	for mod_i in range(len(descripciones_ayuda)):
		valor = ""
		for sub_i in range(len(descripciones_ayuda[mod_i].subs)):
			valor += "**—"+str(mod_i+1)+"."+str(sub_i+1)+". "+descripciones_ayuda[mod_i].subs[sub_i].nombre+"**\n"
			for i in range(len(descripciones_ayuda[mod_i].subs[sub_i].subs)):
				valor += "——"+str(mod_i+1)+"."+str(sub_i+1)+"."+str(i+1)+". "+descripciones_ayuda[mod_i].subs[sub_i].subs[i].nombre+"\n"
		embed.add_field(name=u"\U0001F47B"+" "+str(mod_i+1)+". "+descripciones_ayuda[mod_i].nombre,
						value=valor)
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.set_footer(icon_url=avatar_autor,
					text="Este mensaje ha sido solicitado por {} ({}#{})".format(nick_autor,
							message.author.name, message.author.discriminator))
	await client.send_message(message.channel, embed=embed)