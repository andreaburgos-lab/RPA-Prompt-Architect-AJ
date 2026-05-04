---
name: generar-analisis
description: |
  Genera el JSON de análisis estructurado a partir del .toon leído y la clasificación de tecnología.
  Se activa internamente desde analizar-pdd después de clasificar-tecnologia.
  Produce outputs/<CODIGO>_analisis.json con todos los requerimientos, acciones, reglas,
  excepciones, gaps e información faltante extraídos con fidelidad exacta del PDD.
  No usar directamente por el usuario — es un skill interno del pipeline.
---

# Skill: Generar JSON de Análisis

## Propósito

Transformar el contenido completo del .toon en el JSON de análisis estructurado.
Este JSON es la fuente de verdad para los skills de generación de prompts.
Su calidad determina directamente la calidad de los prompts que se generarán.

Principio rector: cada campo debe reflejar lo que está escrito en el PDD,
con los nombres EXACTOS, las acciones COMPLETAS y los gaps REALES.
Nunca inventar, inferir ni completar lo que el PDD no dice explícitamente.

---

## Criterios de extracción por campo

### Campo proyecto
- Leer el valor EXACTAMENTE como aparece en el campo "ID proyecto" o "id_proyecto" del encabezado.
- Si dice "PDC.002" escribir "PDC.002". No transformar a "PDC002" ni "pdc002".
- Si el campo no existe, usar el ID que aparezca más frecuentemente en los encabezados de página.

### Campo nombre
- Texto exacto después de "Nombre de la acción:", o después del número y punto en el bloque.
- No resumir, no corregir ortografía, no traducir.
- Si el PDD dice "Realizar base cruce" escribir "Realizar base cruce", no "Realizar cruce base".

### Campo sistemas
- Buscar la línea "Sistema:" al final del bloque del requerimiento.
- También extraer sistemas mencionados en la descripción, el Happy Path y los inputs/outputs.
- Separar múltiples sistemas por coma en el array. Excluir "NA" y valores vacíos.
- Si no está explícito en ninguna parte del bloque dejar [].

### Campo acciones

INSTRUCCION CRITICA — leer completo antes de escribir:

Antes de escribir las acciones:
1. Ejecutar PASO A: leer todo el bloque hasta el inicio del siguiente requerimiento (puede ocupar varias páginas)
2. Ejecutar PASO B: si hay lista de campos a extraer o ingresar, CONTAR el total antes de empezar

Reglas de redacción:
- Extraer TODOS los pasos del proceso en orden lógico, incluyendo los de páginas siguientes.
- Si el requerimiento lista N campos a extraer o ingresar generar N acciones explícitas.
- Usar verbo específico + objeto concreto + contexto. NUNCA verbos vagos.
  INCORRECTO: "Procesar archivo"
  CORRECTO: "Abrir el archivo PDF 'Facturas a procesar', leer los campos: Serie, Número de DTE, Fecha de factura, NIT, Razón social, Total, INCOTERM, Peso Bruto, Peso Neto, Flete, Seguro, R. Despacho, Condición de pago"
- Usar nombres EXACTOS de campos, columnas y secciones tal como aparecen en el PDD.
- En pasos de ingreso o actualización, siempre especificar trazabilidad origen destino:
  INCORRECTO: "Ingresar datos del piloto en Observaciones"
  CORRECTO: "En la sección 'Observaciones', ingresar: [Nombre Completo del correo] al campo 'Observaciones'; [Placa del correo] al campo 'Observaciones'; [Cantidad de bultos de la factura] al campo 'Observaciones'"
- Si hay variantes por condición (por INCOTERM, por número de facturas, por país destino) describirlas como sub-pasos dentro de la acción.
- Si el PDD dice "repetir por cada [elemento]" incluir como acción de bucle explícita: "Para cada [elemento]: [descripción del ciclo]"
- Si hay escenarios alternativos (Caso A / Caso B) redactarlos como acciones separadas con su encabezado.
- Incluir solo acciones del bot. No incluir criterios de aceptación de QA.

### Campo inputs
- Extraer de: sección "Input" del bloque, precondiciones, pasos donde el bot lee información.
- Incluir: nombre exacto del archivo o dato, tipo (archivo .xlsx, variable de texto, etc.) y fuente (de dónde lo obtiene el bot).
- Formato: "Nombre exacto (tipo) — fuente: cómo lo obtiene el bot"
- Si el input es el output de un requerimiento anterior documentarlo: "output de [REQ_ID] — nombre exacto"
- Si no está definido dejar "NA" y agregar gap de advertencia.

### Campo outputs
- Extraer de: sección "Output" del bloque, último paso del Happy Path, finalidad mencionada.
- Incluir: nombre exacto, formato y ubicación o ruta si están definidos.
- Formato: "Nombre exacto (formato) — destino: ruta o sistema"
- Si la nomenclatura es dinámica (ej: "[CuentaCorriente][Banco].xlsx") documentarla exactamente así.
- Si no está definido dejar "NA" y agregar gap de advertencia.

### Campo reglas_negocio

PROHIBICION ABSOLUTA: No escribir ninguna regla que no esté textualmente en el PDD.

- Ejecutar PASO E (validación anti-invención) y PASO C (búsqueda de notas) antes de completar.
- Formato obligatorio: "Si [condición exacta del PDD] entonces [acción exacta del bot]"
- Incluir escenarios de borde solo si tienen resolución DEFINIDA en el PDD.
- Si una lógica se infiere pero no está escrita va en informacion_faltante con categoría REGLA DE NEGOCIO.
- Buscar activamente en: cuerpo del requerimiento, "Notas:", párrafos de cierre, texto en negrita de aclaración.

### Campo excepciones

REGLA CRITICA: Leer cada excepción COMPLETA antes de escribirla.
Muchas tienen múltiples sub-acciones en un mismo párrafo. Todas deben estar en el campo accion.

- Ejecutar PASO D (conteo de excepciones) antes de completar.
- El array excepciones DEBE tener exactamente el mismo número de objetos que excepciones documentadas.
- Verificar también en la sección 3.5 del PDD si hay excepciones adicionales asignadas al requerimiento.

Por cada excepción, tres sub-campos obligatorios:
- condicion: causa exacta tal como está escrita en el PDD (sin parafrasear)
- accion: TODAS las acciones que toma el bot, incluyendo las secundarias. Si el PDD dice "detiene el proceso, notifica con mensaje 'X', registra Sin procesar en columna Status, coloca motivo en columna Detalle, mueve las facturas a carpeta Facturas Procesadas" el campo debe incluir las cinco acciones completas.
- log: qué registrar en el log. Si no está especificado en el PDD escribir "(por definir)"

### Campo requiere_script

Marcar true cuando las acciones nativas de la plataforma son insuficientes:

Lógica con múltiples condiciones anidadas complejas:
  justificacion: "Requiere script por lógica de decisión con N niveles de anidación que exceden las acciones nativas de Condición"

Manipulación masiva de datos (búsquedas, prorrateos, transformaciones sobre N registros):
  justificacion: "Requiere script por procesamiento de registros con lógica de prorrateo/transformación"

Procesamiento de texto complejo (regex, parseo estructurado de texto libre):
  justificacion: "Requiere script por extracción de campos mediante regex sobre texto no estructurado"

Cálculos matemáticos que exceden las acciones de expresión nativas:
  justificacion: "Requiere script por cálculo de [tipo] no disponible en acciones nativas"

Interacciones UI complejas sobre sistemas legacy con selectores dinámicos:
  justificacion: "Requiere script por selectores dinámicos en [sistema] que Copilot no puede generar"

Manipulación de archivos PDF, ZIP, XML sin conector nativo disponible:
  justificacion: "Requiere script por procesamiento de [formato] sin conector nativo disponible"

Si no aplica ninguna situación: requiere_script false, justificacion_script ""

### Campo patron_arquitectura
- Solo incluir cuando la tecnología es Power Automate Y el requerimiento es híbrido.
- Describir: qué parte hace el Cloud Flow, qué parte hace el Desktop Flow, cómo se comunican.
- Para requerimientos puramente Desktop o puramente Cloud dejar "".
- Para tecnologías distintas a Power Automate NO incluir este campo en el JSON.

### Campo tipo
- Solo incluir cuando la tecnología es Power Automate.
- Valores posibles: "cloud", "desktop", "hibrido"
- Para UiPath, Automation Anywhere u otras NO incluir este campo en el JSON.

### Campo informacion_faltante

CAMPO CRITICO. Identifica todo dato ausente que bloquee o arriesgue el desarrollo.

Evaluar estas 9 categorías para cada requerimiento:

TRIGGER: Evento de inicio no definido, asunto de correo no especificado, horario o frecuencia no definidos.
SISTEMAS Y ACCESO: URL del sistema, ruta de carpeta de red, credenciales, versión del sistema, tipo de acceso (UI vs API) no definidos.
INPUTS: Nombre exacto del archivo de entrada, ruta, formato, responsable de proveerlo, nomenclatura no definidos.
OUTPUTS: Ruta de destino, nombre exacto del archivo de salida, formato, nomenclatura dinámica no definidos.
REGLA DE NEGOCIO: Condición de borde sin resolución definida en el PDD, lógica que el PDD implica pero no escribe.
EXCEPCION: Destinatario del correo de error no definido, mensaje de notificación no especificado, acción o log dice "por definir".
CRITERIO UI: Selector de elemento UI no definido, criterio para identificar la fila correcta en una tabla no especificado.
CONFIGURACION TECNICA: Parámetros del sistema, licencias requeridas, clase de documento en SAP/JDE, configuración de entorno no definidos.
REFERENCIA HUERFANA: Archivo, dato o sistema mencionado como dado pero sin definir cómo el bot lo obtiene, dónde está, quién lo provee.

Formato de cada item: "[CATEGORIA] — descripción concisa de qué falta y su impacto en el desarrollo"
Ejemplo: "TRIGGER — No se define el asunto exacto del correo que dispara el proceso. Sin esto no se puede configurar el filtro del trigger en el Cloud Flow."

No marcar como REFERENCIA HUERFANA si el insumo es el output directo y explícito de un requerimiento anterior del mismo PDD.

Si todo está completo dejar [].

### Campo gaps

Evaluar para cada requerimiento y sub-requerimiento:

Gaps CRITICOS — impiden generar prompts, puede_generar: false:
- Sistema no especificado, vacío o "NA": "SISTEMAS Y ACCESO — Sistema no especificado. Sin sistema, Copilot no puede inferir qué aplicación automatizar ni qué acciones usar."
- Nombre del requerimiento no definido: "Nombre del requerimiento no definido. No es posible identificar el req."
- Sin descripción Y sin acciones definidas: "Sin descripción ni acciones definidas. No es posible generar prompts útiles para este requerimiento."
- Información faltante que impide definir el trigger o los pasos principales: documentar el item específico.

Gaps de ADVERTENCIA — prompts se generan pero con notas, puede_generar: true:
- Input "NA" o vacío: "INPUTS — Input no especificado. Confirmar datos de entrada con el equipo de BA antes de implementar."
- Output "NA" o vacío: "OUTPUTS — Output no especificado. Confirmar resultado esperado con el equipo de BA."
- Excepción sin acción definida: "EXCEPCION — La excepción '[nombre]' no tiene acción definida. El desarrollador debe confirmar el comportamiento esperado."
- Regla de negocio implícita no escrita: "REGLA DE NEGOCIO — [descripción de la lógica implícita]. Confirmar con BA si aplica y cómo resolverla."

### Campo sub_requerimientos

Incluir TODOS los sub-requerimientos del req padre (notación decimal 8.1, 8.2, etc. o @subaccion[N.M]).

Cada sub-requerimiento se analiza con TODOS los campos completos, igual que un requerimiento principal:
id, nombre, plataforma, sistemas, acciones, inputs, outputs, reglas_negocio, excepciones,
requiere_script, justificacion_script, informacion_faltante, gaps.

Si el req no tiene sub-requerimientos dejar [].

---

## Estructura completa del JSON de salida

{
  "proyecto": "[ID exacto del campo ID proyecto del encabezado, ej: PDC.002]",
  "tecnologia": "[tech_label del skill clasificar-tecnologia, ej: Power Automate Desktop]",
  "es_hibrido": false,
  "clasificacion": {
    "razon": "[razon_clasificacion del skill clasificar-tecnologia]",
    "plataforma_cloud": null,
    "plataforma_desktop": null
  },
  "generado": "[ISO 8601 timestamp]",
  "_meta": {
    "titulo": "[titulo exacto del PDD]",
    "version": "[version del documento]",
    "cliente": "[cliente o empresa]"
  },
  "requerimientos": [
    {
      "id": "[proyecto].[REQ_ID]",
      "nombre": "[nombre EXACTO del requerimiento tal como aparece en el PDD]",
      "plataforma": "Desktop Flow | Cloud Flow",
      "tipo": "desktop | cloud | hibrido",
      "patron_arquitectura": "",
      "sistemas": ["sistema1", "sistema2"],
      "inputs": [
        "[nombre exacto del archivo o dato (tipo) — fuente: cómo lo obtiene el bot]"
      ],
      "outputs": [
        "[nombre exacto del resultado (formato) — destino: ruta o sistema]"
      ],
      "acciones": [
        "Acción 1 con verbo específico + objeto concreto + trazabilidad origen destino si aplica",
        "Acción 2 completa incluyendo todos los campos de la lista si el PDD los enumera",
        "Para cada [elemento]: descripción del bucle si el PDD lo indica"
      ],
      "reglas_negocio": [
        "Si [condición exacta del PDD] entonces [acción exacta del bot]"
      ],
      "excepciones": [
        {
          "condicion": "causa exacta del error tal como está escrita en el PDD",
          "accion": "TODAS las acciones del bot: detener + notificar con mensaje EXACTO X + registrar Sin procesar en columna Status + registrar motivo en columna Detalle + mover archivos a carpeta Y [todas las sub-acciones completas]",
          "log": "qué registrar: fecha/hora, ID req, valores clave, causa del error"
        }
      ],
      "requiere_script": false,
      "justificacion_script": "",
      "informacion_faltante": [
        "[CATEGORIA] — descripción del gap y su impacto en el desarrollo"
      ],
      "gaps": {
        "criticos": ["descripción del gap crítico con categoría"],
        "advertencias": ["descripción de la advertencia con categoría"],
        "puede_generar": true
      },
      "sub_requerimientos": [
        {
          "id": "[proyecto].[REQ_ID].[SUB_ID]",
          "nombre": "[nombre exacto del sub-requerimiento]",
          "plataforma": "Desktop Flow | Cloud Flow",
          "sistemas": ["sistema"],
          "inputs": ["input exacto (tipo) — fuente: origen"],
          "outputs": ["output exacto (formato) — destino: ruta o sistema"],
          "acciones": [
            "Acción completa del sub-req con trazabilidad origen destino"
          ],
          "reglas_negocio": [],
          "excepciones": [],
          "requiere_script": false,
          "justificacion_script": "",
          "informacion_faltante": [],
          "gaps": {
            "criticos": [],
            "advertencias": [],
            "puede_generar": true
          }
        }
      ]
    }
  ]
}

---

## Reglas de formato del JSON — OBLIGATORIAS

Encoding UTF-8 directo: escribir á, é, í, ó, ú, ñ y todos los caracteres directamente.
NUNCA como secuencias de escape unicode.

Valores exactos: usar siempre el texto tal como aparece en el PDD. No parafrasear nombres propios.

Arrays vacíos: si un campo no tiene contenido usar [], no null ni omitir el campo.

Strings vacíos: si un campo de texto no tiene contenido usar "", no null.

Orden de requerimientos: mismo orden que en el documento PDD, sin alteraciones.

Campos tipo y patron_arquitectura: solo para Power Automate. Omitir para UiPath, Automation Anywhere u otras.

---

## Verificación final antes de guardar

1. ¿El campo proyecto es EXACTAMENTE el valor del encabezado del PDD?
2. ¿El número de objetos en requerimientos es igual al número de reqs de la sección 2.4?
3. ¿Cada requerimiento con lista de campos tiene TODOS los campos en acciones (Paso B verificado)?
4. ¿Cada acción de ingreso/actualización especifica [origen] al [campo destino en sección]?
5. ¿Se revisaron Notas, texto en negrita y párrafos de cierre de cada req (Paso C)?
6. ¿Cada array excepciones tiene exactamente el número de excepciones del PDD (Paso D)?
7. ¿Cada objeto de excepción tiene su accion COMPLETA incluyendo sub-acciones secundarias?
8. ¿Ninguna regla_negocio fue inferida — todas están textualmente en el PDD (Paso E)?
9. ¿Los nombres de campos, columnas, mensajes de error y archivos son exactamente como en el PDD?
10. ¿Los sub-requerimientos tienen todos sus campos analizados completamente?
11. ¿El JSON usa caracteres UTF-8 directos, sin escapes unicode?
12. ¿Los campos tipo y patron_arquitectura se incluyen solo cuando la tecnología es Power Automate?

Si alguna respuesta es NO corregir antes de guardar el archivo.

---

## Guardar el archivo

Guardar en: outputs/[CODIGO_NORMALIZADO]_analisis.json

CODIGO_NORMALIZADO = código del proyecto con puntos reemplazados por guiones bajos.

PDC.002 -> PDC_002_analisis.json
FCM.001 -> FCM_001_analisis.json
MMC.001 -> MMC_001_analisis.json