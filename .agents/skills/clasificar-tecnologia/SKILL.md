---
name: clasificar-tecnologia
description: |
  Clasifica la tecnología RPA de un PDD ya leído. Soporta Power Automate (Desktop, Cloud,
  Híbrido), UiPath y Automation Anywhere. Se activa internamente desde analizar-pdd.
  También se activa si el usuario pregunta directamente sobre la clasificación de un req.
---

# Skill: Clasificar Tecnología RPA

## Entrada disponible

- Contenido completo del .toon ya leído
- `tecnologia_rpa` del encabezado (puede ser vago, vacío o específico)
- Lista de sistemas de cada requerimiento/acción

---

## Paso 1 — Identificar la familia tecnológica

Leer el campo `tecnologia_rpa` del encabezado del .toon.

### Detección de UiPath
Si `tecnologia_rpa` contiene cualquiera de: "UiPath", "Ui Path", "uipath", "UI Path",
"UiPath REFramework", "UiPath Attended", "UiPath Unattended", "RPA UiPath"
→ `tech_key: "uipath"`. Ir a la sección **Clasificación UiPath**.

### Detección de Automation Anywhere
Si `tecnologia_rpa` contiene cualquiera de: "Automation Anywhere", "AA", "A360",
"Automation 360", "IQ Bot", "Bot Creator", "Control Room"
→ `tech_key: "automation_anywhere"`. Ir a la sección **Clasificación Automation Anywhere**.

### Detección de Power Automate
Si `tecnologia_rpa` contiene "Power Automate", "PAD", "PAC", "PA Desktop", "PA Cloud",
"Power Automate Desktop", "Power Automate Cloud", "Power Automate Híbrido"
→ Ir a la sección **Clasificación Power Automate**.

### Tecnología ambigua o vacía
Si el campo está vacío o no contiene ninguna palabra clave reconocible:
→ Analizar sistemas de los requerimientos para inferir la familia (ver secciones correspondientes).
→ Si sigue ambiguo, preguntar al usuario (ver sección de preguntas al final).

**REGLA CRÍTICA:** UiPath, Automation Anywhere y Power Automate son familias mutuamente
excluyentes en un mismo proyecto. Si el PDD menciona dos familias distintas → marcar en
`informacion_faltante`: "CONFIGURACION TECNICA — El PDD menciona [TecA] y [TecB]
simultáneamente. Confirmar con BA cuál es la tecnología objetivo definitiva."

---
## Clasificación Power Automate

### Señales CLOUD — Sistemas con conectores nativos en Power Automate

| Sistema / Tipo de Señal | Conector exacto / Componente en Power Automate |
|---|---|
| SharePoint | SharePoint (V1) |
| OneDrive / OneDrive for Business | OneDrive for Business |
| Microsoft Teams | Microsoft Teams (V3) |
| Microsoft Forms | Microsoft Forms |
| Dataverse / Common Data Service | Microsoft Dataverse |
| Power Apps | Power Apps |
| Office 365 Outlook | Office 365 Outlook (V3) |
| Office 365 Users / Groups | Office 365 Users |
| Dynamics 365 / Customer Voice | Dynamics 365 / Microsoft Dataverse |
| HTTP / REST API (Endpoints en la nube) | HTTP (Premium), HTTP + Swagger, Webhook |
| Approvals (Aprobaciones nativas) | Approvals |
| Excel Online | Excel Online (Business) |
| Planner / To Do | Planner / Microsoft To Do |
| Azure SQL / SQL Server Cloud | SQL Server (vía conexión nativa cloud) |
| Azure Blob Storage / DevOps | Azure Blob Storage | Azure DevOps |
| Salesforce / ServiceNow (Nube) | Salesforce (Premium) | ServiceNow (Premium) |
| Jira Cloud / Trello | Jira | Trello |
| SAP ERP (Vía OData / API Cloud) | SAP ERP (Premium) |
| Google Drive / Gmail | Google Drive | Gmail |
| Triggers basados en tiempo (Schedules) | Recurrence (Programación interna) |
| Triggers de Eventos (Webhooks) | When an HTTP request is received |

### Señales DESKTOP — Sistemas que requieren UI automation, scripts o accesos locales

| Sistema / Componente de Destino | Tipo de acción / Tecnología requerida en PAD |
|---|---|
| JDE / JD Edwards | Navegador con UI (web legacy) o automatización de ventanas |
| SAP (transacción por SAP GUI) | SAP GUI automation (Acción: `Open SAP GUI`, `SAP logon`) |
| SIESA / Novasoft | Aplicación de escritorio / Automatización de UI (WinForms/WPF) |
| Oracle EBS / Oracle Forms | Navegador legacy (IE Mode) / Simulación de clics por coordenadas |
| SEADEX / Portales de Aduanas | Navegador con UI (Interacciones mediante selectores CSS/WA) |
| AS400 / iSeries / Mainframe | Emulador de terminal (Acción: `Terminal emulation`) |
| Navision / Business Central local | Thick Client / Automatización de ventanas de Windows |
| Excel local (Archivos `.xls`, `.xlsx`, `.macro`) | Automatización de Excel (Acción: `Launch Excel`, `Attach to Excel`) |
| Outlook Desktop (Client local) | Automatización de Outlook (Acción: `Launch Outlook`, `Send email through Outlook`) |
| Carpetas de red / Unidades compartidas | Sistema de archivos local (Rutas `\\UNC\`, unidades físicas `C:\`, `Z:\`) |
| Portales web sin API / Captcha / OTP | Automatización del navegador (Acción: `Launch new Chrome/Edge/Firefox`) |
| Aplicaciones Java (Applets) | Elementos de UI Java (requiere habilitar extensión Java en PAD) |
| Bases de datos locales (Access / FoxPro) | Conectividad de base de datos local (Acción: `Open SQL connection` vía cadenas OLEDB/ODBC) |
| Ejecución de Scripts Locales | Acciones: `Run DOS command`, `Run VBScript`, `Run JavaScript`, `Run PowerShell script` |
| Manipulación de archivos en máquina local | Acciones: `Copy file`, `Move file`, `Rename file`, `Read text from file` |
| Interacción mediante Imágenes / OCR | Acciones: `If image on screen`, `Click OCR text`, `Extract text with OCR` |
| Descarga/Carga manual de archivos por interfaz | Automatización de diálogos del sistema "Guardar como" / "Abrir" |
| Cualquier app con `tipo: Thick Client` o `Legacy` | Automatización de interfaz de usuario de escritorio (UI Automation) |

### Señales AMBIGUAS — Depende del contexto y arquitectura del PDD

| Sistema | Cloud si... | Desktop si... |
|---|---|---|
| **Excel** | "Excel Online", archivos alojados en SharePoint/OneDrive y modificados a través del conector nativo. | "Excel local", archivos en discos de red (`Z:\`), macros (`.xlsm`), archivos con contraseñas locales, uso de la app instalada. |
| **Outlook** | Conector Office 365, envío/lectura de correos directo desde la API en la nube sin requerir sesión activa en PC. | Aplicación Outlook instalada (Thick Client), uso de cuentas POP3/IMAP locales, manipulación de archivos `.pst` o `.ost`. |
| **SharePoint** | Conector nativo de SharePoint (ej. crear ítem, descargar archivo vía ID). | Navegación visual por el portal mediante Edge/Chrome (ej. dar clic en botones de la interfaz web para descargar). |
| **OneDrive** | Conector nativo de OneDrive/OneDrive for Business sin intervención de interfaz. | Acceso mediante explorador de archivos a la carpeta sincronizada localmente (ej. `C:\Users\Username\OneDrive\...`). |
| **SQL Server** | Instancia en Azure SQL o conexión directa expuesta a través de la nube con credenciales directas. | Base de datos "On-Premises" que se accede mediante cadenas de conexión locales de Windows (requiere PAD o un On-Premises Data Gateway). |
| **PDF** | Extracción de datos con AI Builder (Form Processing) nativo en Cloud. | Extracción de texto con acciones de PAD (`Extract text from PDF`) o procesamiento de archivos PDF protegidos/escaneados localmente. |
| **Archivos/Files** | Manipulación de archivos residentes en almacenamiento en la nube (S3, Azure Blob, SharePoint). | Manipulación de archivos en el escritorio del usuario, descargas de carpetas de descargas del sistema local. |

> **Nota de Consignación por Defecto:** Si el PDD no especifica la naturaleza de un sistema ambiguo:
> - **Excel / Outlook / SQL / PDF** → asumir **Desktop** (enfoque conservador y restrictivo, más frecuente en automatizaciones tradicionales).
> - **SharePoint / OneDrive** → asumir **Cloud** (conectores nativos estables y preferidos por arquitectura corporativa).

---

### Reglas de Clasificación Power Automate (Orden de prioridad)

**Prioridad 1 — Declaración explícita en el PDD:**
| El PDD dice o contiene términos como | tech_key |
|---|---|
| "Power Automate Desktop", "PAD", "RPA", "Flujo de escritorio", "Bot asistido/no asistido" | power_automate_desktop |
| "Power Automate Cloud", "Cloud Flow", "Flujo de nube", "Automatización API", "Flujo automatizado/instantáneo" | power_automate_cloud |
| "Power Automate Desktop y Cloud", "Híbrido", "Cloud invoca a Desktop", "Flujo de nube con paso de RPA" | power_automate_hybrid |
| "Power Automate" (sin especificar componentes ni arquitectura) | → Evaluar Prioridad 2 |

**Prioridad 2 — Inferencia por presencia de Sistemas y Acciones:**
| Señales detectadas | tech_key |
|---|---|
| Solo señales **CLOUD** (ej. Triggers de Forms, acciones de SharePoint Online, envío de correos API) | power_automate_cloud |
| Solo señales **DESKTOP** (ej. SAP GUI, AS400, scripts locales, carpetas compartidas locales, clics en portales web) | power_automate_desktop |
| Combinación de señales **DESKTOP + CLOUD** en distintos requerimientos del mismo proceso | power_automate_hybrid |
| Sin señales claras u omisión absoluta de sistemas | power_automate_desktop (enfoque preventivo por licenciamiento e infraestructura) |

**Prioridad 3 — Granularidad Híbrida (Evaluación individual por Requerimiento / Paso):**
```
Para cada req:
  si sistemas ∈ solo CLOUD  → plataforma = "Cloud Flow"
  si sistemas ∈ solo DESKTOP → plataforma = "Desktop Flow"
  si sistemas ∈ ambos       → plataforma = "Desktop Flow" (Desktop predomina por criticidad de ejecución)
  si sin sistemas            → plataforma = "Desktop Flow" (default)
```

**Señales arquitectónicas adicionales de Híbrido:**
- **Trigger Nube → Ejecución Local:** "El proceso se dispara cuando llega un correo a un buzón compartido (Cloud) pero la información se debe registrar en SAP GUI (Desktop)".
- **Ejecución Local → Almacenamiento Nube:** "El bot extrae datos de una aplicación legacy local (Desktop) y al finalizar sube el reporte consolidado a un sitio de SharePoint corporativo (Cloud)".
- **Arquitectura Orquestada:** "Un Cloud Flow actúa como despachador (Queue manager/Trigger) e invoca a uno o varios Desktop Flows en máquinas virtuales como ejecutores (RPA)".

### Objeto tech para Power Automate
```json
{
  "tech_label": "Power Automate Desktop | Cloud | Híbrido",
  "tech_key":   "power_automate_desktop | power_automate_cloud | power_automate_hybrid",
  "es_hibrido": false,
  "razon_clasificacion": "texto explicando señales detectadas y decisión",
  "plataforma_cloud":   ["sistemas Cloud detectados o null"],
  "plataforma_desktop": ["sistemas Desktop detectados o null"]
}
```

### Campos del JSON de análisis exclusivos de Power Automate
- `tipo`: incluir solo para Power Automate. Valores: "cloud", "desktop", "hibrido".
- `patron_arquitectura`: incluir solo en reqs híbridos para describir qué parte hace cada flujo.

---

## Clasificación UiPath

### Señales de Detección Primaria
El campo o texto del PDD contiene términos clave como: `"UiPath"`, `"Ui Path"`, `"uipath"`, `"UiPath Studio"`, `"UiPath Robots"`, `"UiPath Orchestrator"`, `"UiPath REFramework"`, `"UiPath Attended"`, `"UiPath Unattended"`, `"RPA UiPath"`, `"UiPath Action Center"`, `"UiPath Integration Service"`.

---

### Tipos de Proyecto y Modelo de Ejecución UiPath

| El PDD menciona / Características del Proceso | tech_key | Descripción Arquitectónica |
|---|---|---|
| "UiPath Attended", "Robot Atendido", "Asistido", "Disparado por el usuario", "Bot en modo agente/asistente". | uipath | El robot se ejecuta en la estación de trabajo del usuario y requiere interacción o supervisión humana en tiempo real. |
| "UiPath Unattended", "Robot Desatendido", "Ejecución en Background", "Máquina Virtual dedicada", "Trigger por Orchestrator". | uipath | El robot se ejecuta de forma autónoma en servidores o VMs dedicadas, sin intervención humana, usualmente gatillado por colas o calendarios. |
| "REFramework", "Robotic Enterprise Framework", "Estructura de Estado (State Machine)", "Transaccional con Colas". | uipath | El proyecto utiliza la plantilla estándar empresarial de UiPath basada en estados (Init, Get Transaction, Process, End). |
| Solo "UiPath" (Sin especificar modelo de ejecución). | uipath | Enfoque Base: Marcar la necesidad de aclaración en `informacion_faltante` si el licenciamiento o la infraestructura de producción dependen críticamente de definir Attended vs Unattended. |

---

### Sistemas Compatibles y Paquetes de Actividades (Dependencies)

A diferencia de otras herramientas, UiPath maneja la compatibilidad mediante paquetes de actividades (`NuGet Packages`). La detección de estos sistemas ayuda a mapear las dependencias técnicas del proyecto:

| Sistema / Tecnología en PDD | Paquete de Actividades UiPath Sugerido | Método de Interacción Principal |
|---|---|---|
| SAP ECC, SAP S/4HANA, SAP GUI | `UiPath.UIAutomation.Activities` | SAP GUI Automation Nativo / Scripting API |
| Web Legacy, Portales Modernos (Chrome, Edge, Firefox), JDE, SEADEX | `UiPath.UIAutomation.Activities` | Selectores (Modern/Classic Taxonomy), Objetos Web |
| Aplicaciones de Escritorio, Thick Clients, Java Apps, VB6, SIESA | `UiPath.UIAutomation.Activities` | Win32, WPF, Java Accessibility API, UIA |
| Excel Local (`.xlsx`, `.xls`, `.xlsm`, macros, tablas dinámicas) | `UiPath.Excel.Activities` | Excel App Integration (Thick Client) o File Workbook (sin Excel instalado) |
| Microsoft 365 (SharePoint Online, OneDrive, Excel Online, Teams) | `UiPath.MicrosoftOffice365.Activities` | Conexión directa vía Microsoft Graph API (Integration Service / Azure App Registration) |
| Outlook Desktop, Intercambio de Correo Local | `UiPath.Mail.Activities` | Acciones nativas de Outlook (MAPI) / Cuentas locales |
| Correos Cloud (Exchange Online, Gmail, IMAP, POP3) | `UiPath.Mail.Activities` o `UiPath.MicrosoftOffice365.Activities` | Conexión API / Protocolos de red de mensajería |
| Bases de Datos (SQL Server, Oracle, MySQL, Postgres) | `UiPath.Database.Activities` | Sentencias SQL directas (Execute Query, Execute Non-Query) mediante ODBC/OLEDB |
| Archivos PDF (Digitales o Escaneados) | `UiPath.PDF.Activities` o `UiPath.IntelligentOCR.Activities` | Extracción de texto nativa, Regex o Digitalización OCR (OmniPage, Google Cloud OCR) |
| Orquestación, Colas de Trabajo, Assets, Credenciales | `UiPath.Orchestrator.Activities` | Acciones de comunicación interna con UiPath Orchestrator (`Add Queue Item`, `Get Transaction Item`) |
| APIs de Terceros, Servicios REST / SOAP | `UiPath.WebAPI.Activities` | Solicitudes HTTP directas (JSON/XML) sin interfaz de usuario |
| Terminales, Mainframes, AS400, iSeries | `UiPath.Terminal.Activities` | Conexión por protocolo de emulación de terminal (TN3270, TN5250) |

> **Regla de Consistencia:** La presencia de sistemas Desktop o Cloud **NO altera ni divide** el `tech_key` cuando ya se determinó que la tecnología es UiPath. Toda lógica corre bajo el flujo de trabajo unificado de UiPath.

---

### Patrón de Arquitectura REFramework por Requerimiento

Si el PDD detalla o exige explícitamente el uso de la arquitectura **REFramework (Robotic Enterprise Framework)**, se debe etiquetar de forma granular el campo `patron_arquitectura` en cada requerimiento según la fase de la máquina de estados a la que corresponda:

- `"REFramework — Init"`: Requerimientos orientados a la lectura del archivo de configuración (`Config.xlsx`), inicialización de variables globales, lectura de credenciales desde Orchestrator Assets, apertura y logueo en las aplicaciones involucradas (ej. Abrir SAP, iniciar sesión en portal web).
- `"REFramework — GetNextTransaction"`: Requerimientos que describen la obtención de datos de trabajo, ya sea extrayendo un ítem desde una cola de Orchestrator (`Queue Item`), leyendo una fila de una tabla de datos local o procesando el siguiente archivo de una carpeta.
- `"REFramework — Process"`: Requerimientos que contienen el núcleo o la lógica principal de negocio. Procesamiento del ítem extraído, flujos de toma de decisiones, ingreso de datos en pantallas, validaciones de negocio y control de excepciones transaccionales (`BusinessRuleException` o `SystemException`).
- `"REFramework — End"`: Requerimientos encargados del cierre ordenado de aplicaciones (ej. Logout seguro, matar procesos remanentes), envío de correos con el reporte final de la ejecución, estadísticas del proceso y limpieza de la estación de trabajo.
- `""` (Vacío): Si el PDD no menciona el uso de REFramework, o para requerimientos de documentación/gestión que queden fuera del alcance directo del flujo del bot.

---

### Campos del JSON de análisis para UiPath
- `patron_arquitectura`: SÍ incluir (REFramework si aplica, sino "")
- `tipo`: NO incluir (campo exclusivo de Power Automate)
- `plataforma` por req: usar `"UiPath Workflow"` (no "Desktop Flow" ni "Cloud Flow")

---

### Objeto tech para UiPath
```json
{
  "tech_label": "UiPath",
  "tech_key":   "uipath",
  "es_hibrido": false,
  "razon_clasificacion": "PDD declara UiPath como tecnología RPA objetivo.",
  "plataforma_cloud":   null,
  "plataforma_desktop": null
}
```

---

## Clasificación Automation Anywhere

### Señales de Detección Primaria
El campo o texto del PDD contiene términos clave como: `"Automation Anywhere"`, `"AA"`, `"A360"`, `"Automation 360"`, `"Automation Anywhere Enterprise"`, `"Control Room"`, `"Bot Creator"`, `"Bot Runner"`, `"IQ Bot"`, `"Document Automation"`, `"AARI"` (Automation Anywhere Robotic Interface), `"Co-Pilot"`, `"Attended Bot"`, `"Unattended Bot"`.

---

### Versiones de Automation Anywhere y Modelo de Ejecución

| El PDD menciona | tech_key | Consideración Arquitectónica |
|---|---|---|
| "Automation 360" / "A360" / "v2x" | automation_anywhere | Versión moderna basada en web (Cloud-native). Arquitectura de paquetes dinámicos descargados desde la Control Room web. |
| "Enterprise 11" / "v11" / "v10" / "Client" | automation_anywhere | Versión heredada (Legacy On-Premise) basada en cliente instalado localmente con comandos fijos. **Marcar en `informacion_faltante`** para migración o revisión de licenciamiento. |
| "IQ Bot" / "Document Automation" | automation_anywhere | Módulo especializado en procesamiento inteligente de documentos (IDP) mediante IA/OCR. Requiere configuración de instancias de aprendizaje. |
| "AARI" / "Automation Co-Pilot" | automation_anywhere | Interfaz para automatización asistida que conecta formularios humanos con bots en tiempo real. |
| Solo "Automation Anywhere" (Sin versión) | automation_anywhere | **Marcar en `informacion_faltante`:** "Confirmar versión de la plataforma AA (A360 vs Enterprise 11) debido a diferencias críticas en comandos y arquitectura de desarrollo". |

---

### Tipos de Bot en Automation Anywhere

| El PDD menciona / Características | Tipo de Ejecución | Descripción Operativa |
|---|---|---|
| "Task Bot" / "Bot de tarea" / Flujo lógico estándar. | task_bot | Bot tradicional que ejecuta la lógica de automatización paso a paso mediante scripts de bajo código. |
| "IQ Bot" / "Document Automation" / "Instancia de aprendizaje". | iq_bot | Bot enfocado exclusivamente en la extracción de datos de documentos semiestructurados o no estructurados (facturas, órdenes de compra). |
| "Attended Bot" / "Automatización Asistida" / "AARI" / "Co-Pilot". | attended_bot | El bot se gatilla por el usuario en su estación de trabajo local y coexiste con la actividad humana diaria. |
| "Unattended Bot" / "Desatendido" / "Programado" / "Por cola de Control Room". | unattended_bot | El bot corre de manera autónoma en servidores o máquinas virtuales dedicadas mediante triggers de la Control Room. |
| Sin especificar tipo o modelo de ejecución. | task_bot | Default arquitectónico. Se asume como lógica de tarea estándar y se prioriza levantar la duda sobre el ambiente de ejecución. |

---

### Sistemas Compatibles y Paquetes / Comandos de Automation Anywhere (A360)

Automation Anywhere en su versión moderna (A360) interactúa con los sistemas mediante **Paquetes (Packages)** de acciones específicas. Para PDDs basados en v11 se utilizaban **Comandos (Commands)**.

| Sistema / Tecnología en PDD | Paquete A360 (Acciones Clave) | Comando v11 Equivalente | Método de Interacción Principal |
|---|---|---|---|
| SAP ECC, SAP S/4HANA | `SAP Package` | `SAP Automation` | Conexión nativa mediante API de Scripting de SAP GUI. |
| Aplicaciones Windows, Web legacy, SIESA, JDE, SEADEX | `Recorder Package` (`Capture`) | `Object Cloning` / `Web Recorder` | Captura avanzada de objetos de interfaz basados en tecnología UI Automation, MSAA o selectores web. |
| Páginas web, Portales modernos, Aplicaciones en la nube | `Browser Package` / `Recorder` | `Launch Website` / `Object Cloning` | Interacción directa con elementos DOM en Chrome, Edge o Firefox. |
| Excel Local (Instalado de escritorio) | `Excel Advanced Package` | `Excel Package` | Control mediante la instancia de la aplicación (Thick Client), ideal para macros y tablas dinámicas. |
| Archivos Excel genéricos (Sin requerir Excel instalado) | `Excel Basic Package` | `Open Spreadsheet` | Lectura/Escritura rápida en segundo plano de archivos `.xlsx` directos en memoria. |
| Clientes de correo locales (Outlook de escritorio) | `Email Package` | `Email Automation` | Interacción con el cliente local o configuración de perfiles MAPI en la máquina. |
| Correo corporativo en la nube (Exchange Online, Gmail) | `MS 365 Outlook` / `Gmail Package` | `Email Automation` (OAuth2) | Conexión directa mediante APIs seguras de Microsoft Graph o Google Workspace. |
| Repositorios en la nube (SharePoint / OneDrive) | `MS 365 SharePoint` / `OneDrive` | `REST Web Service` | Gestión de archivos, listas y carpetas usando credenciales API nativas. |
| Bases de Datos (SQL Server, Oracle, DB2, etc.) | `Database Package` | `Database Connect` | Conexión remota por cadenas OLEDB/ODBC para ejecutar Queries y Stored Procedures. |
| Documentos PDF | `PDF Package` | `PDF Integration` | Extracción de texto, combinación de archivos, conversión a imágenes o cifrado local. |
| Terminales, Mainframes, AS400, iSeries | `Terminal Emulator Package` | `Terminal Emulator` | Automatización de pantallas verdes mediante perfiles de emulación HLLAPI o VT100. |
| Consola de comandos, Scripts externos | `Application Package` / `Python` / `VBScript` | `Open Program/File` / `Run Script` | Ejecución de comandos del sistema (`CMD`), scripts de Python o VBScript locales. |
| APIs de terceros, Servicios REST / SOAP | `REST Web Service` / `SOAP Web Service` | `REST Web Service` | Consumo de Web Services nativos con manejo de cargas útiles (Payloads) en formato JSON o XML. |
| Orquestación y Colas de Trabajo | `Workload Package` | `Queue Operations` | Envío y procesamiento de ítems de trabajo vinculados a las colas de la Control Room. |

---

### Campos del JSON de análisis para Automation Anywhere
- `tipo`: usar el tipo de bot detectado ("task_bot", "iq_bot", "attended_bot", "unattended_bot")
- `patron_arquitectura`: usar "Control Room — [nombre del proceso]" si aplica, sino ""
- `plataforma` por req: usar `"AA Bot"` (no "Desktop Flow" ni "Cloud Flow")

---

### Objeto tech para Automation Anywhere
```json
{
  "tech_label": "Automation Anywhere",
  "tech_key":   "automation_anywhere",
  "es_hibrido": false,
  "razon_clasificacion": "PDD declara Automation Anywhere como tecnología RPA.",
  "plataforma_cloud":   null,
  "plataforma_desktop": null
}
```

---

## Criterios para requiere_script = true (Aplica a todas las tecnologías)

Este componente evalúa si un requerimiento o proceso técnico excede las capacidades de las acciones de arrastrar y soltar (*low-code/no-code*) de plataformas como Power Automate, UiPath o Automation Anywhere, haciendo mandatorio o altamente recomendado el uso de código tradicional (Python, JavaScript, PowerShell, C#, VBScript, macros VBA o consultas complejas SQL/DAX).

### Tabla de Criterios Extendida

| Situación / Complejidad Técnica | Justificación Típica para el JSON | Ejemplos de Implementación Común |
|---|---|---|
| **Lógica con 3+ niveles de anidación** | "Requiere script por lógica de decisión con N condiciones anidadas que saturan el diseñador visual." | Estructuras complejas de `If/Else` condicionales o bucles recurrentes basados en múltiples banderas (*flags*) de negocio. |
| **Manipulación y cruce masivo de datos (Data Wrangling)** | "Requiere script por procesamiento complejo de N registros con lógica de [unión/filtrado/pivote/limpieza]." | Realizar *Merges*, *Joins* (Inner/Left/Outer), agrupaciones (`Group By`), desanidación de JSONs masivos o filtrados avanzados entre múltiples fuentes de datos sin cargarlos a la UI. |
| **Consolidación y Transformación de Excels Extensos** | "Requiere script por operaciones multi-archivo en volúmenes altos (filtros dinámicos, uniones, eliminación de duplicados)." | Combinar decenas de archivos Excel pesados, aplicar reglas de negocio cruzadas fila por fila, reestructurar layouts de columnas o generar reportes dinámicos donde los paquetes nativos degradan el rendimiento (vulnerabilidad a caídas de memoria RAM). |
| **Regex / Parseo de texto no estructurado** | "Requiere script por extracción de campos mediante expresiones regulares (Regex) sobre texto libre o plano." | Limpieza de cadenas de texto complejas, validación de formatos dinámicos (emails, identificaciones, contratos) o parseo de cuerpos de correo electrónico desordenados. |
| **Cálculos matemáticos o estadísticos avanzados** | "Requiere script por cálculo de [tipo: prorrateo / interés compuesto / matrices] no disponible en las acciones nativas." | Fórmulas financieras complejas, proyecciones, conciliaciones con redondeos de precisión decimal estricta o algoritmos de distribución/prorrateo de costos. |
| **Selectores UI dinámicos sobre sistemas legacy** | "Requiere script para inyección de código/manipulación de selectores dinámicos en [sistema]." | Construcción de selectores web mediante funciones JavaScript personalizadas debido a IDs mutables, Shadow DOMs profundos o tablas HTML dinámicas que confunden al grabador nativo. |
| **Archivos planos o jerárquicos complejos (XML, JSON, CSV, EDI)** | "Requiere script por procesamiento y serialización de archivos [formato] estructurados complejos." | Generación o lectura de estructuras XML corporativas (como facturación electrónica), traducción de archivos EDI, o parseo de archivos planos de posiciones fijas de gran tamaño. |
| **Automatización y Sanitización del Sistema de Archivos** | "Requiere script por gestión avanzada de sistema de archivos local/red (compresión personalizada, permisos, encriptación)." | Descompresión masiva de archivos `.zip`/`.rar` protegidos con lógicas de contraseñas dinámicas, renombrado masivo con algoritmos específicos, o encriptación de archivos antes de su envío (`PGP`, `AES`). |
| **Llamados avanzados a APIs (Auth Complejo, Paginación)** | "Requiere script para manejo de API de [sistema] con ciclo de autenticación personalizado o paginación iterativa." | Consumo de Web Services que requieren flujos de autenticación encadenados (OAuth2 manual, manejo de tokens/cookies en las cabeceras), o control de paginación iterativa donde la respuesta final depende de loops dinámicos. |
| **Macros Locales Preexistentes / Integración Legacy** | "Requiere script para la invocación, control de errores y paso de parámetros a macros de Excel (.xlsm) o scripts VBScript heredados." | Ejecución controlada de código embebido preexistente en el cliente, asegurando capturar el código de salida (*exit code*) y controlando los *pop-ups* de alerta internos de Office. |

---

### Regla de Evaluación y Consignación por Defecto

Si el análisis del PDD no detecta explícitamente ninguna de las situaciones anteriores:
- `requiere_script`: `false`
- `justificacion_script`: `""`

Sin embargo, si se detecta que el proceso opera con **archivos Excel que superen las 10,000 filas o involucre más de 3 fuentes de datos simultáneas para consolidación**, el analista deberá forzar la bandera a `true` bajo el criterio de **Consolidación y Transformación de Excels Extensos** por motivos de optimización, estabilidad y rendimiento del entorno de producción.

---

## Información faltante — 9 categorías (todas las tecnologías)

| Categoría | Qué buscar |
|---|---|
| **TRIGGER** | Evento de inicio no definido, asunto de correo, horario, cola de Orchestrator no especificados |
| **SISTEMAS Y ACCESO** | URL, ruta de carpeta, versión del sistema, tipo de acceso (UI vs API), credenciales |
| **INPUTS** | Nombre exacto del archivo, ruta, formato, responsable de proveerlo |
| **OUTPUTS** | Ruta de destino, nombre exacto, formato, nomenclatura dinámica |
| **REGLA DE NEGOCIO** | Condición de borde sin resolución, lógica implícita no escrita |
| **EXCEPCIÓN** | Destinatario del correo de error, mensaje exacto, acción o log "por definir" |
| **CRITERIO UI** | Selector de elemento no definido, criterio de fila en tabla no especificado |
| **CONFIGURACIÓN TÉCNICA** | Parámetros del sistema, licencias, versión de AA/UiPath, clase de documento SAP/JDE |
| **REFERENCIA HUÉRFANA** | Archivo/dato mencionado como dado pero sin definir cómo el bot lo obtiene |

Formato: `"[CATEGORÍA] — descripción concisa del gap y su impacto en el desarrollo"`

No marcar como REFERENCIA HUÉRFANA si el insumo es el output explícito de un req anterior.

---

## Preguntar al usuario si la clasificación es ambigua

Si el campo `tecnologia_rpa` está vacío o no es reconocible, preguntar:

> No pude identificar la tecnología RPA en el PDD. Los sistemas detectados son: [lista].
> ¿Cuál es la tecnología objetivo?
> 1. Power Automate Desktop
> 2. Power Automate Cloud
> 3. Power Automate Híbrido (Desktop + Cloud)
> 4. UiPath
> 5. Automation Anywhere

Usar la respuesta del usuario como clasificación definitiva y documentarla en `razon_clasificacion`.
