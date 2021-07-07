import discord
import re
from funciones import borrar_repetidos

async def toggle_roles(client, message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	if message.author.server_permissions.manage_roles:
		for miembro in message.mentions:
			mencion = re.search("<@!?{}>".format(miembro.id), message.content)
			i = mensaje_separado.index(mencion.group())+1
			rol = ""
			Rol = None
			while i < len(mensaje_separado):
				if len(message.role_mentions) == 1:
					if mensaje_separado[i] in message.role_mentions[0].mention:
						Rol = discord.utils.get(message.server.roles, mention = mensaje_separado[i])
						i = len(mensaje_separado)
				else:
					if not re.search("<@!?[0-9]+>", mensaje_separado[i]):
						if mensaje_separado[i] != "\n":
							rol += mensaje_separado[i]+" "
						i += 1
					else:
						i = len(mensaje_separado)
			rol = borrar_repetidos(rol, " ")
			if Rol == None:
				for rol_server in message.server.roles:
					if Rol == None:
						if rol_server.name.lower().startswith(rol.lower()):
							Rol = rol_server
			if Rol == None:
				await client.send_typing(message.channel)
				await client.send_message(message.channel, "No juegues conmigo que soy profesional, tienes que especificar un rol válido en tu mac.")
			else:
				puede = False
				for rol_autor in message.author.roles:
					if rol_autor.position > Rol.position:
						puede = True
				if puede or message.author == message.server.owner:
					if mensaje_separado[1] in {"cambiar", "cambia", "cambiale", "change", "set"}:
						await client.replace_roles(miembro, Rol)
						await client.send_typing(message.channel)
						await client.send_message(message.channel, "{} es ahora el único rol de {}".format(Rol,
																	miembro.display_name))
					else:
						mensaje = "**{}** *{}* tiene ese rol. Hacerme perder el tiempo no es profesional"
						if Rol in miembro.roles:
							if mensaje_separado[1] not in {"dar", "da", "dale", "give", "add"}:
								quita_mensaje = "A *{}* se le ha quitado el rol '**{}**'."
								await client.remove_roles(miembro, Rol)
								await client.send_typing(message.channel)
								await client.send_message(message.channel, quita_mensaje.format(miembro.display_name,Rol.name))
							else:
								await client.send_typing(message.channel)
								await client.send_message(message.channel, mensaje.format(miembro.display_name, "ya"))
						else:
							if mensaje_separado[1] not in {"quitar", "quita", "quitale", "take", "remove"}:
								da_mensaje = "A *{}* se le ha concedido el rol '**{}**'."
								await client.add_roles(miembro, Rol)
								await client.send_typing(message.channel)
								await client.send_message(message.channel, da_mensaje.format(miembro.display_name,Rol.name))
							else:
								await client.send_typing(message.channel)
								await client.send_message(message.channel, mensaje.format(miembro.display_name, "no"))
				else:
					error_permisos = "No tienes los permisos suficientes para eso. Tal vez no eres tan profesional como creí..."
					await client.send_typing(message.channel)
					await client.send_message(message.channel, error_permisos)
	else:
		await client.send_typing(message.channel)
		await client.send_message(message.channel, "No eres profesional, cómprate una MAC y tal vez puedas editar roles.")