---
name: generar-prompts-cloud
description: |
  Genera prompts optimizados para Copilot de Power Automate Cloud a partir del JSON de analisis.
  Se activa internamente desde analizar-pdd o hibrido para reqs con plataforma Cloud Flow.
  Limite: 2000 caracteres por prompt. Produce prompts especificos con conectores exactos,
  variables nombradas, rutas reales y columnas del PDD. No usar directamente por el usuario.
---

# Skill: Generar Prompts Power Automate Cloud Flow

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

**Principio 10 — Correos y politica Beecker:**
  Correos con informacion sensible -> guardar como borrador para revision humana
  Toda informacion del correo parametrizable: asunto, cuerpo, destinatarios
  PROHIBIDO hardcode de correos en acciones

---

## Nombres exactos de acciones y triggers (obligatorio usar estos, nunca parafrasear)

### Office 365 Outlook
  Trigger: Cuando llega un nuevo correo electronico (V3)
  Obtener correo electronico (V2)
  Enviar un correo electronico (V2) — solo si no tiene info sensible; sino: crear borrador
  Mover correo electronico (V2)
  Obtener adjuntos (V2)
  Exportar correo electronico (V2)

### SharePoint
  Trigger: Cuando se crea o modifica un elemento
  Trigger: Cuando se crea un archivo
  Obtener elementos | Obtener elemento | Crear elemento | Actualizar elemento
  Obtener contenido del archivo | Crear archivo | Eliminar elemento
  Enviar una solicitud HTTP a SharePoint

### Excel Online (Business)
  Listar las filas presentes en una tabla
  Agregar una fila a una tabla
  Obtener una fila | Actualizar una fila | Eliminar una fila
  Ejecutar script

### Control / General
  Inicializar variable | Establecer variable | Incrementar variable | Anexar a la variable de cadena
  Condicion | Aplicar a cada uno | Hacer hasta | Ambito | Terminar | Redactar
  Analizar JSON | Filtrar matriz | Seleccionar | Unirse | Crear tabla HTML | HTTP

### Otros conectores frecuentes
  OneDrive for Business: Crear archivo | Obtener contenido del archivo | Crear carpeta
  Teams: Publicar un mensaje en un chat o canal
  Approvals: Iniciar y esperar una aprobacion
  Dataverse: Agregar una nueva fila | Listar filas | Actualizar una fila

---

## Estructura de prompts por requerimiento

Para cada req con puede_generar = true, generar EN ESTE ORDEN:

### Prompt 1 — Trigger (SIEMPRE solo, nunca con acciones)

Formato: "Crear un Cloud Flow automatizado con el trigger {TriggerExacto} del conector
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

### Prompt 2 — Inicializar variables (max 5 en ramas paralelas por Beecker)

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

## Estructura JSON de salida

{
  "id_flujo": "[req.id]",
  "nombre_flujo": "[req.nombre exacto]",
  "plataforma": "Cloud Flow",
  "generar_prompt": true,
  "gaps_detectados": {
    "criticos": [],
    "advertencias": [],
    "impacto": "Sin gaps detectados."
  },
  "prompts_secuenciales": [
    {
      "numero_prompt": 1,
      "titulo": "Trigger del flujo",
      "instruccion_previa": "Pegar en 'Crear tu automatizacion con Copilot' en Power Automate...",
      "prompt": "texto en una sola linea continua sin corchetes en variables, sin \n internos",
      "caracteres": 187,
      "acciones_cubiertas": ["descripcion de que cubre este prompt"],
      "variables_referenciadas": ["StrNombreVar (sin corchetes en Cloud)"],
      "nota_desarrollador": "instruccion post-Copilot especifica con valores reales o placeholders"
    }
  ],
  "resumen_cobertura": "4 prompts para Cloud Flow. Cubren: trigger -> variables -> [conector] -> errores.",
  "pasos_manuales_requeridos": [
    "Descripcion especifica de lo que Copilot no puede generar en Cloud"
  ],
  "sub_prompts": []
}

## Campos eliminados (no incluir)
motivo_no_generado, _resumen a nivel raiz.

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