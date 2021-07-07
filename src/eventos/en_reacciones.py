import os
import discord
import psycopg2
import datetime
import re
from variables import tabla_destacados

async def pone_destacados(client, reaction, user):
	channel = reaction.message.channel
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
	bd = base_de_datos.cursor()
	bd.execute(tabla_destacados.format('"'+reaction.message.server.id+'_destacados"',))
	bd.execute(f'SELECT id_canal, emoji, minimo, ids_destacados, ids_destaque FROM "{reaction.message.server.id}_destacados"')
	id_canal, emoji, minimo, ids_destacados, ids_destaque = bd.fetchone()
	if reaction.emoji == emoji or str(reaction.emoji) == emoji:
		if user == reaction.message.author or user.bot:
			await client.send_message(channel, "Ni tú ni los bots pueden destacar tus mensajes, "+
												user.display_name+".")
		elif id_canal == None:
			await client.send_message(channel, "Aún no han seleccionado ningún canal para mensajes destacados.")
		elif emoji == None:
			await client.send_message(channel, "No se ha seleccionado ningún emoji para mensajes destacados.")
		elif minimo == None:
			await client.send_message(channel, "No se ha establecido la cantidad necesaria de reacciones "+
												"para destacar mensajes.")
		elif reaction.count >= minimo:
			canal = discord.utils.get(channel.server.channels, id=id_canal)
			if canal == None:
				await client.send_message(channel, "El canal elegido no es válido. Por favor cámbialo con "+
													"el comando *dcanal*.")
			elif canal != channel:
				if message.id not in ids_destacados:
					embed = discord.Embed(title=u"\U0001F4CC"+reaction.message.author.display_name+" en #"+channel.name,
											description=reaction.message.content,
											colour=0xFFFF00)
					embed.set_thumbnail(url=reaction.message.author.avatar_url)
					if len(reaction.message.attachments) == 1:
						if re.search("https://.+\.png|jpg|jpeg|bmp|gif", reaction.message.attachments[0]['url']):
							embed.set_image(url=reaction.message.attachments[0]['url'])
						else:
							embed.description += "\n**__Adjunto__**"+"\n["+message.attachments[0]['filename']+"]("+\
													message.attachments[0]['url']+")"
					elif len(reaction.message.attachments) > 1:
						imagenes = 0
						adjuntos = 0
						for adjunto in reaction.message.attachments:
							if re.search("https://.+\.png|jpg|jpeg|bmp|gif", adjunto['url']):
								if imagenes == 0:
									embed.description += "\n**__Imágenes__**"
								imagenes += 1
								embed.description += "\n"+str(imagenes)+") "+adjunto['url']
							else:
								if adjuntos == 0:
									embed.description += "\n**__Adjuntos__**"
								adjuntos += 1
								embed.description += "\n"+str(cuenta)+") ["+adjunto['filename']+"]("+\
												adjunto['url']+")"
					if len(reaction.message.embeds) == 1:
						if 'author' in reaction.message.embeds[0]:
							if 'url' in reaction.message.embeds[0]['author']:
								embed.description += "\n\n[**"+reaction.message.embeds[0]['author']['name']+"**]("+\
														reaction.message.embeds[0]['author']['url']+")"
							else:
								embed.description += "\n\n**"+reaction.message.embeds[0]['author']['name']+"**"
						if 'title' in reaction.message.embeds[0]:
							embed.description += "\n\n**__"+reaction.message.embeds[0]['title']+"__**"
						if 'description' in reaction.message.embeds[0]:
							embed.description += "\n\n"+reaction.message.embeds[0]['description']
						if 'fields' in reaction.message.embeds[0]:
							for campo in reaction.message.embeds[0]['fields']:
								embed.add_field(name=campo['name'], value=campo['value'])
						if 'image' in reaction.message.embeds[0]:
							embed.set_image(url=reaction.message.embeds[0]['image']['url'])
						if 'footer' in reaction.message.embeds[0]:
							embed.add_field(name="Footer", value=reaction.message.embeds[0]['footer']['text'])
					fecha = datetime.datetime.strftime(reaction.message.timestamp, "%d/%m/%Y %H:%M:%S")
					embed.set_footer(text=reaction.message.id+" | "+fecha, icon_url=client.user.avatar_url)
					mensaje = await client.send_message(canal, embed=embed)
					ids_destacados += reaction.message.id+","
					ids_destaque += mensaje.id+","
					bd.execute(f'UPDATE "{reaction.message.server.id}_destacados" SET ids_destacados = %s, ids_destaque = %s'+
								'WHERE minimo = %s', (ids_destacados, ids_destaque, minimo))
					base_de_datos.commit()
	bd.close()
	base_de_datos.close()

async def quita_destacados(client, reaction, user):
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
	bd = base_de_datos.cursor()
	bd.execute(tabla_destacados.format('"'+reaction.message.server.id+'_destacados"',))
	bd.execute(f'SELECT id_canal, emoji, minimo, ids_destacados, ids_destaque FROM "{reaction.message.server.id}_destacados"')
	canal, emoji, minimo, ids_destacados, ids_destaque = bd.fetchone()
	ids_destacados = ids_destacados.split(",")
	ids_destaque = ids_destaque.split(",")
	if reaction.emoji == emoji or str(reaction.emoji) == emoji:
		if reaction.message.id in ids_destacados and reaction.count < minimo:
			i = ids_destacados.index(reaction.message.id)
			canalObjeto = discord.utils.get(reaction.message.server.channels, id=canal)
			mensaje = await client.get_message(canalObjeto, ids_destaque[i])
			ids_destacados.remove(reaction.message.id)
			del ids_destaque[i]
			await client.delete_message(mensaje)
			bd.execute(f'UPDATE "{reaction.message.server.id}_destacados" SET ids_destacados = %s, ids_destaque = %s WHERE id_canal=%s',
				(",".join(ids_destacados), ",".join(ids_destaque), canal))
			base_de_datos.commit()
	bd.close()
	base_de_datos.close()