import os
import psycopg2
from funciones import lista_a_cadena
from discord import Embed

async def maneja_prefijos(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	if len(mensaje_separado) >= 2:
		if mensaje_separado[1] in {"add", "añadir", "agregar", "añade", "agrega", "nuevo", "new", "pon"}:
			await agregar_prefijo(client, message, mensaje_separado)
		elif mensaje_separado[1] in {"remove", "delete", "borrar", "quitar", "quita", "borra"}:
			await quitar_prefijo(client, message, mensaje_separado)
		elif mensaje_separado[1] in {"cambia", "change", "solo", "unico", "only", "cambiar", "único", "sólo", "set"}:
			await cambiar_prefijo(client, message, mensaje_separado)
		else:
			await ver_prefijos(client, message, nick_autor, avatar_autor)
	else:
		await ver_prefijos(client, message, nick_autor, avatar_autor)

async def agregar_prefijo(client, message, mensaje_separado):
	if message.author.server_permissions.administrator:
		if len(mensaje_separado) > 3:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, "El prefijo no debe contener espacios, {}.".format(message.author.mention))
			return
		elif len(mensaje_separado[2]) > 20:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, "La longitud máxima es de 20 carácteres, {}.".format(message.author.mention))
			return
		BD_URL = os.getenv("DATABASE_URL")
		base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
		bd = base_de_datos.cursor()
		bd.execute(f'INSERT INTO "{message.server.id}_prefijos"(prefijo) VALUES(%s)', (mensaje_separado[2],))
		base_de_datos.commit()
		await client.send_typing(message.channel)
		await client.send_message(message.channel, "El prefijo '*{}*' ha sido añadido con éxito.".format(mensaje_separado[2]))
		bd.close()
		base_de_datos.close()
	else:
		msg_permisos = "No tienes los permisos suficientes para editar permisos, {}, debes ser administrador."
		await client.send_typing(message.channel)
		await client.send_message(message.channel, msg_permisos.format(message.author.mention))

async def quitar_prefijo(client, message, mensaje_separado):
	if message.author.server_permissions.administrator:
		BD_URL = os.getenv("DATABASE_URL")
		base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
		bd = base_de_datos.cursor()
		bd.execute(f'SELECT prefijo FROM "{message.server.id}_prefijos";')
		prefijos = bd.fetchall()
		prefijos = [prefijo[0] for prefijo in prefijos]
		if mensaje_separado[2] not in prefijos:
			msg_novalido = "Actualmente '*{}*' no es un prefijo válido, {}."
			await client.send_typing(message.channel)
			await client.send_message(message.channel, msg_novalido.format(mensaje_separado[2],message.author.mention))
			return
		elif len(prefijos) == 1:
			msg_solouno = "**¡ALTO! NO DEBES** eliminar el único prefijo o el bot quedaría inservible, {}."
			await client.send_typing(message.channel)
			await client.send_message(message.channel, msg_solouno.format(message.author.mention))
			return
		else:
			bd.execute(f'DELETE FROM "{message.server.id}_prefijos" WHERE prefijo = %s;', (mensaje_separado[2],))
			base_de_datos.commit()
			await client.send_typing(message.channel)
			await client.send_message(message.channel, "El prefijo '*{}*' ha sido eliminado exitosamente.".format(mensaje_separado[2]))
		bd.close()
		base_de_datos.close()
	else:
		msg_permisos = "No tienes los permisos suficientes para editar permisos, {}, debes ser administrador."
		await client.send_typing(message.channel)
		await client.send_message(message.channel, msg_permisos.format(message.author.mention))

async def cambiar_prefijo(client, message, mensaje_separado):
	if message.author.server_permissions.administrator:
		if len(mensaje_separado) > 3:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, "El prefijo no debe contener espacios, {}.".format(message.author.mention))
			return
		BD_URL = os.getenv("DATABASE_URL")
		base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
		bd = base_de_datos.cursor()
		bd.execute(f'DELETE FROM "{message.server.id}_prefijos"')
		bd.execute(f'INSERT INTO "{message.server.id}_prefijos"(prefijo) VALUES (%s)', (mensaje_separado[2],))
		base_de_datos.commit()
		await client.send_typing(message.channel)
		await client.send_message(message.channel, "El prefijo '*{}*'' es ahora el único prefijo válido.".format(mensaje_separado[2]))
		bd.close()
		base_de_datos.close()
	else:
		msg_permisos = "No tienes los permisos suficientes para editar permisos, {}, debes ser administrador."
		await client.send_typing(message.channel)
		await client.send_message(message.channel, msg_permisos.format(message.author.mention))

async def ver_prefijos(client, message, nick_autor, avatar_autor):
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
	bd = base_de_datos.cursor()
	bd.execute(f'SELECT prefijo FROM "{message.server.id}_prefijos";')
	prefijos = bd.fetchall()
	bd.close()
	base_de_datos.close()
	prefijos = [prefijo[0] for prefijo in prefijos]
	prefijos = lista_a_cadena(prefijos, caracter="\n")
	texto_pie = "Lista solicitada por {} ({}#{})"
	prefijos_embed = Embed(title=u"\U00002699"+" Prefijos",
							description="Lista de prefijos actuales para este servidor.",
							colour=0x2464CC)
	prefijos_embed.set_footer(text=texto_pie.format(nick_autor,message.author.name, message.author.discriminator),
								icon_url=avatar_autor)
	prefijos_embed.add_field(name="Prefijos (uno por línea)", value=prefijos)
	prefijos_embed.set_thumbnail(url=client.user.avatar_url)
	await client.send_typing(message.channel)
	await client.send_message(message.channel, embed=prefijos_embed)