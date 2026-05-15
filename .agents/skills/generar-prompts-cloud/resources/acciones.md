# Acciones soportadas — Power Automate Cloud Flow (Copilot Cloud)

Uso: consultado por `generar-prompts-cloud` al redactar cada prompt para verificar que el
conector y la acción existen con el nombre exacto que aparece en Power Automate.

## Cómo usar este archivo
Cuando el PDD describe una operación, busca en la categoría correspondiente la acción exacta.
Usa SIEMPRE el nombre de la columna "Nombre exacto en Power Automate" en el prompt —
nunca parafrasear ni abreviar.

---

## Office 365 Outlook

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Cuando llega un nuevo correo electrónico (V3) | Trigger | Se dispara al recibir un correo | Carpeta (Bandeja de entrada por defecto) |
| Obtener correo electrónico (V2) | Acción | Recupera un correo por ID | Id. de mensaje |
| Enviar un correo electrónico (V2) | Acción | Envía un correo desde la cuenta | Para, Asunto, Cuerpo |
| Mover correo electrónico (V2) | Acción | Mueve un correo a otra carpeta | Id. de mensaje, Carpeta de destino |
| Obtener adjuntos (V2) | Acción | Lista los adjuntos de un correo | Id. de mensaje |
| Exportar correo electrónico (V2) | Acción | Exporta un correo como archivo .eml | Id. de mensaje |
| Marcar como leído o no leído (V2) | Acción | Cambia estado de lectura | Id. de mensaje, Estado |
| Responder a un correo electrónico (V2) | Acción | Responde a un correo | Id. de mensaje, Cuerpo |
| Crear borrador (V2) | Acción | Crea un borrador (NO envía) | Para, Asunto, Cuerpo |

---

## SharePoint

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Cuando se crea o modifica un elemento | Trigger | Se dispara al crear/modificar un elemento de lista | Dirección del sitio, Nombre de la lista |
| Cuando se crea un archivo | Trigger | Se dispara al crear un archivo en una biblioteca | Dirección del sitio, Nombre de la biblioteca |
| Obtener elementos | Acción | Lista elementos de una lista (con filtros OData opcionales) | Dirección del sitio, Nombre de la lista |
| Obtener elemento | Acción | Obtiene un elemento específico por ID | Dirección del sitio, Nombre de la lista, Id. |
| Crear elemento | Acción | Crea un elemento en una lista | Dirección del sitio, Nombre de la lista, campos |
| Actualizar elemento | Acción | Actualiza un elemento existente por ID | Dirección del sitio, Nombre de la lista, Id. |
| Eliminar elemento | Acción | Elimina un elemento de una lista | Dirección del sitio, Nombre de la lista, Id. |
| Obtener contenido del archivo | Acción | Descarga el contenido binario de un archivo | Dirección del sitio, Identificador del archivo |
| Crear archivo | Acción | Sube un archivo a una biblioteca | Dirección del sitio, Ruta de la carpeta, Nombre del archivo, Contenido del archivo |
| Enviar una solicitud HTTP a SharePoint | Acción | Llamada REST a la API de SharePoint | Dirección del sitio, Método, URI |

---

## Excel Online (Business)

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Listar las filas presentes en una tabla | Acción | Obtiene todas las filas de una tabla como array | Ubicación, Biblioteca de documentos, Archivo, Tabla |
| Agregar una fila a una tabla | Acción | Agrega una fila al final de la tabla | Ubicación, Biblioteca de documentos, Archivo, Tabla, campos |
| Obtener una fila | Acción | Obtiene una fila específica por ID de fila | Ubicación, Biblioteca de documentos, Archivo, Tabla, Id. de fila |
| Actualizar una fila | Acción | Modifica una fila existente | Ubicación, Biblioteca de documentos, Archivo, Tabla, Id. de fila, campos |
| Eliminar una fila | Acción | Elimina una fila de la tabla | Ubicación, Biblioteca de documentos, Archivo, Tabla, Id. de fila |
| Ejecutar script | Acción | Ejecuta un Office Script en el archivo | Ubicación, Biblioteca de documentos, Archivo, Script |

---

## OneDrive for Business

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Cuando se crea un archivo | Trigger | Se dispara al crear un archivo en OneDrive | Carpeta |
| Crear archivo | Acción | Sube un archivo a OneDrive | Ruta de la carpeta, Nombre de archivo, Contenido del archivo |
| Obtener contenido del archivo | Acción | Descarga el contenido de un archivo | Archivo |
| Crear carpeta | Acción | Crea una carpeta en OneDrive | Ruta de la carpeta principal, Nombre de la carpeta |

---

## Microsoft Teams

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Publicar un mensaje en un chat o canal | Acción | Envía un mensaje a un canal o chat | Publicar como, Publicar en, Equipo, Canal, Mensaje |
| Cuando se menciona en un canal | Trigger | Se dispara al mencionar al flow en Teams | Equipo, Canal |

---

## Approvals (Aprobaciones)

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Iniciar y esperar una aprobación | Acción | Envía solicitud de aprobación y espera respuesta | Tipo de aprobación, Título, Asignado a, Detalles |
| Obtener las respuestas de aprobación | Acción | Obtiene las respuestas de una aprobación existente | Id. de aprobación |

---

## Dataverse

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Cuando se agrega, modifica o elimina una fila | Trigger | Se dispara ante cambios en una tabla de Dataverse | Cambiar tipo, Nombre de tabla |
| Listar filas | Acción | Lista registros de una tabla con filtros OData | Nombre de tabla |
| Agregar una nueva fila | Acción | Crea un registro en una tabla | Nombre de tabla, campos |
| Actualizar una fila | Acción | Modifica un registro existente | Nombre de tabla, Id. de fila, campos |
| Eliminar una fila | Acción | Elimina un registro | Nombre de tabla, Id. de fila |

---

## Control General (acciones nativas de Power Automate)

| Nombre exacto en Power Automate | Tipo | Descripción | Parámetros obligatorios |
|---|---|---|---|
| Inicializar variable | Acción | Crea una variable de tipo y valor específico | Nombre, Tipo, Valor |
| Establecer variable | Acción | Cambia el valor de una variable existente | Nombre, Valor |
| Incrementar variable | Acción | Incrementa una variable numérica en N | Nombre, Valor |
| Anexar a la variable de cadena | Acción | Concatena texto a una variable Str | Nombre, Valor a anexar |
| Condición | Acción | Bloque If con rama Verdadero y Falso | Expresión de condición |
| Aplicar a cada uno | Acción | Bucle sobre un array o colección | Seleccionar una salida de los pasos anteriores |
| Hacer hasta | Acción | Bucle que repite hasta que la condición sea falsa | Condición de salida, Límite |
| Ámbito | Acción | Agrupa acciones (equivalente a Try) | Nombre del ámbito |
| Terminar | Acción | Finaliza el flow como Correcto, Cancelado o Fallido | Estado, Código, Mensaje |
| Redactar | Acción | Guarda un valor/expresión como output reutilizable | Entradas |
| Analizar JSON | Acción | Parsea un string JSON a objeto | Contenido, Esquema |
| Filtrar matriz | Acción | Filtra un array según una condición | De, Filtro |
| Seleccionar | Acción | Mapea un array a otro con transformación de campos | De, Asignar |
| Unirse | Acción | Une elementos de un array en un string | De, Unirse con |
| Crear tabla HTML | Acción | Convierte un array en tabla HTML | De |
| HTTP | Acción | Realiza una llamada HTTP a cualquier API | Método, URI |

---

## Acciones NO soportadas (o limitadas) por Copilot Cloud

| Operación | Por qué no la soporta | Alternativa recomendada |
|---|---|---|
| Conectores Premium sin licencia (Salesforce, SAP, ServiceNow, etc.) | Requieren licencia Premium de Power Automate | Verificar con el cliente si tienen la licencia; indicar en nota_desarrollador |
| Acciones On-premises (bases de datos locales, SAP on-prem) | Requieren Data Gateway configurado previamente | Indicar en nota_desarrollador que el dev debe configurar el gateway |
| Llamar a un Desktop Flow (Power Automate Desktop) | Requiere configuración del gateway y la máquina destino | Usar acción "Ejecutar un flujo de escritorio" del conector Power Automate Desktop; indicar en nota_desarrollador |
| Crear conexiones de conectores desde el flow | Las conexiones se configuran en la cuenta del usuario, no en el flow | Indicar en nota_desarrollador que la conexión debe existir previamente |
| Custom Connectors (conectores personalizados) | Requieren desarrollo previo por un administrador | Indicar en nota_desarrollador |
| Webhooks (recibir eventos externos) | Requieren configuración en el sistema externo | Indicar en nota_desarrollador cómo registrar el endpoint del trigger |
