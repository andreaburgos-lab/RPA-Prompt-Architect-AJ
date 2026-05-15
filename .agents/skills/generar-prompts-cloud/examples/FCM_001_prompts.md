# Prompts — FCM_001 — Power Automate Cloud

**Proyecto:** FCM.001 — Automatización de conciliación bancaria
**Cliente:** Empresa Ejemplo S.A.
**Versión PDD:** 1.2
**Tecnología:** Power Automate Cloud Flow (Copilot Cloud — límite 2000 chars/prompt)
**Generado:** 2025-04-10

---

## REQ_01 — Descarga y procesamiento de extracto bancario

> **Instrucción previa Prompt 1:** Pegar en el campo **'Crear tu automatización con Copilot'**
> en make.powerautomate.com > + Crear > Con Copilot.
> Agregar descripción al flujo: REQ_01 FCM.001 — Descarga y procesamiento de extracto bancario.

---

### Prompt 1 — Trigger | ~196 chars

```
Crear un Cloud Flow automatizado con el trigger Cuando llega un nuevo correo electrónico (V3) del conector Office 365 Outlook, filtrado por asunto que contenga 'Extracto Banco'.
```

**Acciones cubiertas:** Trigger del flujo — Office 365 Outlook (V3).
**Nota para el desarrollador:** Configurar el filtro de asunto en el panel de diseño después de generar (el trigger se genera sin filtros; agregarlos manualmente en la propiedad 'Filtro de asunto' del trigger). Si el trigger debe activarse solo para remitentes específicos, agregar también el filtro 'De'.

---

### Prompt 2 — Inicializar variables | ~487 chars

> **Instrucción previa:** Pegar en el panel Copilot dentro del diseñador, después de confirmar el trigger.

```
Agregar la acción Inicializar variable 5 veces usando ramas paralelas: la primera llamada StrModulo de tipo texto con valor 'REQ01_DescargaExtractoBancario', la segunda llamada StrEstadoEjecucion de tipo texto con valor vacío, la tercera llamada StrNombreAdjunto de tipo texto con valor vacío, la cuarta llamada BlnAdjuntoValido de tipo booleano con valor false, la quinta llamada ArrAdjuntos de tipo array con valor vacío.
```

**Acciones cubiertas:** Inicialización de 5 variables en ramas paralelas.
**Nota para el desarrollador:** Máximo 5 ramas paralelas por Beecker. StrNombreAdjunto y ArrAdjuntos son dinámicas — se llenan al obtener adjuntos del correo trigger. StrModulo es estática.

---

### Prompt 3 — Obtener adjuntos del correo | ~398 chars

> **Instrucción previa:** Pegar en el panel Copilot dentro del diseñador.

```
Agregar la acción Obtener adjuntos (V2) del conector Office 365 Outlook usando el Id de mensaje del trigger. Guardar el resultado en la variable ArrAdjuntos. Agregar la acción Aplicar a cada uno para iterar sobre ArrAdjuntos. Dentro del bucle: agregar Establecer variable para guardar el nombre del adjunto actual en StrNombreAdjunto.
```

**Acciones cubiertas:** Obtención de adjuntos, iteración Apply to each, extracción de nombre.
**Nota para el desarrollador:** Verificar que el campo 'Id de mensaje' del trigger está disponible como contenido dinámico en el diseñador. Si el correo tiene múltiples adjuntos, el bucle procesará todos — agregar una condición dentro del bucle si solo se debe procesar el .xlsx.

---

### Prompt 4 — Validar adjunto y subir a SharePoint | ~612 chars

> **Instrucción previa:** Pegar dentro del bucle 'Aplicar a cada uno' del Prompt 3.

```
Agregar la acción Condición renombrada como 'ValidarExtensionAdjunto' que verifique si StrNombreAdjunto termina con '.xlsx'. En la rama Verdadero: agregar la acción Establecer variable para asignar BlnAdjuntoValido con valor true. Agregar la acción Crear archivo del conector SharePoint apuntando al sitio https://empresa.sharepoint.com/sites/Finanzas, carpeta '/Extractos', nombre de archivo StrNombreAdjunto, contenido del archivo con el contenido del adjunto actual del bucle.
```

**Acciones cubiertas:** Validación de extensión .xlsx, subida del adjunto a SharePoint.
**Nota para el desarrollador:** Reemplazar 'https://empresa.sharepoint.com/sites/Finanzas' con la URL real del sitio SharePoint. La carpeta '/Extractos' debe existir previamente. En la rama Falso de la condición, agregar una acción de log para registrar que el adjunto no era un .xlsx.

---

### Prompt 5 — Leer extracto y filtrar pendientes | ~798 chars

> **Instrucción previa:** Pegar después del bucle 'Aplicar a cada uno', fuera del scope del trigger.

```
Agregar la acción Listar las filas presentes en una tabla del conector Excel Online (Business). Seleccionar ubicación SharePoint, sitio https://empresa.sharepoint.com/sites/Finanzas, archivo StrNombreAdjunto, tabla NombreTablaExtracto. Guardar el resultado en la variable ArrFilasExtracto. Agregar la acción Aplicar a cada uno para iterar sobre ArrFilasExtracto. Dentro del bucle: agregar Condición que verifique si el campo Estado de la fila actual es igual a 'Pendiente'. En la rama Verdadero: agregar la acción Agregar una fila a una tabla del conector Excel Online (Business) en el archivo Conciliacion_FCM.xlsx, tabla TablaConciliacion.
```

**Acciones cubiertas:** Lectura de tabla Excel Online, iteración, filtro por Estado = Pendiente, escritura en tabla de conciliación.
**Nota para el desarrollador:** Reemplazar 'NombreTablaExtracto' y 'TablaConciliacion' con los nombres reales de las tablas. El archivo Conciliacion_FCM.xlsx debe existir previamente en SharePoint con la tabla creada. Mapear las columnas del extracto a las columnas de la conciliación en la acción 'Agregar una fila a una tabla'.

---

### Prompt 6 — Manejo de errores | ~698 chars

> **Instrucción previa:** Pegar para agregar un ámbito que envuelva los Prompts 3 al 5.

```
Agregar la acción Ámbito renombrada como 'REQ01_ProcesoPrincipal' para encapsular las acciones de obtención de adjuntos, validación y procesamiento. Agregar rama paralela después del Ámbito. En la rama paralela, agregar la acción Condición configurada con Ejecutar después de — marcar 'Ha producido un error'. En la rama Verdadero: agregar Establecer variable para asignar StrEstadoEjecucion con valor 'Error'. Agregar Crear borrador (V2) del conector Office 365 Outlook con Para soporte@empresa.com, Asunto 'FCM.001 Error REQ_01 — Descarga extracto bancario', Cuerpo 'Error en el procesamiento del extracto bancario. Revisar los registros de ejecución del flujo.'. Agregar Terminar configurada como Fallido.
```

**Acciones cubiertas:** Ámbito de error con RunAfter, borrador de correo de error, Terminar fallido.
**Nota para el desarrollador:** Configurar 'Ejecutar después de' (Configure run after) en la condición de la rama paralela — marcar únicamente 'Ha producido un error'. Reemplazar soporte@empresa.com con el correo real.

**Pasos manuales requeridos para REQ_01:**
- Configurar el filtro de asunto del trigger manualmente en el panel de diseño.
- Crear el archivo Conciliacion_FCM.xlsx en SharePoint con la tabla TablaConciliacion antes de ejecutar.
- Mapear las columnas del extracto a las de la conciliación en el Prompt 5.
- Reemplazar todas las URLs de SharePoint y correos con los valores reales.
- Configurar 'Ejecutar después de' en el manejo de errores del Prompt 6.

---

## REQ_02 — Notificación de resultado del proceso

> **Instrucción previa Prompt 1:** Crear un nuevo Cloud Flow o agregar como un flujo separado
> que se active después del REQ_01. Pegar en el campo 'Crear tu automatización con Copilot'.

---

### Prompt 1 — Trigger programado | ~182 chars

```
Crear un Cloud Flow automatizado con el trigger Periodicidad configurado para ejecutarse diariamente a las 08:00 AM, para enviar la notificación del resultado de la conciliación.
```

**Acciones cubiertas:** Trigger de recurrencia diaria.
**Nota para el desarrollador:** Configurar la hora de ejecución (08:00 AM) y la zona horaria en las propiedades del trigger Periodicidad en el panel de diseño.

---

### Prompt 2 — Inicializar variables | ~387 chars

> **Instrucción previa:** Pegar en el panel Copilot dentro del diseñador.

```
Agregar la acción Inicializar variable 3 veces usando ramas paralelas: la primera llamada StrModulo de tipo texto con valor 'REQ02_NotificacionResultado', la segunda llamada StrEstadoProceso de tipo texto con valor vacío, la tercera llamada StrCuerpoCorreo de tipo texto con valor vacío.
```

**Acciones cubiertas:** Inicialización de 3 variables.
**Nota para el desarrollador:** StrEstadoProceso y StrCuerpoCorreo son dinámicas — se llenan en los prompts siguientes al leer el log de SharePoint.

---

### Prompt 3 — Leer estado del log en SharePoint | ~487 chars

> **Instrucción previa:** Pegar en el panel Copilot dentro del diseñador.

```
Agregar la acción Obtener elementos del conector SharePoint en el sitio https://empresa.sharepoint.com/sites/Finanzas, lista 'LogProcesos'. Ordenar por columna Fecha descendente y limitar a 1 elemento. Guardar el resultado en ArrUltimoLog. Agregar Aplicar a cada uno sobre ArrUltimoLog. Dentro: Establecer variable StrEstadoProceso con el valor de la columna Estado del elemento actual.
```

**Acciones cubiertas:** Obtención del último registro de log desde lista SharePoint.
**Nota para el desarrollador:** Reemplazar 'LogProcesos' con el nombre real de la lista de SharePoint usada como log. Si el log es un archivo Excel en SharePoint, usar 'Listar las filas presentes en una tabla' y filtrar por fecha.

---

### Prompt 4 — Construir cuerpo y enviar borrador | ~623 chars

> **Instrucción previa:** Pegar después del bloque de lectura de log.

```
Agregar la acción Condición renombrada como 'EvaluarEstadoProceso' que verifique si StrEstadoProceso es igual a 'Éxito'. En la rama Verdadero: agregar Establecer variable para asignar StrCuerpoCorreo con 'El proceso FCM.001 finalizó correctamente. Archivo de conciliación disponible. Fecha: ' concatenado con la fecha actual en formato dd/MM/yyyy. En la rama Falso: asignar StrCuerpoCorreo con 'El proceso FCM.001 finalizó con errores. Detalle: ' concatenado con StrEstadoProceso. Agregar Crear borrador (V2) del conector Office 365 Outlook con Para soporte@empresa.com, Asunto 'FCM.001 — Resultado Conciliación ' concatenado con fecha actual, Cuerpo StrCuerpoCorreo.
```

**Acciones cubiertas:** Condición por estado, construcción del cuerpo del correo, creación de borrador.
**Nota para el desarrollador:** Según política Beecker, usar 'Crear borrador (V2)' — no enviar automáticamente. Agregar el destinatario responsable@empresa.com en el campo Para. Si el estado es Éxito, agregar el archivo Conciliacion_FCM.xlsx como adjunto usando 'Obtener contenido del archivo' de SharePoint + adjuntar.

**Pasos manuales requeridos para REQ_02:**
- Confirmar el nombre de la lista de SharePoint usada como log (actualmente: 'LogProcesos').
- Configurar la hora de ejecución del trigger Periodicidad.
- Reemplazar los correos destinatarios con los valores reales.
- Agregar el adjunto de conciliación manualmente si se requiere (el Prompt 4 solo crea el borrador del cuerpo).

---

## Resumen de cobertura

| REQ | Nombre | Prompts | Estado |
|-----|--------|---------|--------|
| REQ_01 | Descarga y procesamiento de extracto bancario | 6 | Generado ✓ |
| REQ_02 | Notificación de resultado del proceso | 4 | Generado ✓ |

**Pasos manuales globales del proyecto FCM.001 — Cloud:**
- Crear el archivo Conciliacion_FCM.xlsx con la tabla TablaConciliacion en SharePoint antes de ejecutar.
- Configurar las conexiones de los conectores Office 365 Outlook y SharePoint con la cuenta correcta.
- Reemplazar todas las URLs de SharePoint (https://empresa.sharepoint.com/sites/Finanzas) con las reales.
- Reemplazar todos los correos placeholder con los correos reales de los responsables.
- Configurar 'Ejecutar después de' (Configure run after) en el manejo de errores del REQ_01 Prompt 6.

> **Gap advertido en REQ_01:** La ruta exacta de la carpeta SharePoint no está especificada en el PDD. Se usó '/Extractos' como placeholder. Confirmar con el cliente antes de ejecutar.
