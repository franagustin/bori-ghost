import re
import psycopg2
import os
from datetime import datetime, timedelta
from variables import (pie_texto, mute_titulo, unmute_titulo, en_descripcion, mute_color,
						frown_usuario, un_usuario, tabla_mute, nuevo_mute, quita_mute)
from funciones import get_mute_role, borrar_repetidos, crear_embed
from discord.errors import Forbidden


async def mute(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	"""Comando "mute". Silencia a uno o más usuarios, impidiéndoles hablar en el servidor por un tiempo
	determinado. Puede especificarse el motivo por el que se los silencia y el tiempo (10min por defecto).
	Envía un mensaje al servidor por cada usuario silenciado y otro al propio usuario que incluye el
	tiempo y el motivo (si fue especificado).
	Parámetros:
		-Usuario (mención): miembro del servidor a quien se quiere silenciar.
		-Tiempo: tiempo durante el que se lo quiere silenciar (si no se especifica, serán 10 minutos).
		-Razón: motivo por el que se lo quiere silenciar.
	Sintaxis:
		1) usuario (razón tiempo uzuario razón tiempo usuario razón tiempo usuario razón tiempo)*
		2) usuario (tiempo razón usuario tiempo razón usuario tiempo razón usuario tiempo razón)*
		* = opcionales
	Notas:
		1) La razón y el tiempo pueden ser intercambiados en orden. Sin embargo, el primer número que
			aparezca será usado como parámetro "tiempo".
		2) El parámetro tiempo puede ir acompañado por los siguientes sufijos, inmediatamente luego del
			número y sin espacios:
				a) a: Años
				b) w: Semanas
				c) d: Días
				d) h: Horas
				e) m: minutos
				f) s: segundos
			De no estar acompañado por ningún sufijo, se asume que el tiempo está en segundos.
		3) Una vez transcurrido el tiempo, el silencio es terminado automáticamente (por la corutina
			auto_unmute). Sin embargo, si deseas desilenciar antes al usuario, puedes usar el 
			comando "unmute".
		4) Este sistema funciona con roles, debes crear en tu servidor un rol llamado "CALLATE BOLUDO" o
			"Muted" y configurar sus permisos para que no pueda hablar. Este comando les dará dicho rol.
	"""
	if message.mention_everyone == False: #Evita mutear a todos los usuarios
		if not (message.author.server_permissions.kick_members or message.author.server_permissions.manage_roles):
			return
		silenciado = get_mute_role(message.server.roles)
		for miembro in message.mentions:
			mencion = re.search("<@!?{}>".format(miembro.id), message.content)
			i = mensaje_separado.index(mencion.group())+1
			razon = ""
			tiempo = None
			while i < len(mensaje_separado):
				if not re.search("<@!?[0-9]+>", mensaje_separado[i]):
					if tiempo == None:
						if re.search("[0-9]+[hms]?$", mensaje_separado[i]):
							try: tiempo = int(mensaje_separado[i])
							except ValueError: tiempo = int(mensaje_separado[i][0:len(mensaje_separado[i])-1:])
							if mensaje_separado[i].endswith("h"):
								multiplicador = 60*60
								tiempo_texto = str(tiempo)+" horas."
							elif mensaje_separado[i].endswith("m"):
								multiplicador = 60
								tiempo_texto = str(tiempo)+" minutos."
							else:
								multiplicador = 1
								tiempo_texto = str(tiempo)+" segundos"
							tiempo *= multiplicador
							termina_muteo = message.timestamp + timedelta(seconds=tiempo)
						elif re.search("[0-9]+[awd]?$", mensaje_separado[i]):
							try: tiempo = int(mensaje_separado[i])
							except ValueError: tiempo = int(mensaje_separado[i][0:len(mensaje_separado[i])-1:])
							if mensaje_separado[i].endswith("a"):
								multiplicador = 365
								tiempo_texto = str(tiempo)+" años."
							elif mensaje_separado[i].endswith("w"):
								multiplicador = 7
								tiempo_texto = str(tiempo)+" semanas."
							else:
								multiplicador = 1
								tiempo_texto = str(tiempo)+" días."
							tiempo *= multiplicador
							termina_muteo = message.timestamp + timedelta(days=tiempo)
						else:
							razon += " "+mensaje_separado[i]
					else:
						razon += " "+mensaje_separado[i]
					i += 1
				else:
					i = len(mensaje_separado)
			if razon == "":
				razon = "No se ha especificado una razón."
			if tiempo == None:
				tiempo = 10*60
				tiempo_texto = "10 minutos."
				termina_muteo = message.timestamp + timedelta(seconds=tiempo)
			pie_embed = pie_texto.format("silenciado",nick_autor,message.author.name,message.author.discriminator)
			mute_embed = crear_embed(client,mute_titulo, en_descripcion, mute_color, miembro, message.author, message.server,
									razon, frown_usuario,tiempo=tiempo_texto,miniatura="avatar",pie=pie_embed,
									ed=("silenciado","en",""))
			BD_URL = os.getenv("DATABASE_URL")
			base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
			bd = base_de_datos.cursor()
			bd.execute(tabla_mute.format('"'+message.server.id+'_silenciados"'))
			bd.execute(quita_mute.format('"'+message.server.id+'_silenciados"'), (miembro.id,))
			bd.execute(nuevo_mute.format('"'+message.server.id+'_silenciados"'), (miembro.id, termina_muteo))
			base_de_datos.commit()
			bd.close()
			base_de_datos.close()
			await client.add_roles(miembro, silenciado)
			await client.send_typing(message.channel)
			await client.send_message(message.channel, embed=mute_embed[0])
			if len(mute_embed) == 2:
				try: await client.send_message(miembro, embed=mute_embed[1])
				except Forbidden: pass


async def unmute(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	"""Comando "unmute". Quita el silencio a uno o más usuarios pudiendo especificar una razón (individual para cada uno).
		Envía un mensaje al servidor por cada usuario desilenciado y uno al propio usuario, incluyendo el motivo (si fue
		especificado).
		Parámetros:
			-Usuario (mención): miembro del servidor que se encuentra silenciado y quieres desilenciar.
			-Razón: motivo por el cual quieres terminar su silencio.
		Sintaxis:
			usuario (razón usuario razón usuario razón usuario razón usuario razón)*
			* = opcionales."""
	if message.mention_everyone == False:
		if not (message.author.server_permissions.kick_members or message.author.server_permissions.manage_roles):
			return
		silenciado = get_mute_role(message.server.roles)
		for miembro in message.mentions:
			razon = ""
			mencion = re.search("<@!?{}>".format(miembro.id), message.content)
			i = mensaje_separado.index(mencion.group())+1
			while i < len(mensaje_separado):
				if not re.search("<@!?[0-9]+>", mensaje_separado[i]):
					razon += " "+mensaje_separado[i]
					i += 1
				else:
					i = len(mensaje_separado)
			razon = borrar_repetidos(razon, " ")
			if razon == "":
				razon = "No se ha especificado una razón."
			pie_embed = pie_texto.format("desilenciado",nick_autor,message.author.name,message.author.discriminator)
			unmute_embed = crear_embed(client,unmute_titulo, en_descripcion, mute_color, miembro, message.author,
								 message.server, razon, un_usuario, miniatura="avatar", pie=pie_embed,
								 ed=("desilenciado","en"," y ya puedes hablar de nuevo"))
			BD_URL = os.getenv("DATABASE_URL")
			base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
			bd = base_de_datos.cursor()
			bd.execute(quita_mute.format('"'+message.server.id+'_silenciados"'), (miembro.id,))
			base_de_datos.commit()
			bd.close()
			base_de_datos.close()
			await client.remove_roles(miembro,silenciado)
			await client.send_typing(message.channel)
			await client.send_message(message.channel, embed=unmute_embed[0])
			if len(unmute_embed) == 2:
				try: await client.send_message(miembro, embed=unmute_embed[1])
				except Forbidden: pass