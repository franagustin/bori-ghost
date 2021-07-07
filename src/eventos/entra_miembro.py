import discord
import psycopg2
import os
from funciones import get_mute_role, get_confiables, get_confiable_role

async def confiable_entrar(client, miembro):
	confiables = get_confiables(miembro.server)
	if miembro.id in confiables:
		confiable_rol = get_confiable_role(miembro.server.roles)
		await client.add_roles(miembro, confiable_rol)

async def silencio_entrar(client, miembro):
	BD_URL = os.getenv('DATABASE_URL')
	silenciado = get_mute_role(miembro.server.roles) #Establece el rol de silenciados para el servidor
	base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
	bd = base_de_datos.cursor()
	bd.execute(f'SELECT discord_id FROM "{miembro.server.id}_silenciados"')
	muteados = bd.fetchall()
	muteados = [dato[0] for dato in muteados] #Lista de ids de los muteados en el server
	if miembro.id in muteados: #Para cada miembro en la lista de silenciados
		await client.add_roles(miembro, silenciado) #Le pone el rol (para evitar perder el silencio)
	bd.close()
	base_de_datos.close()

async def roles_superduperserver(client, miembro):
	if miembro.id=="287424917459173377": #Si es Franquito
		hermanito = discord.utils.get(miembro.server.roles, id="437721721202671629")
		superdupermenos = discord.utils.get(miembro.server.roles, id="338017217650360321")
		await client.add_roles(miembro, hermanito, superdupermenos) #Le pone sus roles
	elif miembro.id=="388711263728828417": #Si es Felipe
		tiernos = discord.utils.get(miembro.server.roles, id="414655214973353986")
		await client.add_roles(miembro, tiernos) #Le pone sus roles
	elif miembro.id=="359534916196892674": #Si es Micha
		rey = discord.utils.get(miembro.server.roles, id="415730343107362826")
		amorcito = discord.utils.get(miembro.server.roles, id="338021657082068992")
		superdupermenos = discord.utils.get(miembro.server.roles, id="338017217650360321")
		await client.add_roles(miembro, rey, amorcito, superdupermenos) #Le pone sus roles
