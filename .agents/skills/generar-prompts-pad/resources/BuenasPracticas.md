# Buenas Prácticas — Power Automate Desktop (PAD)

Fuente oficial: Manual Code Review Power Automate — Beecker (PAut_CR_02, octubre 2024).
Aplica cuando `tech_key = "power_automate_desktop"`.

---

## Preceptos de calidad (fundamento de todas las reglas)

- **Mantenibilidad**: facilidad de extender, modificar y corregir el bot.
- **Legibilidad**: código con comentarios, anotaciones y nombres significativos.
- **Confiabilidad**: manejo de excepciones y reporte de errores.
- **Eficiencia**: el bot alcanza el objetivo sin gastar recursos innecesarios.

---

## Reglas comunes a todas las tecnologías (aplican en Desktop)

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

Parámetros entre flujos:
- Entrada: `in_` → `in_IntNombreEntrada`
- Salida: `out_` → `out_StrNombreSalida`
- Entrada y salida: `io_` → `io_ArrParametro`
- La primera letra del argumento debe ser **minúscula**.

PROHIBIDO: variables sin prefijo de tipo, nombres genéricos sin contexto (`variable1`, `dato`, `resultado`).

### Variables sin utilizar
- Los flujos SOLO deben tener variables necesarias para su ejecución.
- OBLIGATORIO: eliminar la inicialización de variables que no se usan.

### Hardcode prohibido
NUNCA incluir valores fijos para: credenciales, retrasos, número de reintentos, rutas internas de red o disco, nombres de archivos, hojas de Excel, columnas de tablas, URLs, correos electrónicos, información sensible del cliente.

Si el PDD no provee el valor → usar placeholder descriptivo:
`[rutaArchivo\ruta\aqui\Archivo.xlsx]`, `[https://url-sistema-aqui]`, `[NombreHoja]`, . `[TuArchivo.xlsx]`, `[PASSWORD]`, `[TU_USUARIO]`

### Nomenclatura de subflujos
- Estilo **UpperCamelCase** sin espacios.
- Prefijo = aplicación principal con la que trabaja el subflujo.
- PROHIBIDO: acentos (á é í ó ú), caracteres especiales (# ¿ ? / \ : ; * < > [ ] $ & + % { } Ñ ñ).
- PROHIBIDO: versión, número de Sprint o Change Request en el nombre.
- Correctos: `JDE_DescargarLM`, `Excel_AjustarEC`, `Outlook_EnviarNotificacion`
- Incorrectos: `Subflujo1`, `ProcesarDatos`, `Flujo_correo`, `Verificación de correo`

### Correos electrónicos
- Según políticas del CoE: los robots NO deben enviar correos directamente.
- Los correos creados por robots deben guardarse como **BORRADORES** para revisión humana antes de enviar.
- Excepción: correos genéricos sin información sensible.
- Toda la información del correo debe ser **parametrizable**: asunto, cuerpo, destinatarios, etc.
- PROHIBIDO: hardcode de correos de destinatarios.

### Condición If — bloque True
- La acción principal SIEMPRE debe ejecutarse en el bloque **True**.
- PROHIBIDO: bloque True vacío.
- Si la condición original tiene la acción en False → invertir la lógica para que quede en True.

### Anidación de condiciones
- Máximo **3 niveles** de anidación de condiciones If/Else.
- Si se excede: extraer a subflujo separado.
- Indicar en `nota_desarrollador` cuando se detecte lógica con más de 3 niveles.

### Flujos saturados
- Máximo **6 niveles** de anidación total en un subflujo.
- Si se excede: separar usando `Ejecutar subflujo`.

### Mensajes de registro (Log)
- OBLIGATORIO: antes de ejecutar cualquier acción del subflujo, llamar al subflujo **AddToLog** del Framework.
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

### Mensajes de registro (Log) — detalle de campos
- StrLevel: usar solo estos niveles → Error, Warning, Info, Debug.
- StrModule: nombre del subflujo o módulo (ej. `SAP_Login`, `Excel_Export`).
- StrMessageLog: mensaje conciso del evento.
- PROHIBIDO usar mensajes descriptivos en el bloque de error. El bloque de error debe solo generar el log con mensaje de error genérico y ejecutar el subflujo AddToLog.
- En el bloque de error se deben crear variables de tipo texto que guarden los valores de las variables `StrLevel`, `StrModule` y `StrMessageLog` con los siguientes valores:
  - StrLevel: “Error”.
  - StrModule: nombre del subflujo o módulo (ej. `SAP_Login`, `Excel_Export`).
  - StrMessageLog: mensaje genérico de error.
- Ejemplo: “Manejo de errores en el subflujo SAP_Login” (solo para el bloque de error).

### Manejo de errores
- Cada bloque de error DEBE incluir al menos un log llamando al subflujo **AddToLog** con nivel, módulo y mensaje.
- PROHIBIDO: bloques de error vacíos (sin log, sin notificación, sin acción).

### Rastreabilidad de requerimientos
- Llevar rastreabilidad de requerimientos en el flujo usando el ID del documento de definición de requerimientos.
- En Desktop: mediante acción tipo **Comentario** al inicio del subflujo con el ID.
- Formato del ID: según el proyecto (ej. `NYB.001.007`).

### Scopes / Regiones
- Usar acción **Región** para agrupar acciones del mismo tipo o función.
- El nombre debe describir lo que hace la región.
- PROHIBIDO: regiones vacías o con una sola acción.

---

## Reglas específicas de Power Automate Desktop

### Nombre del proyecto
- Formato: `ID-NombreDelProyecto` → ejemplo: `NYB.001-GenerateYearlyReport`
- Descripción del proyecto: funcionalidad del proyecto.
- PROHIBIDO: versión, número de Sprint o Change Request en el nombre del proyecto.

### Variables adicionales de tipo PAD
- Dictionary: prefijo `Dic` → `DicConfiguracion`
- List: prefijo `Lst` → `LstCorreosPendientes`
- DataTable: prefijo `dt_` → `dt_RegistrosExcel`

### Subflujos en PAD
- Copilot PAD NO puede crear subflujos → `instruccion_previa` DEBE indicar que el usuario cree el subflujo manualmente antes de pegar el prompt.
- Al inicio de cada subflujo: agregar acción tipo **Comentario** con propósito, precondiciones, postcondiciones y referencia al req ID.
- Nombre del subflujo: UpperCamelCase con nombre de la aplicación principal.
  - Correctos: `JDE_DescargarLM`, `Excel_AjustarEC`, `Outlook_EnviarNotificacion`
  - Incorrectos: `Subflujo1`, `ProcesarDatos`, `Flujo_correo`

### Descripciones de Subflujos
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

## Verificación final — aplicar antes de incluir cada prompt PAD

1. ¿Las variables usan prefijo de tipo Beecker (Str, Int, Bln, dt_, Lst, Dic)?
2. ¿El nombre del subflujo es UpperCamelCase con prefijo de aplicación, sin acentos ni caracteres especiales?
3. ¿Hay valores hardcodeados (rutas, correos, URLs, tiempos, reintentos)? → usar placeholder
4. ¿La condición If tiene la acción principal en el bloque True?
5. ¿El manejo de errores incluye llamada a AddToLog?
6. ¿Los correos se guardan como borrador si tienen información sensible?
7. ¿Los retrasos usan espera inteligente o variable de configuración?
8. ¿Las acciones de UI tienen nota_desarrollador indicando grabación manual?
9. ¿La instruccion_previa indica crear el subflujo manualmente antes de pegar el prompt?
10. ¿La instruccion_previa incluye el req ID para rastreabilidad?
11. ¿El prompt no supera los 500 caracteres?
12. ¿El campo prompt es una sola línea continua sin \n internos?
13. ¿Los scopes/regiones no están vacíos ni tienen una sola acción?
14. ¿Se eliminaron variables no utilizadas?

Si alguna respuesta es NO → corregir antes de incluir el prompt.
