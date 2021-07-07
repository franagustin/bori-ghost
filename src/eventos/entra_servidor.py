import psycopg2
import os
from variables import tabla_mute, tabla_encuestas, tabla_prefijos, tabla_destacados, tabla_confiables, default_prefix

async def servidor_entro(client, servidor):
	"""Al unirse al server, crea una base de datos."""
	if hasattr(servidor, "id"): #Si tiene id, es un servidor
		#Conecta a la BD o la crea si no existe
		BD_URL=os.getenv("DATABASE_URL")
		base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
		bd = base_de_datos.cursor()
		bd.execute(tabla_mute.format('"'+servidor.id+'_silenciados"',)) #Crea la tabla de silenciados si no existe
		bd.execute(tabla_encuestas.format('"'+servidor.id+'_encuestas"',))
		bd.execute(tabla_prefijos.format('"'+servidor.id+'_prefijos"',))
		bd.execute(tabla_destacados.format('"'+servidor.id+'_destacados"',))
		bd.execute(tabla_confiables.format('"'+servidor.id+'_confiables"',))
		bd.execute(f'INSERT INTO "{servidor.id}_prefijos"(prefijo) VALUES(%s);', (default_prefix,))
		base_de_datos.commit()
		bd.close()
		base_de_datos.close() #Cierra la conexión