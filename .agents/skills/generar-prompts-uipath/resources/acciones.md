# Acciones soportadas — UiPath Studio / Autopilot / Studio Web

> Guía extendida y robustecida de actividades UiPath, librerías NuGet, paquetes oficiales, actividades modernas y mejores prácticas.
>
> Fuente principal: documentación oficial de UiPath Activities y paquetes oficiales.
>
> Compatible con:
> - UiPath Studio Desktop
> - UiPath Studio Web
> - Windows / Cross-platform
> - REFramework
> - Autopilot for Everyone / Studio
>
> Última actualización: Mayo 2026

---

# Índice

1. Arquitectura de paquetes UiPath
2. Paquetes base obligatorios
3. UiPath.System.Activities
4. UiPath.UIAutomation.Activities
5. UiPath.Excel.Activities
6. UiPath.Mail.Activities
7. UiPath.WebAPI.Activities
8. UiPath.Orchestrator.Activities
9. UiPath.PDF.Activities
10. UiPath.Word.Activities
11. UiPath.IntelligentOCR.Activities
12. UiPath.DocumentUnderstanding.Activities
13. UiPath.Database.Activities
14. UiPath.Terminal.Activities
15. UiPath.Cryptography.Activities
16. UiPath.Persistence.Activities
17. UiPath.Testing.Activities
18. Actividades modernas vs clásicas
19. Actividades recomendadas por escenario
20. Actividades parcialmente soportadas por Autopilot
21. Actividades NO soportadas por Autopilot
22. Buenas prácticas profesionales
23. Convenciones recomendadas
24. Recomendaciones REFramework
25. Errores comunes
26. Cheatsheet rápida

---

# 1. Arquitectura de paquetes UiPath

## Paquetes principales oficiales

| Paquete | Propósito | Obligatorio |
|---|---|---|
| UiPath.System.Activities | Actividades base del workflow | Sí |
| UiPath.UIAutomation.Activities | Automatización UI/Web/Desktop | Sí |
| UiPath.Excel.Activities | Excel y hojas de cálculo | Muy común |
| UiPath.Mail.Activities | Correo electrónico | Muy común |
| UiPath.WebAPI.Activities | APIs REST/SOAP | Común |
| UiPath.Orchestrator.Activities | Assets, Queues, Storage Buckets | Empresarial |
| UiPath.PDF.Activities | PDFs | Muy común |
| UiPath.Word.Activities | Word | Común |
| UiPath.Database.Activities | SQL y BD | Común |
| UiPath.IntelligentOCR.Activities | OCR inteligente | Avanzado |
| UiPath.DocumentUnderstanding.Activities | Document Understanding | Avanzado |
| UiPath.Terminal.Activities | Mainframe / Terminal | Legacy |
| UiPath.Cryptography.Activities | Hash, Encrypt, Decrypt | Seguridad |

---

# 2. Paquetes base obligatorios

## UiPath.System.Activities

### Descripción
Contiene las actividades fundamentales del workflow:
- Variables
- Loops
- Manejo de archivos
- DataTables
- Excepciones
- Logs
- Expresiones
- Invocación de workflows

### Namespace principal
```text
UiPath.System.Activities
```

### Dependencias comunes
```text
System.Activities
System.Data
System.IO
```

---

## UiPath.UIAutomation.Activities

### Descripción
Contiene todas las actividades UI:
- Browser automation
- Desktop automation
- OCR
- Selectors
- Keyboard
- Mouse
- Citrix
- Computer Vision

### Namespace principal
```text
UiPath.UIAutomation.Activities
```

### Tecnologías soportadas
- Web
- SAP
- Java
- Citrix
- Remote Desktop
- Windows Apps
- Legacy systems

---

# 3. UiPath.System.Activities

## Actividades fundamentales de lógica

| Actividad | Categoría | Descripción | Uso típico |
|---|---|---|---|
| Assign | Variables | Asigna valores | Inicialización |
| Multiple Assign | Variables | Varias asignaciones | Setup rápido |
| If | Flow Control | Condicional simple | Validaciones |
| Switch | Flow Control | Múltiples casos | Estados |
| While | Loops | Bucle condicional | Polling |
| Do While | Loops | Ejecuta al menos una vez | Reintentos |
| For Each | Loops | Iteración colección | DataTables |
| Parallel | Flow Control | Ejecución paralela | Optimización |
| Parallel For Each | Loops | Iteración paralela | Alto volumen |
| Break | Flow Control | Romper loop | Early exit |
| Retry Scope | Error Handling | Reintentos automáticos | Apps inestables |
| Try Catch | Error Handling | Manejo excepciones | Critical sections |
| Throw | Error Handling | Lanzar excepción | Validaciones |
| Rethrow | Error Handling | Relanzar excepción | Escalamiento |
| Terminate Workflow | Error Handling | Terminar workflow | Fatal errors |
| Delay | Timing | Espera | Sincronización |
| Log Message | Logging | Escribir logs | Auditoría |
| Add Log Fields | Logging | Campos extra logs | Contexto negocio |
| Invoke Workflow File | Modularización | Invoca XAML | Arquitectura |
| Invoke Method | .NET | Ejecutar método .NET | Custom logic |
| Invoke Code | Advanced | Código VB/C# | Lógica compleja |
| Comment | Documentation | Comentarios | Documentación |
| Sequence | Containers | Flujo secuencial | Base workflow |
| Flowchart | Containers | Flujo no lineal | Procesos complejos |
| State Machine | Containers | Máquina estados | REFramework |

---

## Actividades de DataTable

| Actividad | Descripción |
|---|---|
| Build Data Table | Crear DataTable |
| Add Data Row | Insertar fila |
| Remove Data Row | Eliminar fila |
| Filter Data Table | Filtrar |
| Sort Data Table | Ordenar |
| Merge Data Table | Unir tablas |
| Lookup Data Table | Buscar valor |
| Output Data Table | Convertir a texto |
| For Each Row | Iterar filas |
| Join Data Tables | JOIN estilo SQL |
| Remove Duplicate Rows | Eliminar duplicados |

---

## Actividades de archivos y carpetas

| Actividad | Descripción |
|---|---|
| Read Text File | Leer TXT |
| Write Text File | Escribir TXT |
| Append Line | Agregar línea |
| Copy File | Copiar archivo |
| Move File | Mover archivo |
| Delete File | Eliminar archivo |
| Create File | Crear archivo |
| Create Directory | Crear carpeta |
| Delete Folder | Eliminar carpeta |
| Empty Folder | Limpiar carpeta |
| Get Files | Listar archivos |
| Get Subfolders | Listar carpetas |
| Path Exists | Verificar existencia |
| Compress Files | ZIP |
| Extract Files | UNZIP |

---

## Actividades de serialización

| Actividad | Descripción |
|---|---|
| Deserialize JSON | JSON → objeto |
| Serialize JSON | Objeto → JSON |
| Deserialize XML | XML → objeto |
| Serialize XML | Objeto → XML |

---

# 4. UiPath.UIAutomation.Activities

## Scope principal

| Actividad | Descripción |
|---|---|
| Use Application/Browser | Scope moderno principal |
| Open Browser | Abrir navegador |
| Attach Browser | Adjuntar browser |
| Attach Window | Adjuntar ventana |
| Application Card | Scope simplificado |

---

## Actividades de interacción

| Actividad | Descripción | Tecnología |
|---|---|---|
| Click | Click izquierdo | Universal |
| Double Click | Doble click | Universal |
| Right Click | Click derecho | Universal |
| Hover | Mouse hover | Universal |
| Type Into | Escribir texto | Universal |
| Set Text | Establecer texto | Universal |
| Get Text | Extraer texto | Universal |
| Get Full Text | Texto completo | Desktop |
| Get OCR Text | OCR | Citrix |
| Check App State | Espera inteligente | Modern |
| Element Exists | Verificar elemento | Classic |
| Find Element | Encontrar elemento | Universal |
| Find Relative Element | Buscar relativo | Modern |
| Keyboard Shortcuts | Teclas rápidas | Universal |
| Send Hotkey | Atajo teclado | Universal |
| Select Item | Dropdowns | Universal |
| Select Multiple Items | Multi selección | Universal |
| Check/Uncheck | Checkboxes | Universal |
| Highlight | Resaltar elemento | Debug |
| Take Screenshot | Captura pantalla | Evidencias |
| Extract Table Data | Extraer tablas web | Web |
| Table Extraction | Data scraping | Web |
| Screen Scraping | Scraping desktop | Desktop |
| Data Scraping | Scraping estructurado | Web |

---

## OCR y Computer Vision

| Actividad | Descripción |
|---|---|
| OCR Text Exists | OCR búsqueda |
| Click OCR Text | Click usando OCR |
| Get OCR Text | Extraer OCR |
| CV Click | Computer Vision click |
| CV Type Into | Computer Vision typing |
| CV Extract Table | Extraer tabla CV |
| CV Screen Scope | Scope CV |

---

## Selectores

## Tipos

| Tipo | Descripción |
|---|---|
| Full Selector | Selector completo |
| Partial Selector | Selector parcial |
| Dynamic Selector | Variables |
| Fuzzy Selector | IA/Fuzzy matching |
| Image-based | Basado imagen |
| Computer Vision | IA visual |

---

## Input Methods

| Método | Velocidad | Compatibilidad |
|---|---|---|
| Simulate | Muy alta | Web/Desktop |
| SendWindowMessages | Alta | Desktop |
| Hardware Events | Baja | Universal |

---

# 5. UiPath.Excel.Activities

## Scope principales

| Actividad | Descripción |
|---|---|
| Use Excel File | Scope moderno |
| Excel Application Scope | Scope clásico |
| Workbook | Sin Excel instalado |

---

## Lectura y escritura

| Actividad | Descripción |
|---|---|
| Read Range | Leer rango |
| Write Range | Escribir rango |
| Append Range | Agregar filas |
| Read Cell | Leer celda |
| Write Cell | Escribir celda |
| Auto Fill Range | Autollenado |
| Copy Range | Copiar rango |
| Clear Range | Limpiar rango |
| Delete Range | Eliminar rango |
| Insert Range | Insertar rango |

---

## Manipulación avanzada

| Actividad | Descripción |
|---|---|
| Create Pivot Table | Pivot tables |
| Filter Table | Filtros |
| Sort Table | Ordenamiento |
| Remove Duplicates | Duplicados |
| Format Cells | Formato |
| Insert Chart | Gráficas |
| Execute Macro | Ejecutar VBA |
| Save Excel File | Guardar |
| Close Workbook | Cerrar |
| Protect Sheet | Proteger hoja |
| Unprotect Sheet | Desproteger |

---

## Actividades modernas

| Actividad | Descripción |
|---|---|
| For Each Excel Row | Iteración moderna |
| Read Spreadsheet | Cross-platform |
| Write Spreadsheet | Cross-platform |

---

# 6. UiPath.Mail.Activities

## Protocolos soportados

- Outlook Desktop
- Outlook 365
- Exchange
- SMTP
- POP3
- IMAP
- Gmail

---

## Actividades principales

| Actividad | Descripción |
|---|---|
| Get Outlook Mail Messages | Leer Outlook |
| Get IMAP Mail Messages | Leer IMAP |
| Get Exchange Mail Messages | Leer Exchange |
| Send Outlook Mail Message | Enviar Outlook |
| Send SMTP Mail Message | Enviar SMTP |
| Reply To Mail Message | Responder correo |
| Forward Mail Message | Reenviar |
| Save Mail Message | Guardar correo |
| Save Attachments | Descargar adjuntos |
| Move Mail Message | Mover correo |
| Delete Mail Message | Eliminar correo |
| Mark As Read | Marcar leído |

---

## Buenas prácticas Mail

```text
- Filtrar por unread
- Limitar cantidad de correos
- Usar Try Catch
- Validar adjuntos
- Sanitizar nombres de archivo
- Evitar loops infinitos
```

---

# 7. UiPath.WebAPI.Activities

## Actividades REST

| Actividad | Descripción |
|---|---|
| HTTP Request | REST API |
| Deserialize JSON | Parse JSON |
| Serialize JSON | Crear JSON |
| Get OAuth Token | OAuth2 |

---

## Métodos soportados

- GET
- POST
- PUT
- DELETE
- PATCH

---

## Headers comunes

```http
Authorization: Bearer token
Content-Type: application/json
Accept: application/json
```

---

# 8. UiPath.Orchestrator.Activities

## Assets

| Actividad | Descripción |
|---|---|
| Get Asset | Obtener asset |
| Get Credential | Obtener credencial |
| Set Asset | Actualizar asset |

---

## Queues

| Actividad | Descripción |
|---|---|
| Add Queue Item | Insertar transacción |
| Bulk Add Queue Items | Inserción masiva |
| Get Transaction Item | Obtener transacción |
| Set Transaction Status | Actualizar estado |
| Delete Queue Items | Eliminar items |

---

## Storage Buckets

| Actividad | Descripción |
|---|---|
| Upload Storage File | Subir archivo |
| Download Storage File | Descargar archivo |
| Delete Storage File | Eliminar archivo |
| Get Storage Files | Listar archivos |

---

## Jobs y procesos

| Actividad | Descripción |
|---|---|
| Start Job | Iniciar proceso |
| Stop Job | Detener proceso |
| Get Jobs | Consultar jobs |

---

# 9. UiPath.PDF.Activities

| Actividad | Descripción |
|---|---|
| Read PDF Text | Leer PDF texto |
| Read PDF with OCR | Leer OCR |
| Join PDF Files | Unir PDFs |
| Split PDF | Separar PDF |
| Extract PDF Page Range | Extraer páginas |
| Password Protect PDF | Proteger PDF |

---

# 10. UiPath.Word.Activities

| Actividad | Descripción |
|---|---|
| Word Application Scope | Scope Word |
| Read Text | Leer Word |
| Replace Text | Reemplazar |
| Append Text | Agregar texto |
| Export to PDF | Exportar PDF |
| Find and Replace | Buscar reemplazar |

---

# 11. UiPath.IntelligentOCR.Activities

## OCR Engines

| OCR | Uso |
|---|---|
| UiPath Document OCR | Recomendado |
| Microsoft OCR | Básico |
| Google OCR | Cloud |
| Abbyy OCR | Empresarial |
| Tesseract OCR | Open source |

---

## Actividades OCR

| Actividad | Descripción |
|---|---|
| Digitize Document | Digitalización |
| Data Extraction Scope | Extracción |
| Present Validation Station | Validación humana |
| Classify Document Scope | Clasificación |
| Train Classifiers Scope | Entrenamiento |

---

# 12. UiPath.DocumentUnderstanding.Activities

## Pipeline DU

```text
1. Digitize Document
2. Classify Document
3. Extract Data
4. Validate
5. Export Results
```

---

## Actividades

| Actividad | Descripción |
|---|---|
| Document Understanding Process | Scope DU |
| Intelligent Form Extractor | Formularios |
| Machine Learning Extractor | ML |
| Regex Based Extractor | Regex |
| Keyword Based Classifier | Clasificación |
| Intelligent Keyword Classifier | IA |

---

# 13. UiPath.Database.Activities

## Conexión

| Actividad | Descripción |
|---|---|
| Connect | Abrir conexión |
| Disconnect | Cerrar conexión |
| Execute Query | SELECT |
| Execute Non Query | INSERT/UPDATE |
| Insert | Insertar |
| Bulk Insert | Inserción masiva |

---

## Bases soportadas

- SQL Server
- Oracle
- MySQL
- PostgreSQL
- SQLite
- ODBC

---

# 14. UiPath.Terminal.Activities

## Sistemas legacy

| Tecnología | Soporte |
|---|---|
| IBM Mainframe | Sí |
| AS400 | Sí |
| Unix Terminal | Sí |
| VT100 | Sí |
| TN3270 | Sí |

---

## Actividades

| Actividad | Descripción |
|---|---|
| Terminal Session | Scope |
| Send Control Key | Teclas |
| Get Text | Extraer |
| Set Field | Escribir |

---

# 15. UiPath.Cryptography.Activities

| Actividad | Descripción |
|---|---|
| Encrypt Text | Encriptar |
| Decrypt Text | Desencriptar |
| Compute Hash | Hash |
| Generate Random | Random seguro |

---

# 16. UiPath.Persistence.Activities

## Uso

Workflows largos suspendibles.

## Actividades

| Actividad | Descripción |
|---|---|
| Persist Workflow | Persistencia |
| Resume Bookmark | Reanudar |
| Create Form Task | Human in the loop |

---

# 17. UiPath.Testing.Activities

| Actividad | Descripción |
|---|---|
| Verify Expression | Assert |
| Verify Control Attribute | UI Testing |
| Screenshot Verification | Comparación visual |
| Test Case | Caso prueba |
| Data Driven Test Case | Testing data-driven |

---

# 18. Actividades modernas vs clásicas

| Tipo | Modern | Classic |
|---|---|---|
| Browser Scope | Use Application/Browser | Open Browser |
| UI Exists | Check App State | Element Exists |
| Excel Scope | Use Excel File | Excel Application Scope |
| Iteración Excel | For Each Excel Row | For Each Row |

---

# 19. Actividades recomendadas por escenario

## Automatización Web

```text
Use Application/Browser
Check App State
Click
Type Into
Get Text
Extract Table Data
```

---

## Procesamiento Excel

```text
Use Excel File
Read Range
For Each Excel Row
Write Cell
Filter Table
Create Pivot Table
```

---

## Correo electrónico

```text
Get Outlook Mail Messages
Save Attachments
Move Mail Message
Send Outlook Mail Message
```

---

## REFramework

```text
Get Transaction Item
Set Transaction Status
Retry Scope
Try Catch
Log Message
Take Screenshot
```

---

# 20. Actividades parcialmente soportadas por Autopilot

| Área | Limitación |
|---|---|
| Computer Vision | Requiere calibración |
| SAP Automation | Necesita SAP Recorder |
| OCR avanzado | Requiere configuración manual |
| Document Understanding | Modelos deben entrenarse |
| Integration Service | OAuth manual |
| Dynamic selectors complejos | Revisión manual |

---

# 21. Actividades NO soportadas por Autopilot

| Operación | Motivo |
|---|---|
| Crear assets automáticamente | Seguridad |
| Configurar Integration Service | OAuth interactivo |
| Entrenar ML Extractors | Requiere dataset |
| Crear Object Repository automáticamente | Requiere captura UI |
| Configuración avanzada SAP | Dependencia extensiones |

---

# 22. Buenas prácticas profesionales

## Naming

```text
strNombre
intContador
boolExiste
dtClientes
arrArchivos
```

---

## Logging

Siempre registrar:

```text
Inicio proceso
Fin proceso
Errores
Cantidad procesada
Tiempo ejecución
TransactionID
```

---

## Error Handling

```text
Try Catch
Retry Scope
Screenshots
Logs detallados
Take Screenshot en error
```

---

## Selectores

Preferir:

```text
Modern selectors
Fuzzy selectors
Anchors
Computer Vision solo si es necesario
```

---

# 23. Convenciones recomendadas

## Estructura proyecto

```text
Main.xaml
Framework/
Workflows/
Config/
Data/
Logs/
Screenshots/
Tests/
```

---

## Naming workflows

```text
Init_AllApplications.xaml
Process_Invoice.xaml
Close_AllApplications.xaml
Get_TransactionData.xaml
Set_TransactionStatus.xaml
```

---

# 24. Recomendaciones REFramework

## Estados principales

| Estado | Descripción |
|---|---|
| Init | Inicialización |
| Get Transaction Data | Obtener transacción |
| Process Transaction | Procesamiento |
| End Process | Finalización |

---

## Variables comunes

| Variable | Tipo |
|---|---|
| TransactionItem | QueueItem |
| Config | Dictionary |
| SystemError | Exception |
| BusinessRuleException | BusinessRuleException |

---

# 25. Errores comunes

| Error | Causa |
|---|---|
| Selector not found | Selector dinámico |
| Object reference not set | Variable null |
| Collection modified | Modificar lista durante loop |
| Queue item locked | Timeout queue |
| Excel file in use | Archivo abierto |
| Cannot communicate with browser | Extensión faltante |
| Activity package missing | Dependencia no instalada |

---

# 26. Cheatsheet rápida

## Web Automation

```text
Use Application/Browser
Check App State
Click
Type Into
Get Text
```

---

## Excel

```text
Use Excel File
Read Range
For Each Excel Row
Write Cell
Save Excel File
```

---

## Mail

```text
Get Outlook Mail Messages
Save Attachments
Move Mail Message
Send Outlook Mail Message
```

---

## APIs

```text
HTTP Request
Deserialize JSON
Assign
Log Message
```

---

## REFramework

```text
Get Transaction Item
Set Transaction Status
Retry Scope
Take Screenshot
Log Message
```

---

# Referencias oficiales

## Documentación UiPath

- UiPath Activities
- UiPath System Activities
- UiPath UI Automation Activities
- UiPath Excel Activities
- UiPath Mail Activities
- UiPath Orchestrator Activities
- UiPath WebAPI Activities
- UiPath IntelligentOCR Activities
- UiPath Document Understanding

---

# Notas importantes para Autopilot

## Límites

```text
Text-to-Workflow: ~300 caracteres
Expression Editor: ~256 caracteres
```

---

## Recomendaciones para prompts

```text
- Usar nombres exactos actividades
- Indicar paquete NuGet
- Describir claramente input/output
- Separar pasos complejos
- Evitar ambigüedad
```

---

# Fin del documento

