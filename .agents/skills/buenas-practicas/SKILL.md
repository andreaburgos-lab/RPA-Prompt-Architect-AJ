---
name: buenas-practicas
description: |
  Provee las reglas de buenas practicas de Beecker que los skills de generacion de prompts
  deben aplicar a la logica de cada prompt. Se activa internamente ANTES de generar prompts,
  nunca de forma aislada. Cada skill de prompts (generar-prompts-pad, generar-prompts-cloud,
  generar-prompts-uipath, generar-prompts-aa) carga las reglas de su seccion correspondiente
  y las aplica al construir cada bloque logico y cada instruccion_previa / nota_desarrollador.
  Fuente oficial: Manual Code Review Power Automate - Beecker (PAut_CR_02, octubre 2024).
---

# Skill: Buenas Prácticas por Tecnología

## Cómo se usa este skill

Este skill NO genera salida propia. Actúa como una capa de reglas que los skills de
prompts consultan al construir cada prompt. El flujo es:

```
analizar-pdd → (camino 🟡 o 🟢) → buenas-practicas → skill de prompts
                                        ↑
                              carga reglas de la sección
                              correspondiente al tech_key
```

Cada skill de prompts debe:
1. Leer la sección de buenas prácticas correspondiente a su tecnología.
2. Aplicar cada regla como restricción activa al redactar el texto del campo `prompt`.
3. Reflejar las reglas en `instruccion_previa` y `nota_desarrollador` cuando corresponda.
4. Si un prompt viola una regla, corregirlo antes de incluirlo en el .toon.

---

## Preceptos de calidad que guían todas las reglas

Estos cuatro preceptos son el fundamento de cada regla de este documento:

- **Mantenibilidad**: facilidad de extender, modificar y corregir el bot.
- **Legibilidad**: código con comentarios, anotaciones y nombres significativos en flujos, acciones y variables.
- **Confiabilidad**: el bot realiza sus funciones bajo condiciones específicas; incluye manejo de excepciones y reporte de errores.
- **Eficiencia**: el bot alcanza el objetivo con el tiempo marcado y sin gastar recursos innecesarios.

---

## Reglas COMUNES a todas las tecnologías

Estas reglas aplican sin excepción a cualquier tech_key.

### Fundamentos del diseño
- Usar Flujos/Subflujos para realizar pruebas independientes y mantener orden dentro del bot.
- Revisar todos los mensajes y textos entregados o mostrados al cliente: aplica a todo el bot.
- Verificar la ortografía de los textos en acciones y descripciones.

### Nomenclatura de variables
- Estilo **UpperCamelCase**. La primera palabra indica el tipo de dato.
- La primera letra de cada palabra en mayúscula, sin espacios entre palabras.
- Los nombres deben ser únicos e irrepetibles.
- Prefijos obligatorios:

| Tipo       | Prefijo | Ejemplo              |
|------------|---------|----------------------|
| Boolean    | Bln     | BlnProcesoCorrecto   |
| Integer    | Int     | IntContadorRegistros |
| Float      | Flt     | FltTotalFactura      |
| String     | Str     | StrRutaArchivo       |
| Object     | Obj     | ObjRespuestaApi      |
| Array      | Arr     | ArrFilasExcel        |
| List       | Lst     | LstCorreosPendientes |
| DataTable  | dt_     | dt_DatosCorreo       |
| Dictionary | Dic     | DicConfiguracion     |

- Parámetros entre flujos — prefijos obligatorios con guion bajo como separador:
  - Entrada: `in_` → `in_IntNombreEntrada`
  - Salida: `out_` → `out_StrNombreSalida`
  - Entrada y salida: `io_` → `io_ArrParametro`
  - La primera letra del argumento debe ser minúscula.

- PROHIBIDO: variables sin prefijo de tipo, variables con nombre genérico sin contexto ("variable1", "dato", "resultado").

### Variables sin utilizar
- Los flujos SOLO deben tener variables necesarias para su ejecución.
- Las variables no utilizadas hacen el proyecto más difícil de entender.
- OBLIGATORIO: eliminar la inicialización de variables que no se usan.

### Hardcode prohibido
NUNCA incluir valores fijos para:
- Credenciales o contraseñas (amenaza de seguridad grave; pueden ser recuperadas por terceros)
- Retrasos (tiempos de espera)
- Número de reintentos
- Rutas internas de red o de disco
- Nombres de archivos específicos del entorno
- Hojas de archivos (Excel, etc.)
- Columnas de tablas de datos
- Rutas web (URLs)
- Correos electrónicos de destinatarios
- Información sensible del cliente

IMPORTANTE: ninguno de estos datos debe introducirse como hardcode dentro de acciones
"Ejecutar un flujo" al hacer llamado de otros procesos.

Si el PDD no provee el valor → usar placeholder descriptivo entre corchetes:
`[rutaArchivo\ruta\aqui\Archivo.xlsx]`, `[https://url-sistema-aqui]`, `[NombreHoja]`.

### Nomenclatura de flujos, subflujos y scopes
- Estilo **UpperCamelCase** sin el uso de espacios.
- Debe contener el prefijo de la acción que realiza (recomendado Cloud) o la aplicación principal con la que trabaja (recomendado Desktop).
- PROHIBIDO: vocales acentuadas (á é í ó ú), caracteres especiales (# ¿ ? / \ : ; * < > [ ] $ & + % { } Ñ ñ).
- El nombre debe ser coherente con lo que realiza el flujo.
- Ejemplos correctos: `Gmail_RevisarCorreosEntrantes`, `Search_TicketInHerflow`.
- Ejemplos incorrectos: `Verificación de correo` (tiene acento y espacios).
- PROHIBIDO: incluir versión, número de Sprint o Change Request en el nombre.

### Recomendaciones generales de escritura (nombres de flujos, ámbitos, acciones, variables)
- No utilizar los caracteres especiales: `# ¿ ? / \ : ; * < > [ ] $ & + % { } Ñ ñ`
- No hacer uso de acentos.
- El nombre debe ser coherente con lo que se realiza en la acción/flujo.

### Archivo de configuración
- El archivo de configuración debe alojarse en un sitio seguro y añadirse al repositorio de Azure.
- Su uso es primordial para evitar el código duro.
- Solo es válido en las etapas de desarrollo: ramas `feature`, `development` y `main`.
- PROHIBIDO: hardcode de credenciales dentro del archivo de configuración.

### Bots atendidos y desatendidos
- **Bot desatendido**: solo el bot realiza el proceso sin interacción humana.
- **Bot atendido**: el proceso requiere interacción humana.
- PROHIBIDO: usar acciones que esperen input de usuario en bots desatendidos (genera retrasos y conflictos).

### Anidación de condiciones (If)
- Máximo **3 niveles** de anidación de condiciones If/Else.
- Permite que la estructura sea más ligera y fácil de entender.
- Si la lógica requiere más de 3 niveles: extraer a subflujo/workflow separado.
- Nota: en Desktop se puede invocar otros Subflujos para resolver esto. En Cloud, si no es posible aplicar la regla, validar con justificación.
- Indicar al desarrollador en `nota_desarrollador` cuando se detecte lógica con más de 3 niveles.

### Flujos saturados
- Máximo **6 niveles** de anidación total en un flujo/subflujo.
- Si se excede: separar el flujo en otros más pequeños usando `Ejecutar flujo` o `Ejecutar subflujo`.

### Condición If — uso correcto del bloque True
- La acción principal SIEMPRE debe ejecutarse en el bloque **True**.
- PROHIBIDO: bloque True vacío (hace el flujo difícil de entender).
- El código de mayor carga o el flujo principal se realiza sobre el apartado True.
- Si la condición original tiene la acción en False (ej: "Si el archivo NO existe"), invertir la lógica de la condición para que la acción vaya en True (ej: "Si el archivo existe").

### Mensajes de registro (Log)
- Mandar mensajes de registro desde los Subflujos llamando al subflujo **AddToLog** del Framework.
- Establecer las variables: `StrLevel`, `StrModule`, `StrMessageLog` antes de llamar a AddToLog.
- Limitar el uso a puntos de alta prioridad (mayor consumo de recursos si se abusa).
- Puntos recomendados para registrar:
  - Inicio y fin de subflujos
  - Manejo de requerimientos
  - Subida o descarga de archivos
  - Crear o eliminar carpetas o archivos
  - Interacción con cualquier aplicación externa
  - Inicio o cierre de sesión
  - Informe de errores

### Manejo de errores — regla mínima
- Cada bloque de error DEBE incluir al menos un log llamando al subflujo **AddToLog** con nivel, módulo y mensaje.
- PROHIBIDO: bloques de error vacíos (sin log, sin notificación, sin acción).

### Correos electrónicos
- Según políticas del CoE: los robots NO deben enviar correos directamente.
- Los correos creados por robots deben guardarse como **BORRADORES** para revisión humana antes de enviar.
- Excepción: correos genéricos sin información sensible.
- Toda la información del correo debe ser **parametrizable**: asunto, cuerpo, destinatarios, etc.
- PROHIBIDO: hardcode de correos de destinatarios.

### Rastreabilidad de requerimientos
- Llevar rastreabilidad de requerimientos en el flujo usando el ID del documento de definición de requerimientos.
- En Desktop: mediante acción tipo **Comentario** al inicio del subflujo con el ID.
- En Cloud: mediante **Nota** en la Acción, Scope o Subflujo correspondiente.
- Formato del ID: según el proyecto (ej. `NYB.001.007`).

### Uso de Scopes / Regiones (agrupación)
- Usar **Scopes (Ámbitos)** en Cloud o **acciones Región** en Desktop para agrupar acciones del mismo tipo o que cumplan una función específica.
- El nombre del scope/región debe ser alusivo a lo que se realiza en él.
- PROHIBIDO: scopes/regiones vacíos o con una sola acción interna (solo abarrotan el flujo).

---

## Sección: Power Automate Desktop (PAD)

Aplica cuando `tech_key = "power_automate_desktop"`.

### Nombre del proyecto
- Formato: `ID-NombreDelProyecto` → ejemplo: `NYB.001-GenerateYearlyReport`
- Descripción del proyecto: funcionalidad del proyecto.
- PROHIBIDO: versión, número de Sprint o Change Request en el nombre del proyecto.

### Variables — tipos adicionales PAD
- Dictionary: prefijo `Dic` → `DicConfiguracion`
- List: prefijo `Lst` → `LstCorreosPendientes`
- DataTable: prefijo `dt_` → `dt_RegistrosExcel`

### Subflujos en PAD
- Copilot PAD NO puede crear subflujos → `instruccion_previa` DEBE indicar que el usuario cree el subflujo manualmente antes de pegar el prompt.
- Al inicio de cada subflujo: agregar acción tipo **Comentario** con propósito, precondiciones, postcondiciones y referencia al req ID.
- Nombre del subflujo: UpperCamelCase con nombre de la aplicación principal.
  - Correctos: `JDE_DescargarLM`, `Excel_AjustarEC`, `Outlook_EnviarNotificacion`
  - Incorrectos: `Subflujo1`, `ProcesarDatos`, `Flujo_correo`

### Descripciones de Subflujos (Desktop)
- La versión Desktop no permite agregar notas/descripciones directas sobre actividades.
- OBLIGATORIO: usar acción **Comentario** al inicio de cada Subflujo con descripción textual que indique:
  - Propósito del subflujo
  - Condiciones previas y posteriores
  - Referencia al requerimiento (ID)
- Mínimo **33% de comentarios** describiendo el proceso del código y la funcionalidad de sus acciones.

### Regiones (agrupación en Desktop)
- Usar acción **Región** para agrupar acciones del mismo tipo o función.
- El nombre de la región debe describir lo que hace.
- PROHIBIDO: regiones vacías o con una sola acción.
- Ejemplo de uso correcto: agrupar `Establecer variable StrLevel`, `Establecer variable StrModule`, `Establecer variable StrMessageLog` y `Ejecutar subflujo AddToLog` en una Región llamada `Add_Log`.

### Acciones de UI (Desktop)
- Tipo `Automatización de interfaz de usuario`: para aplicativos de software de escritorio.
- Tipo `Automatización de explorador`: para navegadores de internet (Chrome, Edge, Firefox, etc.).
- RECOMENDADO: habilitar propiedad `Simular acción` cuando el control lo permita.
- RECOMENDADO: deshabilitar propiedad `Acciones físicas` (Enviar clic físico) cuando se permita.
- Al capturar ventanas: renombrar cada una con el nombre del aplicativo o portal seguido de un valor descriptivo.
  - Ejemplo: `LinkedInLogin`, `VentasEjemploFormulario`
- Al capturar elementos de cada ventana: colocar el tipo de elemento (cuadro de texto, botón, lista desplegable, etc.).
  - Ejemplo: `CuadroDeTexto_Chashin`, `Boton_Deposit`
  - Nota: en la mayoría de los casos viene por default.
- `nota_desarrollador` DEBE mencionar que los selectores requieren grabación manual con el grabador de PAD.

### Retrasos (Desktop)
- PROHIBIDO: retrasos con valor hardcodeado.
- Reemplazar por acciones de espera inteligente:
  - `Sistema: Esperar al proceso`
  - `Archivo: Esperar al archivo`
  - UI: `Esperar al contenido de la ventana` / `Esperar la imagen` / `Esperar la ventana`
  - SAP: `Esperar a la ventana SAP` / `Esperar que la sesión SAP no esté ocupada` / `Esperar al elemento SAP`
- Si la acción Retraso es estrictamente necesaria:
  - El valor DEBE venir de una variable de configuración (no hardcodeado).
  - OBLIGATORIO: agregar una nota en la acción detallando el motivo de su uso.

### Manejo de errores (Desktop)
- Usar: acción **En error del bloque** (On block error).
- Configurar: nombre del bloque, variables `module`, `message`, `loglevel`.
- Alternativa: configurar `Al producirse error` directamente sobre la acción específica.
- OBLIGATORIO: llamar subflujo `AddToLog` con nivel, módulo y mensaje en cada manejo de errores.
- Ejemplo de configuración del bloque: nombre `Manejo de errores`, variables `module` → `SAP_Login`, `message` → `Error logging into SAP`, `loglevel` → `Error`.

### Flujos saturados (Desktop)
- Máximo 6 niveles de anidación total en un subflujo.
- Si se excede: separar en subflujos usando `Ejecutar subflujo`.

---

## Sección: Power Automate Cloud

Aplica cuando `tech_key = "power_automate_cloud"`.

### Variables Cloud
- Tipos con sus prefijos: Boolean (`Bln`), Integer (`Int`), Float (`Flt`), String (`Str`), Object (`Obj`), Array (`Arr`).
- Mismas reglas de UpperCamelCase y unicidad que la sección común.

### Ramas paralelas para inicializar variables (Cloud)
- Se pueden usar ramas paralelas para inicializar variables simultáneamente.
- Límite recomendado: máximo **5 ramas** paralelas.
  - Conserva buena legibilidad del flujo.
  - Mantiene buena optimización y rendimiento.
- Considerar también: recursos del sistema, límites de licencia del servicio, dependencias entre ramas.

### Nomenclatura para Acciones (Cloud)
- El nombre de las acciones debe estar estructurado en forma de **oración**.
- PROHIBIDO: vocales acentuadas (á é í ó ú) y caracteres especiales (# ¿ ? / \ : ; * < > [ ] $ & + % { } Ñ ñ).
- Dos estructuras válidas:
  - `"Nombre default - Información de acción"` → ej: `Inicializar variable - StrMensajeError`
  - `"Nombre descriptivo"` → ej: `Inicializar Mensaje de Error`
- PROHIBIDO: dejar únicamente el nombre default sin contexto (ej: solo `Inicializar variable`).
- PROHIBIDO: nombres poco descriptivos.
- PROHIBIDO: numeración en acciones y secuencias (acción 1, acción 2). Usar en su lugar: Primera acción, Segunda acción.

### Scopes / Ámbitos (Cloud)
- Usar **Scopes (Ámbitos)** para agrupar acciones del mismo tipo o función.
- El nombre debe ser alusivo a lo que se realiza en él.
- PROHIBIDO: Scopes vacíos o con una sola acción.
- El Scope del manejo de errores: nombrar descriptivamente, ej: `[NombreReq]_ManejadorErrores`.

### Condición If (Cloud)
- REGLA: siempre usar el bloque **True** para la acción principal.
- PROHIBIDO: bloque True vacío.
- El código principal o de mayor carga debe ejecutarse en la rama True.
- Si la condición original pone la acción en False, invertir la lógica.

### Switch - Modificador (Cloud)
- REGLA: siempre realizar una acción en cada posible caso.
- PROHIBIDO: caso **Predeterminado** vacío.
- Cada caso debe tener: acción específica, Log de notificación, o manejo de errores adecuado.

### Trigger (Cloud)
- El trigger va SIEMPRE solo en el Prompt 1. Nunca combinado con acciones.
- Nombre exacto del trigger tal como aparece en Power Automate — nunca parafrasear.

### Manejo de errores (Cloud)
- Usar **rama paralela** después del Scope o acción que se quiera controlar.
- En la acción de manejo de errores: ir a **Configuración → Ejecutar después de (RunAfter)**.
- Seleccionar las opciones: `Ha agotado el tiempo de espera` y `Error`.
- OBLIGATORIO: llamar subflujo `AddToLog` o acción equivalente de log en cada manejo de errores.
- Nota: el ejemplo de configuración es una guía; adaptar según las necesidades del proceso respetando la estructura básica.

### Descripciones de Acciones (Cloud)
- Agregar **notas** a las acciones y ámbitos para tener un flujo descriptivo y facilitar la mantenibilidad.
- El porcentaje de acciones con descripciones debe ser de al menos **33%**.

### Descripciones de Flujos (Cloud)
- Agregar una descripción a cada Flujo que indique:
  - Propósito del flujo
  - Condiciones previas y posteriores
  - Referencia al requerimiento (ID)

### Id de requerimiento (Cloud)
- Añadir el ID de requerimiento a la Acción, Scope o Subflujo correspondiente como una **Nota**.
- Formato: `ID: Descripción breve` → ej: `NYB.001.007: Crea un archivo dentro de drive, con el attachment obtenido del mail`.

---

## Sección: UiPath

Aplica cuando `tech_key = "uipath"`.

Fuente oficial: **Manual Buenas Prácticas UiPath — Beecker** (MCR_UP_06, septiembre 2023).

---

### 4.1 Fundamentos del diseño

- Usar módulos para realizar pruebas independientes y mantener orden dentro del bot.
- Manejar un estándar entre las carpetas del proyecto.
- Uso obligatorio del framework de UiPath (BeeFramework o REFramework estándar de UiPath con VB).
- Manejo de capas RPA (ver sección 4.2).
- Manejar estándar para variables, argumentos y workflows.
- Manejar interacciones o procesamientos de información en background.
- OBLIGATORIO: revisar todos los mensajes o textos entregados/mostrados al cliente en todo el bot; verificar ortografía tanto en actividades como en descripciones.

---

### 4.2 Capas RPA

Cada bot debe respetar las siguientes capas de organización:

| Capa | Contenido |
|---|---|
| **Framework** | Módulos del framework (Init, GetTransaction, etc.) |
| **Business Process** | Workflows con las reglas del negocio |
| **Services** | Scripts y Workflows que consumen Web Services |
| **Application Process** | Workflows con interacción gráfica Y validación de reglas de negocio |
| **Application Screen** | Workflows con interacción gráfica SIN validar reglas de negocio |
| **Data** | Workflows con interacción con datos locales, bases de datos o archivos de configuración |

---

### 4.3 Uso de ReFramework (BeeFramework)

- OBLIGATORIO: usar el **BeeFramework** provisto por el arquitecto como base de todo proceso nuevo.
- Si no es posible usar BeeFramework: crear un nuevo REFramework desde UiPath con lenguaje **Visual Basic** (no C#).
- Se validará el uso adecuado de cada etapa del Framework:

| Etapa | Descripción |
|---|---|
| `InitAllSettings` | Inicia valores necesarios para el bot: Config.xlsx, valores del Orchestrator |
| `InitAllApplications` | Abre las aplicaciones requeridas |
| `KillAllProcesses` | Cierra procesos en caso de error |
| `GetOrchestratorCredentials` | Obtiene credenciales del Orchestrator por AssetName |
| `GetTransactionData` | Obtiene el siguiente ítem de la cola |
| `SetTransactionStatus` | Marca el ítem como Success, BusinessException o ApplicationException |
| `CloseAllApplications` | Cierra todas las aplicaciones al finalizar |
| `FinalizateProcess` | Finaliza el proceso y envía notificación |

- OBLIGATORIO: en el módulo principal `Main.xaml` agregar las siguientes anotaciones:
  - `ID:` "id del robot"
  - `Nombre:` "Nombre del proyecto"
  - `Desarrollador:` "Nombre del desarrollador núcleo"
  - `Aplicaciones:` "Nombre de todas las aplicaciones implicadas, separadas por coma"

---

### 4.4 Nombre del proyecto en UiPath

- Formato: `ID-NombreDelProyecto` → ejemplo: `NYB.001-GenerateYearlyReport`
- Descripción: funcionalidad del proyecto.
- PROHIBIDO: agregar versión, número de Sprint o Change Request al nombre del proyecto.
  - Incorrecto: `NYB.001-GenerateYearlyReport_S1`
  - Correcto: `NYB.001-GenerateYearlyReport`

---

### 4.5 Archivo de configuración (Config.xlsx)

- Ubicación: `Data/Config.xlsx`
- Es primordial para evitar código duro (hardcode).
- Su uso solo es válido en las etapas de desarrollo: ramas `feature`, `develop` y `main`.
- En productivo: el archivo config debe moverse a un directorio seguro en la máquina virtual, exclusivo para este archivo, o hacer uso de **Storage Bucket**.
- El archivo cuenta con tres hojas:

| Hoja | Contenido |
|---|---|
| `Settings` | Datos con probabilidad de cambio |
| `Constants` | Constantes del proceso |
| `Assets` | Datos que se obtienen del Orchestrator |

- La hoja `Settings` debe organizar los valores por categorías con color (Paths Documentos, Paths Programas, APIs, URLs, Emails, Credentials).
- PROHIBIDO: dejar vacíos los campos de valores en Settings, Constants o Assets.
- OBLIGATORIO: todos los campos y valores del archivo config deben tener su respectiva descripción.
- IMPORTANTE: la variable `MaxRetryNumber` en la hoja `Constants` debe tener un valor igual a **3**.
- Si se usan actividades `Delay`: las constantes de tiempo deben estar en config:

| Constante | Valor |
|---|---|
| `DelayShort` / `DelayLow` | 5 |
| `DelayMedium` | 10 |
| `DelayLong` / `DelayHigh` | 15 |

- Credenciales: dentro del config NO se permite hardcode; solo mediante assets.
- Variables de Settings: una vez el proyecto finalice, todas deben cargarse al Orchestrator como Assets para que el cliente las pueda modificar fácilmente.
- Acceso en workflows: `in_Config("NombreClave").ToString`.

---

### 4.6 Carpeta .screenshots

- RECOMENDADO: remover o comprimir la carpeta `.screenshots` antes de subir el proyecto a Orchestrator, para evitar exceder el límite de peso permitido.

---

### 4.7 Bots atendidos y desatendidos

- **Bot desatendido**: el bot realiza el proceso sin interacción humana.
- **Bot atendido**: el proceso requiere interacción humana.
- PROHIBIDO en bots desatendidos: usar actividades que requieran input del usuario como `Input Dialog` o `Message Box` (generan retrasos y conflictos).

---

### 4.8 Versión de UiPath

- Usar siempre la versión más actualizada disponible de UiPath Studio.
- Update Channel: **Stable** (no Preview).
- Si el cliente maneja su propia versión: trabajar con las opciones disponibles en esa versión y buscar alternativas que cumplan las buenas prácticas.

---

### 4.9 Uso de Git

- OBLIGATORIO: usar Git para llevar seguimiento de cambios en el proyecto.
- Se puede usar la herramienta integrada de Git en UiPath Studio (Team > GIT).
- Para problemas o errores complejos de repositorio: usar la consola Git directamente.
- Formato del commit message: `Fix<CR> <TT>: descripción breve de los cambios`
  - Ejemplo: `Fix<CR> <TT>: Cambios en Process para corrección de incidencias BP y resolución de bugs de Testing`

---

### 5.1 Nomenclatura de variables

- Estilo **UpperCamelCase**: primera letra de cada palabra en mayúscula, sin espacios.
- Ejemplo: `NombreVariable`, `FechaRegistro`, `ContadorRegistros`
- Los mismos prefijos de tipo de la sección COMUNES aplican plenamente aquí.

---

### 5.2 Prefijos de argumentos

- Los argumentos usan prefijos para indicar su dirección:
  - `in_` → argumentos de **entrada** → `in_NombreEntrada`
  - `out_` → argumentos de **salida** → `out_NombreSalida`
  - `io_` → argumentos de **entrada y salida** → `io_Nombre`
- La primera letra del prefijo es **minúscula**.
- Después del prefijo: guion bajo como separador, luego el nombre en UpperCamelCase.
- OBLIGATORIO: todos los argumentos deben tener una **descripción detallada** (clic derecho → Design Properties).
- PROHIBIDO: argumentos con valores default o inicialización en sus propiedades.

---

### 5.3 Nombres únicos para variables y argumentos

- PROHIBIDO: dos variables con el mismo nombre aunque técnicamente sea posible.
- PROHIBIDO: una variable y un argumento con el mismo nombre (genera confusión en depuración).
- Incorrecto: `Variable1`, `Variable2`
- Correcto: `ContadorPrimerNivel`, `ContadorSegundoNivel`

---

### 5.5 Nomenclatura para DataTables

- Prefijo obligatorio: `dt_` (minúscula) → `dt_Recorrido`, `dt_DatosMoneda`
- Incorrecto: `DT_Recorrido` (mayúsculas en prefijo)

---

### 5.6 Uso de constantes

- Las variables que no cambian (constantes) deben traer su valor desde el archivo config.
- Incorrecto: inicializar con valor fijo `0` o `"texto"` en la columna Predeterminado.
- Correcto: `CInt(in_Config("Contador"))` como valor predeterminado.
- PROHIBIDO: argumentos con valores default o inicialización hardcodeada.

---

### 5.7 Restringir el alcance (Scope) de variables

- Las variables deben definirse en el **scope más interno posible**.
- Objetivo: mejorar la organización y evitar uso involuntario en ámbitos no deseados.
- Incorrecto: variable declarada en "Secuencia de Alto Nivel" cuando solo se usa en "Secuencia de Bajo Nivel".
- Correcto: declarar la variable directamente en "Secuencia de Bajo Nivel".

---

### 5.8 Variables de bucle (For Each)

- OBLIGATORIO: cambiar el nombre y tipo de la variable de bucle `item` por un nombre descriptivo acorde a los datos procesados.
- Incorrecto: `ForEach item in dt_Ejemplo.ToString` con TypeArgument `Object`
- Correcto: `ForEach ContadoRegistro in dt_Ejemplo.ToString` con TypeArgument `String` y DisplayName `Por cada Recorrido`

---

### 5.9 Valores en Código Duro (Hardcode)

PROHIBIDO incluir valores fijos para:
- Valores en variables
- Retrasos (Delay)
- Número de reintentos
- Rutas internas
- Nombres de archivos
- Hojas de archivos (Excel, etc.)
- Columnas de tablas de datos
- Rutas web (URLs)
- **Credenciales** (amenaza de seguridad grave)
- Información sensible del cliente
- Correos electrónicos

- Correcto: usar assets, Config.xlsx o variables parametrizadas.
- Credenciales: almacenar siempre en Assets, Windows Credentials u otro repositorio seguro.
- OBLIGATORIO: variables o argumentos que contengan contraseñas deben ser de tipo **SecureString**.
- Para archivos JSON de Service Account: no es necesario SecureString ya que es solo una ruta de archivo.
- PROHIBIDO: introducir datos hardcodeados en actividades `Invoke Workflow` al hacer llamado de otros procesos.

---

### 5.10 Variables y argumentos sin utilizar

- OBLIGATORIO: eliminar variables y argumentos no utilizados del flujo.
- Los elementos no usados hacen el proyecto más difícil de entender.
- Solo deben existir variables y argumentos necesarios para la ejecución.

---

### 5.11 Nomenclatura de Assets

- Formato: `tipo_de_asset_Aplicación_NombreAsset`
- Ejemplo correcto: `cred_Okta_MainUser`

---

### 6.1 Recomendaciones de escritura

Al asignar nombre a Workflows, secuencias, módulos y actividades:
- PROHIBIDO: caracteres especiales `# ¿ ? / \ : ; * < > [ ] $ & + % { } Ñ ñ`
- PROHIBIDO: acentos (á é í ó ú)
- Usar UpperCamelCase para variables y argumentos.
- El nombre debe ser coherente con lo que realiza la actividad/módulo.

---

### 6.2 Nomenclatura para XAML

- UpperCamelCase sin espacios.
- Incluir el prefijo de la aplicación o carpeta principal que lo contiene.
- La secuencia principal dentro del archivo debe tener el **mismo nombre que el archivo XAML**.
- PROHIBIDO: acentos, caracteres especiales, `Ñ/ñ`.
- Incorrecto: `Nombre ERRÑoNEO.xaml` con secuencia principal llamada `vNombre priñincipal`
- Correcto: `APIGoogle_CargaGoogleDrive.XAML` con secuencia principal `APIGoogle_CargaGoogleDrive`

---

### 6.3 Estructura de carpetas

- Carpeta `Framework`: todos los módulos del framework.
- Carpeta `Process`: subcarpetas con el nombre de la aplicación en UpperCamelCase.
- Módulos independientes de aplicación: en carpeta con nombre definido por el desarrollador.
- Cada módulo dentro de subcarpetas debe tener el **prefijo de la carpeta principal** del aplicativo.

Ejemplos correctos:
- `Process\APIGoogle\APIGoogle_CargaGoogleDrive.xaml`
- `Process\SAP\SAP_Lista501\SAP_Lista501Borrado.xaml`

- Archivos inamovibles: `Main.xaml`, `Process.xaml`, `project.json`.
- OBLIGATORIO: remover la carpeta `Tests` antes de pasar al ambiente de producción.

---

### 6.4 CloudShore DigitalWorkers

- OBLIGATORIO: incluir las librerías de Digital Workers en **todos** los proyectos, incluso si no usan SAP.
- No es necesario usarlas en el código, pero deben estar instaladas.
- RECOMENDADO: eliminar las dependencias que no se vayan a utilizar para mejor organización y control.

---

### 6.5 Flujo de trabajo adecuado

- **Flowchart**: para flujos con decisiones múltiples y/o complejas.
- **Sequence**: para flujos que son puramente secuenciales.
- Incorrecto: usar Flowchart con solo acciones lineales sin decisiones.
- Correcto: usar Sequence para tareas lineales; Flowchart solo cuando hay ramificaciones complejas.

---

### 6.6 Actividades IF anidadas

- Máximo **2 niveles** de anidación de actividades If (Decisión).
- Si se requieren más de 2 niveles: usar la actividad `Flow Decision` dentro de un Flowchart.
- El exceso de anidación hace la estructura más pesada y difícil de entender.

---

### 6.7 Comment Out

- PROHIBIDO: dejar actividades comentadas (`Comment Out`) o sin conectar a ningún nodo en un diagrama de flujo.
- Las actividades comentadas deben eliminarse.
- Excepción: si un flujo puede usarse en producción pero no en pruebas, se puede comentar con las siguientes condiciones:
  - Eliminar el nombre genérico "Comment Out" y agregar uno que describa el flujo.
  - Agregar una anotación detallando el motivo de su existencia.

---

### 6.8 Switch

- OBLIGATORIO: siempre realizar una acción en el apartado **Default** del Switch.
- El Default puede contener: un case predeterminado, un Log de notificación, o un manejo adecuado de errores.
- PROHIBIDO: apartado Default vacío.

---

### 6.9 Flujo de trabajo saturado

- Máximo **6 niveles** de anidación en un workflow.
- Si se excede: separar en workflows más pequeños usando `Invoke Workflow File`.
- Los flujos profundamente anidados son difíciles de ver, comprender y mantener.

---

### 6.10 Secuencias o diagramas de flujo vacíos

- PROHIBIDO: secuencias vacías dentro de flujos de trabajo.
- PROHIBIDO: secuencias o flujos que contienen solo **una** actividad interna (se pueden eliminar sin impacto en funcionalidad).
- Solo incluir secuencias que cumplan un propósito específico.

---

### 6.11 Descripción en flujo de trabajo

- La actividad de nivel superior (generalmente el Sequence o Flowchart principal) de cada workflow debe tener una **breve descripción textual** que indique:
  - Objetivo del workflow
  - Entradas y salidas
  - Condiciones previas y resultados esperados
- Esto ayuda a otros desarrolladores a comprender rápidamente el propósito del módulo.

---

### 6.12 Id de requerimiento (rastreabilidad CMMI)

- OBLIGATORIO para rastreabilidad CMMI: añadir el ID de requerimiento (obtenido del documento DFR o DAT) como anotación en la secuencia correspondiente.
- Formato: `[ID]\n[Descripción breve]` → ejemplo: `NYB.013.002.001\nIniciar sesión en LinkedIn`

---

### 6.13 Nombre de secuencias

- PROHIBIDO: usar nombres por defecto de secuencias como `Sequence`, `Do`, `Body`.
- Estos nombres genéricos dificultan identificar la ruta o secuencia en cuestión.
- Incorrecto: `Sequence`, `Body`, `Do`
- Correcto: `Ejemplo Buenas Prácticas`, `LoginEnSistema`, `ProcesarTransaccion`

---

### 6.14 Capturas de pantalla de referencia

- Las capturas de pantalla son útiles para explicar qué hace la actividad y con qué elementos interactúa.
- Deben almacenarse en la carpeta `.screenshots` del proyecto.
- Las actividades deben mostrar la captura de referencia, no solo el placeholder `Take informative screenshot`.

---

### 6.15 Títulos genéricos y estándar

- Los nombres de las actividades deben dar una idea clara de cómo se utilizan.
- Agregar información adicional cuando el nombre default sea demasiado genérico.
- Los nombres de actividades deben ser **únicos e irrepetibles**.
- Excepciones (no aplica esta regla): `Log Message`, `Write Line`, `Invoke`.
- PROHIBIDO: numeración en nombres (`Actividad 1`, `Actividad 2`). Usar: `Primera Actividad`, `Segunda Actividad`.
- Incorrecto: `Sequence`, `Open Browser`, `Click`, `Do`
- Correcto: `Secuencia para abrir Navegador`, `Abrir Navegador Beeckerco`, `Click en botón`, `Hacer Después de abrir Navegador`

---

### 6.16 If-Then

- OBLIGATORIO: la acción principal siempre debe estar en el bloque **Then** (rama verdadera).
- PROHIBIDO: bloque Then vacío con toda la lógica en Else.
- Si la condición original pone la acción en Else, invertir la condición para que quede en Then.

---

### 6.17 Actividad Paralela

- El uso de la actividad Paralela puede hacer el flujo difícil de comprender y generar resultados inesperados combinado con UI.
- Si es necesario usarla: agregar una **anotación** que explique la situación.
- PROHIBIDO: usar actividad Paralela sin justificación documentada.

---

### 6.18 Actividades basadas en imágenes

- PROHIBIDO (general): uso de actividades basadas en imágenes como `Click Image` y `Wait Image Vanish`.
- Son sensibles a resoluciones de pantalla y calidad de imagen.
- Excepción: solo si existe una justificación fundamentada. En ese caso: agregar una **anotación** que explique la situación.

---

### 6.19 Selector idx y Selector CSS

- El atributo `idx` debe mantenerse en un valor **bajo (1 o 2)**.
- PROHIBIDO: selector `css` (es un selector genérico poco confiable).
- Si el `idx` es 3 o mayor: agregar una anotación que justifique su uso y envolver en `Retry Scope`.
- Alternativa: usar `Try Catch` con la excepción adecuada y `Log Message` con la información de la excepción.

---

### 6.20 Actividad Attach

- RECOMENDADO: usar contenedores con selectores (`Attach Window` o `Attach Browser`) para todas las actividades UI.
- Esto evita que notificaciones del sistema o ventanas emergentes intercepten la ejecución.
- Actividades `Send Hotkey`: usar solo como último recurso cuando no existe alternativa de navegación. Al usarse debe:
  - Contar con una imagen de referencia.
  - Tener un selector confiable.
  - Estar preferiblemente dentro de una actividad Attach.

---

### 6.21 Elementos UI Automation en Excel

- PROHIBIDO: usar actividades de UI Automation (`Get Text`, `Click`, `Send Hotkey`, etc.) para interactuar con Excel.
- OBLIGATORIO: usar las actividades designadas de la integración de Excel (Excel Application Scope, Read Range, Write Range, etc.).
- Excepción: si el uso de UI Automation es estrictamente necesario, debe ser validado por el Arquitecto o DM del proyecto y agregar una nota en el módulo que los contenga.

---

### 6.22 Log Message

- OBLIGATORIO: agregar `Log Message` al **inicio** y al **final** de cada módulo principal o importante.
- Agregar también en puntos intermedios relevantes (descarga de archivo, interacción crítica, etc.).
- Para actividades `Open Browser` o `Navigate To`: agregar `Log Message` inmediatamente antes o después registrando la URL utilizada.

Puntos recomendados para registrar:
- Manejo de requerimientos
- Subida o descarga de archivos
- Crear o eliminar carpetas o archivos
- Interacción con cualquier aplicación externa
- Inicio o cierre de sesión
- Uso de `Build Data Table`
- Actividades `Try Catch`
- Interacciones con GSuite

**Niveles de Log Message:**

| Nivel | Cuándo usarlo |
|---|---|
| `Fatal` | Error que obliga a cerrar el servicio para evitar pérdida de datos; corrupción de datos |
| `Error` | Error fatal para la operación pero no para el servicio (archivo no encontrado, datos faltantes) |
| `Warn` | Situación anómala recuperable automáticamente (reintento, datos secundarios faltantes) |
| `Info` | Inicio/fin de módulos importantes, progreso del proceso |
| `Trace` | Rastreo de código para depuración específica |

- Formato recomendado del mensaje: `"[NombreModulo] - [descripcion_accion]"` o `"Se está accediendo al Módulo de apertura..."`.

---

### 6.23 Propiedad EmptyField

- Al ingresar datos repetitivamente en un campo, es obligatorio **limpiar el campo** antes de cada nuevo ingreso.
- Propiedad `EmptyField`: establecer en `True`.
- PROHIBIDO: dejar `EmptyField` en el valor default `When this e...` cuando los datos son repetitivos.

---

### 6.24 Actividad Try – Catch

- Las excepciones deben detectarse con un **propósito**, no solo para evitar mensajes de error.
- OBLIGATORIO: insertar `Log Message` en el bloque `Catch` con nivel `Fatal` o `Error`.
- Estructura del mensaje de error: `"Falló el procedimiento" + exception.ToString`
- PROHIBIDO: bloque Catch vacío (sin log, sin notificación, sin acción).
- Especificar el tipo de excepción correcto en el Catch (no usar `Exception` genérico cuando se conoce el tipo).

---

### 6.25 Control de excepción en Transaction con Orchestrator

Elegir el tipo correcto de excepción al manejar ítems de cola:

- **ApplicationException**: error originado en un problema técnico (aplicación no responde, se congela). Orchestrator puede reintentar automáticamente si `Auto Retry = Yes`.
- **BusinessException**: error originado en datos incompletos o inválidos (dígito faltante, campo requerido vacío). NO reintentar automáticamente; notificar al usuario humano.

La actividad `Set Transaction Status` determina cómo Orchestrator trata el ítem:
- `Status = Failed` + `ApplicationException` → puede reintentarse.
- `Status = Failed` + `BusinessException` → no se reintenta por defecto.

---

### 6.26 Uso de Excepciones específicas

Preferir tipos de excepción específicos sobre el tipo genérico `Exception`:

| Tipo | Cuándo usarlo |
|---|---|
| `SystemException` | Clase base del espacio de excepciones del sistema |
| `IOException` | Acceso a información mediante streams, archivos y directorios |
| `NullReferenceException` | Intento de acceso a un miembro de un objeto nulo |
| `InvalidOperationException` | Llamada a método inválida para el estado actual del objeto |
| `ArgumentException` | Argumentos inválidos proporcionados a un método |

- Las excepciones NO sirven para "corregir" errores de programación; sirven para alertar y decidir el comportamiento del programa.

---

### 6.27 Actividad Element Exists

- Debe contar con un **selector confiable** y su respectiva **imagen de referencia**.
- Los tiempos de espera (Timeout) deben provenir del config: `CInt(in_Config("DelayShort"))`.
- La propiedad `WaitForReady` debe estar en `COMPLETE`.
- PROHIBIDO: Timeout hardcodeado (ej: `1000`).

---

### 6.28 Envío de Correos

- Política del CoE: los robots **NO deben enviar correos directamente**.
- Los correos creados por robots deben guardarse como **borradores** para revisión humana.
- Excepción: correos genéricos sin información sensible.
- Toda la información del correo debe ser **parametrizable**: asunto, cuerpo, destinatarios, etc.
- Para Gmail: usar las actividades nativas de la librería de UiPath para Gmail (`Use Gmail with main account`) en lugar de protocolos SMTP cuando sea posible.

---

### 6.29 Protocolos de correos (SMTP/IMAP)

- PROHIBIDO: introducir `Port`, `Server` o correo electrónico en hardcode en actividades de protocolos de correo.
- Estos datos deben estar almacenados y obtenerse como **Assets**.
- Incorrecto: `Port = 993`, `Server = "mail-sitioejemplo.com"`, `Email = "usuario1@sitio.com"`
- Correcto: `Port = CInt(in_PortIMAP)`, `Server = in_ServerIMAP`, `Email = in_Username`

---

### 6.30 Actividad Delay

- Los retrasos pueden afectar innecesariamente el rendimiento del robot.
- PROHIBIDO: usar `Delay` con valor hardcodeado.
- Reemplazar por actividades de espera inteligente:
  - `On Element Appear`
  - `Wait for Download`
  - `Wait Image Vanish`
  - Parámetro `Timeout` en las propias actividades de UI
- Si el uso de `Delay` es estrictamente necesario:
  - El valor DEBE venir de una variable de config (`DelayShort`, `DelayMedium`, `DelayLong`).
  - OBLIGATORIO: agregar una **anotación** en la actividad detallando el motivo de su uso.
  - Las propiedades `DelayAfter` y `DelayBefore` también deben usar constantes del config.

---

### 6.31 Actividad Open Browser

- OBLIGATORIO: usar `Open Browser` (o `Attach Browser`) para trabajar con navegadores.
- PROHIBIDO: usar `Open Application` o `Start Process` para abrir navegadores web.
- `Open Browser` sirve también como contenedor para actividades de automatización web.

---

### 6.32 Actividades de interacción con usuario

- PROHIBIDO en bots desatendidos: mostrar `Message Box` o `Input Dialog`.
- Estos dialogs detienen el robot al esperar input humano.
- Alternativa: usar `Write Line` o `Log Message` para mensajes en consola.

---

### 6.33 SimulateType y SendWindowMessages

- OBLIGATORIO: habilitar `SimulateType = True` siempre que sea posible.
- Si el control no lo soporta: agregar una **anotación** explicando el motivo.
- Comparación de métodos:

| Método | Compatibilidad | Background | Velocidad | Hotkeys | Vaciar campo auto |
|---|---|---|---|---|---|
| Default | 100% | No | 50% | Sí | No |
| SendWindowMessages | 80% | Sí | 50% | Sí | No |
| SimulateType/Click | 99% web / 60% desktop | Sí | 100% | No | Sí |

- `SendWindowMessages`: convierte texto a minúsculas, no vacía el campo automáticamente, no es el más rápido.
- `Simulate Type/Click`: más rápido, funciona en background, soporta vaciado automático del campo, no soporta atajos de teclado.

---

### 6.34 Bucles Infinitos

- PROHIBIDO: incluir posibles bucles infinitos al usar `Flow Decision`.
- Siempre incluir un mecanismo de salida: actividad `Throw` o `Try Catch`.
- PROHIBIDO: módulos que realizan `Invoke` a sí mismos (causa recursión/loop infinito).

---

### 6.35 Uso de Retry Scope

- OBLIGATORIO: usar `Retry Scope` siempre que se haga un login.
  - Cantidad de reintentos para login: **máximo 2**.
  - Debe tener su respectiva condición de validación.
- Para acciones diferentes a login:
  - Cantidad de reintentos: **máximo 3**.
- OBLIGATORIO: agregar `Log Message` con nivel `Trace` dentro del Retry Scope indicando el nombre del proceso que se reintenta.
- Si no es posible validar una condición en el Retry Scope: agregar `Log Message` indicando el número de reintento actual.
- El número de reintentos para login debe venir del config: `ReintentoLogin`.

---

### 6.36 Actividad GSuite Application Scope

- Para **procesamiento de datos** (Google Sheets, Google Drive, Google Docs): `AuthenticationType = ServiceAccountKey`.
- Para **envío de correos Gmail**: `AuthenticationType = OAuthClientID`.
- OBLIGATORIO: agregar `Log Message` al inicio y fin del scope GSuite.

---

### 6.37 Recorrido de tablas de datos

- OBLIGATORIO: al hacer búsquedas en DataTables usar el **nombre de la columna**, no el índice.
- El nombre de la columna debe provenir del archivo config: `in_Config("NombreColumna").ToString`
- Si se usa índice: debe estar justificado y provenir igualmente del archivo config.
- Incorrecto: `ColumnIndex = 0` (hardcode del índice).
- Correcto: `ColumnName = in_Config("LicenseType").ToString`.

---

### 6.38 Navegación entre páginas

- OBLIGATORIO: usar la actividad `Navigate To` para moverse entre páginas, portales o aplicaciones web.
- PROHIBIDO: usar clicks para navegar entre URLs (puede ser inestable).
- Antes o después del `Navigate To`: agregar `Log Message` con la URL destino.

---

### 6.39 Validación de String vacío

- PROHIBIDO: usar `MiVariableString.Equals("")` o `MiVariableString = ""`.
- OBLIGATORIO: usar `String.IsNullOrEmpty(MiVariableString)`.

---

### 6.40 Uso de rutas absolutas

- PROHIBIDO: obtener la ruta del proyecto desde el config, ni introducirla en hardcode.
- OBLIGATORIO: usar el método `Directory.GetCurrentDirectory` para rutas relativas al proyecto.
- Correcto: `Directory.GetCurrentDirectory + "\DocsPorProcesar"`
- Incorrecto: `"C:\Users\Usuario\Documents\UiPath\Proyecto\DocsPorProcesar"`

---

### Manejo de errores completo (UiPath)

- Envolver la lógica principal en `Try Catch`.
- Tipos de excepción en el Catch: preferir específicos (`SystemException`, `IOException`, etc.) sobre el genérico `Exception`.
- Mensaje en el Catch: `"Falló el procedimiento" + exception.ToString`
- Nivel del Log en Catch: `Fatal` o `Error`.
- Para transacciones en Orchestrator:
  - Error técnico → `ApplicationException` → puede reintentarse.
  - Error de datos → `BusinessException` → no reintentarse.
- Usar `Retry Scope` para reintentos configurados (max 3 para acciones, max 2 para login).

---

### Verificación final antes de incluir un prompt UiPath

El skill de prompts debe verificar:

1. ¿Las variables usan UpperCamelCase y el prefijo de tipo correcto?
2. ¿Los argumentos tienen prefijo `in_`, `out_` o `io_` con primera letra minúscula?
3. ¿Hay valores hardcodeados (rutas, correos, tiempos, credenciales)?
4. ¿La condición If tiene la acción principal en el bloque Then?
5. ¿El Switch tiene acción en el caso Default?
6. ¿El Try Catch tiene Log Message con nivel Error/Fatal en el Catch?
7. ¿Los correos se guardan como borrador si tienen información sensible?
8. ¿Los Delay usan constantes del config (no valor fijo)?
9. ¿Los selectores evitan `idx` alto y `css`?
10. ¿Los DataTables se recorren por nombre de columna (del config), no por índice?
11. ¿El Retry Scope para login tiene máximo 2 reintentos, y para otras acciones máximo 3?
12. ¿Se usa `String.IsNullOrEmpty` en lugar de comparación directa con `""`?
13. ¿Se usa `Directory.GetCurrentDirectory` para rutas internas del proyecto?
14. ¿El nombre del XAML coincide con el nombre de la secuencia principal?
15. ¿Los Log Message tienen el nivel correcto (Trace, Info, Warn, Error, Fatal)?
16. ¿Las actividades tienen nombres descriptivos únicos (no solo el nombre default)?
17. ¿Las secuencias no tienen nombres genéricos (`Sequence`, `Do`, `Body`)?
18. ¿Las variables están declaradas en el scope más interno posible?
19. ¿Se eliminaron variables y argumentos no utilizados?
20. ¿El ID de requerimiento está anotado en la secuencia correspondiente?

Si alguna respuesta es NO → corregir antes de incluir el prompt.

---

## Sección: Automation Anywhere

Aplica cuando `tech_key = "automation_anywhere"`.

---

### I. Principios fundamentales

Los cuatro preceptos que guían toda revisión de código en AA son los mismos que los generales: Mantenibilidad, Legibilidad, Confiabilidad y Eficiencia.

---

### II. Reglas generales y arquitectura

#### Estructura de carpetas
- Crear tres carpetas principales en el proyecto:
  - `Framework`: módulos de AA (excepto Main/FrameworkV3).
  - `Process`: taskbots del proyecto (lógica de negocio).
  - `Data`: archivos de configuración, scripts, archivos auxiliares.
- Organizar bots dentro de `Process` por proceso/aplicación.

#### Framework (BeeFramework o equivalente)
- OBLIGATORIO: usar un Framework como base de todo proceso nuevo.
- El taskbot principal (`FrameworkV3`) debe manejar las etapas:
  - **Init**: inicialización de configuración y aplicaciones.
  - **Get Transaction Data**: obtención del siguiente ítem a procesar.
  - **End Process**: cierre de aplicaciones y notificación final.
- El framework proporciona consistencia, reduce el tiempo de desarrollo y asegura buenas prácticas.

#### Archivo de configuración (Config)
- El archivo de configuración es primordial para evitar código duro.
- Debe tener dos hojas/secciones:
  - `Settings`: datos con probabilidad de cambio.
  - `Constants`: constantes del proceso.
- PROHIBIDO: hardcode de valores que deben estar en el config.

#### Rutas con nombre de usuario de máquina
- OBLIGATORIO: usar variables para rutas que contengan el nombre de usuario de la máquina.
- Ejemplo correcto: `C:\Users\{Usuario}\Documents` donde `{Usuario}` es una variable dinámica.
- PROHIBIDO: rutas absolutas con nombre de usuario hardcodeado.

#### Archivos en Azure DevOps
- OBLIGATORIO: subir los archivos extraídos del Zip del Control Room al repositorio de Azure DevOps para facilitar la revisión de código.

#### Pruebas y producción
- OBLIGATORIO: remover todos los elementos generados para pruebas (unitarias o de testing) antes de pasar a producción.

#### Bots desatendidos
- PROHIBIDO: usar actividades que requieran interacción humana como `Message Box` o `Prompt` en bots desatendidos.

#### Análisis de código (Code Analysis)
- RECOMENDADO: usar la herramienta **Code Analysis Result (Assistant)** de AA.
- Objetivo: alcanzar el estatus **"No violations"**.

---

### III. Variables

#### Nomenclatura general
- Estilo **UpperCamelCase** con nombres significativos.
- PROHIBIDO: caracteres especiales en nombres de variables.
- Los mismos prefijos de tipo Beecker aplican plenamente:

| Tipo | Prefijo | Ejemplo |
|---|---|---|
| Boolean | `Bln` | `BlnProcesoCorrecto` |
| Integer | `Int` | `IntContadorRegistros` |
| Float | `Flt` | `FltTotalFactura` |
| String | `Str` | `StrRutaArchivo` |
| Object | `Obj` | `ObjRespuestaApi` |
| Array | `Arr` | `ArrFilasExcel` |
| List | `Lst` | `LstCorreosPendientes` |
| DataTable | `dt_` | `dt_DatosCorreo` |
| Dictionary | `Dic` | `DicConfiguracion` |

#### Prefijos de dirección
- `in_` → variables de **entrada** → `in_StrUrlSistema`
- `out_` → variables de **salida** → `out_BlnProcesoExitoso`
- `io_` → variables de **entrada y salida** → `io_ArrParametro`
- Primera letra del prefijo siempre **minúscula**.

#### Variables de ventana/browser
- El nombre debe iniciar con la aplicación que interactúa, seguido de un nombre descriptivo en UpperCamelCase.
- Usar comodines (`*`) en la propiedad **Título de la ventana** para mayor robustez.
- Ejemplo: `SAPLoginVentana`, `ChromePortalCliente`

#### Código duro (Hardcode)
PROHIBIDO incluir valores fijos para:
- Contraseñas o credenciales
- Retrasos (tiempos de espera)
- Número de reintentos
- Rutas internas o de red
- Nombres de archivos
- Hojas de archivos (Excel, etc.)
- Columnas de tablas de datos
- Rutas web (URLs)
- Correos electrónicos de destinatarios
- Información sensible del cliente

#### Constantes
- Las variables que no cambian (constantes) deben obtener su valor desde el archivo `config`.
- PROHIBIDO: inicializar constantes con valor fijo en el código.

#### Credenciales
- OBLIGATORIO: almacenar todos los IDs de usuario y contraseñas en la **Bóveda de Credenciales (Credential Vault)** del Control Room.
- PROHIBIDO: hardcode de credenciales en cualquier parte del bot.

#### Variables no utilizadas
- OBLIGATORIO: eliminar todas las variables no utilizadas del taskbot.
- Las variables sin uso hacen el proyecto más difícil de entender.

---

### IV. Taskbot y estructura de código

#### Nomenclatura de taskbots
- Formato: `App_NombreTaskbot` donde `App` es la aplicación principal o portal.
- Si no hay aplicación principal: usar prefijo `General_`.
- Estilo UpperCamelCase.
- Ejemplos correctos: `SAP_IngresarFactura`, `Excel_GenerarReporte`, `General_EnviarNotificacion`
- PROHIBIDO: nombres genéricos como `Bot1`, `Taskbot_nuevo`, `Proceso`.

#### Descripciones y Steps
- OBLIGATORIO: agregar una breve descripción textual al **inicio** de cada taskbot indicando su propósito.
- OBLIGATORIO: encapsular funcionalidades con acciones **Step** con nombres significativos.
- Los Steps son la unidad de agrupación lógica dentro del taskbot; cada uno debe describir claramente qué hace.

#### Comentarios
- OBLIGATORIO: documentar el código a lo largo del taskbot.
- Cantidad de comentarios: aproximadamente el **30% de las líneas de código** utilizadas.
- El conteo de líneas para el 30% excluye: Steps, AddToLog, Error Handler y Comments.

#### Trazabilidad de requerimientos (CMMI)
- OBLIGATORIO: añadir el ID de requerimiento (obtenido del DFR, DAT o Azure DevOps) al taskbot correspondiente como un **Step** con el ID y descripción.
- Formato: `Step "ID: [ID_REQ] - [Descripcion breve]"` → ejemplo: `Step "ID: NYB.013.002.001 - Iniciar sesión en LinkedIn"`

#### Flujo saturado
- Máximo **180 líneas de código** por taskbot.
- Si se excede: dividir en taskbots más pequeños y llamarlos con `Run Task`.

#### Anidamiento
- Máximo **7 niveles** de anidación total en un taskbot.
- Máximo **3 niveles** de anidación para actividades `If`.
- Si se excede: extraer a un taskbot separado.

#### If-Then
- OBLIGATORIO: definir la condición para que el código principal pase por la rama **If (verdadera)**.
- PROHIBIDO: bloque `If` vacío con toda la lógica en `Else`.
- Invertir la condición si es necesario para que la acción principal quede en la rama verdadera.

#### Acciones vacías o inhabilitadas
- PROHIBIDO: dejar acciones inhabilitadas o vacías en el flujo de trabajo.
- Eliminar cualquier acción que no se use o que esté comentada/deshabilitada.

---

### V. Log, manejo de errores y optimización

#### Error Handler (estructura obligatoria)
- OBLIGATORIO: cada taskbot debe tener un `Error handler: Try` que abarque la **totalidad del código**.
- El `Error handler: Catch` correspondiente debe:
  - Usar variables para almacenar `Exception message` y `Line Number`.
  - Llamar al taskbot `AddToLog` con nivel **Error** registrando estos valores.
- PROHIBIDO: bloque Catch vacío (sin log, sin notificación).

#### Uso de AddToLog
- OBLIGATORIO: usar el taskbot reutilizable `AddToLog` en:
  - **Inicio** de cada módulo/taskbot.
  - **Final** de cada módulo/taskbot.
  - Puntos importantes del proceso: interacción con aplicaciones externas, subida/descarga de archivos, actividades Try Catch, etc.
- Cantidad mínima de `AddToLog`: **20% de las líneas de código** del taskbot.

#### Niveles de log
| Nivel | Cuándo usarlo |
|---|---|
| `Error` | Errores fatales para la operación; se registra en el Catch del Error Handler |
| `Info` | Progreso del proceso, inicio y cierre de módulos importantes |
| `Trace` | Rastreo específico de código para depuración |

#### Actividad Delay
- PROHIBIDO: usar `Delay` con valor hardcodeado.
- Priorizar acciones de espera inteligente:
  - `Wait for condition`
  - `Wait for screen change`
  - `Wait for window`
- Si el uso de `Delay` es estrictamente necesario: el valor del tiempo debe ser una variable traída del archivo `config`.

#### Acción Loop
- OBLIGATORIO: agregar un `Label` descriptivo a cada `Loop`, `Continue` o `Break`.
- La variable de control para reintentos debe obtenerse del `Config`.
- PROHIBIDO: loops sin etiqueta identificatoria.

#### Cierre de programas (Kill)
- Para cerrar un proceso: usar la acción `Application: Open program/file` con configuración `taskkill` y el parámetro que incluye el nombre del proceso y el nombre de usuario de la máquina.
- El nombre de la aplicación debe ser **parametrizable** (no hardcodeado).

#### Scripts
- PROHIBIDO: uso excesivo de scripts.
- Los valores ingresados en scripts deben ser **dinámicos** (no hardcodeados).
- Los scripts deben incluir un manejo de errores controlable desde Automation Anywhere.

---

### VI. Interacción con aplicaciones

#### Navegadores
- OBLIGATORIO: usar la actividad `Browser: Open` como la forma preferida de trabajar con navegadores web.
- PROHIBIDO: abrir navegadores mediante `Run Program` o atajos del sistema operativo.

#### Recorder
- Usar la opción **Cambiar tamaño de ventana (Size Window)** al grabar.
- Priorizar la acción **Click** sobre `Left click` en las grabaciones.

#### Set Text
- Al usar `Set text`: establecer la propiedad **Time between keystrokes (milliseconds)** en **40ms**.
- PROHIBIDO: dejar el valor default si genera inestabilidad en la escritura.

#### Excel
- PROHIBIDO: usar actividades `Recorder` o `Simulate keystrokes` para interactuar con Excel.
- OBLIGATORIO: usar las actividades designadas de la integración de Excel o macros.

#### Propiedades HTML
- PROHIBIDO: usar `HTML Href` y `HTML FrameSrc` directamente por ser poco confiables.
- Si son requeridas: modificar su valor usando el comodín (`*`).

#### SAP
- Jerarquía de acciones para SAP (prioridad descendente):
  1. **Paquetería SAP** (actividades nativas SAP de AA).
  2. **Recorder: Capture**.
  3. **Scripts** (último recurso).
- OBLIGATORIO: priorizar la acción **SAP: Click** sobre otras alternativas.

#### Sesiones
- OBLIGATORIO: dar un nombre descriptivo a cada sesión.
- OBLIGATORIO: cerrar la sesión **en el mismo taskbot** en que se abre.
- PROHIBIDO: sesiones abiertas que se cierran en taskbots diferentes al de apertura.

#### Envío de correos
- Política del CoE: los robots **NO deben enviar correos directamente**.
- Los correos creados por robots deben guardarse como **borradores** para revisión humana.
- Excepción: correos genéricos sin información sensible.
- OBLIGATORIO: toda la información del correo debe ser **parametrizable**: asunto, cuerpo, destinatarios, archivos adjuntos.
- PROHIBIDO: hardcode de destinatarios, asunto o cuerpo del correo.

### VII. Arquitectura del Framework AA (referencia técnica)
 
Esta sección describe la arquitectura del BeeFramework de AA. El skill de prompts la usa para generar referencias correctas a módulos, variables y flujos del framework en los campos `instruccion_previa` y `nota_desarrollador`.
 
#### Componentes principales del Framework
 
| Componente | Qué hace | Clave de config asociada |
|---|---|---|
| **Config File** | Centraliza rutas, URLs y parámetros de entorno. Ubicado en ruta local o compartida. | — |
| **ReadConfig** | Lee hojas `Settings`, `Constants` y `Assets`. Almacena datos en el diccionario `Config`. Reemplaza etiquetas dinámicas `{user}` y `{year}`. | — |
| **Create Bot Folders** | Genera jerarquía de carpetas: `Log`, `Data`, `Screenshot`, `Input`, `Output`, `Temp` basándose en el `ProcessID`. | `ProcessID` |
| **Prepare Environment** | Limpia el entorno: cierra navegadores y termina procesos definidos en `Taskkill`. | `Taskkill` |
| **Get Credentials** | Extrae credenciales del Control Room vía Credential Utilities e integra al diccionario `Config` (hoja `Assets`). | hoja `Assets` |
 
#### Gestión de transacciones (Get Transaction Data)
 
La clave `TypeTransactionData` del config define el flujo:
 
- **Transactional (Excel)**: itera sobre cada fila del archivo de entrada. Cada fila es un `TransactionItem`.
- **Lineal**: camino de decisión único para procesos sin múltiples ítems independientes.
#### Procesamiento y manejo de errores (Process)
 
- **Reintentos**: en flujos transaccionales, máximo **3 reintentos** ante fallas de sistema.
- Variables de entrada obligatorias en cada módulo de proceso:
  - `In_Config` → Diccionario con la configuración completa.
  - `In_Transaction` → Fila/ítem actual en procesamiento.
  - `io_ErrorMessage` → Captura del mensaje de error.
  - `io_ErrorLineNumber` → Captura del número de línea del error.
- Flujo del Error Handler ante un fallo:
  1. Captura la excepción.
  2. Registra el fallo en el Log (AddToLog nivel Error).
  3. Captura **Screenshot** si el nivel es "Error".
  4. Determina si reintenta o termina la ejecución.
#### Finalización y limpieza (End Process)
 
1. **End Process**: tareas post-procesamiento (correos finales, cierre de sesión, borrado de temporales).
2. **Device Cleanup**: borrado de logs y capturas antiguas según el tiempo definido en `TimeStorage`.
3. **Clean Environment**: cierre final de aplicaciones para dejar la máquina lista para el siguiente bot.
#### Módulos reutilizables del Framework
 
**Task SendMail** — gestiona correos parametrizados para 4 escenarios:
- Inicio del proceso.
- Finalización del proceso.
- Seguimiento (*Follow-up*).
- Error (los destinatarios del Catch general deben ser variables globales por si el Config falla).
**Task AddToLog** — genera un archivo CSV diario con:
- Hora exacta del evento.
- Nivel de log (`Info`, `Trace`, `Error`).
- Módulo origen.
- Nombre de la captura de pantalla (en caso de error).
#### Cómo usar esta referencia al generar prompts AA
 
- Si el prompt menciona leer configuración → referenciar `ReadConfig` y el diccionario `Config`.
- Si el prompt menciona manejo de errores → referenciar el bloque Try-Catch con `io_ErrorMessage`, `io_ErrorLineNumber`, `AddToLog` y captura de Screenshot.
- Si el prompt menciona envío de correos → referenciar `Task SendMail` con sus 4 escenarios.
- Si el prompt menciona logging → referenciar `Task AddToLog` y sus campos (hora, nivel, módulo, screenshot).
- Si el prompt menciona credenciales → referenciar `Get Credentials` y la hoja `Assets` del config.
- Si el prompt menciona carpetas de trabajo → referenciar `Create Bot Folders` y la clave `ProcessID`.
- Si el prompt menciona limpieza del entorno → referenciar `Prepare Environment` (clave `Taskkill`) y `Clean Environment`.
- Si el prompt es para un proceso transaccional → indicar uso de `TypeTransactionData = Transactional` y la variable `In_Transaction`.
- Si el prompt es para un proceso lineal → indicar uso de `TypeTransactionData = Lineal`.
---
 
### Verificación final antes de incluir un prompt de AA
 
El skill de prompts debe verificar:
 
1. ¿Las variables usan UpperCamelCase con el prefijo de tipo correcto (`Str`, `Int`, `Bln`, etc.)?
2. ¿Las variables de dirección tienen prefijo `in_`, `out_` o `io_`?
3. ¿Hay valores hardcodeados que deban ser variables del config?
4. ¿Las credenciales se obtienen de la Bóveda de Credenciales (Credential Vault)?
5. ¿Las rutas con nombre de usuario usan variables dinámicas?
6. ¿El nombre del taskbot sigue el formato `App_NombreTaskbot`?
7. ¿El taskbot tiene Step con el ID de requerimiento para trazabilidad CMMI?
8. ¿El taskbot tiene descripción textual al inicio?
9. ¿Hay un `Error handler: Try` que cubra la totalidad del código?
10. ¿El Catch registra `Exception message` y `Line Number` con AddToLog nivel Error?
11. ¿Hay `AddToLog` al inicio y fin del módulo (mínimo 20% de las líneas)?
12. ¿Los `Delay` usan variables del config (no valores fijos)?
13. ¿Los `Loop` tienen Label descriptivo?
14. ¿La condición If tiene el código principal en la rama verdadera (no en Else)?
15. ¿Se eliminaron acciones vacías o inhabilitadas?
16. ¿Se eliminaron variables no utilizadas?
17. ¿Los correos se guardan como borrador si tienen información sensible?
18. ¿Excel usa actividades nativas de integración (no Recorder/keystrokes)?
19. ¿SAP usa la paquetería SAP nativa como primera opción?
20. ¿Las sesiones se cierran en el mismo taskbot donde se abren?
21. ¿El taskbot no supera las 180 líneas de código?
22. ¿El nivel de anidación no supera 7 niveles (3 para If)?
Si alguna respuesta es NO → corregir antes de incluir el prompt.
 
---

## Cómo aplican las reglas en la generación de prompts

Cada skill de prompts debe verificar estas reglas al construir cada bloque:

### En el campo `prompt` (texto copia-pega)
- Las variables mencionadas siguen el prefijo de tipo correcto para la tecnología.
- Los nombres de subflujo/scope/workflow son UpperCamelCase sin acentos ni caracteres especiales.
- No hay valores hardcodeados (rutas, correos, URLs fijas, tiempos, reintentos).
- Si la acción implica un retraso: usar la alternativa recomendada, no Delay/Retraso fijo.
- Si hay condición If: mencionar que la acción principal va en el bloque True.
- Si hay Switch: mencionar que el caso Predeterminado no puede estar vacío.

### En el campo `instruccion_previa`
- PAD: recordar al usuario crear el subflujo manualmente y agregar acción Comentario con req ID.
- Cloud: indicar dónde pegar el prompt (pantalla de creación vs panel Copilot).
- UiPath: indicar el workflow `.xaml` donde agregar las actividades.
- AA: indicar el Task Bot y la sección donde agregar las acciones.

### En el campo `nota_desarrollador`
- Mencionar la regla de buena práctica específica que aplica al prompt. Ejemplos:
  - "REGLA Beecker: los selectores UI requieren grabación manual con el grabador de PAD."
  - "REGLA Beecker: agregar acción Comentario al inicio del subflujo con propósito y req ID."
  - "REGLA Beecker: el valor del timeout debe venir de la configuración, no hardcodeado."
  - "REGLA Beecker: correos con información sensible deben guardarse como borrador."
  - "REGLA Beecker: agregar Log (AddToLog) al inicio y fin de este subflujo."
  - "REGLA Beecker: el caso Predeterminado del Switch no debe estar vacío."
  - "REGLA Beecker: mínimo 33% de acciones/scopes deben tener nota o descripción."
  - "REGLA Beecker: eliminar variables inicializadas que no se usen en el flujo."
- Mencionar si el req tiene lógica que podría violar el límite de 3 niveles de anidación.
- Indicar los paquetes/dependencias necesarios para UiPath o AA.

---

## Verificación antes de incluir un prompt en el .toon

El skill de prompts debe verificar estas preguntas antes de cerrar cada bloque `@prompt`:

1. ¿Las variables usan el prefijo de tipo correcto para la tecnología?
2. ¿El nombre del subflujo/scope/workflow es UpperCamelCase sin acentos ni caracteres especiales?
3. ¿Hay algún valor hardcodeado que deba ser placeholder?
4. ¿La condición If tiene la acción principal en el bloque True (no en False)?
5. ¿El Switch tiene acción en el caso Predeterminado?
6. ¿El manejo de errores incluye al menos un log (AddToLog)?
7. ¿Los correos se guardan como borrador si tienen información sensible?
8. ¿Los retrasos usan la alternativa recomendada (no Delay/Retraso fijo)?
9. ¿La nota_desarrollador menciona las reglas Beecker relevantes para este prompt?
10. ¿El prompt respeta el límite de caracteres de la tecnología (500 PAD / 2000 Cloud)?
11. ¿La instruccion_previa menciona el req ID para rastreabilidad?
12. ¿Se eliminaron o evitaron variables sin utilizar en el flujo?
13. ¿El scope/región no está vacío ni tiene una sola acción?
14. ¿Las ramas paralelas de inicialización de variables en Cloud no superan 5?
15. ¿Las acciones en Cloud tienen nombre descriptivo (no solo el nombre default)?

Si alguna respuesta es NO → corregir antes de incluir el prompt en el .toon.

---
