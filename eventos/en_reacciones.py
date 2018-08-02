import os
import discord
import psycopg2
from variables import tabla_destacados

async def pone_reaccion(client, reaction, user):
	chanel = reaction.message.channel
	if user == reaction.message.author or user.bot:
		await client.send_message(channel, "Ni tú ni los bots puedes destacar tus propios mensajes, "+
															user.display_name+".")
	else:
		BD_URL = os.getenv("DATABASE_URL")
		base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
		bd = base_de_datos.cursor()
		bd.execute(tabla_destacados)
		bd.execute("SELECT id_canal, emoji, minimo, ids_destacados, ids_destaque FROM destacados")
		id_canal, emoji, minimo, ids_destacados, ids_destaque = bd.execute.fetchone()
			if id_canal == None:
				await client.send_message(channel, "Aún no han seleccionado ningún canal para mensajes destacados.")
			elif emoji == None:
				await client.send_message(channel, "No se ha seleccionado ningún emoji para mensajes destacados.")
			elif minimo == None:
				await client.send_message(channel, "No se ha establecido la cantidad necesaria de reacciones "+
															"para destacar mensajes.")
			elif reaction.count == minimo:
				canal = discord.utils.get(message.server.channels, id=id_canal)
				if canal == None:
					await client.send_message(channel, "El canal elegido no es válido. Por favor cámbialo con "+
														el comando *dcanal*.")
				elif canal != channel and canal not in canales_excluidos:
					embed = discord.Embed(title=u"\U0001F4CC"user.display_name+" en "+channel.mention,
											description=reaction.message.content,
											colour=0xFFFF00)
					embed.set_thumbnail(url=user.avatar_url)
					fecha = datetime.strftime(reaction.message.timestamp, "%d/%m/%Y %H:%M:%S")
					embed.set_footer(reaction.message.id+" | "+fecha)
					mensaje = await client.send_message(canal, embed=embed)
				ids_detacados += reaction.message.id+","
				ids_destaque += mensaje.id+","
				bd.execute("UPDATE destacados SET ids_destacados = %s, ids_destaque = %s"+
							"WHERE minimo = %s", (ids_destacados, ids_destaque, minimo))
				base_de_datos.commit()
		bd.close()
		base_de_datos.close()

async def quita_reaccion(client, reaction, user):
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
	bd = base_de_datos.cursor()
	bd.execute(tabla_destacados)
	bd.execute("SELECT canal, ids_destacados, ids_destaque FROM destacados")
	canal, ids_destacados, ids_destaque = bd.execute.fetchone()
	ids_destacados = ids_destacados.split(",")
	ids_destaque = ids_destaque.split(",")
	if reaction.message.id in ids_destacados and reaction.count == 0:
		i = ids_destacados.index(reaction.message.id)
		mensaje = await client.get_message(canal, ids_destaque[i])
		ids_destacados_new = ids_destacados.remove(reaction.message.id)
		del ids_destaque[i]
		await client.delete_message(mensaje)
		bd.execute("UPDATE destacados SET ids_destacados = %s, ids_destaque = %s WHERE ids_destacados = %s", (ids_destacados_new,
					ids_destaque, ids_destacados))
		base_de_datos.commit()
	bd.close()
	base_de_datos.close()