# Power Automate Desktop — Catálogo Robusto de Acciones (Versión Gratuita)

> Documento expandido y robustecido basado en documentación oficial de Microsoft Learn y funcionalidades disponibles en Power Automate Desktop.
>
> Incluye:
> - Categorías completas
> - Acciones comunes y avanzadas
> - Parámetros importantes
> - Librerías / módulos de PAD
> - Buenas prácticas
> - Limitaciones de la versión gratuita
> - Acciones compatibles con automatización RPA Desktop
> - Acciones recomendadas para Copilot y generación de prompts
>
> Compatible con:
> - Windows 10
> - Windows 11
> - Power Automate Desktop Free
> - Power Automate Desktop Community
>
> Última actualización: 2026

---

# Índice

1. Variables
2. Condiciones
3. Bucles
4. Manejo de Texto
5. Fecha y Hora
6. Archivos y Carpetas
7. Excel
8. PDF
9. Outlook
10. Web Automation
11. UI Automation
12. Sistema
13. Scripts
14. JSON / XML / CSV
15. OCR
16. Clipboard
17. FTP
18. HTTP / APIs
19. Base de Datos
20. Compresión ZIP
21. Active Directory
22. SharePoint
23. Terminal / CMD
24. Servicios Windows
25. Workqueues
26. Manejo de Errores
27. Acciones Premium NO disponibles gratis
28. Buenas prácticas
29. Estructura recomendada para prompts
30. Glosario técnico

---

# Librerías / Módulos principales de Power Automate Desktop

| Librería / Grupo | Descripción |
|---|---|
| Variables | Manipulación de variables |
| Flow Control | Control de flujo |
| Conditionals | Condicionales |
| Loops | Ciclos |
| Excel | Automatización Excel |
| Outlook | Automatización Outlook |
| Email | Correos IMAP/SMTP |
| File | Manejo de archivos |
| Folder | Manejo de carpetas |
| Text | Manipulación de texto |
| DateTime | Manejo de fechas |
| PDF | Lectura PDF |
| Browser Automation | Automatización web |
| UI Automation | Automatización desktop |
| Mouse and Keyboard | Simulación de entradas |
| OCR | Reconocimiento de texto |
| HTTP | APIs y servicios |
| JSON | Objetos JSON |
| XML | XML |
| Database | Bases de datos |
| Compression | ZIP / RAR |
| Scripting | PowerShell / CMD |
| System | Funciones sistema operativo |
| Clipboard | Portapapeles |
| FTP | Transferencias FTP |
| SharePoint | Integración SharePoint |
| Active Directory | Directorio activo |
| Workstation | Información del equipo |
| Terminal Emulation | Emulación terminal |
| Cryptography | Hash y cifrado |

---

# 1. Variables

| Acción | Descripción | Parámetros |
|---|---|---|
| Establecer variable | Asigna valor | Nombre, Valor |
| Incrementar variable | Incrementa número | Variable, Valor |
| Reducir variable | Decrementa número | Variable, Valor |
| Convertir variable | Convierte tipo | Variable, Tipo destino |
| Limpiar variable | Vacía variable | Variable |
| Crear lista nueva | Inicializa lista | Nombre |
| Agregar elemento a lista | Inserta item | Lista, Valor |
| Eliminar elemento de lista | Borra item | Lista, Índice |
| Ordenar lista | Ordena contenido | Lista |
| Obtener sublista | Extrae rango | Lista, Índices |
| Crear diccionario | Inicializa dictionary | Nombre |
| Obtener elemento diccionario | Lee valor | Diccionario, Clave |
| Establecer valor diccionario | Inserta valor | Diccionario, Clave, Valor |
| Crear DataTable | Inicializa tabla | Nombre |
| Agregar fila DataTable | Inserta fila | Tabla, Valores |
| Eliminar fila DataTable | Borra fila | Tabla, Índice |
| Filtrar DataTable | Filtra registros | Tabla, Condición |

---

# 2. Condiciones y Control de Flujo

| Acción | Descripción |
|---|---|
| Si | Evaluación booleana |
| Si no | Rama alternativa |
| Fin Si | Cierre condición |
| Cambiar | Switch |
| Caso | Rama Case |
| Predeterminado | Default |
| Fin Cambiar | Cierre switch |
| Terminar flujo | Finaliza ejecución |
| Detener flujo | Stop |
| Ir a etiqueta | GOTO |
| Etiqueta | Label |
| Salir bucle | Break |
| Continuar bucle | Continue |
| Esperar | Delay |
| Esperar proceso | Wait process |
| Esperar ventana | Wait UI |

---

# 3. Bucles

| Acción | Descripción |
|---|---|
| Para cada uno | Iteración colección |
| Bucle | Loop fijo |
| Bucle mientras | While |
| Bucle hasta | Until |
| Repetir | Repeat |
| Fin de bucle | Fin loop |
| Iterar DataTable | Recorrer tabla |
| Iterar archivos | Loop archivos |
| Iterar carpetas | Loop folders |

---

# 4. Manejo de Texto

| Acción | Descripción |
|---|---|
| Recortar texto | Trim |
| Dividir texto | Split |
| Reemplazar texto | Replace |
| Obtener subcadena | Substring |
| Convertir texto a número | Parse |
| Convertir número a texto | ToString |
| Convertir a mayúsculas | Uppercase |
| Convertir a minúsculas | Lowercase |
| Invertir texto | Reverse |
| Rellenar texto | Padding |
| Concatenar texto | Join |
| Buscar texto | Search |
| Regex coincide | Regex Match |
| Regex reemplazar | Regex Replace |
| Regex extraer | Regex Extract |
| Generar texto aleatorio | Random String |
| Codificar URL | URL Encode |
| Decodificar URL | URL Decode |
| Convertir Base64 | Encode/Decode |

---

# 5. Fecha y Hora

| Acción | Descripción |
|---|---|
| Obtener fecha actual | Fecha sistema |
| Obtener hora actual | Hora sistema |
| Agregar fecha | Add Date |
| Restar fechas | Date Diff |
| Convertir fecha a texto | Format |
| Convertir texto a fecha | Parse |
| Obtener día semana | Weekday |
| Obtener mes | Month |
| Obtener año | Year |
| Obtener timestamp | Epoch |

---

# 6. Archivos y Carpetas

| Acción | Descripción |
|---|---|
| Obtener archivos en carpeta | Listar archivos |
| Obtener subcarpetas | Listar folders |
| Copiar archivo | Copy |
| Mover archivo | Move |
| Eliminar archivo | Delete |
| Renombrar archivo | Rename |
| Crear carpeta | Create folder |
| Eliminar carpeta | Delete folder |
| Vaciar carpeta | Empty folder |
| Verificar existencia archivo | Exists |
| Obtener carpeta especial | Desktop/Documents |
| Leer texto archivo | Read file |
| Escribir texto archivo | Write file |
| Agregar línea archivo | Append |
| Obtener detalles archivo | Metadata |
| Esperar archivo | Wait file |
| Monitorear carpeta | Folder watch |
| Cambiar atributos archivo | ReadOnly/Hidden |

---

# 7. Excel

## Acciones Excel más utilizadas

| Acción | Descripción |
|---|---|
| Iniciar Excel | Launch Excel |
| Adjuntar Excel | Attach instance |
| Crear libro | New workbook |
| Abrir documento Excel | Open workbook |
| Leer celda | Read cell |
| Leer rango | Read range |
| Leer hoja completa | Read worksheet |
| Escribir celda | Write cell |
| Escribir rango | Write range |
| Escribir DataTable | Write DataTable |
| Obtener primera fila libre | First free row |
| Obtener primera columna libre | First free column |
| Obtener hojas | Worksheets |
| Activar hoja | Activate worksheet |
| Insertar fila | Insert row |
| Eliminar fila | Delete row |
| Insertar columna | Insert column |
| Eliminar columna | Delete column |
| Ordenar rango | Sort |
| Filtrar rango | Filter |
| Buscar en Excel | Search |
| Ejecutar macro Excel | VBA Macro |
| Guardar Excel | Save |
| Guardar como | Save As |
| Cerrar Excel | Close |
| Establecer formato celda | Format |
| Autoajustar columnas | Autofit |
| Copiar/Pegar Excel | Clipboard |
| Obtener última fila usada | Last row |
| Obtener última columna usada | Last column |

## Buenas prácticas Excel

- Utilizar instancia única.
- Desactivar visibilidad cuando no sea necesario.
- Guardar periódicamente.
- Cerrar siempre Excel en bloques Try/Catch.
- Evitar UI Automation para Excel cuando exista acción nativa.

---

# 8. PDF

| Acción | Descripción |
|---|---|
| Extraer texto PDF | Read PDF |
| Extraer imágenes PDF | Images |
| Extraer páginas PDF | Split |
| Combinar PDFs | Merge |
| Dividir PDF | Split PDF |
| Leer formulario PDF | PDF Forms |
| OCR PDF | OCR |
| Convertir PDF imagen | Render |

## Limitaciones gratuitas PDF

- OCR avanzado puede requerir AI Builder Premium.
- PDFs escaneados complejos requieren OCR externo.
- Formularios dinámicos pueden fallar.

---

# 9. Outlook

| Acción | Descripción |
|---|---|
| Iniciar Outlook | Launch Outlook |
| Obtener correos | Get emails |
| Enviar correo | Send email |
| Responder correo | Reply |
| Reenviar correo | Forward |
| Guardar correo | Save email |
| Guardar adjuntos | Save attachments |
| Mover correo | Move email |
| Eliminar correo | Delete email |
| Marcar leído | Read/Unread |
| Obtener carpetas Outlook | Folders |
| Crear cita calendario | Calendar |
| Leer contactos | Contacts |

## Recomendaciones Outlook

- Outlook clásico tiene mayor compatibilidad.
- Evitar Outlook New en algunas versiones.
- Cerrar Outlook antes de adjuntar instancia.
- Usar filtros por asunto y remitente.

---

# 10. Web Automation

## Navegadores soportados

- Microsoft Edge
- Google Chrome
- Firefox

## Acciones Web

| Acción | Descripción |
|---|---|
| Iniciar Chrome | Launch Chrome |
| Iniciar Edge | Launch Edge |
| Iniciar Firefox | Launch Firefox |
| Adjuntar navegador | Attach browser |
| Navegar URL | Go to webpage |
| Hacer clic web | Click element |
| Establecer texto | Populate field |
| Obtener detalles web | Extract details |
| Esperar elemento | Wait web element |
| Extraer datos web | Web scraping |
| Ejecutar JavaScript | JS |
| Descargar archivo | Download |
| Subir archivo | Upload |
| Tomar screenshot | Screenshot |
| Cerrar navegador | Close browser |
| Cambiar pestaña | Switch tab |
| Obtener cookies | Cookies |
| Limpiar cookies | Clear cookies |

## Buenas prácticas Web

- Instalar extensión Power Automate.
- Usar selectores robustos.
- Evitar coordenadas.
- Implementar reintentos.
- Validar existencia elemento.

---

# 11. UI Automation

| Acción | Descripción |
|---|---|
| Hacer clic UI | Click desktop |
| Doble clic UI | Double click |
| Establecer texto UI | Populate text |
| Obtener texto UI | Read text |
| Seleccionar dropdown | Select item |
| Obtener ventana | Window handle |
| Esperar ventana | Wait window |
| Activar ventana | Focus |
| Cerrar ventana | Close |
| Enviar teclas | Send keys |
| Mover mouse | Mouse move |
| Arrastrar elemento | Drag and drop |
| Capturar elemento UI | Recorder |

## Limitaciones UI Automation

- SAP requiere configuraciones especiales.
- Citrix puede requerir Computer Vision.
- Aplicaciones legacy son inestables.

---

# 12. Sistema

| Acción | Descripción |
|---|---|
| Ejecutar aplicación | Run app |
| Ejecutar proceso | Run process |
| Terminar proceso | Kill process |
| Obtener procesos | Process list |
| Obtener información sistema | System info |
| Obtener usuario actual | Username |
| Obtener resolución pantalla | Resolution |
| Bloquear estación trabajo | Lock |
| Reiniciar equipo | Restart |
| Apagar equipo | Shutdown |
| Obtener variables entorno | ENV |
| Establecer variable entorno | ENV set |

---

# 13. Scripts

| Acción | Descripción |
|---|---|
| Ejecutar PowerShell | PowerShell |
| Ejecutar CMD | DOS |
| Ejecutar VBScript | VBS |
| Ejecutar JavaScript | JS |
| Ejecutar Python externo | Python |
| Leer salida script | Output |

## Recomendaciones scripts

- Manejar exit codes.
- Capturar stderr.
- Evitar credenciales hardcodeadas.
- Usar parámetros externos.

---

# 14. JSON / XML / CSV

| Acción | Descripción |
|---|---|
| Convertir JSON objeto | Parse JSON |
| Convertir objeto JSON texto | Serialize |
| Leer XML | Parse XML |
| Ejecutar XPath | XPath |
| Convertir CSV DataTable | CSV parse |
| Escribir CSV | CSV write |
| Leer CSV | CSV read |

---

# 15. OCR

| Acción | Descripción |
|---|---|
| OCR imagen | Read image text |
| OCR PDF | OCR PDF |
| OCR pantalla | Screen OCR |
| Extraer texto imagen | Extract text |

## Limitaciones OCR Free

- Precisión variable.
- PDFs escaneados complejos fallan.
- AI Builder OCR es Premium.
- Recomendado usar Tesseract externo en algunos escenarios.

---

# 16. Clipboard

| Acción | Descripción |
|---|---|
| Obtener clipboard | Get clipboard |
| Establecer clipboard | Set clipboard |
| Limpiar clipboard | Clear clipboard |

---

# 17. FTP

| Acción | Descripción |
|---|---|
| Conectar FTP | FTP Connect |
| Descargar FTP | Download |
| Subir FTP | Upload |
| Listar FTP | List files |
| Eliminar FTP | Delete |
| Desconectar FTP | Disconnect |

---

# 18. HTTP / APIs

| Acción | Descripción |
|---|---|
| Invocar servicio web | HTTP Request |
| GET API | GET |
| POST API | POST |
| PUT API | PUT |
| DELETE API | DELETE |
| Configurar headers | Headers |
| Autenticación Bearer | Token |
| Parsear respuesta JSON | JSON |

---

# 19. Base de Datos

| Acción | Descripción |
|---|---|
| Abrir conexión SQL | DB Connect |
| Ejecutar consulta SQL | Execute SQL |
| Leer resultados | Fetch rows |
| Cerrar conexión | Disconnect |
| Ejecutar stored procedure | SP |

## Motores soportados

- SQL Server
- Oracle
- MySQL
- PostgreSQL
- ODBC

---

# 20. Compresión ZIP

| Acción | Descripción |
|---|---|
| Comprimir archivos | ZIP |
| Descomprimir ZIP | Extract ZIP |
| Agregar archivos ZIP | Append ZIP |

---

# 21. Active Directory

| Acción | Descripción |
|---|---|
| Obtener usuario AD | AD User |
| Obtener grupos AD | AD Groups |
| Buscar usuario AD | Search |
| Validar usuario | Validation |

---

# 22. SharePoint

| Acción | Descripción |
|---|---|
| Subir archivo SharePoint | Upload |
| Descargar SharePoint | Download |
| Listar documentos | List docs |
| Obtener metadata | Metadata |

## Nota

Algunas integraciones SharePoint requieren conectores premium en cloud flows.

---

# 23. Terminal / CMD

| Acción | Descripción |
|---|---|
| Abrir CMD | Launch CMD |
| Ejecutar comando | Execute |
| Capturar salida | Output |
| Ejecutar batch | BAT |
| Ejecutar PowerShell | PS |

---

# 24. Servicios Windows

| Acción | Descripción |
|---|---|
| Iniciar servicio | Start service |
| Detener servicio | Stop service |
| Reiniciar servicio | Restart |
| Obtener estado servicio | Status |

---

# 25. Workqueues

| Acción | Descripción |
|---|---|
| Crear queue item | Queue |
| Obtener queue item | Get item |
| Actualizar queue item | Update |
| Completar queue item | Complete |

## Nota

Workqueues avanzados pueden requerir licenciamiento premium.

---

# 26. Manejo de Errores

| Acción | Descripción |
|---|---|
| En error de bloque | Try Catch |
| Reintentar acción | Retry |
| Continuar flujo | Continue |
| Registrar error | Log |
| Capturar screenshot | Screenshot |
| Obtener mensaje excepción | Exception |

## Buenas prácticas errores

- Manejar errores críticos.
- Capturar screenshots.
- Registrar logs.
- Implementar reintentos.
- Liberar recursos.

---

# 27. Acciones Premium NO disponibles en versión gratuita

| Funcionalidad | Estado |
|---|---|
| AI Builder avanzado | Premium |
| Unattended RPA | Premium |
| Orquestación enterprise | Premium |
| Process Mining | Premium |
| Conectores premium cloud | Premium |
| SAP avanzado enterprise | Premium |
| OCR IA avanzada | Premium |
| Dataverse enterprise | Premium |
| Machine Learning Builder | Premium |

---

# 28. Buenas prácticas generales

## Arquitectura

- Separar lógica por subflows.
- Nombrar variables correctamente.
- Utilizar prefijos:
  - Str
  - Int
  - Dt
  - Bool
  - List
  - Dct
  - Tbl

## Logs

- Registrar inicio y fin.
- Guardar errores.
- Capturar screenshots.
- Registrar duración.

## Seguridad

- No hardcodear contraseñas.
- Utilizar variables seguras.
- Evitar exponer tokens.

## Performance

- Evitar delays excesivos.
- Preferir acciones nativas.
- Minimizar UI Automation.

---

# 29. Estructura recomendada para prompts Copilot PAD

```markdown
Objetivo:
Automatizar la descarga de correos y guardar adjuntos.

Acciones requeridas:
- Iniciar Outlook
- Recuperar mensajes Outlook
- Guardar archivos adjuntos
- Mover archivo
- Escribir log

Variables:
- StrRutaDestino
- StrAsuntoFiltro
- DtCorreos

Validaciones:
- Validar existencia carpeta
- Validar cantidad correos
- Manejar errores

Resultado esperado:
Guardar adjuntos PDF en carpeta compartida.
```

---

# 30. Glosario técnico

| Término | Significado |
|---|---|
| RPA | Robotic Process Automation |
| Desktop Flow | Flujo desktop |
| Cloud Flow | Flujo nube |
| Selector | Identificador UI |
| OCR | Reconocimiento óptico |
| UI Automation | Automatización interfaz |
| DataTable | Tabla memoria |
| Queue | Cola transacciones |
| Trigger | Disparador |
| Recorder | Grabador acciones |
| Instance | Instancia aplicación |

---

# Resumen final

Este documento contiene una recopilación robusta y expandida de las acciones más utilizadas y soportadas en Power Automate Desktop versión gratuita.

Incluye:

- Automatización Desktop
- Automatización Web
- Excel
- Outlook
- PDF
- OCR
- APIs
- Scripts
- Manejo de errores
- Bases de datos
- SharePoint
- UI Automation
- Variables avanzadas
- DataTables
- JSON/XML
- Buenas prácticas enterprise

Diseñado especialmente para:

- Generación automática de prompts
- Ingeniería RPA
- Documentación técnica
- Clasificación tecnológica
- Automatización enterprise
- Generadores de PDD
- Sistemas Copilot PAD
- Frameworks RPA

---

# Referencias técnicas

- Microsoft Learn
- Documentación oficial Power Automate Desktop
- Power Platform Documentation
- Comunidad Microsoft Flow
- Experiencias reales RPA enterprise

---

FIN DEL DOCUMENTO

