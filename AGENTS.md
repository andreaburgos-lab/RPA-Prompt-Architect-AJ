# RPA PDD Agent — Reglas Compartidas

## Estructura de carpetas (no modificar)
```
rpa-pdd-agent/
├── inputs/          ← archivos .toon colocados por el usuario
├── outputs/         ← JSON generados por el agente
├── GEMINI.md        ← reglas base (siempre activas)
├── AGENTS.md        ← este archivo
└── .agents/
    └── skills/      ← skills del agente
```

## Reglas de lectura de archivos .toon

### Formato Clásico (PDD_BA_05)
Se reconoce si las primeras líneas contienen `codigo:`, `proyecto:`, `tecnologia_rpa:`
- Secciones: MAYÚSCULAS (`REQUISITOS`, `INTERFACES`, `EXCEPCIONES_NEGOCIO_CONOCIDAS`)
- Requerimientos: bloques `REQ_01`, `REQ_02`, etc.
- Campos: `clave: valor` con indentación
- Multilínea: `clave: >` seguido de texto indentado

### Formato Anotado (@document)
Se reconoce si las primeras líneas contienen `@document` o `@seccion`
- Acciones: `@accion[N] Nombre`
- Sub-acciones: `@subaccion[N.M] Nombre`
- Excepciones: `@excepcion Nombre`
- Tablas: `@tabla nombre` con filas `campo | valor`
- Listas: `@lista nombre` con ítems `- texto`
- Multilínea: `campo: |` seguido de texto indentado

## Reglas de nomenclatura de outputs

| Código proyecto | Nombre archivo análisis    | Nombre archivo prompts  |
|-----------------|----------------------------|-------------------------|
| FCM.001         | FCM_001_analisis.json      | FCM_001_prompts.md      |
| PDC.002         | PDC_002_analisis.json      | PDC_002_prompts.md      |
| MMC.001         | MMC_001_analisis.json      | MMC_001_prompts.md      |

Regla: reemplazar `.` por `_` en el código del proyecto.

## Reglas para el texto de cada prompt en el .md de salida

El bloque de código de cada prompt contiene ÚNICAMENTE el texto que el usuario copia y pega en Copilot.
- Sin encabezados de sección (sin "OBJETIVO:", "ACCIONES:", "REGLAS:")
- Sin metadatos del req
- Sin saltos de línea internos — texto continuo separado por punto y espacio
- Texto directo, accionable, listo para pegar

El contexto y las notas se colocan FUERA del bloque de código:
- `> **Instrucción previa:**` → qué hacer ANTES de pegar el prompt (antes del bloque)
- `> **Nota para el desarrollador:**` → qué configurar DESPUÉS (después del bloque)
- `**Acciones cubiertas:**` → qué parte del PDD cubre este prompt
- `**Pasos manuales requeridos:**` → lo que Copilot no puede generar

## Manejo de nombres de archivos en prompts

Si el PDD especifica nombres exactos de archivos, SIEMPRE usarlos en los prompts.
Nunca usar nombres genéricos si el PDD tiene el nombre real.

| PDD dice                                   | Usar en prompt                              |
|--------------------------------------------|---------------------------------------------|
| input: Detalle conciliaciones bancarias.xlsx | "el archivo Detalle conciliaciones bancarias.xlsx" |
| input: CuentaCorriente                     | "la variable CuentaCorriente" (no es archivo) |
| output: Plantilla Conciliación.xlsx        | "guardar en Plantilla Conciliación.xlsx"    |
| output: NotificaciónConciliación           | "generar la notificación de conciliación"   |

## Reglas globales de formato — OBLIGATORIAS para todos los skills

### Texto del prompt: una sola línea continua
El texto dentro del bloque de código ` ``` ` en el `.md` DEBE ser una cadena continua sin saltos de línea internos.
Separar las instrucciones con punto y espacio.

  INCORRECTO:
  ```
  Abrir Excel.
  Leer datos.
  ```
  CORRECTO:
  ```
  Abrir Excel. Leer datos con Read from Excel Worksheet desde la hoja 'Hoja1'.
  ```

### Sin escapes unicode en ningún archivo generado
Todos los archivos de salida (JSON de análisis y .md de prompts) deben usar caracteres UTF-8 directamente.
NUNCA usar secuencias de escape unicode.

  INCORRECTO: "Acción principal"
  CORRECTO:   "Acción principal"

### JSON de análisis: formato interno
El archivo `_analisis.json` sigue su propio esquema definido en el skill `generar-analisis`.
El archivo `_prompts.md` sigue el formato markdown definido en cada skill generador de prompts.
