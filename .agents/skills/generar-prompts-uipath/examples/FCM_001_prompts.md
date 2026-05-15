# Prompts — FCM_001 — UiPath Autopilot

**Proyecto:** FCM.001 — Automatización de conciliación bancaria
**Cliente:** Empresa Ejemplo S.A.
**Versión PDD:** 1.2
**Tecnología:** UiPath Autopilot — Studio Desktop
**Límite de caracteres:** 300 chars (Text-to-Workflow) / 256 chars (Expression Editor)
**Generado:** 2025-04-10

## Prerrequisitos globales del proyecto
- **Object Repository:** No aplica para este proyecto (sin UI Automation)
- **Assets de Orchestrator:** `FCM_Credential` (tipo: Credential, carpeta: Production) — si aplica
- **Queues de Orchestrator:** No aplica
- **Paquetes NuGet:** `UiPath.Excel.Activities`, `UiPath.Mail.Activities`, `UiPath.System.Activities`
- **Rutas locales:** `C:\RPA\FCM001\Extracto Bancario Mensual.xlsx`, `C:\RPA\FCM001\Conciliacion_FCM.xlsx`

---

## REQ_01 — Descarga y procesamiento de extracto bancario

> **Instrucción previa:**
> 0. GUARDAR EL PROYECTO (Ctrl+S) antes de usar Autopilot.
> 1. Abrir o crear el archivo XAML `DescargaExtractoBancario.xaml`.
> 2. Agregar Sequence vacía al canvas. Clic derecho > Add Annotation.
> 3. Activar la anotación y pegar el prompt. Hacer clic en Generate.
> 4. Prerrequisitos: paquetes UiPath.Excel.Activities y UiPath.Mail.Activities instalados.

---

### Prompt 1 — Variables e inicialización | ~293 chars

```
Create string 'str_ExtractoPath' value 'C:\RPA\FCM001\Extracto Bancario Mensual.xlsx'. Create string 'str_ConciliPath' value 'C:\RPA\FCM001\Conciliacion_FCM.xlsx'. Create string 'str_Status' empty. Create string 'str_Module' value 'DescargaExtractoBancario'. Create DataTable 'dt_Extracto'. Log Message Info 'Starting DescargaExtractoBancario'.
```

**Actividades cubiertas:** Assign str_ExtractoPath, Assign str_ConciliPath, Assign str_Status, Assign str_Module, Assign dt_Extracto, Log Message.
**Nota para el desarrollador:** En producción, las rutas deben obtenerse de Assets de Orchestrator. Guardar el proyecto (Ctrl+S) antes de ejecutar el siguiente prompt.

---

### Prompt 2 — Obtener correos con extracto | ~290 chars

```
Get Mail Messages from Outlook using UiPath.Mail.Activities. Filter subject contains 'Extracto Banco' received in last 7 days. Store messages in 'lst_Correos'. If 'lst_Correos' is empty log Error 'No email found with extracto bancario subject'. Else save attachments of first email to folder 'C:\RPA\FCM001\'.
```

**Actividades cubiertas:** Get Mail Messages, If condition, Save Attachments.
**Nota para el desarrollador:** El filtro 'received in last 7 days' puede requerir ajuste manual de la propiedad 'ReceivedDate' en la actividad Get Mail Messages. Verificar que el adjunto descargado corresponde a 'Extracto Bancario Mensual.xlsx'.

---

### Prompt 3 — Leer Excel y filtrar pendientes | ~299 chars

```
Open Excel 'str_ExtractoPath' using UiPath.Excel.Activities. Read Range from sheet 'Movimientos' store in 'dt_Extracto'. Close Excel. For Each row in 'dt_Extracto': If row column 'Estado' equals 'Pendiente': Assign 'str_Status' = 'Processing row'.
```

**Actividades cubiertas:** Excel Application Scope, Read Range, Close, For Each Row, If condition.
**Nota para el desarrollador:** Reemplazar 'Movimientos' con el nombre exacto de la hoja. Dentro del For Each se ejecuta el Prompt 4 para escribir cada fila pendiente.

---

### Prompt 4 — Escribir fila pendiente en conciliación | ~297 chars

```
Open Excel 'str_ConciliPath' using UiPath.Excel.Activities. Find first empty row in sheet 'Conciliacion'. Write current row data to that empty row. Save and close Excel 'str_ConciliPath'.
```

**Actividades cubiertas:** Excel Application Scope, Find First Empty Row, Write Row, Save, Close.
**Nota para el desarrollador:** Este prompt se ejecuta DENTRO del For Each del Prompt 3, en el bloque de la rama Verdadero de la condición Estado = 'Pendiente'. Verificar que las columnas del extracto coinciden con las de Conciliacion_FCM.xlsx.

---

### Prompt 5 — Manejo de errores | ~298 chars

```
Add Try Catch around previous activities. In Catch Exception: Assign 'str_Status' = 'Error: ' + exception.Message. Log Message Error 'DescargaExtractoBancario failed: ' + exception.Message. Send email using UiPath.Mail.Activities To 'soporte@empresa.com' Subject 'FCM.001 Error REQ_01' Body 'str_Status'.
```

**Actividades cubiertas:** Try Catch, Assign str_Status error, Log Message Error, Send Mail.
**Nota para el desarrollador:** Según política Beecker, si el correo tiene información sensible, guardar como borrador. Reemplazar soporte@empresa.com con el correo real. En producción, el destinatario debe ser un Asset de Orchestrator.

---

### Prompt 6 — Log y cierre | ~284 chars

```
If 'str_Status' is empty Assign 'str_Status' = 'Success'. Log Message Info 'DescargaExtractoBancario completed: ' + 'str_Status'. Open Excel 'C:\RPA\FCM001\Log_FCM.xlsx' using UiPath.Excel.Activities. Write row DateTime.Now, 'str_Module', 'REQ_01', 'str_Status'. Close Excel.
```

**Actividades cubiertas:** Assign str_Status Success, Log Message Info, Excel log write.
**Nota para el desarrollador:** La ruta del log debe configurarse como argumento In del Main.xaml. Columnas del log: Fecha, Módulo, REQ, Estado.

**Pasos manuales requeridos para REQ_01:**
- Configurar el filtro de fecha de correos manualmente en la actividad Get Mail Messages (propiedad ReceivedDate).
- Verificar que 'Extracto Bancario Mensual.xlsx' es el nombre exacto del adjunto esperado.
- Confirmar el nombre de hoja 'Movimientos' con el cliente.
- El Prompt 4 debe ejecutarse dentro del bloque For Each del Prompt 3 — posicionar correctamente en el canvas.

---

## REQ_02 — Notificación de resultado del proceso

> **Instrucción previa:**
> 0. GUARDAR EL PROYECTO (Ctrl+S).
> 1. Abrir o crear el archivo XAML `NotificacionResultado.xaml`.
> 2. Agregar Sequence vacía. Clic derecho > Add Annotation.

---

### Prompt 1 — Variables e inicialización | ~278 chars

```
Create string 'str_LogPath' value 'C:\RPA\FCM001\Log_FCM.xlsx'. Create string 'str_EstadoProceso' empty. Create string 'str_Module' value 'NotificacionResultado'. Create string 'str_CuerpoCorreo' empty. Log Message Info 'Starting NotificacionResultado'.
```

**Actividades cubiertas:** Assign str_LogPath, Assign str_EstadoProceso, Assign str_Module, Assign str_CuerpoCorreo, Log Message.
**Nota para el desarrollador:** str_LogPath debe venir de un Asset de Orchestrator en producción. str_EstadoProceso es dinámica — se llena en el Prompt 2.

---

### Prompt 2 — Leer estado del log | ~267 chars

```
Open Excel 'str_LogPath' using UiPath.Excel.Activities. Read Range from sheet 'Log' store in 'dt_Log'. Close Excel. Assign 'str_EstadoProceso' = dt_Log.Rows(dt_Log.Rows.Count - 1)("Estado").ToString.
```

**Actividades cubiertas:** Excel Application Scope, Read Range, Close, Assign última fila columna Estado.
**Nota para el desarrollador:** La expresión `dt_Log.Rows(dt_Log.Rows.Count - 1)("Estado")` obtiene el valor de la última fila. Ajustar el nombre de la columna "Estado" según los encabezados reales del log.

---

### Prompt 3 — Construir y enviar correo (borrador) | ~299 chars

```
If 'str_EstadoProceso' equals 'Success': Assign 'str_CuerpoCorreo' = 'FCM.001 completed OK. Date: ' + DateTime.Now.ToString("dd/MM/yyyy"). Else Assign 'str_CuerpoCorreo' = 'FCM.001 error: ' + 'str_EstadoProceso'. Send email using UiPath.Mail.Activities To 'soporte@empresa.com' Subject 'FCM.001 Resultado ' + DateTime.Now.ToString("dd/MM/yyyy") Body 'str_CuerpoCorreo'.
```

**Actividades cubiertas:** If condition, Assign str_CuerpoCorreo, Send Mail.
**Nota para el desarrollador:** Según política Beecker, guardar como borrador si el correo tiene información sensible. Agregar el destinatario responsable@empresa.com. Si str_EstadoProceso = 'Success', adjuntar Conciliacion_FCM.xlsx usando la actividad Attach File.

**Pasos manuales requeridos para REQ_02:**
- Ajustar el nombre de la columna "Estado" en el Prompt 2 según los encabezados reales de Log_FCM.xlsx.
- Configurar en producción: str_LogPath como Asset de Orchestrator.
- Agregar attachment de Conciliacion_FCM.xlsx manualmente si se requiere para el estado Éxito.
- Reemplazar correos placeholder con los reales.

---

## Resumen de cobertura

| REQ | Nombre | Prompts | Plataforma | Estado |
|-----|--------|---------|------------|--------|
| REQ_01 | Descarga y procesamiento de extracto bancario | 6 | Studio Desktop | Generado ✓ |
| REQ_02 | Notificación de resultado del proceso | 3 | Studio Desktop | Generado ✓ |

**Pasos manuales globales del proyecto FCM.001 — UiPath:**
- Instalar los paquetes NuGet: UiPath.Excel.Activities, UiPath.Mail.Activities, UiPath.System.Activities.
- Configurar en producción: rutas de archivos y correos como Assets de Orchestrator.
- Guardar el proyecto (Ctrl+S) antes de cada uso de Autopilot para que detecte las variables.
- Variables entre comillas simples en cada prompt para que Autopilot las reconozca.

> **Gap advertido en REQ_01:** La ruta exacta de la carpeta de destino del extracto no está especificada en el PDD. Se usó `C:\RPA\FCM001\` como placeholder. Confirmar con el cliente antes de ejecutar.
