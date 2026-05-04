---
name: generar-prompts-pad
description: |
  Genera prompts optimizados para Copilot de Power Automate Desktop a partir del JSON de analisis.
  Se activa internamente desde analizar-pdd o hibrido para reqs con plataforma Desktop Flow.
  Limite: 500 caracteres por prompt. Produce prompts especificos con variables, rutas,
  columnas y nombres de archivo reales del PDD. No usar directamente por el usuario.
---

# Skill: Generar Prompts Power Automate Desktop (PAD)

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

**Principio 6 — Especificidad de columnas y campos:**
Si el PDD lista columnas a leer o escribir, nombrarlas TODAS en el prompt.
Si no caben en 500 chars, dividir en subprompts con numeracion (2a, 2b, etc.)
y en nota_desarrollador indicar: "Verificar que se crearon las N columnas:
[Col1], [Col2]... Si el prompt cubrio solo X, ejecutar el subprompt siguiente."

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

**Principio 8 — Nomenclatura de acciones y subflujos (Buenas Practicas Beecker):**
  Subflujos: UpperCamelCase con nombre de aplicacion principal (ej: JDE_DescargarLM, Excel_AjustarEC)
  PROHIBIDO: acentos, caracteres especiales (#, ?, /, \, :, *, Ñ), numeracion tipo "accion1"
  Variables: PROHIBIDO hardcode de credenciales, rutas, nombres de archivo, correos en acciones
  Correos: guardar como borrador si tienen informacion sensible; toda informacion parametrizable

---

## Estructura de prompts por requerimiento

Para cada requerimiento con puede_generar = true, generar EN ESTE ORDEN:

### Prompt 1 — Variables e inicializacion (el mas importante, contexto de sesion)

Este prompt establece TODAS las variables que usara el subflow.
Copilot recuerda estas variables en los prompts siguientes de la sesion.

Estructura del prompt:
"Inicializar variable de texto [Str{NombreReq}Ruta] con la ruta [rutaArchivo\aqui\va\la\ruta\{NombreArchivo}].
Inicializar variable de texto [StrEstadoEjecucion] con valor vacio.
Inicializar variable de texto [StrModulo] con valor '{NombreSubflow}'.
{Si hay variables adicionales especificas del req: Inicializar variable {tipo} [Prefijo{NombreVar}] con {valor_inicial}.}"

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

### Prompt 2 — Accion principal (especifica por tipo de sistema)

El prompt debe describir la accion ESPECIFICA del req, no una accion generica.
Incluir: sistema exacto, archivo con ruta o placeholder, hoja si aplica, columnas si las lista el PDD.

**Para Excel (lectura):**
"Abrir el archivo Excel [Str{NombreReq}Ruta] con la accion Launch Excel.
Leer el rango de la hoja [{NombreHoja}] con Read from Excel Worksheet y
guardar en [dt_{NombreReq}].
{Si el PDD lista columnas: Las columnas a leer son: {Col1}, {Col2}, {Col3}... (listar TODAS).}"

nota_desarrollador: "Verificar ruta exacta del archivo. Nombre de hoja: [{NombreHoja}].
Si el prompt no alcanzo a listar todas las columnas, ejecutar Prompt 2b (continuacion)."

**Para Excel (escritura con columnas especificas):**
"En el archivo Excel [{NombreArchivo}.xlsx], hoja [{NombreHoja}], escribir en la siguiente
fila disponible los valores: columna {Col1} <- [Str{Var1}], columna {Col2} <- [Str{Var2}]...
{Si hay muchas columnas y no caben: ver Prompt 2b.}"

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

**Para SharePoint (descarga via UI de navegador):**
"Abrir navegador Chrome y navegar a [{https://sharepoint-url-aqui}].
Esperar al contenido de la pagina con 'Esperar al contenido de la ventana'.
Localizar el archivo [{NombreArchivo}.xlsx] en la carpeta [{rutaCarpetaSharePoint}].
Hacer clic en Descargar y guardar en [Str{NombreReq}Ruta]."

nota_desarrollador: "ACCION UI sobre SharePoint web: usar grabador de PAD para selectores del
navegador. Ruta en SharePoint: [{rutaCarpetaSharePoint}]. Si hay API de SharePoint disponible
considerar migracion a Cloud Flow para este req."

**Para lectura de correos (extraccion de datos):**
"Usar la accion Get Email Messages de Outlook con filtro de asunto que contenga
'{AsuntoFiltroDelPDD}'. Guardar los correos en [Lst{NombreReq}Correos].
Para cada correo en [Lst{NombreReq}Correos], extraer: asunto en [StrAsunto],
remitente en [StrRemitente], cuerpo en [StrCuerpo], adjuntos en [Lst{NombreReq}Adjuntos]."

### Prompt 3 — Manejo de errores (solo si el req tiene excepciones definidas)

"Agregar bloque 'On block error' despues de las acciones anteriores con nombre
'{NombreSubflow}_ErrorHandler'. Si ocurre {condicion_exacta_del_PDD}: establecer
[StrEstadoEjecucion] en 'Error'. Llamar subflujo AddToLog con [StrModulo],
mensaje '{MensajeExactoDelPDD}' y nivel 'Error'.
{Si hay correo de notificacion: Usar Send Email con asunto '{AsuntoExacto}'.}"

nota_desarrollador: "Excepciones completas del req:
{listar TODAS las excepciones del req en formato: condicion -> accion completa -> log}
Configurar 'Al producirse error' directamente sobre acciones criticas si aplica.
REGLA Beecker: enviar como minimo un log AddToLog en cada manejo de errores."

Si el prompt excede 500 chars con todas las excepciones, dividir en Prompt 3a, 3b por excepcion.

### Prompt 4 — Registro en log de ejecucion

"Abrir el archivo Excel de log [rutaLog\aqui\va\la\ruta\Log_{NombreProyecto}.xlsx]
con Launch Excel. Escribir en la siguiente fila disponible: fecha y hora actual
con accion Get Current Date and Time en [DtFechaEjecucion], modulo [StrModulo],
proceso '{NombreReqExacto}', estado [StrEstadoEjecucion]. Guardar y cerrar con Close Excel."

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