import discord
import traceback
import sys

async def maneja_errores(client,event,message):
	print(traceback.format_exc())
	error = sys.exc_info()
	if isinstance(error[1], discord.errors.Forbidden):
		await client.send_message(message.channel,"ERROR 403: PROHIBIDO\nPrueba a subir mi rol de posición.")
	elif isinstance(error[1], discord.errors.HTTPException):
		await client.send_message(message.channel,"ERROR 400: BAD REQUEST\nPrueba a salir corriendo. Muy lejos...")