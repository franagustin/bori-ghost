import discord
import os
import psycopg2
from variables import (embed_titulo, embed_descripcion, usuario_texto, razon_titulo, 
						tiempo_titulo, tiempo_texto, ed_descripcion, fue_usuario_texto,
						tabla_prefijos, tabla_confiables)

def get_prefijos(message):
	"""
	Función que me permite seleccionar la lista de prefijos disponibles en el servidor.
	Parámetros: 1
		-message: Mensaje que esté en el server para el cual quiere obtenerse los prefijos.
	"""
	#Carga la url de la base de datos desde las variables de ambiente
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require') #Conecta a la base de datos
	bd = base_de_datos.cursor() #Crea un cursor para ejecutar queries en la base de datos
	bd.execute(tabla_prefijos.format('"'+message.server.id+'_prefijos"')) #Crea la tabla de prefijos si no existe
	base_de_datos.commit()
	#Selecciona todos los prefijos
	bd.execute(f'SELECT prefijo FROM "{message.server.id}_prefijos";')
	prefijos = bd.fetchall()
	#Cierra el cursor y la conexión con la base de datos
	bd.close()
	base_de_datos.close()
	#Convierte los datos obtenidos en una lista de prefijos
	lista_prefijos = [prefijo[0] for prefijo in prefijos]
	return lista_prefijos #Devuelve la lista de prefijos

def get_confiables(server):
	"""
	Función que devuelve la lista de usuarios que son considerados confiables en el servidor.
	"""
	#Carga la url de la base de datos desde las variables de ambiente
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require') #Conecta a la base de datos
	bd = base_de_datos.cursor() #Crea un cursor para ejecutar queries en la base de datos
	bd.execute(tabla_confiables.format('"'+server.id+'_confiables"',)) #Crea la tabla de confiables si no existe
	base_de_datos.commit() #Guarda los cambios en la base de datos
	#Selecciona los usuarios de la lista de confiables
	bd.execute(f'SELECT user_id FROM "{server.id}_confiables";')
	confiables = bd.fetchall()
	#Convierte los datos obtenidos en un conjunto con los ids de los usuarios confiables
	confiables_whitelist = {confiable[0] for confiable in confiables}
	#Cierra el cursor y la conexión con la base de datos
	bd.close()
	base_de_datos.close()
	return confiables_whitelist #Devuelve el conjunto de usuarios confiables

def lista_a_cadena(lista, inicio: int=None, final: int=None, caracter=" "):
	"""
	Función que une los elementos de una lista, convirtiéndola en cadena.
	Parámetros: 4
		-lista: Lista que se desea convertir en cadena.
		-inicio: Offset de la lista que se desea sea el primer elemento. (opcional)
		-final: Offset de la lista que se desea sea el último elemento. (opcional)
		-caracter: Caracter de separación entre elementos (opcional) (por defecto whitespace)
	"""
	if inicio == None: #Si no se ha especificado inicio
		inicio = 0 #Empieza en el primer elemento
	if final == None: #Si no se ha especificado final
		final = len(lista) #Termina en el último elemento
	mensaje_sin_comando = "" #Declara la variable donde guardaré el mensaje
	for i in range(inicio,final):
		if lista[i] != "\n": #Si no es un salto de línea
			mensaje_sin_comando += lista[i]+caracter #Agrega el elemento y un caracter de separación
		else: #Si es un salto de línea
			mensaje_sin_comando += lista[i] #Agrega el elemento sin la separación
	return mensaje_sin_comando #Devuelve el mensaje

def get_mute_role(lista):
	"""
	Selecciona el rol para los usuarios silenciados en una lista de roles.
		Parámetros:
			-Lista: Una lista que contiene objetos discord.Role en la que se 
			selecciona el rol de silencio.
	"""
	silenciado = discord.utils.get(lista, id="338022067880329216") #CB en SDUMS
	if silenciado == None: #Si no lo encuentra
		silenciado = discord.utils.get(lista, name="CALLATE BOLUDO")
	if silenciado == None: #Si no lo encuentra
		silenciado = discord.utils.get(lista, name="Muted")
	if silenciado == None: #Si no lo encuentra
		silenciado = ""
	return silenciado #Devuelve el rol

def get_confiable_role(lista):
	"""
	Función que permite obtener el rol para usuarios confiables en el servidor.
	Parámetros:
		-lista: Lista de roles desde donde debe seleccionarse.
	"""
	#Selecciona el rol por id
	confiable = discord.utils.get(lista, id="482391907289268244")
	if confiable == None: #Si no se ha encontrado
		#Selecciona el rol por nombre en minúsculas
		confiable = discord.utils.get(lista, name="confiable")
	if confiable == None: #Si no se ha encontrado
		#Selecciona el rol por nombre con primera letra mayúscula
		confiable = discord.utils.get(lista, name="Confiable")
	if confiable == None: #Si no se ha encontrado
		#Selecciona el rol por nombre en mayúsculas
		confiable = discord.utils.get(lista, name="CONFIABLE")
	return confiable #Devuelve el rol

def borrar_repetidos(mensaje, caracter):
	"""
	Borra los caracteres repetidos al principio y al final de un mensaje.
		Lo uso principalmente para borrar espacios extras.
		Parámetros:
			-Mensaje (string): Cadena de texto que quiero modificar.
			-Caracter: Caracter a eliminar (generalmente " ").
	"""
	while mensaje.startswith(caracter):
		mensaje = mensaje[1::]
	while mensaje.endswith(caracter):
		mensaje = mensaje[0:len(mensaje)-1:]
	return mensaje

def get_nick_avatar(miembro):
	"""
	Devuelve el nick y el avatar de un miembro dado.
		Parámetros:
			-Miembro: Usuario cuyos nick y avatar se quieren obtener.
	"""
	#Si es un objeto discord.Member (no User) y tiene nick
	if hasattr(miembro, "nick") and miembro.nick != None:
		nick = miembro.nick #Lo seleccione
	else: #Si no
		nick = miembro.name #El nick es el nombre de usuario
	if miembro.avatar_url == "": #Si no tiene avatar
		avatar = miembro.default_avatar_url #Selecciona el por defecto
	else: #Si no
		avatar = miembro.avatar_url #Devuelve el del miembro
	return nick, avatar

def crear_embed(client,titulo:tuple,descripcion,color,miembro,autor,servidor,razon,
				usuario=None,tiempo=None,miniatura=None,pie:str=None,ed:tuple=None):
	"""
	Función que me permite crear embeds con un sólo código para no andar repitiendo
		lo mismo una y otra vez.
		La llamo para los mensajes que se envían luego de cada comando.
		Parámetros:
			-Titulo (emoji, tipo): El emoji que acompaña al título y la palabra que sigue a "Usuario"
			-Descripción: Discierne entre "en el" o "del" servidor.
			-Color: Color del embed (RGB en hex).
			-Miembro (discord.Member): usuario sobre el que se actúa.
			-Autor (discord.Member o discord.User): Objeto que representa al usuario que usa
				el comando (o al bot).
			-Servidor (discord.Server): Servidor de discord en que se ejecuta el comando.
			-Razon: Motivo por el que se usa el comando.
			-Usuario: Título del campo "usuario" en el embed.
			-Tiempo: Si es el comando mute, es el tiempo de silencio.
			-Miniatura: Si es "avatar", pone el avatar del miembro como miniatura del
				embed. Si es "server_icon", pone el icono del server.
			-Pie: Texto para el footer.
			-ed (tupla): Datos para completar el embed que se manda al usuario.
	"""
	nick, avatar = get_nick_avatar(miembro) #Consigue el nick y el avatar del miembro
	nick_autor, avatar_autor = get_nick_avatar(autor) #Consigue el nick y el avatar del autor
	#Crea el primer embed y lo guarda en la lista "embed"
	embed = [discord.Embed(title=embed_titulo.format(titulo[0],titulo[1].capitalize()),
							description=embed_descripcion.format(titulo[1],descripcion),
							colour=color)]
	if usuario != None: #Si debe llevar el campo "Usuario"
		embed[0].add_field(name=usuario,
						value=usuario_texto.format(nick, miembro.name, miembro.discriminator),
						inline=False) #Lo crea
	embed[0].add_field(name=razon_titulo, value=razon, inline=False) #Crea el campo "Razón"
	if tiempo != None: #Si debe llevar el campo "Tiempo"
		embed[0].add_field(name=tiempo_titulo,
						value=tiempo_texto.format(str(tiempo)),
						inline=False) #Lo crea
	if miniatura == "avatar": #Si debe llevar el avatar
		embed[0].set_thumbnail(url=avatar) #Lo pone de miniatura
	elif miniatura == "server_icon": #Si debe llevar el icono del server (nada por ahora)
		embed[0].set_thumbnail(url=servidor.icon_url) #Lo pone de miniatura
	if pie != None: #Si debe llevar footer
		embed[0].set_footer(text=pie, 
						icon_url=avatar_autor) #Lo crea
	if miembro != autor and miembro != client.user: #Si el usuario sobre el que se actúa no es quien llamó al comando
		#Crea un segundo embed que se le enviará
		embed.append(discord.Embed(title=u"\U0001F50A "+servidor.name.capitalize(),
									  description=ed_descripcion.format(ed[0],ed[1],servidor.name.capitalize(),ed[2]),
									  colour=color)) #Lo agrega en la lista "embed"
		embed[1].add_field(name=razon_titulo, value=razon, inline=False) #Crea el campo "Razón"
		embed[1].add_field(name=u"\U0001F46E"+" Usuario",
								value=fue_usuario_texto.format(ed[0],nick_autor,autor.name,autor.discriminator),
								inline=False) #Crea el campo que indica quién usó el comando
		if tiempo != None: #Si debe llevar el campo "Tiempo"
			embed[1].add_field(name=tiempo_titulo,
							value=tiempo_texto.format(str(tiempo)),
							inline=False) #Lo crea
		embed[1].set_thumbnail(url=servidor.icon_url) #Pone de miniatura el avatar del server
	return (embed)