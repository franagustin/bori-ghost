class informacionComando:
	def __init__(self, nombre, descripcion, alias, parametros, sintaxis, ejemplo, subs, ident=None):
		self.nombre = nombre
		self.descripcion = descripcion
		self.alias = alias
		self.parametros = parametros
		self.sintaxis = sintaxis
		self.ejemplo = ejemplo
		self.subs = []
		for i in range(len(subs)):
			sub_ident = None
			if len(subs[i]) >= 8:
				sub_ident = subs[i][7]
			self.subs.append(informacionComando(subs[i][0], subs[i][1], subs[i][2], subs[i][3], subs[i][4], subs[i][5], subs[i][6], sub_ident))
		if ident != None:
			self.ident = ident
		else:
			self.ident = nombre
	def __str__(self):
		return nombre+": "+descripcion

info_utilidad = informacionComando(
"Utilidad",
"Este módulo contiene los comandos que son útiles para el usuario del bot.",
None,
(None,),
None,
None,
[
#info_informacion
("Información",
"Comando que brinda información sobre este bot.",
("information", "info"),
(None,),
"{}informacion",
"{}info",
[],
"informacion"),
#info_ayuda
("Ayuda",
"Muestra la lista de comandos o el modo de uso y la información sobre cada uno, \
según accedas a la ayuda general o específica.",
("help", "comandos", "commands"),
("Módulo o comando sobre el que se quiere recibir información. **Opcional**: Si no se especifica, se accederá a la ayuda general.",),
"{}ayuda <modulo / comando> (opcional)",
"{}ayuda prefijos.ver",
[]),
#info_prefijos
("Prefijos",
"Comandos que permiten ver o configurar los prefijos disponibles.",
("prefijos", "prefix", "prefixes"),
("Acción que se desea realizar. **Opcional**: Si no se especifica, se asume que quiere verse la lista.","Si se quiere añadir, \
quitar o cambiar a un prefijo, debe especificarse cuál. **Nota**: Sólo si la acción deseada es *añadir*, *quitar* o *cambiar*."),
"{}prefijos <acción> (opcional) <nuevo / viejo prefijo> (si se quiere añadir, quitar o cambiar)",
"{}prefijos ver",
[
#info_prefijos.ver
("Ver",
"Muestra la lista de prefijos disponibles actualmente.",
None,
(None,),
"{}prefijos ver",
"{}prefijos ver",
[]),
("Añadir",
"Agrega un nuevo prefijo a la lista para poder utilizarlo.",
("agregar", "añade", "agrega", "nuevo", "pon", "add", "new"),
("Prefijo que se desea incluir en la lista.",),
"{}prefijos añadir <prefijo>",
"{}prefijos añadir $",
[]),
("Quitar",
"Elimina un prefijo de la lista por lo que deja de ser utilizable.",
("borrar", "quita", "borra", "remove", "delete"),
("Prefijo que se desea remover de la lista.",),
"{}prefijos quitar <prefijo>",
"{}prefijos quitar $",
[]),
("Cambiar",
"Elimina todos los prefijos disponibles y los reemplaza por uno nuevo. Éste se convertirá en el único utilizable.",
("cambia", "solo", "unico", "sólo", "único", "change", "only", "set"),
("Prefijo que quieres establecer como único disponible.",),
"{}prefijos cambiar <prefijo>",
"{}prefijos cambiar $",
[])
]),
#info_ping
("Ping",
"Consulta el tiempo de respuesta del bot.",
None,
(None,),
"{}ping",
"{}ping",
[])
]
)

info_moderacion = informacionComando(
"Moderación",
"En este módulo se encuentran todos los comandos de moderación que los administradores pueden usar. Se requieren permisos especiales \
que varían según cada comando.",
None,
(None,),
None,
None,
[
#info_nick
("Nick",
"Este comando permite cambiar el apodo de uno o más usuarios. Puede usarse para cambiar el propio.\n\
Requiere, en el primer caso, permiso de *administrar apodos* en el servidor y; en el segundo, premiso de *cambiar apodo*.",
("nicks", "setnick", "apodo", "apodos"),
("Usuario cuyo apodo quiere cambiarse. **Nota**: Ha de ser una mención.", "Apodo que se desea darle.",
"**Nota**: Puede cambiarse el apodo de múltiples usuarios, repitiendo estos dos parámetros cuantas veces sea necesario."),
"{}nick <usuario> (mención) <apodo>",
"{}nick @BORI GHOST#1213 Ghost",
[]),
#info_roles
("Roles",
"Comandos que permiten dar o quitar roles a los usuarios. No pueden otorgarse roles que estén por encima del máximo poseído por el moderador.\n\
Requiere permiso de *administrar roles* en el servidor.",
("rol", "role"),
("Acción que se desea realizar. **Opcional**: Si no se especifica, se asumirá *toggle*.", "Usuario a quien desea dársele o quitársele \
un rol. **Nota**: Ha de ser una mención.", "Rol que desea dársele o quitársele. **Nota**: Debe ser el nombre (al menos su primera parte) \
o bien una mención.", "**Nota**: Puede modificarse los roles a varios usuarios a la vez, repitiendo los parámetros 2 y 3 tantas veces \
como sea necesario."),
"{}roles <accion> (opcional) <usuario> (mencion) <rol> (comienzo del nombre o mención)",
"{}roles @BORI GHOST#1213 Developer",
[
#info_roles.dar
("Dar",
"Este comando otorga un rol a un usuario. Si el usuario ya tiene ese rol, no hace nada.\n\
Requiere permiso de *administrar roles* en el servidor.",
("da","dale", "give", "add"),
("Usuario a quien desea dársele un rol. **Nota**: Ha de ser una mención.", "Rol que desea dársele. **Nota**: Debe ser \
el nombre (al menos su primera parte o bien una mención.", "**Nota**: Puede modificarse los roles a varios usuarios a la vez, \
repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}roles dar <usuario> (mención) <rol> (comienzo del nombre o mención)",
"{}roles dar @BORI GHOST#1213 Developer Profesional",
[]),
#info_roles.quitar
("Quitar",
"Este comando remueve un rol a un usuario. Si el usuario ya tiene ese rol, no hace nada.\n\
Requiere permiso de *administrar roles* en el servidor.",
("quita", "quitale","take", "remove"),
("Usuario a quien desea quitársele un rol. **Nota**: Ha de ser una mención.", "Rol que desea quitársele. **Nota**: Debe ser \
el nombre (al menos su primera parte o bien una mención.", "**Nota**: Puede modificarse los roles a varios usuarios a la vez, \
repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}roles quitar <usuario> (mención) <rol> (comienzo del nombre o mención)",
"{}roles quitar @BORI GHOST#1213 Dev",
[]),
#info_roles.cambiar
("Cambiar",
"Este comando modifica los roles a un usuario, dejándole únicamente con el especificado.\n\
Requiere permiso de *administrar roles* en el servidor.",
("cambia", "cambiale", "change", "set"),
("Usuario cuyos roles desean modificarse. **Nota**: Ha de ser una mención.", "Rol que desea dejársele. **Nota**: Debe ser \
el nombre (al menos su primera parte o bien una mención.", "**Nota**: Puede modificarse los roles a varios usuarios a la vez, \
repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}roles cambiar <usuario> (mención) <rol> (comienzo del nombre o mención)",
"{}roles cambiar @BORI GHOST#1213 Developer Prof",
[]),
#info_roles.toggle
("Toggle",
"Este comando otorga o remueve un rol a un usario. Si el usuario ya tiene el rol especificado, se lo quita y, si no lo tiene, se lo da.\n\
Requiere permiso de *administrar roles* en el servidor.",
(None,),
("Usuario a quien desea dársele o quitársele un rol. **Nota**: Ha de ser una mención.", "Rol que desea dársele o quitársele. **Nota**: \
Debe ser el nombre (al menos su primera parte) o bien una mención.", "**Nota**: Puede modificarse los roles a varios usuarios a la vez, \
repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}roles toggle <usuario> (mención) <rol> (comienzo del nombre o mención)",
"{}roles toggle @BORI GHOST#1213 Develop",
[])
]),
#info_silencio
("Silencio",
"Modúlo con comandos que permiten silenciar a los usuarios, impidiéndoles enviar mensajes, y desilenciarlos, cancelando esa prohibición.\n\
Funciona dándoles un rol que debes crear manualmente llamado \"*CALLATE BOLUDO*\" o \"*Muted*\".\n\
Requiere permiso de *administrar roles* o *expulsar miembros* en el servidor.",
None,
(None,),
None,
None,
[
#info_silencio.silenciar
("Silenciar",
"Silencia a uno o más usuarios, impidiéndoles hablar en el servidor por un tiempo determinado. Puede especificarse el motivo por \
el que se los silencia y el tiempo (10min por defecto).\n\
Envía un mensaje al servidor por cada usuario silenciado y otro al propio usuario que incluye el tiempo y el motivo (si fue \
especificado).\n\
Requiere permiso de *administrar roles* o *expulsar miembros* en el servidor.",
("silencia", "mute"),
("Usuario al que se desea silenciar. **Nota**: Debe ser una mención.", "Razón por la que se le desea silenciar. **Opcional**",
"Tiempo durante el que se le desea silenciar. **Opcional**: Si no se especifica, será de 10 minutos. **Nota**: Pueden usarse sufijos \
para indicar distintas unidades de tiempo: **s** = segundos, **m** = minutos, **h** = horas, **d** = días, **w** = semanas, \
**a** = años.",
"**Nota 1**: Puede silenciarse a varios usuarios a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario.",
"**Nota 2**: El orden de los parámetros 2 y 3 es indistinto."),
"{}silenciar <usuario> (mención) <tiempo> (opcional) <razón> (opcional)\
<usuario> (mención) (opcional) <razón> (opcional) <tiempo> (opcional)",
"{}silenciar @BORI GHOST#1213 2a Prueba de silenciado.",
[]),
#info_silencio.desilenciar
("Desilenciar",
"Quita el silencio a uno o más usuarios pudiendo especificar una razón (individual para cada uno).\n\
Envía un mensaje al servidor por cada usuario desilenciado y uno al propio usuario, incluyendo el motivo (si fue especificado).",
("desilencia", "unmute"),
("Usuario al que se desea silenciar. **Nota**: Debe ser una mención.", "Razón por la que se le desea silenciar. **Opcional**",
"**Nota**: Puede desilenciarse a varios usuarios a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}desilenciar <usuario> (mención) <razón> <usuario> (mención) (opcional) <razón> (opcional)",
"{}desilenciar @BORI GHOST#1213 Prueba de desilenciado.",
[])
]),
#info_exclusion
("Exclusión",
"Módulo con comandos que permiten expulsar, banear y desbanear usuarios del servidor.\n\
Requiere permiso de *expulsar miembros*, en el primer caso, y de *banear miembros* en los otros dos.",
None,
(None,),
None,
None,
[
#info_exclusion.excluir
("Excluir",
"Expulsa a uno o más usuarios especificando una razón (individual para cada uno).\n\
Envía un mensaje al servidor por cada usuario excluido y, también, uno a cada usuario avisándole e incluyendo \
el motivo (si fue especificado).\n\
Requiere permiso de *excluir miembros* en el servidor.",
("kick",),
("Usuario al que se desea excluir. **Nota**: Debe ser una mención.", "Razón por la que se le desea excluir. **Opcional**",
"**Nota**: Puede excluirse a varios usuarios a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}excluir <usuario> (mención) <razón> (opcional) <usuario> (mención) (opcional) <razón> (opcional)",
"{}excluir @BORI GHOST#1213 Prueba de exclusión.",
[]),
#info_exclusión.banear
("Banear",
"Banea a uno o más usuarios especificando una razón (individual para cada uno).\n\
Envía un mensaje al servidor por cada usuario baneado y, también, uno a cada usuario avisándole e incluyendo \
el motivo (si fue especificado).\n\
Requiere permiso de *banear miembros* en el servidor.",
("ban",),
("Usuario al que se desea banear. **Nota**: Debe ser una mención.", "Razón por la que se le desea banear. **Opcional**",
"**Nota**: Puede banearse a varios usuarios a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}banear <usuario> (mención) <razón> (opcional> <usuario> (mención) (opcional) <razón> (opcional)",
"{}banear @BORI GHOST#1213 Prueba de ban.",
[]),
#info_exclusión.desbanear
("Desbanear",
"Desbanea a un usuario del servidor pudiendo especificar una razón para ello.\n\
Envía un mensaje en el servidor y puede, opcionalmente, enviar uno al usuario donde figura quién lo desbaneó y la razón \
(si fue especificada).\n\
Requiere permiso de *banear miembros* en el servidor.",
("unban",),
("Usuario al que se desea desbanear. **Nota**: Debe ser una mención.", "Razón por la que se le desea desbanear. **Opcional**",
"Si se le desea enviar un mensaje al usuario o no. **Opcional**. **Nota**: Puede escribirse lo que sea mientras no esté en blanco.",
"**Nota 1**: Puede desbanearse a varios usuarios a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario.",
"**Nota 2**: Entre cada parámetro debe haber un \";\" o un \"|\"."),
"{}desbanear <usuario>; <razón> (opcional); <aviso> (opcional)",
"{}desbanear @BORI GHOST#1213; Prueba de desbaneo; a",
[])
],
"exclusion"),
#info_confiables
("Confiables",
"Comandos que permiten añadir o quitar miembros de la lista de usuarios confiables así como darles el rol correspondiente. Al \
incluirlos en la lista, se les otorgará el rol automáticamente cada vez que entren al servidor.\n\
Funciona con un rol creado a mano llamado \"Confiable\".\n\
Requiere permiso de *administrar roles* en el servidor.",
("confiable", "conf", "confi", "confia", "confio"),
("Acción a realizar. **Opcional**: Si no se especifica, se asume que es toggle.", "Usuario a quien se desea añadir o quitar\
de la lista. **Nota**: Debe ser una mención.", "**Nota**: Puedes confiar en varios usuarios a la vez, repitiendo los \
parámetros anteriores tantas veces como sea necesario."),
"{}confiables <acción> (opcional) <usuario> (mención) <usuario> (mención) (opcional)",
"{}confiables @BORI GHOST#1213",
[
#info_confiables.añadir
("Añadir",
"Este comando añade a un usuario a la lista de confiables y le otorga el rol. Si el usuario ya está allí y tiene el rol, no\
hace nada.\n\
Requiere permiso de *administrar roles* en el servidor.",
("agregar", "añade", "agrega", "pon", "add", "put", "a"),
("Usuario a quien se desea añadir a la lista. **Nota**: Debe ser una mención.", "**Nota**: Puedes añadir a varios usuarios \
a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}confiables añadir <usuario> (mención) <usuario> (mención) (opcional)",
"{}confiables añadir @BORI GHOST#1213",
[]),
#info_confiables.quitar
("Quitar",
"Este comando elimina a un usuario de la lista de confiables y le quita el rol. Si el usuario no está allí ni tiene el rol, no\
hace nada.\n\
Requiere permiso de *administrar roles* en el servidor.",
("sacar", "quita", "saca", "remove", "delete", "rm", "del", "q"),
("Usuario a quien se desea quitar de la lista. **Nota**: Debe ser una mención.", "**Nota**: Puedes quitar a varios usuarios a \
la vez, repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}confiables quitar <usuario> (mención) <usuario> (mención) (opcional)",
"{}confiables quitar @BORI GHOST#1213",
[]),
#info_confiables.toggle
("Toggle",
"Este comando agrega o elimina usuarios de la lista de confiables y les otorga o les quita el rol. Si el usuario está \
en la lista, lo quita; y si no está, lo añade.\n\
Requiere permiso de *administrar roles* en el servidor.",
None,
("Usuario a quien se desea añadir o quitar de la lista. **Nota: Debe ser una mención.", "**Nota**: Puedes confiar en varios \
usuarios a la vez, repitiendo los parámetros anteriores tantas veces como sea necesario."),
"{}confiables toggle <usuario> (mención) <usuario> (mención) (opcional)",
"{}confiables toggle @BORI GHOST#1213",
[])
])
],
"moderacion")

info_usuarios = informacionComando(
"Usuarios",
"Módulo de uso para todos los miembros del servidor. Contiene comandos útiles y entretenidos.",
None,
(None,),
None,
None,
[
#info_democracia
("Democracia",
"Comandos que permiten a los miembros ejercer sus derechos cívicos llevando a cabo votaciones.\n\
Sólo se permite una votación activa por canal.",
("votar", "vota", "votacion", "encuesta", "vote", "poll"),
("Acción que se desea realizar. **Nota**: No especificarla indica que se quiere votar en una encuesta.",
"Opción que deseas votar. Ya sea escribiendo exactamente su contenido textual o su número de orden. **Nota**: Sólo para votar.",
"Parámetros variables según la acción. Consultar ayudas específicas de cada una."),
"{}democracia <acción> / <opción>",
"{}democracia 1",
[
#info_democracia.crear
("Crear",
"Crea una encuesta. Sólo puede haber una activa en cada canal, para comenzar una nueva, debes cerrar la anterior.",
("empezar", "nueva", "create", "start", "new"),
("Título de la encuesta: Temática o pregunta a la que se desea contestar. **Opcional**", "Opción A", "Opción B",
"Otras opciones (opcional)",
"**IMPORTANTE**: Puedes incluir más de dos opciones pero no menos.",
"**Nota 1**: El orden de los primeros tres parámetros es indistinto.",
"**Nota 2**: Los parámetros deben estar separados por \";\" o \"|\"."),
"{}democracia crear <titulo> (opcional); <opcion A> (opcional); <opcion B> (opcional)",
"{}democracia crear t:¿T'agrada?; M'agrada; M'encanta; No m'agrada",
[]),
#info_democracia.revisar
("Revisar",
"Consulta los resultados parciales de la encuesta en curso. El mensaje se elimina tras diez segundos.",
("ver", "consultar", "checkear", "view", "check"),
(None,),
"{}democracia revisar",
"{}democracia revisar",
[]),
#info_democracia.votar
("Votar",
"Para votar en una encuesta, sólo usa el comando de democracia sin ningún parámetro de acción, seguido por la \
opción que desees, o copiada textualmente o por su número de orden.",
None,
("Opción que deseas votar. Ya sea escribiendo exactamente su contenido textual o su número de orden.",),
"{}democracia <opción>",
"{}democracia 5",
[]),
#info_democracia.cerrar
("Cerrar",
"Cierra la encuesta en curso. Es necesario si quieres abrir otra.",
("terminar", "finalizar", "fin", "close", "end"),
(None,),
"{}democracia cerrar",
"{}democracia cerrar",
[]),
]),
#info_destacados
("Destacados",
"Sistema que permite destacar mensajes a través de reacciones. Coloca un embed con su contenido en el canal designado.",
None,
(None,),
None,
None,
[
#info_destacados.canal
("Canal",
"Comando que permite consultar el canal desginado para los mensajes destacados o cambiarlos.\n\
Requiere permiso de *administrar canales* en el servidor.\n\
**__Comando__**: dcanal",
("dchannel",),
("Canal donde se desea que salgan los mensajes destacados. **Nota**: Debe ser una mención. **Opcional**: De \
no especificarse, el bot responderá mencionando el canal designado actualmente.",),
"{}dcanal <canal>",
"{}dcanal #parábolas",
[]),
#info_destacados.emoji
("Emoji",
"Comando que permite consultar el emoji designado para destacar mensajes al reaccionar con él o cambiarlo.\n\
Requiere permiso de *administrar canales* o *administrar mensajes* en el servidor.\n\
**__Comando__**: demoji",
("dreaccion", "dreaction"),
("Emoji con el cual se desea destacar mensajes. **Nota**: Puede ser un emoji personalizado del servidor.\
**Opcional**: De no especificarse, el bot responderá con el emoji designado actualmente.",),
"{}demoji <emoji>",
"{}demoji :star:",
[]),
#info_destacados.minimo
("Mínimo",
"Comando que permite consultar el mínimo de reacciones requeridas para destacar mensajes o modificarlo.\n\
Requiere permiso de *administrar canales* o *administrar mensajes* en el servidor.\n\
**__Comando__**: dminimo",
("dminimum", "dmin"),
("Cantidad de reacciones que se desea sean necesarias para destacar un mensaje. **Nota**: Debe ser un número\
entero. **Opcional**: De no especificarse, el bot responderá con el mínimo actual.",),
"{}dminimo <minimo> (entero)",
"{}dminimo 5",
[],
"minimo")
])
])

info_entretenimiento = informacionComando(
"Entretenimiento",
"Módulo que contiene un cambalache de comandos cuyo fin es entretener, divertir y pasar el rato. Algunos también\
pueden ser útiles.",
None,
(None,),
None,
None,
[
#info_reverso
("Reverso",
"Diré el mismo mensaje que tú... !séver la oreP¡",
("reves", "revés", "reverse"),
("Texto que quieres verme repetir al revés.",),
"{}reverso <texto>",
"{}reverso arribalabirra",
[]),
("Decir",
"Diré exactamente lo que me digas... Sin excepciones.",
("di", "say"),
("Texto que quieres verme decir.",),
"{}decir <texto>",
"{}decir No eres profesional.",
[]),
("Elegir",
"Decidiré por ti entre las opciones que me brindes.",
("elige", "choose"),
("Opción 1", "Opción 2", "Opción 3 **Opcional**", "**IMPORTANTE**: Puedes hacerme elegir entre más de dos opciones pero, \
por motivos obvios, no entre menos.", "**Nota**: Las opciones deben estar separadas por \";\" o \"|\"."),
"{}elegir <opción>; <opción>; <opción> (opcional)",
"{}elegir Reír | Gozar | Vivir mi vida lalalala",
[]),
("Avatar",
"Enviaré el avatar de los usuarios que me digas.",
None,
("Usuario cuyo avatar quieres ver. **Nota**: Debe ser una mención. **Opcional**: Si no se especifica, te enviaré el tuyo.",
"**Nota**: Puedes mencionar a más de un usuario y te enviaré el avatar de cada uno."),
"{}avatar <usuario> (mención) (opcional) <usuario> (mención) (opcional)",
"{}avatar @BORI GHOST#1213",
[])
])