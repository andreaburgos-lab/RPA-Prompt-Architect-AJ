---
name: generar-prompts-autopilot-uipath
description: |
  Genera prompts optimizados para el Autopilot de UiPath (Studio Desktop y Studio Web)
  a partir del JSON de analisis de requerimientos (PDD/SDD).
  Se activa internamente desde analizar-pdd o hibrido para reqs con plataforma
  Studio Desktop o Studio Web. Produce prompts secuenciales especificos con rutas,
  nombres de assets, queues, variables y actividades reales del documento de diseno.
  Cada prompt esta calibrado para maximizar la cantidad de actividades generadas
  correctamente en una sola pasada de Autopilot.
  No debe ser usado directamente por el usuario final.
---

# Skill: Generar Prompts para UiPath Autopilot (Studio Desktop / Studio Web)

---

## Contexto del motor Autopilot

UiPath Autopilot usa lenguaje natural para generar secuencias de actividades en Studio
Desktop (panel Autopilot / anotacion en Sequence) y Studio Web (Generate with Autopilot).
El motor subyacente es una mezcla de modelos propietarios de UiPath y modelos de terceros
(Google Gemini 2.5 Flash/Pro, Gemini 2.0 Flash segun el caso de uso).

El servicio de generacion se actualiza mensualmente e interpreta el prompt dentro del
contexto del archivo XAML o workflow abierto en ese momento:
- Variables definidas en el archivo actual
- Actividades previamente usadas en el workflow actual
- Assets y paquetes disponibles via Data Manager
- Elementos del Object Repository referenciados en el proyecto

Autopilot NO puede acceder a:
- Otros archivos de workflow del proyecto
- Variables globales
- La estructura completa del proyecto
- Assets, queues u objetos del OR que no existan previamente en Orchestrator/OR

---

## Principios de prompting para Autopilot — basados en documentacion oficial y comunidad

**Principio 1 — Acciones pequenas y concretas (Granularidad 1 a N):**
Autopilot genera secuencias mas precisas cuando se le dan pasos concretos y separados.
No limitarse a 4 prompts. Generar de 1 a N prompts segun sea necesario para cubrir
entre el 80% y 100% de la funcionalidad. Cada prompt debe cubrir entre 3 y 8 actividades.
Si un requerimiento es complejo, dividirlo en tantos prompts como sea necesario para no perder detalle.

**Principio 2 — Voz activa y verbos de accion:**
Usar verbos de accion directos que correspondan a actividades reales de UiPath:
  Leer Excel -> "Read Range from Excel file [ruta] sheet [hoja] store in [variable]"
  Escribir Excel -> "Write Range to Excel file [ruta] sheet [hoja] from [variable]"
  Enviar correo -> "Send email to [destinatario] subject [asunto] body [cuerpo]"
  Navegar web -> "Navigate browser to [URL]"
  Click UI -> "Click on element [NombreEnOR] in [NombreAplicacion]"
  Extraer asset -> "Get asset named [NombreAsset] from Orchestrator folder [NombreCarpeta]"

**Principio 3 — Rutas y valores reales, nunca en blanco:**
Si el PDD define rutas, nombres de archivo, URLs o nombres de asset, incluirlos
LITERALMENTE en el prompt. Si el PDD no los define, usar placeholders descriptivos:
  Ruta desconocida:     C:\RPA\[NombreProyecto]\[NombreArchivo].xlsx
  Asset desconocido:    [NombreAsset_Aqui]
  URL desconocida:      https://[url-del-sistema-aqui]
  Hoja desconocida:     [NombreHoja]
  Queue desconocida:    [NombreQueue]
  Carpeta Orchestrator: [NombreCarpeta]
NUNCA omitir el parametro ni usar texto vago como "el archivo" o "la ruta".

**Principio 4 — Prerrequisitos antes del prompt (critico):**
Autopilot FALLA silenciosamente si los recursos no existen antes del prompt.
Para cada requerimiento verificar que existen antes de generar:
  - Object Repository: elementos UI deben estar capturados y nombrados en el OR
  - Assets de Orchestrator: deben existir en la carpeta correcta ANTES del prompt
  - Queues de Orchestrator: deben existir en Orchestrator ANTES del prompt
  - Archivos/carpetas: las rutas mencionadas deben existir en el robot
Documentar TODOS estos prerrequisitos en instruccion_previa del Prompt 1.

**Principio 5 — Especificar el paquete de actividades cuando hay ambiguedad:**
Autopilot favorece actividades que ya se han usado en el workflow actual.
Si hay posible ambiguedad (ej: enviar correo puede ser SMTP o Outlook), especificar
el paquete: "Send email using UiPath.Mail.Activities" o "using GSuite Activities".
Ejemplos de especificacion de paquete en prompt:
  "Read email using UiPath.Mail.Activities"
  "Write to Excel using UiPath.Excel.Activities"
  "Get asset using UiPath.Core.Activities"

**Principio 6 — Logica condicional con formato If-Else explicito:**
Para actividades de decision, escribir el If-Else de forma explicita con la condicion
exacta del PDD. Autopilot no infiere condiciones; deben estar literalmente en el prompt.
Formato recomendado:
  "If [condicion exacta]: [accion rama verdadera]. Else: [accion rama falsa]."
  "If [variable] is empty, log message '[mensaje de error]'. Else [siguiente accion]."

**Principio 7 — Nombrar variables con tipo y contexto:**
Incluir el nombre exacto de la variable en el prompt para que Autopilot la cree
o la reutilice si ya existe. Usar nomenclatura Beecker con prefijo de tipo:
  String   -> str_  -> str_NombreVariable (ej: str_RutaArchivo)
  Integer  -> int_  -> int_NombreVariable (ej: int_ContadorFilas)
  Boolean  -> bln_  -> bln_NombreVariable (ej: bln_EjecucionExitosa)
  DataTable -> dt_  -> dt_NombreVariable  (ej: dt_DatosExcel)
  List     -> lst_  -> lst_NombreVariable (ej: lst_Correos)
  GenericValue -> gv_ -> gv_NombreVariable
En el prompt: "store result in variable str_RutaArchivo" o "save emails to lst_Correos"

**Principio 8 — UI Automation requiere Object Repository previo:**
Autopilot usa matching semantico del OR para encontrar elementos UI.
El prompt debe referenciar el nombre EXACTO del elemento como esta en el OR.
Si el elemento no existe en el OR, el prompt fallara en la UI automation.
Para elementos UI siempre especificar: nombre del elemento en OR, aplicacion/browser,
y la accion (Click, Type Into, Get Text, Check App State, etc.).
Formato: "Click on [NombreElementoEnOR] in [NombreAplicacionEnOR]"
         "Type [valor] into [NombreCampoEnOR] in application [NombreApp]"

**Principio 9 — Anotaciones en Sequence para prompts en Studio Desktop:**
En Studio Desktop, el prompt se pega en la anotacion de una Sequence vacia
(clic derecho > Add Annotation o activar annotation > Generate).
Una Sequence por prompt. El contexto de variables y actividades previas
ya usadas en el workflow actual se mantiene entre prompts del mismo archivo XAML.
En Studio Web, el prompt se ingresa en la barra de busqueda > Generate with Autopilot,
o desde Actions > Annotate with Autopilot en cualquier Sequence/Scope.

**Principio 10 — Longitud optima de prompt y Cobertura de Campos:**
No existe un limite de caracteres documentado oficialmente, pero se recomienda:
  - Prompts CORTOS y ESPECIFICOS generan mejores resultados que prompts largos.
  - Si el PDD lista muchos campos (ej: 20+ campos), NOMBRARLOS TODOS. Si no caben,
    usar sub-prompts (2a, 2b...).
  - Apuntar a prompts de entre 200 y 600 palabras para cobertura optima.
  - El prompt DEBE incluir explicitamente "For Each" si hay iteracion de correos/filas.
  - Diferenciar claramente entre extraer texto de un adjunto y simplemente guardarlo.

**Principio 11 — Lo que Autopilot NO puede generar (solo nota_desarrollador):**
Las siguientes acciones requieren intervencion manual del desarrollador:
  - Crear Assets o Queues en Orchestrator (deben existir antes del prompt)
  - Crear elementos en el Object Repository (deben capturarse antes del prompt)
  - Configurar Connection Strings o credenciales de Integration Service
  - Workflows padre (Main.xaml) o REFramework: Autopilot genera dentro de un XAML,
    no crea la estructura REFramework completa
  - Selectores UI complejos o dinámicos que requieren UiExplorer
  - Actividades de Document Understanding con modelos ML personalizados
  - Actividades de Computer Vision con coordenadas especificas
  Para estas, escribir en nota_desarrollador: "Requiere configuracion manual:
  [descripcion exacta de lo que el dev debe hacer antes o despues del prompt]."

**Principio 12 — Contexto persistente dentro del mismo archivo XAML:**
Autopilot recuerda en la sesion actual las variables y actividades creadas
en el mismo archivo XAML. Aprovechar esto:
  - Prompt 1 establece variables y configuraciones iniciales
  - Prompts siguientes pueden referenciar esas variables por nombre sin redefinirlas
  - Cambiar de archivo XAML reinicia el contexto de Autopilot para ese archivo

---

## Estructura de prompts por requerimiento

Para cada requerimiento generar una secuencia de 1 a N prompts asegurando cobertura total (80-100%):

### Paso 1: Inicializacion de variables y configuracion

Establece TODAS las variables del workflow y la configuracion inicial.
"Create string variable str_[NombreReq]FilePath with value 'C:\RPA\[Proyecto]\[Archivo.xlsx]'.
Create string variable str_Status with empty value.
Create string variable str_Module with value '[NombreWorkflow]'.
[Si hay DataTable: Create DataTable variable dt_[NombreReq].]
Add a Log Message activity with level Information and message 'Starting [NombreReq] workflow'."

### Paso 2: Logica de Proceso (1 a N prompts)

**Manejo de Iteraciones:**
"Get Mail Messages from Outlook. For each email in the list: save attachments to 'C:\RPA\Adjuntos\' and store subject in str_Asunto."

**Extraccion y Mapeo Masivo (REGLA DE ORO):**
"Read Range from Excel file. The DataTable contains the following columns: {Col1}, {Col2}, {Col3}, {Col4}... {NOMBRAR TODAS LAS COLUMNAS DEL PDD}."

**UI Automation con Object Repository:**
"Use Browser activity. Click on [NombreElemento_EnOR], type str_Valor into [NombreCampo_EnOR]... {Referenciar nombres exactos del OR}."

### Paso 3: Manejo de errores y excepciones

"Add Try Catch block around previous activities. In Catch section: Assign str_Status = 'Error', Log message '[MensajeExactoPDD]', and send email notification."

### Paso 4: Log de ejecucion y cierre

"Assign str_Status = 'Success'. Write row in Excel log with: current date, str_Module, '{NombreReq}', str_Status. Close all applications."

**Para UI Automation - Web (browser):**
"Use Browser activity to open '[https://url-del-sistema-aqui]' using Chrome.
Inside the browser scope:
Click on [NombreElemento_EnOR] to navigate to login.
Type str_Usuario into [NombreCampoUsuario_EnOR].
Type str_Contrasena into [NombreCampoContrasena_EnOR].
Click on [NombreBotonLogin_EnOR]."

nota_desarrollador: "PRERREQUISITO CRITICO: Los elementos UI deben existir en el
Object Repository con los nombres exactos usados en el prompt antes de generar.
Si no existen, capturarlos con el App/Web Recorder primero. Nombres requeridos en OR:
[NombreElemento_EnOR], [NombreCampoUsuario_EnOR], [NombreCampoContrasena_EnOR],
[NombreBotonLogin_EnOR]. URL del sistema: [https://url-aqui]."

**Para UI Automation - Desktop (aplicacion):**
"Use Application activity to open '[C:\Ruta\Aplicacion.exe]'.
Inside the application scope:
Click on [NombreElementoEnOR] in application [NombreAppEnOR].
Type [valor] into [NombreCampoEnOR].
Click on [NombreBotonEnOR].
Get Text from [NombreResultadoEnOR] and store in str_Resultado."

nota_desarrollador: "Elementos UI requeridos en Object Repository: [lista de nombres].
Si la aplicacion usa SAP GUI, IBM AS400 u otro sistema legacy, puede requerirse
el Extension de UiPath para ese sistema. Verificar que la Extension este instalada."

**Para correo electronico (envio con Outlook):**
"Send email using UiPath.Mail.Activities.
To: str_Destinatarios (value: '[correo@empresa.com]').
Subject: '[AsuntoExactoDelPDD]'.
Body: '[CuerpoDelTemplate con variables: str_Variable1, str_Variable2]'.
[Si tiene adjunto: Attach file str_[NombreReq]FilePath.]"

nota_desarrollador: "Segun politica Beecker, correos con informacion sensible deben
revisarse antes de enviar. Considerar guardar como borrador si aplica. Asunto y
destinatarios deben ser parametrizables, no hardcodeados."

**Para correo electronico (lectura/filtrado):**
"Get Mail Messages from Outlook using UiPath.Mail.Activities.
Filter by: subject contains '[FiltroAsunto]', received in last [N] days.
Store messages list in lst_[NombreReq]Correos.
For each email in lst_[NombreReq]Correos:
  Store subject in str_Asunto, sender in str_Remitente, body in str_Cuerpo.
  [Si tiene adjuntos: Save attachments to folder 'C:\RPA\[Proyecto]\Adjuntos\'.]"

**Para Integration Service (conectores de terceros: Salesforce, Jira, ServiceNow, etc.):**
"Use [NombreConector] connection from Integration Service.
[Accion especifica del conector: Get Record / Create Record / Update Record].
[Objeto/entidad: NombreObjeto]. Filter by: [campo] = [valor].
Store result in dt_[NombreReq] or str_[NombreReq]."

nota_desarrollador: "La conexion de Integration Service para [NombreConector] debe
estar configurada en Orchestrator > Integration Service antes de ejecutar.
Autopilot no puede crear connections dinamicamente."

**Para lectura/escritura de archivos (texto, JSON, CSV):**
"Read text file at '[C:\RPA\[Proyecto]\[archivo.txt]]' and store content in str_Contenido.
[O: Write text str_Contenido to file '[C:\RPA\[Proyecto]\[archivo.txt]]'.]
[O para CSV: Read CSV file '[C:\RPA\[Proyecto]\[archivo.csv]]' store in dt_[NombreReq].]"

### Prompt 3 — Manejo de errores y excepciones

Solo generar si el req tiene excepciones definidas en el PDD.

"Add Try Catch block around the previous activities.
In the Catch section for [TipoExcepcion] (or Exception):
  Assign str_Status = 'Error: ' + exception.Message.
  Log message with level Error: '[MensajeExactoDelPDD] - ' + exception.Message.
  [Si hay correo de notificacion: Send email to '[correo]' subject
  '[AsuntoExactoDelPDD]' body 'Error in [NombreReq]: ' + exception.Message.]
  [Si debe relanzar la excepcion: Rethrow the exception.]"

nota_desarrollador: "Excepciones del req segun PDD:
[listar TODAS: condicion -> accion completa -> mensaje de log exacto]
Para excepciones especificas de actividad, agregar 'On Error' directamente sobre
la actividad critica en Studio. REGLA Beecker: minimo un Log Message en cada
manejo de errores con nivel Error y modulo identificable."

Si el prompt excede lo comodo con todas las excepciones, dividir en Prompt 3a, 3b.

### Prompt 4 — Log de ejecucion y cierre

"Assign str_Status = 'Success' if not already set to Error.
Log message with level Information: '[NombreReq] completed with status: ' + str_Status.
[Si hay archivo de log Excel: Open Excel file 'C:\RPA\[Proyecto]\Log_[NombreProyecto].xlsx'.
Write row with: current date/time, str_Module, '[NombreReqExacto]', str_Status.
Save and close the log file.]
[Si usa AddToLog de Framework: Call workflow AddToLog with str_Module,
str_Status, and message '[NombreReqExacto] finished'.]"

nota_desarrollador: "Ruta del log debe configurarse como variable global o argumento
In del workflow principal, no como valor fijo aqui. Columnas del log: Fecha, Modulo,
Proceso, Estado. Si el proyecto usa REFramework, usar el mecanismo de log del framework."

---

## Sub-prompts por desbordamiento de columnas o actividades

Si las columnas o actividades del PDD no caben en un prompt comodo (aprox. 400 palabras):

1. Dividir en Prompt 2a (primeras columnas/actividades) y Prompt 2b, 2c (continuacion).
2. En nota_desarrollador del Prompt 2a indicar EXACTAMENTE:
   "Este prompt cubre [N] de [Total] columnas/actividades. Ejecutar Prompt 2b a
   continuacion para completar: [lista de lo que falta]. Al finalizar, verificar
   que se generaron exactamente [Total] actividades/columnas: [lista completa]."
3. El Prompt 2b comenzar con:
   "Continuing the previous sequence. Add the following additional columns/actions:
   [lista de lo pendiente]."

---

## Sub-requerimientos

Para cada sub-requerimiento con puede_generar = true dentro de un req:
1. Generar sus propios 4 prompts con la misma estructura.
2. En instruccion_previa del Prompt 1 del sub-req indicar:
   "Este sub-req [sub_req.id] es parte de [req.id]. Sus actividades se generan
   dentro del mismo archivo XAML '[NombreWorkflow].xaml', en una Sequence separada
   (no en un workflow nuevo). Posicionarse en la Sequence correcta antes de pegar."
3. Si el sub-req merece su propio archivo XAML por complejidad o reusabilidad,
   indicarlo explicitamente en instruccion_previa.

---

## Actividades soportadas vs. no soportadas por Autopilot

### SOPORTADAS (generar prompt normal):
- Variables y asignaciones (Assign, Set Variable)
- Condiciones (If/Else, Switch)
- Bucles (For Each, While, Do While)
- Excel: Read Range, Write Range, Append Range, Read Cell, Write Cell,
  Get Workbook Sheet, Sort Data Table, Filter Data Table
- Correo: Get Mail Messages, Send Mail (SMTP/Exchange/Outlook/Gmail)
- Archivos y carpetas: Copy File, Move File, Delete File, Get Files,
  Create Directory, Path Exists, Read Text File, Write Text File
- Orquestador: Get Asset, Get Credential, Add Queue Item, Get Transaction Item,
  Set Transaction Status, Add Log Fields
- UI Automation basica con OR: Click, Type Into, Get Text, Check App State,
  Use Application/Browser, Navigate To URL, Hover, Select Item
- HTTP / API: HTTP Request (configuracion basica)
- Texto: Matches, Split, Trim, Replace, Concatenate
- Fecha y hora: Get Current Date and Time, Add Time to DateTime
- Matematicas: operaciones aritmeticas basicas en expresiones
- Log Message (todos los niveles)
- Delay / Wait
- Invoke Workflow File (referenciar otro XAML existente)
- Integration Service connectors (si la conexion ya existe en Orchestrator)

### PARCIALMENTE SOPORTADAS (generar prompt + nota_desarrollador):
- UI Automation compleja: Autopilot puede generar el scope y actividades basicas,
  pero los selectores avanzados o dinamicos requieren ajuste manual en UiExplorer.
  nota_desarrollador: "Verificar y ajustar selectores generados con UiExplorer."
- Document Understanding: Autopilot puede generar el scope, pero el modelo ML
  y los campos de extraccion requieren configuracion manual.
- REFramework: Autopilot genera actividades dentro de un estado/secuencia,
  pero no crea la estructura REFramework completa.

### NO SOPORTADAS (solo nota_desarrollador, no generar prompt):
- Crear Assets, Queues o Buckets en Orchestrator
- Capturar elementos en el Object Repository
- Configurar conexiones de Integration Service
- Computer Vision con coordenadas o imagenes de referencia
- Scripts PowerShell embebidos (generar como Invoke Power Shell con placeholder)
- Actividades de SAP con transacciones especificas de SAP GUI (requieren grabacion)
- Configurar REFramework o estructura de proyecto desde cero
Para estas escribir en nota_desarrollador: "Esta accion requiere configuracion manual.
[Descripcion exacta de los pasos manuales que el desarrollador debe realizar.]"

---

## Estructura JSON de salida

{
  "id_flujo": "[req.id]",
  "nombre_flujo": "[req.nombre exacto]",
  "plataforma": "Studio Desktop | Studio Web",
  "generar_prompt": true,
  "gaps_detectados": {
    "criticos": [],
    "advertencias": [],
    "impacto": "Sin gaps detectados. | Prompts generados con advertencias. | No se generaron prompts."
  },
  "prerrequisitos": {
    "object_repository": ["Elemento1EnOR", "Elemento2EnOR"],
    "assets_orchestrator": ["NombreAsset1 (tipo: Credential, carpeta: X)", "NombreAsset2"],
    "queues_orchestrator": ["NombreQueue1 (carpeta: X)"],
    "rutas_locales": ["C:\\RPA\\Proyecto\\Archivo.xlsx"],
    "conexiones_integration_service": ["NombreConector1"],
    "paquetes_nuget": ["UiPath.Excel.Activities", "UiPath.Mail.Activities"]
  },
  "prompts_secuenciales": [
    {
      "numero_prompt": 1,
      "titulo": "Inicializacion de variables",
      "plataforma_prompt": "Studio Desktop | Studio Web",
      "instruccion_previa": "ANTES DE PEGAR: [pasos exactos incluyendo prerrequisitos]",
      "prompt": "texto del prompt en lenguaje natural claro, verbos de accion, variables por nombre",
      "palabras_estimadas": 80,
      "actividades_cubiertas": ["Assign str_RutaArchivo", "Assign str_Status", "Log Message"],
      "variables_referenciadas": ["str_RutaArchivo", "str_Status", "str_Module", "dt_Datos"],
      "nota_desarrollador": "instruccion post-Autopilot: que ajustar, que verificar, que configurar manualmente"
    }
  ],
  "resumen_cobertura": "4 prompts para [plataforma]. Cubren: variables -> [sistema/actividad principal] -> errores -> log.",
  "pasos_manuales_requeridos": [
    "Descripcion especifica de lo que Autopilot no puede generar y el dev debe hacer"
  ],
  "sub_prompts": [
    {
      "id_subflujo": "[sub_req.id]",
      "nombre_subflujo": "[sub_req.nombre]",
      "plataforma": "Studio Desktop | Studio Web",
      "generar_prompt": true,
      "gaps_detectados": { "criticos": [], "advertencias": [] },
      "prerrequisitos": {},
      "prompts_secuenciales": [],
      "pasos_manuales_requeridos": []
    }
  ]
}

## Campos eliminados del JSON (no incluir)
Los siguientes campos NO deben aparecer en el JSON de salida:
motivo_no_generado (reemplazado por gaps_detectados.impacto),
_resumen (nivel raiz), prompts (nivel raiz concatenado sin estructura).

---

## Diferencias clave: Studio Desktop vs Studio Web

| Aspecto                  | Studio Desktop                          | Studio Web                              |
|--------------------------|----------------------------------------|-----------------------------------------|
| Donde se pega el prompt  | Anotacion de Sequence > Generate       | Barra busqueda > Generate with Autopilot|
| Contexto UI Automation   | Object Repository del proyecto local   | Object Repository en la nube            |
| Actividades disponibles  | Todas (incl. SAP, legacy, clasicas)    | Subconjunto moderno + cross-platform    |
| Correo                   | Outlook local o Exchange               | M365 / GSuite via Integration Service  |
| Archivos locales         | Rutas locales del robot                | Rutas del robot o nube (OneDrive, etc) |
| Formato de ruta          | C:\Carpeta\Archivo.xlsx                | C:\Carpeta\Archivo.xlsx o URL nube      |
| Lenguaje expresiones     | VB.NET (por defecto) o C#              | VB.NET (por defecto) o C#              |
| Paquetes recomendados    | Windows-compatibility, clasicos        | Cross-platform, modernos               |

---

## Ejemplos de prompts efectivos (referencia oficial UiPath)

### Ejemplo 1 — Extraccion de correos y escritura en Excel:
"Extract the latest 100 emails from Outlook from the current month using
UiPath.Mail.Activities. Create an Excel file at 'C:\RPA\Proyecto\Emails.xlsx'
with columns Sender and Subject. Write each email's sender and subject to a new row."

### Ejemplo 2 — Condicion If-Else con asset:
"Get Credential asset named 'ACME_Credential' from Orchestrator folder 'Production'.
Store username in str_Usuario and password in str_Contrasena.
If str_Usuario is empty or str_Contrasena is empty, log message with level Error:
'Not able to extract credentials from asset'. Else log message with level Information:
'Credentials retrieved correctly'."

### Ejemplo 3 — UI Web con Object Repository:
"Use Browser activity to open 'https://acme-test.uipath.com/login' using Chrome.
Inside the browser scope, type str_Usuario into element 'UsernameField'.
Type str_Contrasena into element 'PasswordField'. Click on element 'LoginButton'."

### Ejemplo 4 — Lectura de Excel con condicion y correo:
"Read Range from Excel file 'C:\RPA\Recruitment\Candidates.xlsx' sheet 'Sheet1'
store in dt_Candidatos. For each row in dt_Candidatos: if column Score value is
greater than 45, send email using UiPath.Mail.Activities to the email in column
Email with subject 'Congratulations - You passed' and body 'Dear [Name], you passed
the assessment'. Else send email with subject 'Assessment Result' and body
'Dear [Name], unfortunately you did not pass this round'."

### Ejemplo 5 — Archivo de texto a Word:
"Read text file at 'C:\RPA\Logs\Robot.log' and store content in str_LogContent.
Create a new Word document, write str_LogContent into it, and save as
'AutoPilotDoc.docx' at 'C:\RPA\Output\'."

---

## Verificacion final antes de guardar

1. Cada prompt usa variables con prefijo de tipo Beecker (str_, dt_, int_, bln_, lst_)?
2. Ningun prompt tiene rutas, URLs, nombres de asset o queues vacios? (placeholder si no hay valor real)
3. Si el PDD lista columnas, estan todas nombradas en el prompt o en nota_desarrollador con aviso de continuacion?
4. Los prompts de sub-requerimientos estan incluidos en sub_prompts?
5. Los prerrequisitos de OR, assets, queues y rutas estan documentados en el campo prerrequisitos?
6. Las actividades no soportadas tienen nota_desarrollador con instruccion manual especifica?
7. Los prompts usan voz activa y verbos de accion de UiPath (Click, Type, Read, Write, Send, Get)?
8. La logica condicional usa formato If-Else explicito con la condicion exacta del PDD?
9. Se especifica el paquete de actividades cuando hay posible ambiguedad?
10. El campo plataforma_prompt refleja correctamente Studio Desktop o Studio Web segun el PDD?
11. El JSON incluye el campo prerrequisitos con todos los recursos que deben existir antes de ejecutar?
12. Las actividades_cubiertas por prompt son <= 8 para garantizar generacion precisa?