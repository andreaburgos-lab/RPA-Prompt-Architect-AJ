---
name: clasificar-tecnologia
description: |
  Clasifica la tecnología RPA de un PDD ya leído como Desktop Flow, Cloud Flow o Híbrido
  para Power Automate. Se activa internamente desde analizar-pdd después de leer el .toon.
  También se activa si el usuario pregunta directamente sobre la clasificación de un req.
  No usar para tecnologías distintas a Power Automate sin indicación explícita.
---

# Skill: Clasificar Tecnología RPA

## Entrada disponible

Al activarse, tienes disponible:
- Contenido completo del .toon ya leído
- `tecnologia_rpa` del encabezado (puede ser vago: "Power Automate", vacío, o específico)
- Lista de sistemas de cada requerimiento/acción

---

## Señales de clasificación por sistema

### Señales CLOUD — sistemas nativos Microsoft 365 / conectores API
Estos sistemas se automatizan **sin UI automation** mediante conectores nativos:

| Sistema | Conector en Power Automate |
|---|---|
| SharePoint | SharePoint (V1) |
| OneDrive / OneDrive for Business | OneDrive for Business |
| Microsoft Teams | Microsoft Teams (V3) |
| Microsoft Forms | Microsoft Forms |
| Dataverse / Common Data Service | Dataverse |
| Power Apps | Power Apps |
| Office 365 (correo vía API) | Office 365 Outlook (V3) |
| Dynamics 365 (vía API) | Dynamics 365 |
| HTTP / REST API con conector | HTTP |
| Approvals | Approvals |

### Señales DESKTOP — sistemas que requieren UI automation
Estos sistemas **no tienen conector nativo** o se acceden mediante interfaz gráfica:

| Sistema | Tipo de acceso |
|---|---|
| JDE / JD Edwards | Navegador con UI (web legacy) |
| SAP (cualquier transacción) | SAP GUI o navegador legacy |
| SIESA | Aplicación de escritorio |
| Oracle EBS | Navegador legacy |
| SEADEX | Navegador con UI |
| AS400 / iSeries | Emulador de terminal |
| Navision / Business Central local | Thick Client |
| Excel local (Thick Client) | Aplicación de escritorio |
| Outlook Desktop (Thick Client) | Aplicación de escritorio |
| Carpetas de red (UNC paths, drives mapeados) | Sistema de archivos local |
| Portales web sin conector oficial | Navegador con UI |
| Cualquier app con `tipo: Thick Client` | Aplicación de escritorio |
| Descarga de archivos desde portales externos sin API | Navegador con UI |

### Señales AMBIGUAS — pueden ser Cloud o Desktop según contexto
Estos sistemas requieren analizar el PDD para determinar el tipo de acceso:

| Sistema | Cloud si... | Desktop si... |
|---|---|---|
| Excel | "Excel Online", conector Excel Online | "Excel local", "archivo en red", Thick Client |
| Outlook | Conector Office 365, API | Aplicación Outlook instalada, Thick Client |
| SharePoint | Conector SharePoint, API | Acceso por navegador con UI, sin conector |
| OneDrive | Conector OneDrive, API | Navegador, carpeta sincronizada local |

**Si el PDD no especifica el tipo de acceso para un sistema ambiguo:**
- Excel / Outlook → asumir **Desktop** (conservador, más común en contexto RPA empresarial)
- SharePoint / OneDrive → asumir **Cloud** (conectores maduros y estables)

---

## Reglas de clasificación (en orden de prioridad)

### Prioridad 1 — Declaración explícita en el PDD
| El PDD dice | Clasificación |
|---|---|
| "Power Automate Desktop" (sin Cloud) | `power_automate_desktop` |
| "Power Automate Cloud" (sin Desktop) | `power_automate_cloud` |
| "Power Automate Desktop y Cloud" / "Híbrido" | `power_automate_hybrid` |
| "Power Automate" (sin especificar) | → continuar con Prioridad 2 |

### Prioridad 2 — Inferencia por sistemas detectados en los requerimientos
| Señales detectadas | Clasificación |
|---|---|
| Solo señales DESKTOP | `power_automate_desktop` |
| Solo señales CLOUD | `power_automate_cloud` |
| Señales DESKTOP + señales CLOUD en distintos reqs | `power_automate_hybrid` |
| Sin señales claras de ningún tipo | `power_automate_desktop` (default conservador) |

### Prioridad 3 — Caso híbrido: clasificar cada req individualmente
Si el resultado es `power_automate_hybrid`, asignar a cada requerimiento su plataforma individual:

```
Para cada req:
  sistemas_cloud   = {sistemas del req} ∩ {señales CLOUD}
  sistemas_desktop = {sistemas del req} ∩ {señales DESKTOP}

  Si solo sistemas_cloud y no sistemas_desktop  → plataforma = "Cloud Flow"
  Si solo sistemas_desktop (o ambigüo sin tipo)  → plataforma = "Desktop Flow"
  Si tiene ambos tipos                           → plataforma = "Desktop Flow" (el Desktop predomina)
  Si sin sistemas detectados                     → plataforma = "Desktop Flow" (default)
```

**Señales adicionales de híbrido a buscar en el PDD:**
- "El trigger es por correo, pero la ejecución opera en [sistema desktop]" → Híbrido
- "Cloud Flow invoca Desktop Flow" → Híbrido
- "El flujo inicia en SharePoint pero luego abre [app de escritorio]" → Híbrido

---

## Criterios de clasificación por tipo de acción

### Clasifica como DESKTOP si el requerimiento:
- Navega por interfaz gráfica (clics, escritura en campos, lectura de pantalla)
- Descarga archivos desde portales externos sin API
- Opera sobre carpetas compartidas de red (UNC paths o drives mapeados)
- Interactúa con aplicaciones de escritorio sin API disponible
- Requiere JDE por navegador con interacción UI
- Abre Excel como aplicación de escritorio (no Online)
- Usa Outlook como aplicación de escritorio (Thick Client)

### Clasifica como CLOUD si el requerimiento:
- Usa conectores nativos de Power Automate (ver tabla de señales Cloud)
- Tiene trigger basado en eventos: llegada de correo, creación de archivo, formulario enviado
- Opera con Excel Online, Forms, Dataverse
- Implementa aprobaciones, notificaciones o lógica de orquestación
- Consume APIs documentadas con conector disponible en Power Automate
- Accede a SharePoint o OneDrive mediante conector (no UI)

### Clasifica como HÍBRIDO si:
- El trigger o notificación es Cloud (correo, SharePoint, Forms) PERO la ejecución principal opera sistemas Desktop
- Un requerimiento mezcla acciones Cloud y Desktop en el mismo flujo
- El proyecto tiene requerimientos que son claramente Cloud y otros claramente Desktop

---

## Criterios para requiere_script = true

Marcar como `true` y documentar en `justificacion_script` cuando las acciones nativas son insuficientes:

| Situación | Justificación típica |
|---|---|
| Lógica con múltiples condiciones anidadas complejas | "Requiere script por lógica de decisión con N condiciones anidadas que exceden las acciones nativas de Condición" |
| Manipulación masiva de datos (búsquedas, prorrateos, transformaciones) | "Requiere script por procesamiento de [N] registros con lógica de [tipo]" |
| Procesamiento de texto complejo (regex, parseo estructurado) | "Requiere script por extracción de campos con regex sobre texto no estructurado" |
| Cálculos matemáticos complejos | "Requiere script por cálculo de [tipo] que no es posible con acciones nativas" |
| Interacciones UI complejas sobre sistemas legacy | "Requiere script por selectores dinámicos en [sistema] que Copilot no puede generar" |
| Manipulación de archivos PDF, ZIP, XML complejos | "Requiere script por procesamiento de [tipo de archivo] sin conector nativo" |

Si ninguna aplica → `requiere_script: false`, `justificacion_script: ""`

---

## Información faltante — Categorías de evaluación

Para cada requerimiento, evaluar estas 9 categorías y documentar los gaps encontrados:

| Categoría | Qué buscar |
|---|---|
| **TRIGGER** | Evento de inicio no definido, asunto de correo no especificado, horario no definido |
| **SISTEMAS Y ACCESO** | URL del sistema, ruta de la carpeta, credenciales, versión del sistema, tipo de acceso (UI vs API) |
| **INPUTS** | Nombre exacto del archivo de entrada, ruta, formato, responsable de proveerlo |
| **OUTPUTS** | Ruta de destino del archivo de salida, nombre exacto, formato, nomenclatura dinámica |
| **REGLA DE NEGOCIO** | Condición de borde sin resolución definida, lógica no escrita pero implícita |
| **EXCEPCIÓN** | Destinatario del correo de error no definido, acción o log dice "por definir" |
| **CRITERIO UI** | Selector de elemento no definido, criterio de fila en tabla no especificado |
| **CONFIGURACIÓN TÉCNICA** | Parámetros del sistema, licencias requeridas, clase de documento en SAP/JDE |
| **REFERENCIA HUÉRFANA** | Archivo/dato/sistema mencionado como dado pero sin definir cómo el bot lo obtiene |

Formato de cada gap: `"[CATEGORÍA] — descripción concisa de qué falta y su impacto en el desarrollo"`

⚠ No marcar como REFERENCIA HUÉRFANA si el insumo es el output directo y explícito de un requerimiento anterior.

---

## Objeto de salida de este skill

Produce internamente el objeto `tech` para uso de los skills siguientes:

```json
{
  "tech_label": "Power Automate Desktop | Power Automate Cloud | Power Automate Híbrido",
  "tech_key": "power_automate_desktop | power_automate_cloud | power_automate_hybrid",
  "es_hibrido": false,
  "razon_clasificacion": "Texto explicando en qué señales se basó la decisión, qué sistemas se detectaron y por qué se eligió esta clasificación",
  "plataforma_cloud": ["lista de sistemas Cloud detectados, o null si no aplica"],
  "plataforma_desktop": ["lista de sistemas Desktop detectados, o null si no aplica"]
}
```

Y por cada requerimiento (especialmente en híbrido), el campo:
```json
"plataforma": "Cloud Flow | Desktop Flow"
```

---

## Preguntar al usuario si la clasificación no es clara

Si después de aplicar todas las reglas la clasificación sigue siendo ambigua
(ej: todos los sistemas son ambiguos y el PDD no especifica), preguntar al usuario:

> La tecnología en el PDD dice "[valor del PDD]" pero no especifica si es Desktop, Cloud o Híbrido.
> Los sistemas detectados son: [lista].
> ¿Cuál es la clasificación correcta?
> 1. Power Automate Desktop
> 2. Power Automate Cloud
> 3. Power Automate Híbrido (mezcla de ambos)

Usar la respuesta del usuario como clasificación definitiva y documentarla en `razon_clasificacion`.
