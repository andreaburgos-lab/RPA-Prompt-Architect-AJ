# Prompts — FCM_001 — Automation Anywhere A360

**Proyecto:** FCM.001 — Automatización de conciliación bancaria
**Cliente:** Empresa Ejemplo S.A.
**Versión PDD:** 1.2
**Tecnología:** Automation Anywhere A360 (Copilot AA — límite 450 chars/prompt)
**Generado:** 2025-04-10

---

## REQ_01 — Descarga y procesamiento de extracto bancario

---

### Prompt 1 — Inicialización de variables (Parte 1 de 2) | ~437 chars

> **Prompt para Copilot:**

```
Crea un Step llamado 'REQ01_DescargaExtractoBancario'. DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', usa String: Assign para inicializar strExtractoRuta con valor 'C:\RPA\FCM001\Extracto Bancario Mensual.xlsx'. DENTRO del mismo Step, usa String: Assign para inicializar strConciliRuta con valor 'C:\RPA\FCM001\Conciliacion_FCM.xlsx'. DENTRO del mismo Step, usa String: Assign para inicializar strEstado con valor vacío ''.
```

**Nota de Arquitectura:** Inicialización de variables de ruta estáticas. En producción, obtener strExtractoRuta y strConciliRuta del dictConfig para evitar hardcode. Invocar AddToLog al inicio del Step con strModulo = 'REQ01_DescargaExtractoBancario'.

---

### Prompt 1b — Inicialización de variables (Parte 2 de 2) | ~398 chars

```
DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', usa String: Assign para inicializar strModulo con valor 'REQ01_DescargaExtractoBancario'. DENTRO del mismo Step, usa String: Assign para inicializar strFiltroAsunto con valor 'Extracto Banco'. DENTRO del mismo Step, usa String: Assign para inicializar strNombreAdjunto con valor vacío ''.
```

**Nota de Arquitectura:** Prompt dividido por límite de 450 chars. strFiltroAsunto es estática. strNombreAdjunto es dinámica — se llena al obtener el adjunto del correo.

---

### Prompt 2 — Obtener correo y descargar adjunto | ~443 chars

```
DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', usa Email: Get All Messages filtrando por asunto que contenga strFiltroAsunto y recibidos en los últimos 7 días, guardar en lstCorreos SIN crear variables de captura. DENTRO del mismo Step, usa Email: Save Attachments del primer elemento de lstCorreos en la carpeta 'C:\RPA\FCM001\'. DENTRO del mismo Step, usa String: Assign para asignar strNombreAdjunto con valor 'Extracto Bancario Mensual.xlsx'.
```

**Nota de Arquitectura:** Uso del paquete Email para obtener correos filtrados. Se descarga el adjunto del primer correo que cumpla el filtro. Si se esperan múltiples correos, agregar un loop For Each sobre lstCorreos.

---

### Prompt 3 — Leer Excel y filtrar filas pendientes | ~447 chars

```
DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', usa Excel Advanced: Open para abrir strExtractoRuta con sesión sessExtracto. SIN crear variables de captura. DENTRO del mismo Step, usa Excel Advanced: Read From Range para leer desde A1 hasta la última fila de la hoja 'Movimientos' y guardar en dtExtracto. DENTRO del mismo Step, usa DataTable: Filter sobre dtExtracto con condición que la columna Estado sea igual a 'Pendiente' guardando en dtPendientes.
```

**Nota de Arquitectura:** Uso de Excel Advanced (prohibido Excel Basic). DataTable: Filter evita iterar para búsqueda simple. Reemplazar 'Movimientos' con el nombre real de la hoja una vez confirmado.

---

### Prompt 4 — Escribir filas en conciliación | ~432 chars

```
DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', agrega un loop For Each sobre dtPendientes. DENTRO del loop, usa Excel Advanced: Open para abrir strConciliRuta con sesión sessConcili. SIN crear variables de captura. Usa Excel Advanced: Get Rows Count de sessConcili para obtener numUltimaFila. Usa Excel Advanced: Write To Range para escribir la fila actual de dtPendientes en la posición numUltimaFila + 1. Usa Excel Advanced: Close para cerrar sessConcili guardando cambios.
```

**Nota de Arquitectura:** Se abre y cierra el archivo de conciliación dentro del loop para garantizar que cada fila se escriba correctamente. Si el volumen de filas es grande (>100), considerar acumular en dtSalida y escribir en una sola operación fuera del loop.

---

### Prompt 5 — Excepción: sin correo con extracto | ~378 chars

```
DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', usa ErrorHandler: Try-Catch para envolver las acciones de Email: Get All Messages. En el bloque Catch, usa ErrorHandler: Throw con tipo Business y mensaje 'BUSINESS: No se encontró correo con asunto Extracto Banco en los últimos 7 días'. Usa Email: Send para notificar a soporte@empresa.com con asunto 'FCM.001 — Sin extracto bancario'.
```

**Nota de Arquitectura:** Excepción de negocio (condición esperada, no error técnico) — mensaje con prefijo 'BUSINESS:'. El correo de notificación debe usar el correo configurado en dictConfig, no hardcodeado.

---

### Prompt 6 — Log y cierre | ~362 chars

```
DENTRO del mismo Step 'REQ01_DescargaExtractoBancario', usa Excel Advanced: Close para cerrar sessExtracto guardando cambios. Si strEstado está vacío: usa String: Assign para asignar strEstado con valor 'Éxito'. Invoca el taskbot reusable AddToLog con strModulo, strEstado y mensaje 'REQ01_DescargaExtractoBancario finalizado'.
```

**Nota de Arquitectura:** Cierre de sesiones Excel antes de finalizar. Invocación de AddToLog al final del Step — convención obligatoria del BeeFramework.

**Desarrollador:** Insertar llamada a Taskbot hijo AddToLog aquí con los parámetros (strModulo, strEstado, 'REQ01_DescargaExtractoBancario finalizado').

**Pasos manuales requeridos para REQ_01:**
- Confirmar el nombre de la hoja del extracto ('Movimientos') con el cliente antes de ejecutar.
- Configurar dictConfig con las rutas de archivo (strExtractoRuta, strConciliRuta) y el correo de soporte.
- Verificar que el TaskBot AddToLog existe en el Control Room antes de ejecutar.
- Si el volumen de filas es alto, optimizar el Prompt 4 para escritura masiva fuera del loop.

---

## REQ_02 — Notificación de resultado del proceso

---

### Prompt 1 — Inicialización de variables | ~388 chars

> **Prompt para Copilot:**

```
Crea un Step llamado 'REQ02_NotificacionResultado'. DENTRO del mismo Step 'REQ02_NotificacionResultado', usa String: Assign para inicializar strLogRuta con valor 'C:\RPA\FCM001\Log_FCM.xlsx'. DENTRO del mismo Step, usa String: Assign para inicializar strModulo con valor 'REQ02_NotificacionResultado'. DENTRO del mismo Step, usa String: Assign para inicializar strEstadoProceso con valor vacío ''.
```

**Nota de Arquitectura:** strLogRuta es estática — debe venir de dictConfig en producción. strEstadoProceso es dinámica — se llena al leer el log en el Prompt 2.

---

### Prompt 2 — Leer estado del log | ~426 chars

```
DENTRO del mismo Step 'REQ02_NotificacionResultado', usa Excel Advanced: Open para abrir strLogRuta con sesión sessLog. SIN crear variables de captura. Usa Excel Advanced: Get Rows Count de sessLog para obtener numTotalFilas. Usa Excel Advanced: Read From Cell para leer la celda de la columna Estado en la fila numTotalFilas y guardar en strEstadoProceso. Usa Excel Advanced: Close para cerrar sessLog sin guardar.
```

**Nota de Arquitectura:** Lee únicamente la última fila del log. Si la estructura del log tiene encabezado en fila 1, el índice real de la última fila de datos es numTotalFilas (no numTotalFilas - 1 si Get Rows Count ya excluye el encabezado).

---

### Prompt 3 — Construir cuerpo y enviar notificación | ~449 chars

```
DENTRO del mismo Step 'REQ02_NotificacionResultado', usa String: Assign para asignar strCuerpoCorreo: si strEstadoProceso es igual a 'Éxito' asignar 'El proceso FCM.001 finalizó correctamente. Fecha: ' + fechaActual. Si no: asignar 'FCM.001 finalizó con errores. Detalle: ' + strEstadoProceso. Usa Email: Send para enviar a soporte@empresa.com con asunto 'FCM.001 — Resultado Conciliación ' + fechaActual, cuerpo strCuerpoCorreo.
```

**Nota de Arquitectura:** El correo de notificación se envía directamente (no es información sensible — es una notificación operativa). Si el proceso fue Éxito, agregar Email adjuntando strConciliRuta antes de enviar. Los destinatarios deben estar en dictConfig.

**Desarrollador:** Insertar llamada a Taskbot hijo AddToLog aquí con los parámetros (strModulo, strEstadoProceso, 'REQ02_NotificacionResultado finalizado').

**Pasos manuales requeridos para REQ_02:**
- Configurar dictConfig con strLogRuta y los correos destinatarios.
- Verificar el nombre de la columna 'Estado' en el log para alinear con lo que escribe REQ_01.
- Si el proceso fue Éxito, agregar attachment de Conciliacion_FCM.xlsx al correo (ver Prompt 3).

---

## Resumen de cobertura

| REQ | Nombre | Prompts | Estado |
|-----|--------|---------|--------|
| REQ_01 | Descarga y procesamiento de extracto bancario | 6 (incl. 1b) | Generado ✓ |
| REQ_02 | Notificación de resultado del proceso | 3 | Generado ✓ |

**Pasos manuales globales del proyecto FCM.001 — AA A360:**
- Crear el TaskBot AddToLog en el Control Room del proyecto (convención obligatoria BeeFramework).
- Configurar dictConfig con todas las variables estáticas: rutas, correos, credenciales.
- Todos los prompts se ejecutan dentro del mismo Bot Task; los Steps son unidades lógicas dentro del Task.
- Límite crítico de 450 chars por prompt — si se supera, dividir en Parte 1 / Parte 2 como en REQ_01 Prompt 1.

> **Gap advertido en REQ_01:** La ruta exacta de la carpeta de destino no está especificada en el PDD. Se usó `C:\RPA\FCM001\` como placeholder. Confirmar con el cliente antes de ejecutar.
