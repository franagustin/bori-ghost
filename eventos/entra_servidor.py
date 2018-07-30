import psycopg2
import os
from variables import tabla_mute, tabla_encuestas, tabla_prefijos, default_prefix

async def servidor_entro(client, servidor):
	"""Al unirse al server, crea una base de datos."""
	if hasattr(servidor, "id"): #Si tiene id, es un servidor
		#Conecta a la BD o la crea si no existe
		BD_URL=os.getenv("DATABASE_URL")
		base_de_datos = psycopg2.connect(BD_URL, sslmode='require')
		bd = base_de_datos.cursor()
		bd.execute(tabla_mute) #Crea la tabla de silenciados si no existe
		bd.execute(tabla_encuestas)
		bd.execute(tabla_prefijos)
		bd.execute("INSERT INTO prefijos('prefijo') VALUES('%s');", (default_prefix))
		bd.commit()
		bd.close()
		base_de_datos.close() #Cierra la conexión