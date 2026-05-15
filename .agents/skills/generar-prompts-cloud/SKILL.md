---
name: generar-prompts-cloud
description: |
  Genera prompts optimizados para Copilot de Power Automate Cloud a partir del JSON de analisis.
  Se activa internamente desde analizar-pdd o hibrido para reqs con plataforma Cloud Flow.
  Limite: 2000 caracteres por prompt. Produce prompts especificos con conectores exactos,
  variables nombradas, rutas reales y columnas del PDD. No usar directamente por el usuario.
---

# Skill: Generar Prompts Power Automate Cloud Flow

**REGLA MANDATARIA — Leer recursos antes de generar:** Antes de comenzar cualquier generacion de prompts, el agente DEBE leer:
1. `resources/BuenasPracticas.md` — y aplicar sus lineamientos.
2. `resources/acciones.md` — para usar los nombres exactos de acciones y conectores soportados.

## Principios de prompting para Copilot Cloud — basados en documentacion oficial y foros

**Principio 1 — Formato "Cuando X ocurre, hacer Y":**
El trigger siempre en formato: "Cuando {evento} ocurre en {conector}, {accion principal}."
Para acciones dentro del diseñador: "Agregar la accion {NombreExacto} del conector {Conector}."

**Principio 2 — Trigger SIEMPRE solo en el Prompt 1:**
El primer prompt solo describe el trigger. Nunca combinar trigger con acciones.
Las acciones van en prompts separados usando el panel Copilot dentro del diseñador.

**Principio 3 — Conector + accion exacta siempre juntos:**
INCORRECTO: "guardar los adjuntos"
CORRECTO: "usando el conector SharePoint, usar la accion Crear archivo en la carpeta /Documentos/[NombreCarpeta]"
NUNCA usar nombres genericos; siempre el nombre exacto de Power Automate.

**Principio 4 — Variables SIN corchetes en Cloud:**
En Cloud, Copilot interpreta [variable] como texto literal.
INCORRECTO: "guardar en [correoAsunto]"
CORRECTO: "guardar el asunto del correo en una variable de tipo texto llamada StrCorreoAsunto"

**Principio 5 — Nomenclatura Beecker para variables Cloud:**
  Boolean  -> Bln  -> BlnNombreVariable
  Integer  -> Int  -> IntNombreVariable
  Float    -> Flt  -> FltNombreVariable
  String   -> Str  -> StrNombreVariable
  Object   -> Obj  -> ObjNombreVariable
  Array    -> Arr  -> ArrNombreVariable
Parametros: in_StrNombreEntrada (entrada), out_StrNombreSalida (salida)

**Principio 6 — Especificidad de parametros obligatorios:**
Si Copilot Cloud no recibe el sitio de SharePoint, la tabla de Excel o el canal de Teams,
deja el campo vacio y requiere configuracion manual. SIEMPRE incluir:
  SharePoint: sitio URL o placeholder [https://empresa.sharepoint.com/sites/NombreSitio]
  Excel Online: nombre de tabla o placeholder [NombreTabla]
  Teams: canal o placeholder [NombreCanal]

**Principio 7 — Maximo de acciones por prompt Cloud:**
  Trigger: 1 elemento, prompt independiente
  Inicializar variable: maximo 5 variables en ramas paralelas por prompt (limite Beecker)
  Acciones del mismo conector: maximo 2 por prompt
  Condicion completa (if + ramas): 1 por prompt
  Notificacion/error: 1 por prompt
Si hay mas, dividir en prompts numerados.

**Principio 8 — Columnas y campos especificos:**
Si el PDD lista columnas de Excel o campos de SharePoint, nombrarlos TODOS en el prompt.
Si exceden 2000 chars, dividir en Prompt 3a, 3b con nota al desarrollador.
nota_desarrollador: "Verificar que se mapearon las N columnas: [Col1], [Col2]...
Si el prompt cubrio solo X, ejecutar Prompt 3b."

**Principio 9 — Scopes y nombres de acciones (Buenas Practicas Beecker):**
  Usar Scopes (Ambitos) para agrupar acciones del mismo tipo o funcion
  El nombre del scope debe ser descriptivo de lo que realiza
  Nombres de acciones: "Nombre default - informacion de accion" o nombre descriptivo
  PROHIBIDO: dejar nombre default sin modificar, acentos, caracteres especiales en nombres
  33% minimo de acciones deben tener nota/descripcion (porcentaje minimo Beecker)

**Principio 11 — Granularidad y Cobertura (1 a N):**
No limitarse a 4 prompts por requerimiento. Generar de 1 a N prompts segun sea necesario
para cubrir entre el 80% y 100% de la funcionalidad descrita en el PDD/JSON.
Si un requerimiento tiene 10 pasos logicos, generar 6-8 prompts si es necesario para
mantener la precision y no perder detalles.

**Principio 12 — Bucles, Iteraciones y Campos Masivos:**
- Si el proceso implica procesar varios elementos (correos, filas de Excel), el prompt DEBE incluir explicitamente la accion "Aplicar a cada uno" (Apply to each).
- Si el PDD lista muchos campos (ej: 20+ campos de una factura), NOMBRARLOS TODOS en el prompt. Si no caben en 2000 chars, dividir en subprompts (3a, 3b...).
- Diferenciar claramente entre extraer datos del cuerpo de un correo y guardar sus adjuntos.

**Principio 13 — Validaciones Robustas:**
Evitar validaciones basadas UNICAMENTE en comparacion de texto literal si el PDD sugiere
patrones. Ej: Validar longitud de cadena o presencia de palabras clave combinadas.

**Principio 14 — Fidelidad de texto en valores de prompt (acentos y puntuacion):**
Los valores textuales del PDD (nombres de columnas, asuntos de correo, mensajes de error,
nombres de tablas/listas de SharePoint) se reproducen en el prompt EXACTAMENTE como aparecen
en el PDD, incluyendo acentos, tildes, enes con tilde y puntuacion.
EXCEPCION: los NOMBRES de variables siguen la regla Beecker (sin acentos, CamelCase).
Esta excepcion aplica SOLO a nombres de codigo, nunca a valores textuales o etiquetas de UI.
Ejemplo:
  PDD dice columna SharePoint: "Número de factura"
  INCORRECTO: columna 'Numero de factura'
  CORRECTO:   columna 'Número de factura'

**Principio 15 — Datos dinamicos vs. datos estaticos en Cloud:**
Al describir valores en el Prompt 2 (inicializacion de variables):
  ESTATICO: valor fijo entre ejecuciones (nombre de un flow, un texto de configuracion).
    En el prompt: "tipo texto con valor 'ValorFijo'" — escribir el valor literal.
    En nota_desarrollador: indicar que debe venir de configuracion, no hardcodeado.
  DINAMICO: cambia cada ejecucion (datos del trigger, resultados de una accion anterior).
    En el prompt: "tipo texto con valor vacio (se llena con el trigger o accion posterior)."
    En nota_desarrollador: documentar de donde se obtiene el valor dinamico.
PROHIBIDO: inicializar una variable dinamica con un valor estatico de ejemplo.

---

> **Referencia de acciones y conectores:** Consultar `resources/acciones.md` para la lista
> completa de conectores, triggers y acciones con nombres exactos, sufijos de versión (V2/V3)
> y parámetros obligatorios. NUNCA parafrasear los nombres de acciones.

---

## Estructura de prompts por requerimiento

Para cada req con puede_generar = true, generar una secuencia de 1 a N prompts
asegurando cobertura total (80-100%):

### [STAGE:trigger] Paso 1 — Trigger (Prompt independiente)

"Crear un Cloud Flow automatizado con el trigger {TriggerExacto} del conector
{ConectorExacto}{, filtrado por {condicion_exacta_del_PDD} si aplica}."

Mapeo sistema -> trigger:
  Outlook/correo:   Cuando llega un nuevo correo electronico (V3) del conector Office 365 Outlook
  SharePoint:       Cuando se crea o modifica un elemento del conector SharePoint
  OneDrive:         Cuando se crea un archivo del conector OneDrive for Business
  Forms:            Cuando se envia una nueva respuesta del conector Microsoft Forms
  Sin trigger claro: trigger manual (Instant Flow - se ejecuta manualmente)

instruccion_previa: "Pegar este prompt en el campo 'Crear tu automatizacion con Copilot'
en la pagina de inicio de Power Automate (make.powerautomate.com > + Crear > Con Copilot).
Agregar descripcion al flujo con: proposito, condiciones previas, referencia al req {req.id}."

nota_desarrollador: "Conector: {ConectorExacto}. Configurar filtros del trigger en el panel
de diseno despues de generarlo (ej: filtro de asunto, sitio de SharePoint, carpeta)."

### [STAGE:variables] Prompt 2 — Inicializar variables (max 5 en ramas paralelas por Beecker)

**PROTOCOLO DE COMPLETITUD DE VARIABLES (ejecutar ANTES de escribir el Prompt 2):**
1. Leer el array "acciones" y "reglas_negocio" completos del req en el JSON de analisis.
2. Identificar TODOS los datos que el flow necesitara almacenar durante su ejecucion.
3. Incluir TODAS en el Prompt 2, con tipo y valor inicial correcto.
4. Si hay mas de 5 variables: dividir en Prompt 2a (primeras 5) y Prompt 2b (siguientes).
5. Verificar que NINGUNA variable aparece por primera vez en el Prompt 3 o siguientes
   sin haber sido inicializada en el Prompt 2. En Cloud, las variables deben existir
   antes de poder usarlas en el flow.

Estructura: "Agregar la accion Inicializar variable {N} veces usando ramas paralelas:
la primera llamada Str{NombreVar1} de tipo texto con valor '{valorInicial}',
la segunda llamada Str{NombreVar2} de tipo texto con valor vacio,
{continuar para cada variable del req}."

Variables minimas siempre presentes:
  StrEstadoEjecucion: estado del proceso (Exito/Error)
  StrModulo: nombre del flujo para logs, valor = '{NombreFlowExacto}'
  Variables especificas del req segun sus inputs (ej: StrCuentaCorriente, StrEmpresa)
  Si hay listas: ArrResultados o ArrNombreContenido

instruccion_previa: "Pegar en el panel Copilot dentro del diseñador, despues de confirmar el trigger.
Seleccionar 'Agregar un paso' en el panel Copilot del diseñador."

nota_desarrollador: "Maximo 5 ramas paralelas recomendado por Beecker para conservar
legibilidad. Si hay mas de 5 variables, dividir en dos acciones de ramas paralelas.
Tipos: texto (String), numero entero (Int), booleano (Bln), array (Arr), objeto (Obj)."

### [STAGE:logic] Paso 3 — Logica de Proceso (1 a N prompts)

**Manejo de Iteraciones:**
"Agregar la accion Aplicar a cada uno (Apply to each) para iterar sobre [Lista/Adjuntos].
Dentro del bucle: {Acciones de extraccion o procesamiento}."

**Extraccion y Mapeo de Campos (REGLA DE ORO):**
"Usando el conector {Conector}, mapear los campos: '{Campo1}' <- {Origen1}, '{Campo2}' <- {Origen2},
'{Campo3}' <- {Origen3}... {NOMBRAR TODOS LOS CAMPOS DEL PDD. Si no caben, dividir en Prompt 3b}."

### Prompt 3 — Accion principal (especifica por tipo de sistema)

El prompt describe la accion ESPECIFICA del req. Incluir conector exacto, nombre de tabla,
sitio de SharePoint, carpeta, y columnas si el PDD las lista.

**Para SharePoint (obtener archivo):**
"Agregar la accion Obtener contenido del archivo del conector SharePoint apuntando al
sitio [{https://empresa.sharepoint.com/sites/NombreSitio}], carpeta
'[{/Documentos/RutaCarpeta}]', archivo '{NombreArchivo.xlsx}'.
Luego agregar la accion Establecer variable para guardar el contenido en StrArchivoContenido."

**Para SharePoint (crear/actualizar elemento con columnas):**
"Agregar la accion Crear elemento del conector SharePoint en el sitio
[{https://empresa.sharepoint.com/sites/NombreSitio}], lista '{NombreLista}'.
Mapear los campos: columna '{Campo1}' <- {Origen1}, columna '{Campo2}' <- {Origen2},
columna '{Campo3}' <- {Origen3}. {Si hay mas columnas: ver Prompt 3b.}"

nota_desarrollador: "Verificar que se mapearon los N campos del req:
{lista COMPLETA de campos del PDD}. Si el prompt cubrio solo X, ejecutar Prompt 3b."

**Para Excel Online (leer tabla):**
"Agregar la accion Listar las filas presentes en una tabla del conector
Excel Online (Business). Seleccionar la ubicacion [{OneDrive/SharePoint}],
archivo '{NombreArchivo.xlsx}', hoja '{NombreHoja}', tabla '{NombreTabla}'.
Guardar el resultado en la variable ArrFilas."

**Para Excel Online (escribir fila con columnas especificas):**
"Agregar la accion Agregar una fila a una tabla del conector Excel Online (Business).
Archivo '{NombreArchivo.xlsx}', tabla '{NombreTabla}'.
Columnas a poblar: '{ColA}' <- StrValorA, '{ColB}' <- StrValorB, '{ColC}' <- StrValorC.
{Si hay mas columnas: ver Prompt 3b.}"

**Para correo (extraccion de campos del cuerpo):**
"Agregar la accion Obtener adjuntos (V2) del conector Office 365 Outlook usando el
Id de mensaje del trigger. Guardar resultado en ArrAdjuntos.
Agregar la accion Establecer variable para guardar el asunto del correo
en la variable StrCorreoAsunto y el remitente en StrCorreoRemitente."

**Para condicion de validacion:**
"Agregar la accion Condicion renombrada como '{CondicionDescriptiva}' que verifique
si {condicion_exacta_del_PDD}. En la rama Verdadero: {accion_rama_true}.
En la rama Falso: {accion_rama_false o log de error}."

nota: El bloque True debe tener la accion principal. PROHIBIDO bloque True vacio (regla Beecker).

**Diferenciacion de Adjuntos:**
"Usando el conector Outlook, obtener adjuntos del correo. Para cada adjunto: usar el conector SharePoint
para la accion Crear archivo en la carpeta '{Ruta}'."

### [STAGE:errors] Prompt 4 — Manejo de errores y Logs

"Agregar Ambito '{Nombre}_ManejadorErrores'. Si falla: enviar correo '{Asunto}' y establecer StrEstadoEjecucion en 'Error'. Finalizar con Terminar Fallido."

### Prompt 4 — Manejo de errores (si el req tiene excepciones)

"Agregar la accion Ambito renombrada como '{NombreSubflow}_ManejadorErrores' para
encapsular las acciones anteriores. Agregar rama paralela despues del ambito.
En la rama paralela, configurar la accion Condicion con RunAfter para que se
ejecute si el ambito falla. En la rama Verdadero de la condicion: agregar la
accion Enviar un correo electronico (V2) del conector Office 365 Outlook con
asunto '{AsuntoExactoDelPDD}' y establecer la variable StrEstadoEjecucion en 'Error'.
Agregar la accion Terminar configurada como Fallido."

nota_desarrollador: "Excepciones del req:
{listar TODAS las excepciones: condicion -> accion completa -> log}.
Configurar 'Ejecutar despues de' (Configure run after) en las acciones criticas del Ambito:
marcar 'Ha producido un error' y 'Se ha agotado el tiempo de espera'.
Segun Beecker: enviar al menos un log de error con nivel, modulo y mensaje."

---

## Subprompts por desbordamiento

Si el prompt 3 excede 2000 chars por cantidad de columnas o acciones:

Prompt 3a: primeras N columnas/acciones (dentro de 2000 chars)
  nota_desarrollador: "Este prompt cubre {N} de {Total} columnas. Ejecutar Prompt 3b para:
  {lista de columnas/acciones pendientes}. Verificar al final: {Total} columnas mapeadas."

Prompt 3b: "Continuacion del Prompt 3a. Agregar las siguientes columnas/acciones al
mismo elemento/tabla: '{ColN+1}' <- {OrigenN+1}, '{ColN+2}' <- {OrigenN+2}..."

---

## Sub-requerimientos

Para cada sub-req con puede_generar = true:
1. Generar sus propios prompts con la misma estructura.
2. instruccion_previa del Prompt 1: "Este sub-req {sub_req.id} es parte de {req.id}.
   Agregar estos pasos dentro del Ambito del req padre o como un subflow invocado."
3. Si el sub-req tiene sistema distinto al padre, puede requerir un Ambito propio.

---

## Formato de salida — archivo `_prompts.md`

El skill genera UN ÚNICO archivo `.md` con TODOS los requerimientos del proyecto.
El archivo cubre los reqs con `puede_generar: true` leídos del `_analisis.json`.
Nombre del archivo: `<CODIGO>_prompts.md` (ej: FCM_001_prompts.md).

### Plantilla de estructura del archivo

```
# Prompts — [CODIGO_PROYECTO] — Power Automate Cloud

**Proyecto:** [nombre exacto del proyecto]
**Cliente:** [cliente]
**Versión PDD:** [version]
**Tecnología:** Power Automate Cloud Flow (Copilot Cloud — límite 2000 chars/prompt)
**Generado:** [fecha]

---

## REQ_01 — [Nombre exacto del requerimiento]

> **Instrucción previa Prompt 1:** Pegar en 'Crear tu automatización con Copilot'
> en make.powerautomate.com > + Crear > Con Copilot.

---

### Prompt 1 — Trigger | ~NNN chars

[texto del trigger en una sola línea continua. Variables sin corchetes: StrNombreVar]

**Acciones cubiertas:** Trigger del flujo — [nombre del trigger exacto]
**Nota para el desarrollador:** [configurar filtros del trigger en el panel de diseño]

---

### Prompt 2 — Inicializar variables | ~NNN chars

> **Instrucción previa:** Pegar en el panel Copilot dentro del diseñador.

[texto del prompt]

**Acciones cubiertas:** Inicialización de N variables en ramas paralelas.
**Nota para el desarrollador:** [tipos, origen de valores dinámicos]

---

### Prompt 3 — [Descripción de la lógica] | ~NNN chars

[texto del prompt]

**Acciones cubiertas:** [qué parte del req cubre]
**Nota para el desarrollador:** [notas específicas]

---

### Prompt 4 — Manejo de errores | ~NNN chars

[texto del prompt]

**Nota para el desarrollador:** [configurar RunAfter, excepciones del req]

---

**Pasos manuales requeridos para REQ_01:**
- [Paso que Copilot no puede generar]

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
- [Paso manual global]
```

**Reglas del archivo de salida:**
- Variables sin corchetes: `StrNombreVar` nunca `[StrNombreVar]`
- El texto de cada prompt va en un bloque de código en una sola línea continua
- Trigger siempre en Prompt 1 con instrucción de pegar en la página de creación de Power Automate
- Prompts 2+ con instrucción de pegar en el panel Copilot del diseñador

---

## Verificacion final

1. Ningun prompt Cloud usa [corchetes] para variables?
2. El trigger esta siempre solo en el Prompt 1?
3. Cada prompt menciona conector Y accion exacta juntos?
4. Los nombres de acciones son exactamente como aparecen en Power Automate?
5. Ningun prompt supera 2000 caracteres?
6. El campo prompt es texto en una sola linea continua sin \n?
7. Caracteres UTF-8 directos, sin escapes unicode?
8. Si el PDD lista columnas, estan todas en el prompt o en nota_desarrollador con aviso?
9. Hay nota de borrador para correos con informacion sensible (politica Beecker)?
10. Los scopes tienen nombres descriptivos (no "Ambito 1", "Ambito 2")?
11. Todas las variables del Prompt 3+ aparecen tambien inicializadas en el Prompt 2?
12. Los valores textuales del PDD (columnas, asuntos, nombres de lista) preservan acentos exactos?
13. Las variables dinamicas estan inicializadas con valor vacio en Prompt 2 con nota de origen?