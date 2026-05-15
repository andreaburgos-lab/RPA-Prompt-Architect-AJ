---
name: generar-prompts-pad
description: |
  Genera prompts optimizados para Copilot de Power Automate Desktop a partir del JSON de analisis.
  Se activa internamente desde analizar-pdd o hibrido para reqs con plataforma Desktop Flow.
  Limite: 500 caracteres por prompt. Produce prompts especificos con variables, rutas,
  columnas y nombres de archivo reales del PDD. No usar directamente por el usuario.
---

# Skill: Generar Prompts Power Automate Desktop (PAD)

**REGLA MANDATARIA — Leer recursos antes de generar:** Antes de comenzar cualquier generacion de prompts, el agente DEBE leer:
1. `resources/BuenasPracticas.md` — y aplicar sus lineamientos.
2. `resources/acciones.md` — para usar los nombres exactos de acciones soportadas por Copilot PAD.

## Principios de prompting para Copilot PAD — basados en documentacion oficial y foros

**Principio 1 — Especificidad de parametros obligatorios:**
Si el prompt omite parametros obligatorios de una accion PAD (ruta de archivo, nombre de hoja,
URL), Copilot deja el campo vacio y marca la accion como error. SIEMPRE incluir el valor real
o un placeholder descriptivo con formato [rutaArchivo\aqui\va\la\ruta.xlsx].

**Principio 2 — Variables globales y contexto de sesion:**
Las variables en PAD son GLOBALES al proyecto — una variable inicializada en el Prompt 1 de
REQ_01 SI esta disponible en REQ_02 y todos los subflows siguientes. Esto es una ventaja para
compartir configuracion, pero tambien fuente de errores de asignacion entre ciclos.
REGLA: Al final de cada subflow (Paso 4 — Logs), restablecer TODAS las variables del req
a su valor por defecto vacio antes de terminar, para evitar que un valor de un ciclo o
req anterior contamine la siguiente ejecucion.
Ejemplo de restablecimiento en Prompt 4:
  "Asignar [StrEstadoEjecucion] con valor vacio."
  "Asignar [dt_DatosCorreo] con valor Nothing."
Copilot PAD mantiene contexto DENTRO de la sesion activa. El Prompt 1 establece
variables y rutas; los prompts siguientes pueden referenciarlas sin repetir.

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

**Principio 12 — Extraccion de texto vs. recorte de texto (CRITICO — accion incorrecta frecuente):**
Distinguir SIEMPRE entre estas dos operaciones diferentes:
  RECORTE (Trim text / Recortar texto):
    - Elimina espacios en blanco del inicio y final de un string ya obtenido.
    - Usar SOLO cuando el valor ya esta en una variable y tiene espacios sobrantes.
  EXTRACCION (Get text from window / captura con Recorder):
    - Obtiene un valor de un elemento de pantalla, correo, PDF o aplicacion.
    - Usar cuando el texto esta visible en una interfaz.
  SUBCADENA (Get subtext / Obtener subcadena de texto):
    - Extrae una porcion especifica de un string ya en memoria.
    - Usar para obtener un campo de un cuerpo de correo o texto ya capturado.
PROHIBIDO: usar 'Recortar texto' cuando el PDD dice 'extraer [campo] de [fuente]'.
El prompt debe especificar la accion correcta segun la fuente real del dato.

**Principio 13 — Fidelidad de texto en valores de prompt (acentos y puntuacion):**
Los valores textuales del PDD (asuntos de correo, nombres de columnas, mensajes de excepcion,
nombres de hojas, etiquetas de campos) se reproducen en el prompt EXACTAMENTE como aparecen
en el PDD, incluyendo:
  - Acentos: a con tilde, e con tilde, i, o, u con tilde, u con dieresis, n con tilde, N con tilde
  - Signos de puntuacion: comas, puntos, dos puntos exactos del PDD
  - Mayusculas y minusculas: respetar el uso del PDD
EXCEPCION: los NOMBRES de variables y subflows siguen la regla Beecker (sin acentos,
UpperCamelCase). Esta excepcion aplica SOLO a nombres de codigo, nunca a valores de datos.
Ejemplo:
  PDD dice columna: "Número de DTE"
  INCORRECTO en prompt: "columna Numero de DTE"
  CORRECTO en prompt:   "columna [Número de DTE]"

**Principio 14 — Datos dinamicos vs. datos estaticos:**
Al inicializar variables en el Prompt 1, clasificar cada dato como:
  ESTATICO: valor fijo que no cambia entre ejecuciones (ruta de carpeta, nombre de hoja).
    En el prompt: inicializar con el valor literal del PDD.
    En nota_desarrollador: indicar que debe venir del archivo de configuracion, no hardcodeado.
  DINAMICO: cambia cada ejecucion (fecha de hoy, datos de un correo, resultado de extraccion).
    En el prompt: "Inicializar [StrVariable] con valor vacio (se obtendra en Paso 2)."
    En nota_desarrollador: documentar de donde y como se llena el valor dinamico.
PROHIBIDO: inicializar una variable dinamica con un valor estatico de ejemplo.

**Principio 11 — Nomenclatura de acciones y subflujos (Buenas Practicas Beecker):**
  Subflujos: UpperCamelCase con nombre de aplicacion principal (ej: JDE_DescargarLM, Excel_AjustarEC)
  PROHIBIDO: acentos, caracteres especiales (#, ?, /, \, :, *, Ñ), numeracion tipo "accion1"
  Variables: PROHIBIDO hardcode de credenciales, rutas, nombres de archivo, correos en acciones
  Correos: guardar como borrador si tienen informacion sensible; toda informacion parametrizable

---

## Estructura de prompts por requerimiento

Para cada requerimiento con puede_generar = true, generar una secuencia de 1 a N prompts
respetando el flujo logico y asegurando cobertura total (80-100%):

### [STAGE:variables] Paso 1 — Variables e inicializacion (Contexto de sesion)

**PROTOCOLO DE COMPLETITUD DE VARIABLES (ejecutar ANTES de escribir el Prompt 1):**
1. Leer el array "acciones" COMPLETO del req en el JSON de analisis.
2. Leer el array "reglas_negocio" completo del req.
3. Identificar CADA dato que el subflow necesitara en memoria durante su ejecucion:
   - Cada archivo de entrada o salida: variable Str (ruta) o dt_ (datos)
   - Cada valor a extraer de correo, PDF o pantalla: variable Str
   - Cada acumulador de estado o bandera logica: variable Bln o Int
   - Cada lista de elementos a iterar: variable Lst o dt_
4. Incluir TODAS estas variables en el Prompt 1, inicializadas a su valor por defecto.
   Las variables dinamicas se inicializan con valor vacio — documentar en nota_desarrollador
   de donde y como se llena cada una.
5. Verificar que NINGUNA variable del Prompt 2 o siguientes es nueva (no declarada en Prompt 1).
   Si hay variables nuevas en Prompt 2+: regresar al Prompt 1 y agregarlas antes de guardar.
Copilot PAD puede perder el contexto de inicializacion si la variable aparece por primera vez
fuera del Prompt 1.

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

### [STAGE:logic] Paso 2 — Logica de Proceso (Dividir en tantos prompts como sea necesario)

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


### [STAGE:errors] Paso 3 — Manejo de Errores y Excepciones

Generar prompts especificos para las excepciones del PDD. Si son muchas, agrupar o separar.
"Agregar bloque 'On block error' con nombre '{NombreSubflow}_Handler'. Si ocurre {Excepcion}: establecer [StrEstadoEjecucion] en 'Error', llamar AddToLog con mensaje '{Mensaje}' y enviar correo de notificacion."

### [STAGE:log] Paso 4 — Cierre y Logs (Se pueden consolidar si son pasos breves)

"Escribir en el log de ejecucion [{RutaLog} o [rutaLog\aqui\va\la\ruta]\{NombreArchivoLog}.xlsx]: Fecha actual, Modulo [StrModulo], Proceso '{NombreReq}', Estado [StrEstadoEjecucion]. Cerrar todas las aplicaciones y archivos abiertos. Restablecer [StrEstadoEjecucion] con valor vacio. Restablecer [dt_{NombreReq}] con valor Nothing."

nota_desarrollador: "Configurar la ruta del archivo de log como parametro global al inicio
del flow principal, no como hardcode aqui. Columnas del log: Fecha, Modulo, Proceso, Estado.
Segun Beecker, usar subflujo AddToLog del Framework con variables StrLevel, StrModule, StrMessageLog.
IMPORTANTE: Restablecer TODAS las variables del req a su valor vacio/Nothing al finalizar
para evitar contaminacion de datos en ciclos o reqs posteriores (ver Principio 2)."

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

## Formato de salida — archivo `_prompts.md`

El skill genera UN ÚNICO archivo `.md` con TODOS los requerimientos del proyecto.
El archivo cubre los reqs con `puede_generar: true` leídos del `_analisis.json`.
Nombre del archivo: `<CODIGO>_prompts.md` (ej: FCM_001_prompts.md).

### Plantilla de estructura del archivo

```
# Prompts — [CODIGO_PROYECTO] — Power Automate Desktop

**Proyecto:** [nombre exacto del proyecto]
**Cliente:** [cliente]
**Versión PDD:** [version]
**Tecnología:** Power Automate Desktop (Copilot PAD — límite 500 chars/prompt)
**Generado:** [fecha]

---

## REQ_01 — [Nombre exacto del requerimiento]

> **Instrucción previa:** ANTES DE PEGAR ESTE PROMPT: Crear manualmente el subflow
> '[NombreSubflow]' (Menú Subflows > Nuevo subflujo). Copilot no puede crear subflows.
> Posicionarse dentro del subflow antes de pegar.

---

### Prompt 1 — Variables e inicialización | [NombreSubflow] | ~NNN chars

[texto del prompt en una sola línea continua con variables en [Corchetes]]

**Acciones cubiertas:** Inicialización de N variables del subflow.
**Nota para el desarrollador:** [instrucción post-Copilot: qué ajustar, qué grabar, qué verificar]

---

### Prompt 2 — [Descripción de la lógica] | ~NNN chars

[texto del prompt]

**Acciones cubiertas:** [qué parte del req cubre]
**Nota para el desarrollador:** [notas]

---

### Prompt 3 — Manejo de errores | ~NNN chars

[texto del prompt]

**Nota para el desarrollador:** [notas]

---

### Prompt 4 — Log y cierre | ~NNN chars

[texto del prompt]

**Nota para el desarrollador:** [notas]

**Pasos manuales requeridos para REQ_01:**
- [Paso que Copilot no puede generar]
- [Otro paso manual]

---

## REQ_02 — [Nombre exacto del requerimiento]

[misma estructura...]

---

## Resumen de cobertura

| REQ | Nombre | Prompts | Estado |
|-----|--------|---------|--------|
| REQ_01 | [nombre] | N | Generado |
| REQ_02 | [nombre] | N | Generado |

**Pasos manuales globales del proyecto:**
- [Paso manual que aplica a todo el proyecto]
```

**Reglas del archivo de salida:**
- El texto de cada prompt va en un bloque de código (``` ```) en una sola línea continua
- El encabezado de cada prompt incluye el número, descripción y estimado de caracteres
- Los sub-requerimientos van como sub-secciones `### Sub-REQ_01.1` dentro del REQ padre
- Advertencias de gaps menores documentadas al inicio de cada REQ afectado

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
11. Todas las variables del Prompt 2+ aparecen tambien inicializadas en el Prompt 1?
12. Los valores textuales del PDD (columnas, asuntos, mensajes) preservan acentos y puntuacion exacta?
13. Las variables dinamicas estan inicializadas con valor vacio en Prompt 1 con nota de como se llenan?
14. El Paso 4 incluye restablecimiento de variables a vacio/Nothing al finalizar el subflow?
15. La accion de extraccion de texto usa la accion correcta segun la fuente (no Trim cuando es extraccion)?