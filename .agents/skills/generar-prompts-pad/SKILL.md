---
name: generar-prompts-pad
description: |
  Genera prompts optimizados para Copilot de Power Automate Desktop a partir del JSON de analisis.
  Se activa internamente desde analizar-pdd o hibrido para reqs con plataforma Desktop Flow.
  Limite: 500 caracteres por prompt. Produce prompts especificos con variables, rutas,
  columnas y nombres de archivo reales del PDD. No usar directamente por el usuario.
---

# Skill: Generar Prompts Power Automate Desktop (PAD)

**REGLA MANDATARIA — Leer Buenas Practicas:** Antes de comenzar cualquier generacion de prompts, el agente DEBE leer el archivo `resources/BuenasPracticas.md` de esta skill y aplicar sus lineamientos.

## Principios de prompting para Copilot PAD — basados en documentacion oficial y foros

**Principio 1 — Especificidad de parametros obligatorios:**
Si el prompt omite parametros obligatorios de una accion PAD (ruta de archivo, nombre de hoja,
URL), Copilot deja el campo vacio y marca la accion como error. SIEMPRE incluir el valor real
o un placeholder descriptivo con formato [rutaArchivo\aqui\va\la\ruta.xlsx].

**Principio 2 — Contexto de sesion:**
Copilot PAD mantiene contexto dentro de la sesion. El Prompt 1 establece variables y rutas;
los prompts siguientes pueden referenciarlas sin repetir. El Prompt 1 es el mas importante:
debe ser comprehensivo con objetivos, variables y rutas base.

**Principio 3 — Variables entre llaves:**
Las variables en prompts PAD van entre corchetes: [StrNombreVariable].
Usar nomenclatura Beecker: prefijo de tipo + UpperCamelCase.
  Boolean  -> Bln   -> [BlnNombreVariable]
  Integer  -> Int   -> [IntNombreVariable]
  Float    -> Flt   -> [FltNombreVariable]
  String   -> Str   -> [StrNombreVariable]
  Object   -> Obj   -> [ObjNombreVariable]
  List     -> Lst   -> [LstNombreVariable]
  DataTable -> dt_  -> [dt_NombreVariable]

**Principio 4 — Subflows manuales:**
Copilot PAD NO puede crear subflows. El usuario debe crearlo manualmente antes de pegar el prompt.
El nombre del subflow usa UpperCamelCase sin espacios ni acentos (ej: ObtenerEC, AjustarBasecruce).

**Principio 5 — Placeholders descriptivos cuando faltan datos:**
Si el PDD no define una ruta, URL o nombre de archivo, usar placeholder descriptivo:
  Ruta desconocida:  [rutaArchivo\aqui\va\la\ruta]
  Archivo sin nombre: [archivoEntrada.xlsx]
  URL desconocida:   [https://url-del-sistema-aqui]
  Hoja sin nombre:   [NombreHoja]
  Columna sin nombre: [NombreColumna]
NUNCA dejar el parametro en blanco ni usar texto vago como "el archivo".

**Principio 6 — Cobertura Total de Columnas y Campos (REGLA DE ORO):**
Si el PDD lista columnas a leer o escribir, NOMBRARLAS TODAS en el prompt sin excepcion.
Si hay 20 columnas, las 20 deben estar en el prompt. Si no caben en 500 chars (limite de PAD),
se DEBE dividir el proceso en subprompts (2a, 2b, 2c...) de la siguiente manera:
- Prompt 2a: "Escribir en Excel las columnas 1 a 10: [Col1], [Col2]..."
- Prompt 2b: "Continuar escribiendo en la misma fila las columnas 11 a 20: [Col11], [Col12]..."
NUNCA omitir campos del PDD por falta de espacio.

**Principio 7 — Acciones soportadas por Copilot PAD:**
Solo generar prompts para acciones que Copilot PAD puede crear:
  SOPORTADAS: Variables, Condiciones (If/Else), Bucles (For Each/Loop),
    Excel (Launch, Read, Write, Close), Archivos y Carpetas (Copy, Move, Delete, Get files),
    Outlook (Launch, Get Email Messages, Send Email), Web basico (Launch browser, navigate),
    Sistema (Run application, Get special folder, Wait), Texto (Trim, Split, Replace),
    Fecha y hora, Matematicas
  NO SOPORTADAS (solo nota_desarrollador): SAP GUI, UI Automation compleja con selectores
    XPath/CSS especificos, PowerShell scripts, grabacion de pantalla, Image Recognition.
    Para estas escribir en nota_desarrollador: "Esta accion requiere grabacion manual con
    el grabador de PAD. Copilot insertara un placeholder que debes completar."

**Principio 8 — Granularidad y Cobertura (1 a N):**
No limitarse a X prompts por requerimiento. Generar de 1 a N prompts segun sea necesario
para cubrir entre el 80% y 100% de la funcionalidad descrita en el PDD y JSON de analisis.
Si un requerimiento tiene 10 pasos logicos en sus acciones del analisis y reglas de negocio , generar de 1,5,10 ...N prompts si es necesario para cubrir el porcentaje requerido y mantener la precision y no perder detalles.

**Principio 9 — Bucles, Iteraciones y Archivos Adjuntos:**
- Si el proceso implica procesar varios elementos (correos, archivos, filas), el prompt DEBE incluir explicitamente la accion "For Each" o "Loop".
- Diferenciar claramente entre EXTRACCION de texto y GUARDADO de archivos.
- Si el PDD dice "Guardar factura adjunta", usar la accion "Save Outlook email attachments" (o similar para archivos locales) en lugar de intentar extraer texto del archivo si no se pide explicitamente.

**Principio 10 — Validaciones Robustas:**
Evitar validaciones basadas UNICAMENTE en comparacion de texto literal si el PDD sugiere
patrones. Ej: En lugar de "asunto es igual a DUCA", usar "asunto contiene la palabra DUCA
y tiene una longitud de X caracteres" si el contexto lo permite.

**Principio 11 — Nomenclatura de acciones y subflujos (Buenas Practicas Beecker):**
  Subflujos: UpperCamelCase con nombre de aplicacion principal (ej: JDE_DescargarLM, Excel_AjustarEC)
  PROHIBIDO: acentos, caracteres especiales (#, ?, /, \, :, *, Ñ), numeracion tipo "accion1"
  Variables: PROHIBIDO hardcode de credenciales, rutas, nombres de archivo, correos en acciones
  Correos: guardar como borrador si tienen informacion sensible; toda informacion parametrizable

---

## Estructura de prompts por requerimiento

Para cada requerimiento con puede_generar = true, generar una secuencia de 1 a N prompts
respetando el flujo logico y asegurando cobertura total (80-100%):

### Paso 1: Variables e inicializacion (Contexto de sesion)

Establece TODAS las variables que usara el subflow.
"Inicializar variable de texto [Str{NombreReq}Ruta] con la ruta [rutaArchivo\aqui\va\la\ruta\{NombreArchivo}].
Inicializar variable de texto [StrEstadoEjecucion] con valor vacio.
Inicializar variable de texto [StrModulo] con valor '{NombreSubflow}'.
{Variables adicionales del PDD: [Prefijo{NombreVar}] con {valor_inicial}.}"

Reglas:
- [Str{NombreReq}Ruta]: si el PDD define el nombre del archivo de input, usarlo directamente.
  Si no: usar placeholder [rutaArchivo\aqui\va\la\ruta\{NombreReq}.xlsx]
- [StrEstadoEjecucion]: siempre presente, para log de estado
- [StrModulo]: siempre presente con el nombre exacto del subflow, para logs AddToLog
- Variables adicionales: una por cada input diferenciado del req (ej: [StrCuentaCorriente], [StrEmpresa])
- Si hay DataTable para datos extraidos: [dt_{NombreReq}]

instruccion_previa: "ANTES DE PEGAR ESTE PROMPT: En Power Automate Desktop, crear manualmente
el subflow '{NombreSubflow}' (Menu Subflows > Nuevo subflujo). Copilot no puede crear subflows.
Posicionarse dentro del subflow antes de pegar. Nombre sugerido: {NombreSubflow} en UpperCamelCase
sin acentos ni espacios. Agregar al inicio una accion Comentario con: descripcion del subflow,
req ID {req.id}, precondiciones y postcondiciones."

### Paso 2: Logica de Proceso (Dividir en tantos prompts como sea necesario)

Cada prompt debe ser especifico y no superar los 500 caracteres.

**Manejo de Iteraciones (Ejemplo correos/archivos):**
"Obtener mensajes de correo con Get Email Messages filtrando por asunto '{Asunto}' y guardar en [LstCorreos].
Para cada correo en [LstCorreos]: extraer el cuerpo en [StrCuerpo] y guardar los adjuntos en la carpeta [StrRutaAdjuntos]."

**Extraccion Masiva de Campos (Respetar Principio 6):**
"De la variable [StrCuerpo], extraer los siguientes campos: {Campo1}, {Campo2}, {Campo3}, {Campo4}, {Campo5}... {Si no caben todos, crear Prompt 2b para los restantes}."

**Acciones en Excel / Sistemas:**
"Abrir el archivo Excel [Str{NombreReq}Ruta]. En la hoja [{NombreHoja}], escribir en la siguiente fila: {Col1} <- [Var1], {Col2} <- [Var2]... {Seguir listando TODOS los campos del PDD}."

**Para SharePoint (descarga via UI de navegador):**
"Abrir navegador Chrome y navegar a [{https://sharepoint-url-aqui}].
Esperar al contenido de la pagina con 'Esperar al contenido de la ventana'.
Localizar el archivo [{NombreArchivo}.xlsx] en la carpeta [{rutaCarpetaSharePoint}].
Hacer clic en Descargar y guardar en [Str{NombreReq}Ruta]."

nota_desarrollador: "ACCION UI sobre SharePoint web: usar grabador de PAD para selectores del
navegador. Ruta en SharePoint: [{rutaCarpetaSharePoint}]. Si hay API de SharePoint disponible
considerar migracion a Cloud Flow para este req."

"Usar la accion Get Email Messages de Outlook con filtro de asunto que contenga
'{AsuntoFiltroDelPDD}'. Guardar los correos en [Lst{NombreReq}Correos].
Para cada correo en [Lst{NombreReq}Correos], extraer: asunto en [StrAsunto],
remitente en [StrRemitente], cuerpo en [StrCuerpo], adjuntos en [Lst{NombreReq}Adjuntos]."

**Para UI de sistema legacy (JDE, SAP, SEADEX, SIESA, Oracle, AS400):**
"Abrir navegador Chrome y navegar a [{https://url-del-sistema-aqui}].
Esperar a que cargue la pagina de inicio de sesion usando la accion
'Esperar al contenido de la ventana'.
Hacer clic en el campo usuario e ingresar [StrUsuario].
Hacer clic en el campo contrasena e ingresar [StrContrasena].
Hacer clic en el boton Ingresar."

nota_desarrollador: "ACCION UI DETECTADA: Copilot insertara un placeholder de grabacion.
Usar el grabador de PAD para capturar los selectores reales de {sistema}.
Habilitar 'Simular accion' en cada elemento UI cuando el control lo permita.
Nombrar cada ventana como '{Sistema} - {descripcion}' y cada elemento por tipo
(cuadro de texto, boton, lista desplegable). URL del sistema: [{https://url-aqui}]."

**Para Outlook (envio):**
"Usar la accion Launch Outlook para abrir la aplicacion.
Crear un borrador de correo con Send Email: destinatarios en [StrDestinatarios],
asunto '{AsuntoExactoDelPDD}', cuerpo '{CuerpoDelTemplate}'.
{Si tiene adjunto: Adjuntar el archivo [Str{NombreReq}Ruta].}"

nota_desarrollador: "Segun politica Beecker, los correos creados por robots deben guardarse
como borradores para revision humana si contienen informacion sensible. Toda la info del
correo (asunto, cuerpo, destinatarios) debe ser parametrizable, no hardcodeada."


### Paso 3: Manejo de Errores y Excepciones

Generar prompts especificos para las excepciones del PDD. Si son muchas, agrupar o separar.
"Agregar bloque 'On block error' con nombre '{NombreSubflow}_Handler'. Si ocurre {Excepcion}: establecer [StrEstadoEjecucion] en 'Error', llamar AddToLog con mensaje '{Mensaje}' y enviar correo de notificacion."

### Paso 4: Cierre y Logs (Se pueden consolidar si son pasos breves)

"Escribir en el log de ejecucion [{RutaLog} o [rutaLog\aqui\va\la\ruta]\{NombreArchivoLog}.xlsx]: Fecha actual, Modulo [StrModulo], Proceso '{NombreReq}', Estado [StrEstadoEjecucion]. Cerrar todas las aplicaciones y archivos abiertos."

nota_desarrollador: "Configurar la ruta del archivo de log como parametro global al inicio
del flow principal, no como hardcode aqui. Columnas del log: Fecha, Modulo, Proceso, Estado.
Segun Beecker, usar subflujo AddToLog del Framework con variables StrLevel, StrModule, StrMessageLog."

---

## Subprompts por desbordamiento de columnas o acciones

Si las columnas o acciones listadas en el PDD no caben en 500 chars:

1. Dividir en Prompt 2a (primeras columnas/acciones) y Prompt 2b, 2c, etc. (continuacion).
2. En nota_desarrollador del Prompt 2a indicar EXACTAMENTE:
   "Este prompt cubre {N} de {Total} columnas/acciones. Ejecutar Prompt 2b a continuacion
   para completar: {lista de lo que falta}. Verificar al final que se crearon
   exactamente {Total} acciones/columnas: {lista completa}."
3. El Prompt 2b comenzar con: "Continuacion del paso anterior. Agregar las siguientes
   columnas/acciones adicionales: {lista de lo que quedo pendiente}."

---

## Sub-requerimientos

Para cada sub-requerimiento con puede_generar = true dentro de un req:
1. Generar sus propios 4 prompts con la misma estructura.
2. La instruccion_previa del Prompt 1 del sub-req indicar:
   "ANTES DE PEGAR: Posicionarse dentro del subflow '{NombreSubflowPadre}'.
   Este sub-req {sub_req.id} es parte de {req.id}. Los prompts de sub-reqs
   se pegan dentro del mismo subflow del req padre, no en uno nuevo."
3. Si el sub-req tiene su propio subflow (ej: por complejidad), indicarlo explicitamente.

---

## Estructura JSON de salida

{
  "id_flujo": "[req.id]",
  "nombre_flujo": "[req.nombre exacto]",
  "plataforma": "Desktop Flow",
  "generar_prompt": true,
  "gaps_detectados": {
    "criticos": [],
    "advertencias": [],
    "impacto": "Sin gaps detectados. | Prompts generados con advertencias. | No se generaron prompts."
  },
  "prompts_secuenciales": [
    {
      "numero_prompt": 1,
      "titulo": "Variables e inicializacion",
      "instruccion_previa": "ANTES DE PEGAR ESTE PROMPT: Crear manualmente el subflow '{NombreSubflow}'...",
      "prompt": "texto en una sola linea continua sin saltos de linea, con variables en [Corchetes]",
      "caracteres": 234,
      "acciones_cubiertas": ["descripcion de que parte del req cubre este prompt"],
      "variables_referenciadas": ["[StrNombreVar1]", "[dt_NombreVar2]"],
      "nota_desarrollador": "instruccion post-Copilot: que ajustar, que verificar, que grabar manualmente"
    }
  ],
  "resumen_cobertura": "4 prompts para Desktop Flow. Cubren: variables -> [sistema] -> errores -> log.",
  "pasos_manuales_requeridos": [
    "Descripcion especifica de lo que Copilot no puede generar y el dev debe hacer"
  ],
  "sub_prompts": [
    {
      "id_subflujo": "[sub_req.id]",
      "nombre_subflujo": "[sub_req.nombre]",
      "plataforma": "Desktop Flow",
      "generar_prompt": true,
      "gaps_detectados": { "criticos": [], "advertencias": [] },
      "prompts_secuenciales": [],
      "pasos_manuales_requeridos": []
    }
  ]
}

## Campos eliminados del JSON (no incluir)
Los siguientes campos de versiones anteriores NO deben aparecer en el JSON de salida:
motivo_no_generado (reemplazado por gaps_detectados.impacto),
_resumen (nivel raiz), prompts (nivel raiz con subprompts concatenados).

---

## Verificacion final antes de guardar

1. Cada prompt usa variables con prefijo de tipo Beecker (Str, Int, Bln, dt_, Lst, etc.)?
2. Ningun prompt tiene rutas, URL, nombres de archivo vacios? (usar placeholder si no hay valor real)
3. Si el PDD lista columnas, todas estan nombradas en el prompt o en nota_desarrollador con aviso de continuacion?
4. Los prompts de sub-requerimientos estan incluidos en sub_prompts?
5. Ningun prompt supera 500 caracteres?
6. El campo prompt es una sola linea continua sin \n internos?
7. Los caracteres son UTF-8 directos sin escapes unicode?
8. Los nombres de subflows usan UpperCamelCase sin acentos ni caracteres especiales?
9. Las acciones de UI tienen nota_desarrollador indicando grabacion manual?
10. El correo de error tiene el asunto EXACTO del PDD, no un texto generico?