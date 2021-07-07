import os
import discord
import psycopg2
from variables import tabla_destacados

async def editar_destacados(client, antes, despues):
	BD_URL = os.getenv("DATABASE_URL")
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
	bd = base_de_datos.cursor()
	bd.execute(f'SELECT id_canal, ids_destacados, ids_destaque FROM "{antes.server.id}_destacados"'),
	try:
		id_canal, ids_destacados, ids_destaque = bd.fetchone()
	except TypeError: return
	ids_destacados = ids_destacados.split(",")
	ids_destaque = ids_destaque.split(",")
	if antes.id in ids_destacados:
		i = ids_destacados.index(antes.id)
		channel = discord.utils.get(antes.server.channels, id= id_canal)
		mensaje_a_editar = await client.get_message(channel, ids_destaque[i])
		embed = discord.Embed.from_data(mensaje_a_editar.embeds[0])
		embed.description = antes.content
		if antes.content != despues.content:
			embed.description = despues.content
		if 'thumbnail' in mensaje_a_editar.embeds[0]:
			embed.set_thumbnail(url=mensaje_a_editar.embeds[0]['thumbnail']['url'])
		if 'image' in mensaje_a_editar.embeds[0]:
			embed.set_image(url=mensaje_a_editar.embeds[0]['image']['url'])
		if 'footer' in mensaje_a_editar.embeds[0]:
			embed.set_footer(icon_url=mensaje_a_editar.embeds[0]['footer']['icon_url'],
								text=mensaje_a_editar.embeds[0]['footer']['text'])
		if antes.embeds != despues.embeds:
			if 'author' in despues.embeds[0]:
				if 'url' in despues.embeds[0]['author']:
					embed.description += "\n\n[**"+despues.embeds[0]['author']['name']+"**]("+\
											despues.embeds[0]['author']['url']+")"
				else:
					embed.description += "\n\n**"+despues.embeds[0]['author']['name']+"**"
			if 'title' in despues.embeds[0]:
				embed.description += "\n\n**__"+despues.embeds[0]['title']+"__**"
			if 'description' in despues.embeds[0]:
				embed.description += "\n\n"+despues.embeds[0]['description']
			if 'fields' in despues.embeds[0]:
				for campo in despues.embeds[0]['fields']:
					embed.add_field(name=campo['name'], value=campo['value'])
			if 'image' in despues.embeds[0]:
				embed.set_image(url=despues.embeds[0]['image']['url'])
			if 'footer' in despues.embeds[0]:
				embed.add_field(name="Footer", value=despues.embeds[0]['footer']['text'])
		print(antes.embeds, despues.embeds, mensaje_a_editar.embeds, embed.to_dict(), sep="\n")
		await client.edit_message(mensaje_a_editar, embed=embed)