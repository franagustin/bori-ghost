import discord
import psycopg2
import asyncio
import os
from funciones import crear_embed, get_mute_role
from variables import tabla_mute, pie_texto, unmute_titulo, en_descripcion, mute_color, un_usuario, quita_mute
from datetime import datetime, timedelta

async def auto_unmute(client):
	"""Corutina incluida como tarea en el loop que se ejecuta una vez por segundo y se encarga de desilenciar
		automáticamente a los usuarios que estén silenciados en cada servidor.
		Les quita el rol y los borra de la BD.
		*No lleva parámetros*.
	"""
	await client.wait_until_ready() #Espera a que esté listo
	while not client.is_closed: #Mientras esté abierto el bot
		servidor = discord.utils.get(client.servers, id = "337854421876736003")
		if servidor != None: #Para cada servidor en el que esté
			#Conecta con la base de datos o la crea si no existe
			BD_URL = os.getenv('DATABASE_URL')
			base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
			bd = base_de_datos.cursor()
			bd.execute(tabla_mute.format('"'+servidor.id+'_silenciados"')) #Crea la tabla de silenciados si no existe
			#Seleciona la id de usuario y la fecha en que debe levantarse cada silencio (tupla)
			bd.execute(f'SELECT discord_id, termina FROM "{servidor.id}_silenciados"')
			tiempos_muteo = bd.fetchall()
			for usuario in tiempos_muteo: #Por cada pareja usuario-fecha
				tiempo_unmute = usuario[1] #Le da formato de fecha
				if datetime.now() >= tiempo_unmute: #Lo compara con la hora actual (UTC)
					miembro = discord.utils.get(servidor.members, id = usuario[0]) #Selecciona el miembro con esa id
					razon="Ha transcurrido el tiempo de silencio especificado." #Establece la razón
					#Define los parámetros para el tiempo del footer
					pie_embed=pie_texto.format("desilenciado",client.user.name,client.user.name,client.user.discriminator)
					unmute_embed = crear_embed(client,unmute_titulo,en_descripcion,mute_color,miembro,client.user,servidor,
												razon,un_usuario,miniatura="avatar", pie=pie_embed,
												ed=("desilenciado","en"," y ya puedes hablar de nuevo"))
					silenciado = get_mute_role(servidor.roles) #Selecciona el rol de silenciados para el servidor
					bd.execute(quita_mute.format('"'+servidor.id+'_silenciados"'), (usuario[0],)) #Quita al usuario de la lista en la bd
					base_de_datos.commit()
					await client.remove_roles(miembro, silenciado) #Le quita el rol en el server
					await client.send_typing(servidor) #Mensaje de "*BOT* está escribiendo"
					await client.send_message(servidor, embed=unmute_embed[0]) #Envía el mensaje informativo
					if len(unmute_embed) == 2: #Si hay un segundo mensaje
						try: await client.send_message(miembro, embed=unmute_embed[1]) #Lo manda al usuario
						except discord.errors.Forbidden: pass
			bd.close()
			base_de_datos.close()
		await asyncio.sleep(1) #Encargado de que se ejecute una vez por segundo