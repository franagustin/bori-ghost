from comandos.ayuda_objetos import *

whitelist = {
	"295748486253510658": "franco",
	"287554491916746752": "katie",
	"244535132097216512": "yoru",
	#"239709477392089109": "zero",
	"451551868070526977": "prueba"
}

#--------- Textos generales de los embeds ---------#
embed_titulo = "{} Usuario {}"
embed_descripcion = "Un usuario ha sido **{}** {} servidor."
en_descripcion = "en el"
del_descripcion = "del"
un_usuario = u"\U0001F64B"+" Usuario"
frown_usuario = u"\U0001F64D"+" Usuario"
razon_titulo = u"\U0001F5DE"+" Razón"
usuario_texto = "**{}** (*{}#{}*)"
tiempo_titulo = u"\U0001F570"+" Tiempo"
tiempo_texto = "La duración del silencio es de {}"
ed_descripcion = "Has sido {} {} **{}**{}."
fue_usuario_texto="Fuiste {} por **{}** (*{}#{}*)"
pie_texto = "Este usuario fue {} por {} ({}#{})"

#--------- Textos mute_embed ---------#
mute_titulo = (u"\U0001F910", "silenciado")
mute_color = 0xFFFF00

#--------- Textos ban_kick_embed ---------#
ban_kick_color = 0xAA0000

#--------- Textos unmute_embed ---------#
unmute_titulo = (u"\U0001F50A", "desilenciado")

#--------- Textos unban_embed ---------#
unban_titulo = (u"\U00002705", "desbaneado")
unban_color = 0x00AA00


#--------- SQL Statements para la tabla de mutes ---------#
#Crea la tabla de mutes si no existe
tabla_mute="""
CREATE TABLE IF NOT EXISTS {}(
key SERIAL NOT NULL PRIMARY KEY,
discord_id VARCHAR(30) NOT NULL,
termina TIMESTAMP WITHOUT TIME ZONE NOT NULL);
"""
#Introduce un nuevo miembro silenciado
nuevo_mute="""
INSERT INTO {} (discord_id,termina)
VALUES (%s,%s);
"""
#Quita a un miembro de la tabla de silenciados
quita_mute="""
DELETE FROM {}
WHERE discord_id=%s;
"""

#--------- SQL Statements para la tabla de encuestas ---------#
#Crea la tabla de encuestas si no existe
tabla_encuestas="""
CREATE TABLE IF NOT EXISTS {}(
key SERIAL NOT NULL PRIMARY KEY,
channel_id VARCHAR(30) NOT NULL,
titulo VARCHAR NOT NULL,
opciones VARCHAR NOT NULL,
votos VARCHAR NOT NULL,
terminada INTEGER NOT NULL,
votantes VARCHAR,
votocada VARCHAR);
"""

#Crea una nueva encuesta
nueva_encuesta="""
INSERT INTO {}(channel_id,titulo,opciones,votos,terminada, votantes, votocada)
VALUES (%s,%s,%s,%s,%s, %s, %s);
"""

#--------- SQL Statements para la tabla de prefijos ---------#
#Crea la tabla de prefijos si no existe
tabla_prefijos = """
CREATE TABLE IF NOT EXISTS {}(
key SERIAL NOT NULL PRIMARY KEY,
prefijo VARCHAR(20) NOT NULL);
"""

#Prefijo del bot por defecto
default_prefix = "g$"

#--------- SQL Statements para la tabla de destacados ---------#
#Crea la tabla de destacados si no existe
tabla_destacados = """
CREATE TABLE IF NOT EXISTS {}(
id_canal VARCHAR(30) NOT NULL PRIMARY KEY,
emoji VARCHAR NOT NULL DEFAULT '⭐',
minimo INT NOT NULL DEFAULT 1,
ids_destacados VARCHAR NOT NULL DEFAULT '',
ids_destaque VARCHAR NOT NULL DEFAULT '');
"""

#--------- SQL Statements para la tabla de confiables ---------#
#Crea la tabla de mutes si no existe
tabla_confiables = """
CREATE TABLE IF NOT EXISTS {}(
user_id VARCHAR(30) NOT NULL);
"""

#Introduce un nuevo miembro confiable
nuevo_confiable = """
INSERT INTO {}(user_id) VALUES (%s);
"""

#Quita a un miembro de la tabla de confiables
quita_confiable = """
DELETE FROM {}
WHERE user_id = %s;
"""

#--------- Variables para el sistema de ayuda ---------#
#Mensaje de ayuda general que explica el sistema
ayuda = """
Esta es la lista de comandos del bot {}. Debajo encontrarán los módulos y, dentro de ellos, cada uno de los comandos.
Al consultar la ayuda general, recibirán este mensaje. Para obtener más información sobre cada una de las funciones \
puedes llamar a este mismo comando pero especificando como primer parámetro el nombre particular. Ídem con los \
módulos.
Por ejemplo, para obtener ayuda respecto al módulo `Prefijos`, puedes hacer:
```{}ayuda utilidad.prefijos```
Y para obtener información sobre el comando `Añadir` del módulo nombrado, usa:
```{}ayuda utilidad.prefijos.añadir```
También puedes usar el orden numérico. Considerando el mismo ejemplo quedaría:
```{}ayuda 1.3.2```
"""

"""
comandos_ayuda = {
"Utilidad": {"Información": ("Información",),
			"Ayuda": ("Ayuda",),
			"Prefijos": ("Ver", "Añadir", "Quitar", "Cambiar"),
			"Ping": ("Ping",)},
"Moderación": {"Nicks": ("Nick (Cambiar)",),
				"Roles": ("Dar", "Quitar", "Cambiar", "Toggle"),
				"Silencio": ("Silenciar", "Desilenciar"),
				"Exclusión": ("Expulsar", "Banear", "Desbanear"),
				"Confiables": ("Agregar", "Quitar", "Toggle")},
"Usuarios": {"Democracia": ("Crear", "Revisar", "Votar", "Cerrar"),
				"Destacados": ("Canal", "Emoji", "Mínimo")},
"Entretenimiento": {"Reverso": ("Reverso",),
					"Decir": ("Decir",),
					"Elegir": ("Elegir",),
					"Avatar": ("Avatar",)}
}
"""

#Lista que contiene los objetos de información que saldrán en la ayuda
descripciones_ayuda = (info_utilidad, info_moderacion, info_usuarios, info_entretenimiento)