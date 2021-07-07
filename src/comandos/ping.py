import discord
async def ping(client,message, nick_autor, avatar_autor, mensaje_separado, prefijo):
	"""Comando "ping". Responde "¡Pong!" y lo edita. Luego cambia ese mensaje por un embed que
		contenga el tiempo que tarda en responder, el tiempo que tarda en editar desde que
		responde y el tiempo total entre el primer mensaje y la edición.
		Parámetros: NINGUNO
		Sintaxis:
			ping
		await client.say("Pong!")
	"""
	nick_autor = message.author.nick
	avatar_autor = message.author.avatar_url
	tiempo1=message.timestamp
	msg_pong = await client.send_message(message.channel,"¡Pong!")
	tiempo2=msg_pong.timestamp
	msg_pong = await client.edit_message(msg_pong,msg_pong.content+" `:{}:`".format(tiempo2-tiempo1))
	tiempo3=msg_pong.edited_timestamp
	tiempo_respuesta=tiempo2-tiempo1
	tiempo_respuesta=tiempo_respuesta.seconds*1000+tiempo_respuesta.microseconds/1000
	tiempo_edicion=tiempo3-tiempo2
	tiempo_edicion=tiempo_edicion.seconds*1000+tiempo_edicion.microseconds/1000
	tiempo_total=tiempo3-tiempo1
	tiempo_total=tiempo_total.seconds*1000+tiempo_total.microseconds/1000
	pong_embed=discord.Embed(title=u"\U0001F3D3"+"¡Pong!",
							 description="Me dices ping, te digo pong.",
							 colour=0xDD2E44)
	pong_embed.add_field(name=u"\U0001F54A"+" Tiempo de respuesta",
						 value="Respondí en: {}ms.".format(tiempo_respuesta),
						 inline=False)
	pong_embed.add_field(name=u"\U0000270F"+" Tiempo de edición",
						 value="Edité mi mensaje en: {}ms.".format(tiempo_edicion),
						 inline=False)
	pong_embed.add_field(name=u"\U0001F4F0"+" Tiempo total",
						 value="Entre tu mensaje y mi edición pasaron: {}ms.".format(tiempo_total),
						 inline=False)
	pong_embed.set_thumbnail(url="https://i.imgur.com/QzF08A1.png")
	pong_embed.set_footer(text="Este mensaje es una respuesta a {} ({}#{})".format(nick_autor,
								message.author.name, message.author.discriminator),
						  icon_url=avatar_autor)
	await client.edit_message(msg_pong, new_content=" ", embed=pong_embed)