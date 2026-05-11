# Buenas Prácticas — Power Automate Cloud Flow

Fuente oficial: Manual Code Review Power Automate — Beecker (PAut_CR_02, octubre 2024).
Aplica cuando `tech_key = "power_automate_cloud"`.

---

## Preceptos de calidad (fundamento de todas las reglas)

- **Mantenibilidad**: facilidad de extender, modificar y corregir el bot.
- **Legibilidad**: código con comentarios, anotaciones y nombres significativos.
- **Confiabilidad**: manejo de excepciones y reporte de errores.
- **Eficiencia**: el bot alcanza el objetivo sin gastar recursos innecesarios.

---

## Reglas comunes a todas las tecnologías (aplican en Cloud)

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

Parámetros entre flujos:
- Entrada: `in_` → `in_StrNombreEntrada`
- Salida: `out_` → `out_StrNombreSalida`
- Entrada y salida: `io_` → `io_ArrParametro`
- La primera letra del argumento debe ser **minúscula**.

PROHIBIDO: variables sin prefijo de tipo, nombres genéricos sin contexto, variables no utilizadas.

### Hardcode prohibido
NUNCA incluir valores fijos para: credenciales, retrasos, número de reintentos, rutas internas, nombres de archivos, hojas de Excel, columnas de tablas, URLs, correos electrónicos, información sensible.

Si el PDD no provee el valor → usar placeholder descriptivo:
`[https://empresa.sharepoint.com/sites/NombreSitio]`, `[NombreTabla]`, `[NombreHoja]`.

### Correos electrónicos
- Los correos creados por robots deben guardarse como **BORRADORES** para revisión humana.
- Excepción: correos genéricos sin información sensible.
- PROHIBIDO: hardcode de correos de destinatarios. Toda la información del correo debe ser parametrizable.

### Condición If — bloque True
- La acción principal SIEMPRE debe ejecutarse en el bloque **True**.
- PROHIBIDO: bloque True vacío.
- Si la condición original tiene la acción en False → invertir la lógica para que quede en True.

### Anidación de condiciones
- Máximo **3 niveles** de anidación de condiciones If/Else.
- Si en Cloud no es posible aplicar la regla: validar con justificación.
- Indicar en `nota_desarrollador` cuando se detecte lógica con más de 3 niveles.

### Flujos saturados
- Máximo **6 niveles** de anidación total en un flujo.
- Si se excede: separar en flujos usando `Ejecutar flujo`.

### Mensajes de registro (Log)
- Llamar a subflujo o acción equivalente de **AddToLog** o log de nivel equivalente.
- Puntos obligatorios: inicio y fin de subflujos, interacción con aplicaciones externas, subida/descarga de archivos, inicio/cierre de sesión, informe de errores.

### Manejo de errores
- Cada bloque de error DEBE incluir al menos un log.
- PROHIBIDO: bloques de error vacíos.

### Rastreabilidad de requerimientos
- OBLIGATORIO: añadir el ID del requerimiento como **Nota** en la Acción, Scope o Subflujo correspondiente.
- Formato: `ID: Descripción breve` → ej: `NYB.001.007: Crea un archivo dentro de drive con el attachment del mail`.

### Scopes / Ámbitos
- Usar **Scopes (Ámbitos)** para agrupar acciones del mismo tipo o función.
- El nombre debe ser alusivo a lo que se realiza.
- PROHIBIDO: Scopes vacíos o con una sola acción.

---

## Reglas específicas de Power Automate Cloud

### Variables Cloud
- Tipos con prefijos: Boolean (`Bln`), Integer (`Int`), Float (`Flt`), String (`Str`), Object (`Obj`), Array (`Arr`).
- Mismas reglas de UpperCamelCase y unicidad que la sección común.

### Ramas paralelas para inicializar variables
- Límite recomendado: máximo **5 ramas paralelas**.
- Conserva buena legibilidad, optimización y rendimiento.

### Nomenclatura para Acciones Cloud
- El nombre de las acciones debe estar estructurado en forma de **oración**.
- PROHIBIDO: acentos y caracteres especiales (# ¿ ? / \ : ; * < > [ ] $ & + % { } Ñ ñ).
- Dos estructuras válidas:
  - `"Nombre default - Información de acción"` → ej: `Inicializar variable - StrMensajeError`
  - `"Nombre descriptivo"` → ej: `Inicializar Mensaje de Error`
- PROHIBIDO: dejar únicamente el nombre default sin contexto (ej: solo `Inicializar variable`).
- PROHIBIDO: numeración en acciones (acción 1, acción 2). Usar: Primera acción, Segunda acción.

### Scopes / Ámbitos Cloud
- El Scope del manejo de errores: nombrar descriptivamente → ej: `[NombreReq]_ManejadorErrores`.

### Switch - Modificador
- REGLA: siempre realizar una acción en cada posible caso.
- PROHIBIDO: caso **Predeterminado** vacío.
- Cada caso debe tener: acción específica, Log de notificación, o manejo de errores adecuado.

### Trigger
- El trigger va SIEMPRE solo en el Prompt 1. Nunca combinado con acciones.
- Nombre exacto del trigger tal como aparece en Power Automate — nunca parafrasear.

### Manejo de errores Cloud
- Usar **rama paralela** después del Scope o acción que se quiera controlar.
- En la acción de manejo de errores → **Configuración → Ejecutar después de (RunAfter)**.
- Seleccionar: `Ha agotado el tiempo de espera` y `Error`.
- OBLIGATORIO: incluir log (AddToLog o equivalente) en cada manejo de errores.

### Descripciones de Acciones Cloud
- Agregar **notas** a las acciones y ámbitos.
- El porcentaje de acciones con descripciones debe ser de al menos **33%**.

### Descripciones de Flujos Cloud
- Agregar una descripción a cada Flujo que indique: propósito, condiciones previas y posteriores, referencia al requerimiento (ID).

---

## Verificación final — aplicar antes de incluir cada prompt Cloud

1. ¿Las variables usan prefijo de tipo Beecker (Str, Int, Bln, Obj, Arr)?
2. ¿Ningún prompt Cloud usa [corchetes] para referenciar variables?
3. ¿El trigger está siempre solo en el Prompt 1?
4. ¿Cada prompt menciona conector Y acción exacta juntos?
5. ¿Los nombres de acciones son exactamente como aparecen en Power Automate?
6. ¿Ningún prompt supera 2000 caracteres?
7. ¿Las acciones tienen nombre descriptivo (no solo el nombre default)?
8. ¿Los Scopes tienen nombres descriptivos (no "Ámbito 1", "Ámbito 2")?
9. ¿El caso Predeterminado del Switch tiene acción definida?
10. ¿La condición If tiene la acción principal en el bloque True?
11. ¿El manejo de errores tiene rama paralela con RunAfter configurado?
12. ¿Los correos con información sensible se guardan como borrador?
13. ¿Las ramas paralelas de inicialización no superan 5?
14. ¿Al menos 33% de acciones/scopes tienen nota o descripción?
15. ¿La instruccion_previa incluye el req ID para rastreabilidad?
16. ¿El campo prompt es texto en una sola línea continua sin \n?
17. ¿Se eliminaron o evitaron variables no utilizadas en el flujo?

Si alguna respuesta es NO → corregir antes de incluir el prompt.
