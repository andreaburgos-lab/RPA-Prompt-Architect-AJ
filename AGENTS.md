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

| Código proyecto | Nombre archivo análisis    | Nombre archivo prompts    |
|-----------------|----------------------------|---------------------------|
| FCM.001         | FCM_001_analisis.json      | FCM_001_prompts.json      |
| PDC.002         | PDC_002_analisis.json      | PDC_002_prompts.json      |
| MMC.001         | MMC_001_analisis.json      | MMC_001_prompts.json      |

Regla: reemplazar `.` por `_` en el código del proyecto.

## Reglas para el campo "prompt" en el JSON de prompts

El campo `prompt` contiene ÚNICAMENTE el texto que el usuario copia y pega en Copilot.
- Sin encabezados de sección (sin "OBJETIVO:", "ACCIONES:", "REGLAS:")
- Sin metadatos del req
- Sin saltos de línea decorativos
- Texto directo, accionable, listo para pegar

El contexto, las notas y las instrucciones van en campos SEPARADOS:
- `instruccion_previa` → qué hacer ANTES de pegar el prompt
- `nota_desarrollador` → qué hacer DESPUÉS de aplicar el prompt
- `acciones_cubiertas` → qué parte del PDD cubre este prompt
- `pasos_manuales_requeridos` → lo que Copilot no puede generar

## Manejo de nombres de archivos en prompts

Si el PDD especifica nombres exactos de archivos, SIEMPRE usarlos en los prompts.
Nunca usar nombres genéricos si el PDD tiene el nombre real.

| PDD dice                                   | Usar en prompt                              |
|--------------------------------------------|---------------------------------------------|
| input: Detalle conciliaciones bancarias.xlsx | "el archivo Detalle conciliaciones bancarias.xlsx" |
| input: CuentaCorriente                     | "la variable CuentaCorriente" (no es archivo) |
| output: Plantilla Conciliación.xlsx        | "guardar en Plantilla Conciliación.xlsx"    |
| output: NotificaciónConciliación           | "generar la notificación de conciliación"   |

## Reglas globales de formato JSON — OBLIGATORIAS para todos los skills

### Prompts en una sola línea
El campo  en cualquier JSON generado DEBE ser una cadena de texto continua sin saltos de línea.
Separar las instrucciones con punto y espacio. NUNCA incluir  dentro del valor del campo prompt.

  INCORRECTO: {"prompt": "Abrir Excel.
Leer datos."}
  CORRECTO:   {"prompt": "Abrir Excel. Leer datos con Read from Excel Worksheet."}

### Sin escapes unicode
Todos los campos de texto en el JSON deben usar caracteres UTF-8 directamente.
NUNCA usar secuencias de escape unicode como , , , , .

  INCORRECTO: {"titulo": "Acción principal"}
  CORRECTO:   {"titulo": "Acción principal"}

Esta regla aplica a TODOS los campos: titulo, prompt, instruccion_previa, nota_desarrollador,
acciones_cubiertas, resumen_cobertura, pasos_manuales_requeridos, y cualquier otro campo de texto.
