# Buenas Prácticas — UiPath

Fuente oficial: Manual Buenas Prácticas UiPath — Beecker (MCR_UP_06, septiembre 2023).
Aplica cuando `tech_key = "uipath"`.

---

## Preceptos de calidad (fundamento de todas las reglas)

- **Mantenibilidad**: facilidad de extender, modificar y corregir el bot.
- **Legibilidad**: código con comentarios, anotaciones y nombres significativos.
- **Confiabilidad**: manejo de excepciones y reporte de errores.
- **Eficiencia**: el bot alcanza el objetivo sin gastar recursos innecesarios.

---

## Reglas comunes a todas las tecnologías (aplican en UiPath)

### Nomenclatura de variables

Estilo **UpperCamelCase**. La primera palabra indica el tipo de dato.

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

Parámetros (argumentos) entre workflows — prefijos de dirección:
- Entrada: `in_` → `in_StrNombreEntrada`
- Salida: `out_` → `out_StrNombreSalida`
- Entrada y salida: `io_` → `io_ArrParametro`
- La primera letra del prefijo es **minúscula**.

PROHIBIDO: variables sin prefijo de tipo, nombres genéricos sin contexto (`variable1`, `dato`, `resultado`).

### Hardcode prohibido
NUNCA incluir valores fijos para: credenciales, retrasos (Delay), número de reintentos, rutas internas, nombres de archivos, hojas de Excel, columnas de tablas, URLs, correos electrónicos, información sensible del cliente.
- Correcto: usar Assets, Config.xlsx o variables parametrizadas.
- Credenciales: almacenar siempre en Assets tipo Credential o Windows Credentials como **SecureString**.
- PROHIBIDO: introducir datos hardcodeados en actividades `Invoke Workflow` al hacer llamado de otros procesos.

### Correos electrónicos
- Los correos creados por robots deben guardarse como **BORRADORES** para revisión humana.
- Excepción: correos genéricos sin información sensible.
- PROHIBIDO: hardcode de destinatarios, asunto o cuerpo del correo. Todo debe ser parametrizable.
- Para Gmail: usar actividades nativas de la librería UiPath para Gmail (`Use Gmail with main account`).
- PROHIBIDO en protocolos SMTP/IMAP: hardcode de Port, Server o correo electrónico. Obtener como Assets.

### Condición If — bloque Then
- La acción principal SIEMPRE debe estar en el bloque **Then** (rama verdadera).
- PROHIBIDO: bloque Then vacío con toda la lógica en Else.
- Si la condición original pone la acción en Else → invertir la condición para que quede en Then.

### Anidación de condiciones
- Máximo **2 niveles** de anidación de actividades If (Decisión).
- Si se requieren más de 2 niveles: usar `Flow Decision` dentro de un Flowchart.

### Flujos saturados
- Máximo **6 niveles** de anidación en un workflow.
- Si se excede: separar en workflows más pequeños usando `Invoke Workflow File`.

### Mensajes de registro (Log Message)
- OBLIGATORIO: agregar `Log Message` al **inicio** y al **final** de cada módulo principal.
- Agregar también en puntos intermedios relevantes.
- Niveles:

| Nivel   | Cuándo usarlo |
|---------|---------------|
| `Fatal` | Error que obliga a cerrar el servicio; corrupción de datos |
| `Error` | Error fatal para la operación (archivo no encontrado, datos faltantes) |
| `Warn`  | Situación anómala recuperable automáticamente |
| `Info`  | Inicio/fin de módulos importantes, progreso del proceso |
| `Trace` | Rastreo de código para depuración específica |

- Formato recomendado: `"[NombreModulo] - [descripcion_accion]"`

### Manejo de errores (Try Catch)
- OBLIGATORIO: insertar `Log Message` en el bloque `Catch` con nivel `Fatal` o `Error`.
- Mensaje: `"Falló el procedimiento" + exception.ToString`
- PROHIBIDO: bloque Catch vacío.
- Especificar el tipo de excepción correcto (no usar `Exception` genérico cuando se conoce el tipo).

### Variables sin utilizar
- OBLIGATORIO: eliminar variables y argumentos no utilizados del flujo.

---

## Reglas específicas de UiPath

### Fundamentos del diseño
- Usar módulos para realizar pruebas independientes y mantener orden.
- Manejar un estándar entre las carpetas del proyecto.
- Uso obligatorio del **BeeFramework** (o REFramework estándar con VB si BeeFramework no está disponible).
- OBLIGATORIO: revisar todos los mensajes o textos entregados/mostrados al cliente; verificar ortografía.

### Capas RPA
Cada bot debe respetar las siguientes capas:

| Capa | Contenido |
|---|---|
| **Framework** | Módulos del framework (Init, GetTransaction, etc.) |
| **Business Process** | Workflows con las reglas del negocio |
| **Services** | Scripts y Workflows que consumen Web Services |
| **Application Process** | Workflows con interacción gráfica Y validación de reglas de negocio |
| **Application Screen** | Workflows con interacción gráfica SIN validar reglas de negocio |
| **Data** | Workflows con interacción con datos locales, bases de datos o archivos de configuración |

### BeeFramework / REFramework — etapas obligatorias

| Etapa | Descripción |
|---|---|
| `InitAllSettings` | Inicia valores necesarios: Config.xlsx, valores del Orchestrator |
| `InitAllApplications` | Abre las aplicaciones requeridas |
| `KillAllProcesses` | Cierra procesos en caso de error |
| `GetOrchestratorCredentials` | Obtiene credenciales del Orchestrator por AssetName |
| `GetTransactionData` | Obtiene el siguiente ítem de la cola |
| `SetTransactionStatus` | Marca el ítem como Success, BusinessException o ApplicationException |
| `CloseAllApplications` | Cierra todas las aplicaciones al finalizar |
| `FinalizateProcess` | Finaliza el proceso y envía notificación |

OBLIGATORIO en `Main.xaml`: agregar anotaciones con `ID:`, `Nombre:`, `Desarrollador:`, `Aplicaciones:`.

### Nombre del proyecto
- Formato: `ID-NombreDelProyecto` → ejemplo: `NYB.001-GenerateYearlyReport`
- Descripción: funcionalidad del proyecto.
- PROHIBIDO: agregar versión, número de Sprint o Change Request al nombre del proyecto.
  - Incorrecto: `NYB.001-GenerateYearlyReport_S1`
  - Correcto: `NYB.001-GenerateYearlyReport`

### Archivo de configuración (Config.xlsx)
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

### Bots atendidos y desatendidos
- **Bot desatendido**: PROHIBIDO usar `Input Dialog` o `Message Box` (generan retrasos y conflictos).

### Nomenclatura de variables — reglas adicionales UiPath
- DataTables: prefijo `dt_` en **minúscula** → `dt_Recorrido` (incorrecto: `DT_Recorrido`).
- OBLIGATORIO: cambiar el nombre de la variable de bucle `item` en For Each por un nombre descriptivo con TypeArgument correcto.
- PROHIBIDO: dos variables con el mismo nombre; una variable y un argumento con el mismo nombre.
- Las variables deben definirse en el **scope más interno posible**.
- Las constantes deben traer su valor desde el config, no inicializar con valor fijo.
- PROHIBIDO: argumentos con valores default o inicialización hardcodeada.
- OBLIGATORIO: todos los argumentos deben tener descripción detallada (Design Properties).

### Nomenclatura para XAML
- UpperCamelCase sin espacios. Incluir prefijo de la aplicación o carpeta principal.
- La secuencia principal dentro del archivo debe tener el **mismo nombre que el archivo XAML**.
- PROHIBIDO: acentos, caracteres especiales, Ñ/ñ.
- Correcto: `APIGoogle_CargaGoogleDrive.xaml` con secuencia principal `APIGoogle_CargaGoogleDrive`.

### Nombre de secuencias
- PROHIBIDO: nombres por defecto como `Sequence`, `Do`, `Body`.
- Correcto: `LoginEnSistema`, `ProcesarTransaccion`, `ObtenerDatosExcel`.

### Estructura de carpetas
- `Framework/`: todos los módulos del framework.
- `Process/`: subcarpetas con nombre de aplicación en UpperCamelCase. Cada módulo lleva el prefijo de su carpeta.
- Archivos inamovibles: `Main.xaml`, `Process.xaml`, `project.json`.
- OBLIGATORIO: remover la carpeta `Tests` antes de pasar a producción.
- RECOMENDADO: remover o comprimir `.screenshots` antes de subir a Orchestrator.

### Flujo de trabajo adecuado
- **Flowchart**: para flujos con decisiones múltiples y/o complejas.
- **Sequence**: para flujos puramente secuenciales.

### Comment Out
- PROHIBIDO: dejar actividades comentadas (`Comment Out`) o sin conectar a ningún nodo.
- Las actividades comentadas deben eliminarse.

### Switch
- OBLIGATORIO: siempre realizar una acción en el apartado **Default**.
- PROHIBIDO: Default vacío.

### Secuencias o diagramas vacíos
- PROHIBIDO: secuencias vacías o que contengan solo **una** actividad interna.

### Descripción en flujo de trabajo
- La actividad de nivel superior (generalmente el Sequence o Flowchart principal) de cada workflow debe tener una **breve descripción textual** que indique:
  - Objetivo del workflow
  - Entradas y salidas
  - Condiciones previas y resultados esperados
- Esto ayuda a otros desarrolladores a comprender rápidamente el propósito del módulo.


### Id de requerimiento (rastreabilidad CMMI)
- OBLIGATORIO: añadir el ID de requerimiento como anotación en la secuencia correspondiente.
- Formato: `[ID]\n[Descripción breve]` → ejemplo: `NYB.013.002.001\nIniciar sesión en LinkedIn`.

### Actividades IF anidadas
- Máximo **2 niveles** de anidación de actividades If.
- Si se requieren más: usar `Flow Decision` dentro de un Flowchart.

### Actividad Paralela
- Si es necesario usarla: agregar **anotación** que explique la situación.
- PROHIBIDO: usar sin justificación documentada.

### Actividades basadas en imágenes
- PROHIBIDO (general): `Click Image`, `Wait Image Vanish`.
- Excepción: solo si existe justificación fundamentada con anotación.

### Selector idx y Selector CSS
- `idx` debe mantenerse en valor **bajo (1 o 2)**.
- PROHIBIDO: selector `css`.
- Si `idx` es 3 o mayor: agregar anotación justificando y envolver en `Retry Scope`.

### Actividad Attach
- RECOMENDADO: usar `Attach Window` o `Attach Browser` para todas las actividades UI.
- `Send Hotkey`: usar solo como último recurso; debe tener imagen de referencia y selector confiable, preferiblemente dentro de Attach.

### Títulos genéricos y estándar

- Los nombres de las actividades deben dar una idea clara de cómo se utilizan.
- Agregar información adicional cuando el nombre default sea demasiado genérico.
- Los nombres de actividades deben ser **únicos e irrepetibles**.
- Excepciones (no aplica esta regla): `Log Message`, `Write Line`, `Invoke`.
- PROHIBIDO: numeración en nombres (`Actividad 1`, `Actividad 2`). Usar: `Primera Actividad`, `Segunda Actividad`.
- Incorrecto: `Sequence`, `Open Browser`, `Click`, `Do`
- Correcto: `Secuencia para abrir Navegador`, `Abrir Navegador Beeckerco`, `Click en botón`, `Hacer Después de abrir Navegador`

### Elementos UI Automation en Excel
- PROHIBIDO: usar actividades UI Automation (`Get Text`, `Click`, `Send Hotkey`) para interactuar con Excel.
- OBLIGATORIO: usar actividades designadas de integración de Excel (Excel Application Scope, Read Range, Write Range, etc.).

### Actividad Delay
- PROHIBIDO: usar `Delay` con valor hardcodeado.
- Reemplazar por espera inteligente: `On Element Appear`, `Wait for Download`, `Wait Image Vanish`, o `Timeout` en las propias actividades UI.
- Si es estrictamente necesario: el valor DEBE venir de config (`DelayShort`, `DelayMedium`, `DelayLong`). OBLIGATORIO: agregar anotación con el motivo.

### Open Browser
- OBLIGATORIO: usar `Open Browser` (o `Attach Browser`) para trabajar con navegadores.
- PROHIBIDO: usar `Open Application` o `Start Process` para abrir navegadores.

### Actividades de interacción con usuario
- PROHIBIDO en bots desatendidos: `Message Box` o `Input Dialog`.

### SimulateType y SendWindowMessages
- OBLIGATORIO: habilitar `SimulateType = True` siempre que sea posible.
- Si el control no lo soporta: agregar anotación explicando el motivo.

### Bucles Infinitos
- PROHIBIDO: bucles infinitos en `Flow Decision`.
- Siempre incluir mecanismo de salida: `Throw` o `Try Catch`.
- PROHIBIDO: módulos que hagan `Invoke` a sí mismos.

### Retry Scope
- OBLIGATORIO: usar `Retry Scope` siempre que se haga un login (máximo **2 reintentos**).
- Para otras acciones: máximo **3 reintentos**.
- OBLIGATORIO: agregar `Log Message` con nivel `Trace` dentro del Retry Scope.
- El número de reintentos para login debe venir del config: `ReintentoLogin`.

### Control de excepción en transacciones con Orchestrator
- **ApplicationException**: error técnico (app no responde). Orchestrator puede reintentar si `Auto Retry = Yes`.
- **BusinessException**: error de datos (campo vacío, dígito faltante). NO reintentar; notificar al usuario.

### Uso de excepciones específicas
Preferir sobre el genérico `Exception`:
`SystemException`, `IOException`, `NullReferenceException`, `InvalidOperationException`, `ArgumentException`.

### Actividad Element Exists
- Selector confiable con imagen de referencia.
- Timeout desde config: `CInt(in_Config("DelayShort"))`.
- `WaitForReady` en `COMPLETE`.
- PROHIBIDO: Timeout hardcodeado.

### Recorrido de tablas de datos
- OBLIGATORIO: usar el **nombre de la columna** (del config), no el índice.
- Correcto: `ColumnName = in_Config("LicenseType").ToString`.

### Navegación entre páginas
- OBLIGATORIO: usar `Navigate To` para moverse entre URLs.
- PROHIBIDO: usar clicks para navegar entre URLs.
- Antes o después del `Navigate To`: agregar `Log Message` con la URL destino.

### Validación de String vacío
- PROHIBIDO: `MiVariableString.Equals("")` o `MiVariableString = ""`.
- OBLIGATORIO: usar `String.IsNullOrEmpty(MiVariableString)`.

### Uso de rutas absolutas
- PROHIBIDO: obtener la ruta del proyecto desde el config o en hardcode.
- OBLIGATORIO: usar `Directory.GetCurrentDirectory` para rutas relativas al proyecto.

### Propiedad EmptyField
- Al ingresar datos repetitivamente en un campo: establecer `EmptyField = True` antes de cada ingreso.

### GSuite Application Scope
- Para procesamiento de datos: `AuthenticationType = ServiceAccountKey`.
- Para envío de correos Gmail: `AuthenticationType = OAuthClientID`.
- OBLIGATORIO: `Log Message` al inicio y fin del scope GSuite.

### Git
- OBLIGATORIO: usar Git para llevar seguimiento de cambios.
- Formato del commit: `Fix<CR> <TT>: descripción breve de los cambios`.

### CloudShore DigitalWorkers
- OBLIGATORIO: incluir las librerías de Digital Workers en **todos** los proyectos, incluso si no usan SAP.

### Log Message

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

## Verificación final — aplicar antes de incluir cada prompt UiPath

1. ¿Las variables usan UpperCamelCase con prefijo de tipo correcto (Str, Int, Bln, dt_, Lst, etc.)?
2. ¿Los argumentos tienen prefijo `in_`, `out_` o `io_` con primera letra minúscula?
3. ¿Hay valores hardcodeados (rutas, correos, tiempos, credenciales)? → usar Assets o Config
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
