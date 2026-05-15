
# Acciones soportadas — Automation Anywhere A360 / Automation 360

> Documento robustecido para referencia rápida de paquetes, acciones, comandos y librerías utilizadas en Automation Anywhere A360.
>
> Basado en documentación oficial de Automation Anywhere y referencias comunitarias.
>
> Fuentes:
> - https://docs.automationanywhere.com/
> - https://docs.automationanywhere.com/bundle/enterprise-v2019/page/enterprise-cloud/topics/aae-client/bot-creator/using-the-workbench/cloud-package-management.html
> - https://www.automationanywhere.com/products/automation-360

---

# Índice

1. Variables y Tipos
2. String Package
3. Number Package
4. File Package
5. Folder Package
6. Excel Basic Package
7. Excel Advanced Package
8. CSV Package
9. DataTable Package
10. Database Package
11. Email Package
12. Outlook Package
13. MS365 Package
14. PDF Package
15. OCR Package
16. Recorder / UI Automation
17. Browser Package
18. Window Package
19. Mouse Package
20. Keyboard Package
21. Delay / Wait
22. Loop Package
23. Conditional Package
24. Error Handler
25. Log Package
26. XML Package
27. JSON Package
28. REST Web Service
29. FTP / SFTP
30. SAP Package
31. Terminal Emulator
32. Workload Management
33. Credential Vault
34. Bot Insight
35. IQ Bot
36. Salesforce Package
37. AWS Package
38. Google Workspace Packages
39. Active Directory
40. Control Room Actions
41. Variables recomendadas
42. Buenas prácticas
43. Acciones NO soportadas por Copilot AA

---

# Variables y Tipos

| Tipo | Prefijo sugerido | Ejemplo |
|---|---|---|
| String | str | strNombre |
| Number | num | numTotal |
| Boolean | bln | blnExiste |
| List | lst | lstArchivos |
| Dictionary | dict | dictConfig |
| DataTable | dt | dtClientes |
| Window | window | windowSAP |
| Session | ses | sesExcel |
| Credential | cred | credSAP |

---

# String Package

| Acción | Descripción | Salida |
|---|---|---|
| String: Assign | Asigna texto | strValor |
| String: Trim | Quita espacios | strResultado |
| String: Split | Divide texto | lstValores |
| String: Replace | Reemplaza texto | strResultado |
| String: Contains | Busca substring | blnExiste |
| String: Length | Longitud del texto | numLongitud |
| String: To Upper Case | Convierte a mayúsculas | strUpper |
| String: To Lower Case | Convierte a minúsculas | strLower |
| String: Index Of | Busca posición | numIndice |
| String: Substring | Extrae parte del texto | strSub |
| String: Concatenate | Une textos | strFinal |
| String: Reverse | Invierte texto | strInvertido |
| String: Pad Left | Completa izquierda | strPad |
| String: Pad Right | Completa derecha | strPad |
| String: Format | Formato dinámico | strFormat |
| String: To Number | Convierte a número | numValor |

---

# Number Package

| Acción | Descripción |
|---|---|
| Number: Assign | Asigna valor |
| Number: Add | Suma |
| Number: Subtract | Resta |
| Number: Multiply | Multiplicación |
| Number: Divide | División |
| Number: Modulo | Residuo |
| Number: Absolute | Valor absoluto |
| Number: Round | Redondeo |
| Number: Random | Número aleatorio |
| Number: To String | Convierte a texto |

---

# File Package

| Acción | Descripción |
|---|---|
| File: Create | Crear archivo |
| File: Copy | Copiar archivo |
| File: Move | Mover archivo |
| File: Delete | Eliminar archivo |
| File: Rename | Renombrar archivo |
| File: Exists | Verificar existencia |
| File: Read Text From File | Leer archivo |
| File: Write Text File | Escribir archivo |
| File: Append Line | Agregar línea |
| File: Get Files In Folder | Obtener archivos |
| File: Get File Info | Información del archivo |
| File: Wait For File | Esperar archivo |
| File: Zip Files | Comprimir |
| File: Unzip Files | Descomprimir |

---

# Folder Package

| Acción | Descripción |
|---|---|
| Folder: Create | Crear carpeta |
| Folder: Copy | Copiar carpeta |
| Folder: Delete | Eliminar carpeta |
| Folder: Rename | Renombrar carpeta |
| Folder: Exists | Verificar carpeta |
| Folder: Get Subfolders | Obtener subcarpetas |
| Folder: Get Files | Obtener archivos |
| Folder: Zip Folder | Comprimir carpeta |
| Folder: Unzip Folder | Descomprimir carpeta |

---

# Excel Basic Package

| Acción | Descripción |
|---|---|
| Excel: Open Spreadsheet | Abrir Excel |
| Excel: Close Spreadsheet | Cerrar Excel |
| Excel: Read Cell | Leer celda |
| Excel: Write Cell | Escribir celda |
| Excel: Read Range | Leer rango |
| Excel: Write Range | Escribir rango |
| Excel: Save | Guardar |
| Excel: Save As | Guardar como |
| Excel: Activate Worksheet | Activar hoja |

---

# Excel Advanced Package

| Acción | Descripción |
|---|---|
| Excel Advanced: Open | Abrir workbook |
| Excel Advanced: Close | Cerrar workbook |
| Excel Advanced: Read From Cell | Leer celda |
| Excel Advanced: Write To Cell | Escribir celda |
| Excel Advanced: Read From Range | Leer rango |
| Excel Advanced: Write To Range | Escribir rango |
| Excel Advanced: Delete Row | Eliminar fila |
| Excel Advanced: Delete Column | Eliminar columna |
| Excel Advanced: Insert Row | Insertar fila |
| Excel Advanced: Insert Column | Insertar columna |
| Excel Advanced: Sort Range | Ordenar rango |
| Excel Advanced: Filter Range | Filtrar |
| Excel Advanced: Find | Buscar valor |
| Excel Advanced: Run Macro | Ejecutar macro |
| Excel Advanced: Get Worksheets | Obtener hojas |
| Excel Advanced: Set Active Worksheet | Activar hoja |
| Excel Advanced: Save Workbook | Guardar |
| Excel Advanced: Get Last Row | Última fila |
| Excel Advanced: Get Last Column | Última columna |

---

# CSV Package

| Acción | Descripción |
|---|---|
| CSV: Open | Abrir CSV |
| CSV: Read | Leer CSV |
| CSV: Write | Escribir CSV |
| CSV: Append | Agregar registros |
| CSV: Close | Cerrar CSV |

---

# DataTable Package

| Acción | Descripción |
|---|---|
| DataTable: Create | Crear tabla |
| DataTable: Add Row | Agregar fila |
| DataTable: Delete Row | Eliminar fila |
| DataTable: Filter | Filtrar |
| DataTable: Lookup | Buscar registro |
| DataTable: Sort | Ordenar |
| DataTable: Merge | Unir tablas |
| DataTable: Get Row Count | Total filas |
| DataTable: Export CSV | Exportar CSV |

---

# Database Package

| Acción | Descripción |
|---|---|
| Database: Connect | Conectar BD |
| Database: Disconnect | Desconectar |
| Database: Select | Ejecutar SELECT |
| Database: Insert | Ejecutar INSERT |
| Database: Update | Ejecutar UPDATE |
| Database: Delete | Ejecutar DELETE |
| Database: Execute Stored Procedure | Ejecutar SP |
| Database: Begin Transaction | Iniciar transacción |
| Database: Commit | Confirmar |
| Database: Rollback | Revertir |

---

# Email Package

| Acción | Descripción |
|---|---|
| Email: Connect | Conectar correo |
| Email: Get All Messages | Obtener correos |
| Email: Send | Enviar correo |
| Email: Save Attachments | Guardar adjuntos |
| Email: Move Message | Mover correo |
| Email: Delete Message | Eliminar correo |
| Email: Mark As Read | Marcar leído |

---

# Outlook Package

| Acción | Descripción |
|---|---|
| Outlook: Launch | Abrir Outlook |
| Outlook: Get Emails | Obtener emails |
| Outlook: Send Email | Enviar email |
| Outlook: Save Attachments | Guardar adjuntos |
| Outlook: Create Appointment | Crear cita |
| Outlook: Get Calendar Items | Obtener calendario |

---

# MS365 Package

## Outlook

- MS365 Outlook: Get Emails
- MS365 Outlook: Send Email
- MS365 Outlook: Reply Email
- MS365 Outlook: Forward Email

## SharePoint

- MS365 SharePoint: Upload File
- MS365 SharePoint: Download File
- MS365 SharePoint: Get List Items
- MS365 SharePoint: Create List Item
- MS365 SharePoint: Update List Item

## OneDrive

- MS365 OneDrive: Upload File
- MS365 OneDrive: Download File
- MS365 OneDrive: Delete File

## Teams

- MS365 Teams: Send Message
- MS365 Teams: Create Team
- MS365 Teams: Create Channel

---

# PDF Package

| Acción | Descripción |
|---|---|
| PDF: Extract Text | Extraer texto |
| PDF: Merge | Unir PDFs |
| PDF: Split | Dividir PDF |
| PDF: Encrypt | Encriptar |
| PDF: Decrypt | Desencriptar |
| PDF: Get Page Count | Número páginas |

---

# OCR Package

| Acción | Descripción |
|---|---|
| OCR: Extract Text | Extraer texto OCR |
| OCR: Screen OCR | OCR pantalla |
| OCR: Region OCR | OCR región |

Motores soportados:
- Tesseract
- ABBYY
- IQ Bot OCR
- Google OCR

---

# Recorder / UI Automation

| Acción | Descripción |
|---|---|
| Recorder: Capture | Capturar objeto |
| Recorder: Click | Click |
| Recorder: Double Click | Doble click |
| Recorder: Right Click | Click derecho |
| Recorder: Set Text | Escribir texto |
| Recorder: Get Text | Obtener texto |
| Recorder: Select | Seleccionar |
| Recorder: Hover | Hover |
| Recorder: Scroll | Scroll |
| Recorder: Wait For | Esperar elemento |
| Recorder: Verify | Verificar elemento |

---

# Browser Package

| Acción | Descripción |
|---|---|
| Browser: Open | Abrir navegador |
| Browser: Close | Cerrar navegador |
| Browser: Go To | Navegar URL |
| Browser: Refresh | Refrescar |
| Browser: Back | Regresar |
| Browser: Forward | Adelante |
| Browser: Download File | Descargar |
| Browser: Execute JavaScript | Ejecutar JS |

Navegadores:
- Chrome
- Edge
- Firefox

---

# Window Package

| Acción | Descripción |
|---|---|
| Window: Activate | Activar ventana |
| Window: Close | Cerrar ventana |
| Window: Minimize | Minimizar |
| Window: Maximize | Maximizar |
| Window: Wait | Esperar ventana |

---

# Mouse Package

| Acción | Descripción |
|---|---|
| Mouse: Click | Click |
| Mouse: Double Click | Doble click |
| Mouse: Move | Mover |
| Mouse: Drag and Drop | Arrastrar |
| Mouse: Scroll | Scroll |

---

# Keyboard Package

| Acción | Descripción |
|---|---|
| Keyboard: Keystrokes | Simular teclas |
| Keyboard: Press Key | Presionar tecla |
| Keyboard: Hotkey | Atajo |
| Keyboard: Type Text | Escribir texto |

---

# Delay / Wait

| Acción | Descripción |
|---|---|
| Delay | Espera fija |
| Wait For Window | Esperar ventana |
| Wait For File | Esperar archivo |
| Wait For Process | Esperar proceso |

---

# Loop Package

| Acción | Descripción |
|---|---|
| Loop: Each Row | Iterar filas |
| Loop: List | Iterar lista |
| Loop: Files | Iterar archivos |
| Loop: While | While |
| Loop: Times | N veces |

---

# Conditional Package

| Acción | Descripción |
|---|---|
| If | Condicional |
| Else If | Condicional adicional |
| Else | Alternativa |
| Switch | Switch case |

---

# Error Handler

| Acción | Descripción |
|---|---|
| Try | Inicio manejo |
| Catch | Captura error |
| Finally | Bloque final |
| Throw | Lanzar excepción |

Convenciones:
- BUSINESS EXCEPTION
- APPLICATION EXCEPTION

---

# Log Package

| Acción | Descripción |
|---|---|
| Log To File | Registrar logs |
| Log Message | Registrar mensaje |
| Audit Log | Auditoría |

---

# XML Package

| Acción | Descripción |
|---|---|
| XML: Parse | Parse XML |
| XML: Read Node | Leer nodo |
| XML: Write Node | Escribir nodo |
| XML: XPath Query | Consulta XPath |

---

# JSON Package

| Acción | Descripción |
|---|---|
| JSON: Parse | Parse JSON |
| JSON: Get Value | Obtener valor |
| JSON: Set Value | Establecer valor |
| JSON: Convert To String | Convertir texto |

---

# REST Web Service

| Acción | Descripción |
|---|---|
| REST: GET | Consulta GET |
| REST: POST | Consulta POST |
| REST: PUT | Consulta PUT |
| REST: DELETE | Consulta DELETE |
| REST: Authentication | Autenticación |

---

# FTP / SFTP

| Acción | Descripción |
|---|---|
| FTP: Connect | Conectar |
| FTP: Upload | Subir archivo |
| FTP: Download | Descargar archivo |
| FTP: Delete | Eliminar |
| FTP: Disconnect | Desconectar |

---

# SAP Package

| Acción | Descripción |
|---|---|
| SAP: Launch | Abrir SAP |
| SAP: Login | Login SAP |
| SAP: Execute Transaction | Ejecutar transacción |
| SAP: Read Field | Leer campo |
| SAP: Write Field | Escribir campo |
| SAP: Click Button | Click botón |

---

# Terminal Emulator

| Acción | Descripción |
|---|---|
| Terminal: Connect | Conectar |
| Terminal: Send Keys | Enviar teclas |
| Terminal: Read Screen | Leer pantalla |
| Terminal: Disconnect | Desconectar |

Compatibilidad:
- AS400
- Mainframe
- IBM Emulator

---

# Workload Management

| Acción | Descripción |
|---|---|
| Workload: Add Work Items | Agregar items |
| Workload: Get Work Item | Obtener item |
| Workload: Update Work Item | Actualizar estado |
| Workload: Complete Work Item | Completar |

---

# Credential Vault

| Acción | Descripción |
|---|---|
| Credential: Get | Obtener credencial |
| Credential: Store | Guardar credencial |
| Credential: Update | Actualizar |

---

# Bot Insight

| Acción | Descripción |
|---|---|
| Bot Insight: Create Dashboard | Dashboard |
| Bot Insight: Push Metrics | Métricas |
| Bot Insight: Generate Reports | Reportes |

---

# IQ Bot

| Acción | Descripción |
|---|---|
| IQ Bot: Process Document | Procesar documento |
| IQ Bot: Extract Data | Extraer datos |
| IQ Bot: Validate Data | Validar |

Documentos:
- Facturas
- OCR inteligente
- Formularios
- PDFs escaneados

---

# Salesforce Package

| Acción | Descripción |
|---|---|
| Salesforce: Login | Login |
| Salesforce: Query | Consulta |
| Salesforce: Insert Record | Insertar |
| Salesforce: Update Record | Actualizar |
| Salesforce: Delete Record | Eliminar |

---

# AWS Package

| Acción | Descripción |
|---|---|
| AWS S3: Upload File | Subir S3 |
| AWS S3: Download File | Descargar S3 |
| AWS Textract: OCR | OCR |
| AWS Lambda: Execute | Ejecutar Lambda |

---

# Google Workspace Packages

## Google Drive
- Upload File
- Download File
- Delete File

## Google Sheets
- Read Sheet
- Write Sheet
- Append Row

## Gmail
- Send Email
- Read Emails

## Google Calendar
- Create Event
- Read Events

---

# Active Directory

| Acción | Descripción |
|---|---|
| AD: Create User | Crear usuario |
| AD: Update User | Actualizar usuario |
| AD: Disable User | Deshabilitar |
| AD: Reset Password | Reset password |

---

# Control Room Actions

| Acción | Descripción |
|---|---|
| Run Bot | Ejecutar bot |
| Deploy Bot | Desplegar |
| Schedule Bot | Programar |
| Get Bot Status | Estado |
| Manage Queue | Administrar colas |

---

# Variables recomendadas

| Tipo | Convención |
|---|---|
| String | str |
| Number | num |
| Boolean | bln |
| List | lst |
| DataTable | dt |
| Window | window |
| Session | ses |

---

# Buenas prácticas

1. Usar nombres descriptivos.
2. Centralizar credenciales en Credential Vault.
3. Manejar errores con Try/Catch.
4. Evitar hardcode.
5. Usar DataTable Filter en vez de loops innecesarios.
6. Liberar sesiones Excel.
7. Implementar logs.
8. Manejar timeouts.
9. Utilizar queues para escalabilidad.
10. Separar lógica en subbots.

---

# Acciones NO soportadas completamente por Copilot AA

| Operación | Observación |
|---|---|
| Scripts externos complejos | Requiere configuración |
| SAP avanzado | Requiere SAP GUI |
| Mainframe complejo | Configuración externa |
| DLL personalizadas | Requiere Package SDK |
| Bots legacy V11 | Conversión parcial |

---

# Librerías / Integraciones comunes

| Tecnología | Integración |
|---|---|
| Excel COM | Microsoft Office |
| SAP GUI | SAP Scripting |
| OCR | ABBYY / Tesseract |
| Cloud | AWS / Azure / GCP |
| API | REST / SOAP |
| Bases de datos | SQL Server / Oracle / MySQL |

---

# Notas finales

- Automation Anywhere A360 trabaja con paquetes y acciones.
- Los paquetes pueden extenderse usando Package SDK.
- Muchas acciones cambian ligeramente dependiendo de la versión del Control Room.
- Algunas acciones requieren licenciamiento Enterprise.
- El Bot Store agrega paquetes adicionales reutilizables.

---

Documento generado y robustecido automáticamente.
