---
name: hibrido
description: |
  Coordina la generacion de prompts para proyectos hibridos Power Automate (Cloud + Desktop).
  Se activa internamente desde analizar-pdd cuando tech_key = power_automate_hybrid.
  Asigna plataforma individual a cada req y delega a generar-prompts-pad y generar-prompts-cloud.
  No usar directamente por el usuario.
---

# Skill: Proyectos Hibridos Power Automate

## Que es un proyecto hibrido

Un proyecto hibrido combina Cloud Flow y Desktop Flow en el mismo proceso de automatizacion.
Ambos tipos se pueden encadenar: un Cloud Flow puede invocar un Desktop Flow mediante la
accion "Ejecutar un flujo de escritorio" del conector Power Automate Desktop.

**Cloud Flow:** automatiza acciones sobre conectores Microsoft 365 sin necesidad de UI.
  Sistemas tipicos: SharePoint, OneDrive, Teams, Forms, Outlook API, Dataverse, Excel Online.

**Desktop Flow:** automatiza aplicaciones de escritorio o web que requieren interaccion UI.
  Sistemas tipicos: JDE, SAP, SEADEX, SIESA, Oracle, AS400, Excel local, Outlook Desktop.

---

## Paso 1 — Asignar plataforma individual a cada req

Para cada req del JSON de analisis, determinar su plataforma segun estas reglas:

| Condicion | Plataforma asignada |
|---|---|
| Sistemas solo Cloud (SharePoint, OneDrive, Teams, Forms, Dataverse) | Cloud Flow |
| Sistemas solo Desktop (JDE, SAP, SEADEX, SIESA, Oracle, AS400) | Desktop Flow |
| Sistemas ambiguos (Excel, Outlook) sin especificar tipo de acceso | Desktop Flow (conservador) |
| Sistemas ambiguos con "tipo: Thin Client" o "entorno: Web" en el PDD | Cloud Flow |
| Req con sistemas mixtos Cloud + Desktop | Desktop Flow (el Desktop predomina) |
| Req sin sistemas detectados | Desktop Flow (default) |

Registrar la decision en el campo plataforma de cada req en el JSON de prompts.

---

## Paso 2 — Aplicar reglas de cada plataforma sin mezclarlas

CRITICO: Cada req sigue ESTRICTAMENTE las reglas de su plataforma asignada.

Reqs con plataforma "Cloud Flow":
  Aplicar TODAS las reglas del skill generar-prompts-cloud:
  - Variables SIN corchetes
  - Trigger solo en Prompt 1
  - Conector + accion exacta siempre juntos
  - Limite 2000 chars por prompt
  - Nombres sin acentos para variables y scopes

Reqs con plataforma "Desktop Flow":
  Aplicar TODAS las reglas del skill generar-prompts-pad:
  - Variables entre [corchetes] con prefijo de tipo Beecker
  - Subflows manuales con instruccion_previa
  - Acciones PAD con nombres en ingles exactos
  - Limite 500 chars por prompt
  - Placeholders descriptivos para rutas/URLs faltantes

NUNCA mezclar: no usar corchetes en prompts Cloud, no omitir corchetes en prompts Desktop.

---

## Paso 3 — Campo nota_hibrido en el JSON de prompts

Incluir este bloque en el JSON de prompts a nivel raiz:

"nota_hibrido": {
  "explicacion": "Este proyecto es HIBRIDO: combina Cloud Flow y Desktop Flow. Los Cloud Flows gestionan los conectores Microsoft 365 (SharePoint, OneDrive, Teams, Forms). Los Desktop Flows automatizan aplicaciones locales o sistemas legacy con interaccion de interfaz de usuario. Ambos se pueden encadenar: un Cloud Flow invoca un Desktop Flow mediante la accion 'Ejecutar un flujo de escritorio' del conector Power Automate Desktop.",
  "pasos_implementacion": [
    "1. Crear primero los Desktop Flows para reqs con plataforma 'Desktop Flow' en Power Automate Desktop.",
    "2. Crear los Cloud Flows para reqs con plataforma 'Cloud Flow' en make.powerautomate.com.",
    "3. En el Cloud Flow coordinador, agregar la accion 'Ejecutar un flujo de escritorio' del conector Power Automate Desktop para invocar los Desktop Flows cuando sea necesario.",
    "4. Configurar la conexion de maquina (gateway) en el entorno de Power Automate para permitir que el Cloud Flow se comunique con la maquina donde corren los Desktop Flows.",
    "5. Parametrizar la comunicacion entre flujos: los outputs del Desktop Flow se pasan al Cloud Flow como variables de salida (out_StrNombreSalida)."
  ],
  "reqs_cloud": ["lista de req.id con plataforma Cloud Flow"],
  "reqs_desktop": ["lista de req.id con plataforma Desktop Flow"]
}

---

## Paso 4 — Req de coordinacion entre flujos

Si el proyecto tiene un req que actua como orquestador (invoca otros flujos), identificarlo y
generar prompts especificos de coordinacion:

**Si un Cloud Flow invoca un Desktop Flow:**

Prompt especial para Cloud Flow coordinador:
"Agregar la accion 'Ejecutar un flujo de escritorio' del conector Power Automate Desktop.
Seleccionar la conexion de maquina [{NombreMaquina}] y el Desktop Flow '{NombreDesktopFlow}'.
Mapear los parametros de entrada: in_Str{NombreParam} <- {OrigenEnCloudFlow}.
Guardar los parametros de salida: out_Str{NombreResult} en la variable Str{NombreResult}."

nota_desarrollador: "Configurar el gateway de Power Automate Desktop antes de usar este paso.
Los Desktop Flows invocados desde Cloud deben tener parametros in_ y out_ definidos.
Nombrar la conexion de maquina de forma descriptiva: '{Proyecto}-MaquinaAutomatizacion'."

---

## Estructura JSON de salida para proyectos hibridos

{
  "proyecto": "[proyecto]",
  "tecnologia": "Power Automate Hibrido",
  "es_hibrido": true,
  "nota_hibrido": {
    "explicacion": "...",
    "pasos_implementacion": ["1...", "2...", "3...", "4...", "5..."],
    "reqs_cloud": ["req.id1", "req.id2"],
    "reqs_desktop": ["req.id3", "req.id4"]
  },
  "generado": "[ISO 8601 timestamp]",
  "_resumen": {
    "total_requerimientos": 0,
    "con_prompts": 0,
    "sin_prompts": 0,
    "total_prompts": 0,
    "prompts_cloud": 0,
    "prompts_desktop": 0
  },
  "prompts_generados": [
    {
      "id_flujo": "[req.id]",
      "nombre_flujo": "[req.nombre]",
      "plataforma": "Cloud Flow | Desktop Flow",
      "generar_prompt": true,
      "gaps_detectados": { "criticos": [], "advertencias": [], "impacto": "" },
      "prompts_secuenciales": [],
      "resumen_cobertura": "",
      "pasos_manuales_requeridos": [],
      "sub_prompts": []
    }
  ]
}

---

## Verificacion final hibrido

1. Cada req tiene su campo plataforma asignado individualmente?
2. Los reqs Cloud usan reglas Cloud (sin corchetes, trigger solo, conector exacto)?
3. Los reqs Desktop usan reglas Desktop (corchetes, prefijos Beecker, 500 chars)?
4. El campo nota_hibrido esta presente a nivel raiz del JSON?
5. Las listas reqs_cloud y reqs_desktop estan completas y correctas?
6. El _resumen tiene conteos diferenciados de prompts Cloud vs Desktop?
7. Si hay req coordinador, tiene el prompt de Ejecutar un flujo de escritorio?
8. Los parametros entre Cloud y Desktop usan prefijos in_ y out_?