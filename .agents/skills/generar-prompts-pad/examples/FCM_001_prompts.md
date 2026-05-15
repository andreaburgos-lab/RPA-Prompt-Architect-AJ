# Prompts — FCM_001 — Power Automate Desktop

**Proyecto:** FCM.001 — Automatización de conciliación bancaria
**Cliente:** Empresa Ejemplo S.A.
**Versión PDD:** 1.2
**Tecnología:** Power Automate Desktop (Copilot PAD — límite 500 chars/prompt)
**Generado:** 2025-04-10

---

## REQ_01 — Descarga y procesamiento de extracto bancario

> **Instrucción previa:** ANTES DE PEGAR ESTE PROMPT: En Power Automate Desktop, crear
> manualmente el subflow **`DescargaExtractoBancario`** (Menú Subflows > Nuevo subflujo).
> Copilot no puede crear subflows. Posicionarse dentro del subflow antes de pegar.
> Agregar al inicio una acción Comentario con: REQ_01 — Descarga y procesamiento de extracto bancario.

---

### Prompt 1 — Variables e inicialización | ~478 chars

```
Inicializar variable de texto [StrExtractoRuta] con valor [rutaArchivo\aqui\va\la\ruta\Extracto Bancario Mensual.xlsx]. Inicializar variable de texto [StrConciliacionRuta] con valor [rutaArchivo\aqui\va\la\ruta\Conciliacion_FCM.xlsx]. Inicializar variable de texto [StrEstadoEjecucion] con valor vacío. Inicializar variable de texto [StrModulo] con valor 'DescargaExtractoBancario'. Inicializar variable de tabla de datos [dt_Extracto]. Inicializar variable booleana [BlnCorreoEncontrado] con valor False.
```

**Acciones cubiertas:** Inicialización de 6 variables del subflow.
**Nota para el desarrollador:** Las rutas de archivo deben configurarse como variables globales en el flow principal, no hardcodeadas aquí. [BlnCorreoEncontrado] se evalúa en el Prompt 2 al filtrar correos. [dt_Extracto] se llena en el Prompt 3 al leer Excel.

---

### Prompt 2 — Filtrar y descargar correo con extracto | ~492 chars

```
Usar la acción Recuperar mensajes de correo electrónico de Outlook filtrando por asunto que contenga 'Extracto Banco' y recibidos en los últimos 7 días. Guardar los correos en [LstCorreosExtracto]. Si [LstCorreosExtracto] está vacío: asignar [StrEstadoEjecucion] con valor 'Advertencia — Sin extracto bancario'. Si no está vacío: asignar [BlnCorreoEncontrado] con valor True y guardar los archivos adjuntos del primer correo en la carpeta [StrExtractoRuta].
```

**Acciones cubiertas:** Filtrado de correos por asunto, descarga de adjunto.
**Nota para el desarrollador:** Si hay más de un correo con el mismo asunto, el prompt procesa solo el primero (correo más reciente). Confirmar con el cliente si deben procesarse todos o solo el más reciente.

---

### Prompt 2b — Validar adjunto y abrir Excel | ~387 chars

```
Si el archivo [StrExtractoRuta] existe y tiene extensión .xlsx: iniciar Excel con [StrExtractoRuta]. Leer el rango de la hoja 'Movimientos' desde la celda A1 hasta la última fila y guardar en [dt_Extracto]. Cerrar Excel sin guardar. Si el archivo no existe o no es .xlsx: asignar [StrEstadoEjecucion] con valor 'Error — Adjunto no válido'.
```

**Acciones cubiertas:** Validación de extensión, apertura de Excel, lectura de rango a DataTable.
**Nota para el desarrollador:** Reemplazar 'Movimientos' con el nombre exacto de la hoja una vez confirmado. El DataTable [dt_Extracto] contendrá las columnas: Estado, y todas las columnas del extracto bancario definidas en el PDD.

---

### Prompt 3 — Iterar y copiar filas pendientes | ~455 chars

```
Abrir Excel [StrConciliacionRuta] o crearlo si no existe. Para cada fila en [dt_Extracto]: si la columna 'Estado' es igual a 'Pendiente', obtener la primera fila libre en la hoja 'Conciliacion' y escribir todos los valores de la fila actual en esa posición. Guardar y cerrar [StrConciliacionRuta]. Mover el primer correo de [LstCorreosExtracto] a la carpeta 'Procesados' de Outlook.
```

**Acciones cubiertas:** Iteración For Each, filtro condicional por Estado, escritura en Excel de salida, archivo del correo.
**Nota para el desarrollador:** La hoja de destino en Conciliación_FCM.xlsx debe llamarse 'Conciliacion'. Si el archivo no existe, PAD lo creará vacío y habrá que agregar los encabezados manualmente la primera vez (o agregar un Prompt 3a que cree los encabezados si la primera fila está vacía).

---

### Prompt 4 — Manejo de errores | ~427 chars

```
Agregar bloque 'En error de bloque' con nombre 'DescargaExtractoBancario_Handler'. Si ocurre un error: asignar [StrEstadoEjecucion] con valor 'Error — ' concatenado con el mensaje de error. Enviar correo electrónico a través de Outlook con destinatario soporte@empresa.com, asunto 'FCM.001 — Error en DescargaExtractoBancario', cuerpo [StrEstadoEjecucion]. Guardar como borrador para revisión humana.
```

**Acciones cubiertas:** Captura de error global, notificación por correo (borrador).
**Nota para el desarrollador:** Reemplazar soporte@empresa.com con el correo real del equipo de soporte. Según política Beecker, guardar como borrador. El asunto y destinatario deben parametrizarse como variables globales.

---

### Prompt 5 — Log y cierre | ~418 chars

```
Si [StrEstadoEjecucion] está vacío: asignar [StrEstadoEjecucion] con valor 'Éxito'. Abrir Excel [rutaLog\aqui\va\la\ruta\Log_FCM.xlsx]. Obtener la primera fila libre y escribir: fecha actual, [StrModulo], 'REQ_01 — Descarga y procesamiento de extracto bancario', [StrEstadoEjecucion]. Guardar y cerrar. Restablecer [StrEstadoEjecucion] con valor vacío. Restablecer [dt_Extracto] con valor Nothing.
```

**Acciones cubiertas:** Registro en log Excel, restablecimiento de variables globales.
**Nota para el desarrollador:** Configurar la ruta del log como variable global en el flow principal. Restablecer TODAS las variables del req a vacío/Nothing al finalizar para evitar contaminación en ciclos posteriores.

**Pasos manuales requeridos para REQ_01:**
- Crear el subflow `DescargaExtractoBancario` manualmente antes de pegar los prompts.
- Confirmar con el cliente el nombre exacto de la hoja del extracto bancario (actualmente: 'Movimientos').
- Configurar la ruta de destino del extracto descargado y de la conciliación como variables globales.
- La primera ejecución puede requerir crear manualmente los encabezados en Conciliación_FCM.xlsx.

---

## REQ_02 — Notificación de resultado del proceso

> **Instrucción previa:** ANTES DE PEGAR ESTE PROMPT: Crear manualmente el subflow
> **`NotificacionResultado`**. Posicionarse dentro del subflow antes de pegar.

---

### Prompt 1 — Variables e inicialización | ~336 chars

```
Inicializar variable de texto [StrLogRuta] con valor [rutaArchivo\aqui\va\la\ruta\Log_FCM.xlsx]. Inicializar variable de texto [StrEstadoProceso] con valor vacío. Inicializar variable de texto [StrModulo] con valor 'NotificacionResultado'. Inicializar variable de texto [StrCuerpoCorreo] con valor vacío.
```

**Acciones cubiertas:** Inicialización de 4 variables del subflow.
**Nota para el desarrollador:** [StrLogRuta] es una variable estática — configerar como variable global. [StrEstadoProceso] es dinámica — se llena leyendo el log en el Prompt 2.

---

### Prompt 2 — Leer estado del log | ~384 chars

```
Iniciar Excel con [StrLogRuta]. Obtener la primera fila libre de la hoja 'Log' para determinar la última fila con datos. Leer la celda de la columna 'Estado' de la última fila y guardar en [StrEstadoProceso]. Cerrar Excel sin guardar cambios.
```

**Acciones cubiertas:** Apertura de log Excel, lectura de última fila, cierre.
**Nota para el desarrollador:** Ajustar el nombre de la hoja 'Log' y el nombre de la columna 'Estado' según los encabezados reales del Log_FCM.xlsx generado en REQ_01.

---

### Prompt 3 — Construir cuerpo del correo | ~498 chars

```
Si [StrEstadoProceso] es igual a 'Éxito': asignar [StrCuerpoCorreo] con valor 'El proceso FCM.001 finalizó correctamente. Archivo de conciliación disponible en la ruta configurada. Fecha de proceso: ' concatenado con la fecha actual. Si [StrEstadoProceso] contiene 'Error': asignar [StrCuerpoCorreo] con valor 'El proceso FCM.001 finalizó con errores. Detalle: ' concatenado con [StrEstadoProceso] y ' — Revisar el log para más información.'.
```

**Acciones cubiertas:** Lógica condicional por estado, construcción del cuerpo del correo.
**Nota para el desarrollador:** El texto del cuerpo es un template base — el cliente puede solicitar ajustes de redacción.

---

### Prompt 4 — Enviar correo de notificación (borrador) | ~468 chars

```
Usar la acción Enviar correo electrónico a través de Outlook con destinatarios soporte@empresa.com y responsable@empresa.com, asunto 'FCM.001 — Resultado Conciliación ' concatenado con la fecha actual en formato DD/MM/YYYY, cuerpo [StrCuerpoCorreo]. Guardar como borrador para revisión humana antes de enviar. Si [StrEstadoProceso] es igual a 'Éxito': adjuntar el archivo [rutaArchivo\aqui\va\la\ruta\Conciliacion_FCM.xlsx].
```

**Acciones cubiertas:** Creación de borrador de correo, adjunto condicional del archivo de conciliación.
**Nota para el desarrollador:** Según política Beecker, el correo debe guardarse como borrador. Reemplazar soporte@empresa.com y responsable@empresa.com con los correos reales. Los destinatarios deben parametrizarse.

---

### Prompt 5 — Log y cierre | ~289 chars

```
Si [StrEstadoProceso] está vacío: asignar [StrEstadoProceso] con valor 'Error — Log no disponible'. Abrir Excel [StrLogRuta]. Escribir en nueva fila: fecha actual, [StrModulo], 'REQ_02 — Notificación de resultado', [StrEstadoProceso]. Guardar y cerrar.
```

**Acciones cubiertas:** Manejo de log vacío, registro en log.
**Nota para el desarrollador:** Si el Log_FCM.xlsx no existe (excepción del PDD), este prompt fallará — el bloque de errores del Prompt 4 debe capturar ese caso.

**Pasos manuales requeridos para REQ_02:**
- Crear el subflow `NotificacionResultado` manualmente.
- Reemplazar los correos destinatarios (soporte@empresa.com, responsable@empresa.com) con los correos reales y parametrizarlos.
- Ajustar el nombre de la hoja y columna del log según los encabezados reales de Log_FCM.xlsx.

---

## Resumen de cobertura

| REQ | Nombre | Prompts | Estado |
|-----|--------|---------|--------|
| REQ_01 | Descarga y procesamiento de extracto bancario | 5 (incl. 2b) | Generado ✓ |
| REQ_02 | Notificación de resultado del proceso | 5 | Generado ✓ |

**Pasos manuales globales del proyecto FCM.001:**
- Crear ambos subflows manualmente antes de iniciar la generación con Copilot.
- Configurar las rutas de archivos (extracto, conciliación, log) como variables globales en el flow principal.
- Configurar los correos destinatarios como variables globales o parámetros.
- Primera ejecución: crear manualmente los encabezados de Conciliación_FCM.xlsx y Log_FCM.xlsx.

> **Gap advertido en REQ_01:** La ruta de la carpeta de red no está especificada en el PDD.
> Se usaron placeholders `[rutaArchivo\aqui\va\la\ruta\...]`. Confirmar con el cliente antes de ejecutar.
