import discord
import listas
import os

#Carga el token del bot desde las variables de ambiente
TOKEN = os.getenv("TOKEN")

#Crea el cliente
client = discord.Client()

@client.event
async def on_ready():
	"""
	Código que se ejecuta al estar listo el bot.
	"""
	#Enlace para invitar al bot a un servidor
	invitacion = "Invitación: https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=469888071&scope=bot"
	#Imprime un mensaje avisando que está conectado y la invitación
	print("Logged in as "+client.user.name, invitacion.format(client.user.id), sep="\n")

@client.event
async def on_server_join(servidor):
	"""
	Código que se ejecuta cada vez que el bot se une a un servidor.
	"""
	#Para cada funcion especificada en la lista
	for funcion in listas.evs["entra_servidor"]:
		#La ejecuta
		await funcion(client, servidor)

@client.event
async def on_member_join(miembro):
	"""
	Código que se ejecuta cada vez que un nuevo miembro se une al servidor.
	"""
	if hasattr(miembro.server, "id"): #Si es en un servidor
		#Para cada función especificada en la lista
		for funcion in listas.evs["entra_miembro"]:
			#La ejecuta
			await funcion(client, miembro)

@client.event
async def on_message(message):
	"""
	Código que se ejecuta cada vez que un mensaje es recibido.
	"""
	if hasattr(message.server, "id"): #Si es en un servidor
		#Para cada función especificada en la lista
		for funcion in listas.evs["por_mensaje"]:
			#La ejecuta
			await funcion(client, message)

@client.event
async def on_reaction_add(reaction,user):
	"""
	Código que se ejecuta cada vez que alguien reacciona a un mensaje.
	"""
	if hasattr(reaction.message.server, "id"): #Si es en un servidor
		#Para cada función especificada en la lista
		for funcion in listas.evs["pone_reaccion"]:
			#La ejecuta
			await funcion(client,reaction,user)

@client.event
async def on_reaction_remove(reaction,user):
	"""
	Código que se ejecuta cada vez que alguien quita una reacción de un mensaje.
	"""
	if hasattr(reaction.message.server, "id"): #Si es en un servidor
		#Para cada función especificada en la lista
		for funcion in listas.evs["quita_reaccion"]:
			#La ejecuta
			await funcion(client,reaction,user)

@client.event
async def on_message_edit(before, after):
	"""
	Código que se ejecuta cada vez que un mensaje es editado.
	"""
	if hasattr(before.server, "id"): #Si es en un servidor
		#Para cada función especificada en la lista
		for funcion in listas.evs["en_edicion"]:
			#La ejecuta
			await funcion(client, before, after)

@client.event
async def on_error(event, *args, **kwargs):
	"""
	Código que se ejecuta cada vez que se produce un error.
	"""
	#Para cada función en la lista
	for funcion in listas.evs["en_error"]:
		#La ejecuta
		await funcion(client,event,args[0])

if __name__ == "__main__": #Si estoy ejecutándolo desde este mismo archivo
	#Para cada tarea en la lista
	for tarea in listas.tasks:
		#La agrega al grupo de tareas a ejecutar en bucle
		client.loop.create_task(tarea(client))
	client.run(TOKEN) #Ejecuta el bot (lo enciende)