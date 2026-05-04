# RPA PDD Agent para Antigravity

Agente que analiza PDDs de proyectos RPA en formato `.toon` y genera automáticamente
los dos JSONs de salida: análisis estructurado + prompts listos para Copilot de Power Automate.

## Cómo instalar

1. Abre Antigravity y crea un nuevo workspace
2. Abre este proyecto como workspace (la carpeta `rpa-pdd-agent/`)
3. Antigravity detectará automáticamente `GEMINI.md` y los skills en `.agents/skills/`
4. No se requiere instalar ninguna dependencia ni ejecutar ningún script

## Cómo usar

1. Coloca tu archivo `.toon` en la carpeta `inputs/`
2. En el chat de Antigravity escribe:
   ```
   analizar pdd
   ```
3. El agente te pedirá el código del proyecto (ej: `FCM.001`)
4. Escríbelo y el agente procesará todo automáticamente
5. Los archivos JSON aparecerán en `outputs/`

## Estructura del proyecto

```
rpa-pdd-agent/
├── GEMINI.md                          ← reglas base del agente (siempre activas)
├── AGENTS.md                          ← reglas compartidas y referencia técnica
├── README.md                          ← este archivo
├── inputs/                            ← poner los archivos .toon aquí
├── outputs/                           ← JSON generados aquí
└── .agents/
    └── skills/
        ├── analizar-pdd/              ← skill principal (orquestador)
        │   └── SKILL.md
        ├── clasificar-tecnologia/     ← detecta si es Desktop/Cloud/Híbrido
        │   └── SKILL.md
        ├── generar-analisis/          ← genera el JSON de análisis
        │   └── SKILL.md
        ├── generar-prompts-pad/       ← prompts para Power Automate Desktop
        │   └── SKILL.md
        ├── generar-prompts-cloud/     ← prompts para Power Automate Cloud
        │   └── SKILL.md
        └── hibrido/                   ← coordina Cloud + Desktop
            └── SKILL.md
```

## Tecnologías soportadas

| Tecnología                  | Clave interna            | Skill de prompts      |
|-----------------------------|--------------------------|-----------------------|
| Power Automate Desktop      | power_automate_desktop   | generar-prompts-pad   |
| Power Automate Cloud        | power_automate_cloud     | generar-prompts-cloud |
| Power Automate Híbrido      | power_automate_hybrid    | hibrido               |
| UiPath (beta)               | uipath                   | generar-prompts-pad*  |
| Automation Anywhere (beta)  | automation_anywhere      | generar-prompts-pad*  |

*Con nota de tecnología genérica hasta que se agreguen skills específicos.

## Agregar soporte para nuevas tecnologías

Para agregar UiPath o Automation Anywhere como primera clase:
1. Crear `.agents/skills/generar-prompts-uipath/SKILL.md`
2. Seguir el mismo patrón que `generar-prompts-pad/SKILL.md`
3. Actualizar `analizar-pdd/SKILL.md` paso 4 para incluir el nuevo tech_key
4. No se requiere modificar código; solo archivos Markdown

## Formatos de .toon soportados

- **Clásico (PDD_BA_05)**: `proyecto: X`, `REQ_01`, secciones MAYÚSCULAS
- **Anotado**: `@document`, `@accion[N]`, `@subaccion[N.M]`, `@excepcion`
