#!/usr/bin/env python3
"""
generate_output.py  —  RPA PDD Agent v3
Lee un archivo .toon de /inputs y genera:
  outputs/<PROYECTO>_analisis.json
  outputs/<PROYECTO>_prompts.json

Sin dependencias externas. Python 3.9+
Uso: python generate_output.py [nombre_o_codigo.toon]
     python generate_output.py              # procesa el primero que encuentre en inputs/
"""

import json, re, sys
from datetime import datetime, timezone
from pathlib import Path

BASE   = Path(__file__).parent
INPUTS = BASE / "inputs"
OUTDIR = BASE / "outputs"
OUTDIR.mkdir(exist_ok=True)

# ─── Límites Copilot ──────────────────────────────────────────────────────────
LIMIT_DESKTOP = 500
LIMIT_CLOUD   = 2000

# ─── Nomenclatura Beecker ─────────────────────────────────────────────────────
TYPE_PREFIX = {
    "texto": "Str", "string": "Str", "str": "Str",
    "entero": "Int", "integer": "Int", "int": "Int",
    "flotante": "Flt", "float": "Flt", "flt": "Flt",
    "booleano": "Bln", "boolean": "Bln", "bln": "Bln",
    "objeto": "Obj", "object": "Obj", "obj": "Obj",
    "lista": "Lst", "list": "Lst", "lst": "Lst",
    "tabla": "dt_", "datatable": "dt_", "dt": "dt_",
    "arreglo": "Arr", "array": "Arr", "arr": "Arr",
}

def beecker_var(name: str, tipo: str = "Str") -> str:
    """Genera nombre de variable con prefijo Beecker sin acentos ni caracteres especiales."""
    prefix = TYPE_PREFIX.get(tipo.lower(), tipo if tipo else "Str")
    clean  = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    parts  = [w.capitalize() for w in clean.split() if w]
    return prefix + "".join(parts)

def subflow_name(nombre: str) -> str:
    """UpperCamelCase sin acentos ni caracteres especiales."""
    clean = re.sub(r'[áä]', 'a', re.sub(r'[éë]', 'e', re.sub(r'[íï]', 'i',
            re.sub(r'[óö]', 'o', re.sub(r'[úü]', 'u', re.sub(r'[ñ]', 'n',
            nombre.lower()))))))
    clean = re.sub(r'[^a-zA-Z0-9 ]', '', clean)
    return "".join(w.capitalize() for w in clean.split())

def safe_id(codigo: str) -> str:
    return codigo.replace(".", "_")

def trunc(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit - 3] + "..."


# ══════════════════════════════════════════════════════════════════════════════
# 1. PARSER .TOON
# ══════════════════════════════════════════════════════════════════════════════

class ToonParser:
    """
    Parser adaptativo para archivos .toon.
    Soporta:
      - Formato Clásico (PDD_BA_05): secciones MAYÚSCULAS, bloques REQ_XX
      - Formato Anotado (@document): @accion[N], @subaccion[N.M], @excepcion
    """

    def __init__(self, path: Path):
        self.path    = path
        self.raw     = path.read_text(encoding="utf-8")
        self.lines   = self.raw.splitlines()
        self.formato = self._detect()

    def _detect(self) -> str:
        for l in self.lines[:12]:
            if l.strip().startswith("@document") or l.strip().startswith("@seccion"):
                return "annotated"
        return "classic"

    # ── Extracción de valor de línea ─────────────────────────────────────────
    def _val(self, pattern: str, default: str = "") -> str:
        m = re.search(pattern, self.raw, re.IGNORECASE)
        return m.group(1).strip() if m else default

    # ── Extraer listas de items (- item o numbered 01: item) ─────────────────
    def _extract_list_block(self, block_text: str) -> list[str]:
        items = []
        for line in block_text.splitlines():
            s = line.strip()
            # numbered: "- 01: Serie" or "01: Serie" or "- Serie"
            m = re.match(r'^-?\s*(?:\d+[:.]\s*)?(.+)', s)
            if m and s and not s.endswith(':') and '|' not in s:
                val = m.group(1).strip()
                if val:
                    items.append(val)
        return items

    # ── Extraer columnas con fuente (REQ_03 style) ───────────────────────────
    def _extract_columns(self, block_text: str) -> list[dict]:
        cols = []
        for line in block_text.splitlines():
            s = line.strip()
            # "- 01: Documento | valor_fijo: DUCA"  or  "- 01: Campo | fuente: correo"
            m = re.match(r'^-?\s*(?:\d+[:.]\s*)?([\w\s/áéíóúÁÉÍÓÚñÑ]+)\s*\|(.+)', s)
            if m:
                col_name = m.group(1).strip()
                meta     = m.group(2).strip()
                fuente   = ""
                fm = re.search(r'fuente:\s*([^|]+)', meta)
                vf = re.search(r'valor_fijo:\s*([^|]+)', meta)
                if fm: fuente = fm.group(1).strip()
                elif vf: fuente = "FIJO: " + vf.group(1).strip()
                cols.append({"col": col_name, "fuente": fuente})
        return cols

    # ── Extraer excepciones de un bloque ─────────────────────────────────────
    def _extract_excepciones(self, block_text: str, req_id: str = "") -> list[dict]:
        """
        Soporta:
          excepcion: > texto...
          excepciones
            - login_fallo: > texto
            - nombre: > texto
        """
        exceps = []
        # Multilínea con excepcion: >
        m_single = re.search(
            r'\bexcepcion(?:es)?:\s*>\s*((?:.|\n)+?)(?=\n\s{0,4}[a-zA-Z_]|\Z)',
            block_text
        )
        if m_single and 'login_fallo' not in block_text and '- ' not in block_text.split('excepcion')[1][:20]:
            txt = " ".join(m_single.group(1).split())
            cond, _, acc = txt.partition(':')
            exceps.append({
                "condicion": cond.strip() or txt[:80],
                "accion": acc.strip() or txt,
                "log": "(ver detalle en PDD)"
            })
            return exceps

        # Bloque de excepciones con items
        exc_block_m = re.search(
            r'\bexcepciones?\s*\n((?:.*\n)*?)(?=\n\s{0,4}[A-Z_]|\n  REQ_|\Z)',
            block_text
        )
        block = exc_block_m.group(1) if exc_block_m else block_text

        for item_m in re.finditer(r'- ([\w_]+):\s*>\s*((?:.|\n)+?)(?=\n\s{6}-\s|\n\s{4}[a-zA-Z_]|\Z)', block):
            nombre = item_m.group(1).strip()
            txt    = " ".join(item_m.group(2).split())
            exceps.append({
                "condicion": nombre.replace("_", " "),
                "accion": txt,
                "log": "(ver detalle en PDD)"
            })

        # Fallback: excepcion_<nombre>: >
        for fb_m in re.finditer(r'excepcion_\w+:\s*>\s*((?:.|\n)+?)(?=\n\s{4}[a-zA-Z_]|\Z)', block_text):
            txt = " ".join(fb_m.group(1).split())
            exceps.append({
                "condicion": "(ver PDD)",
                "accion": txt,
                "log": "(ver detalle en PDD)"
            })

        return exceps

    # ── Extraer campos estructurados (campos_seadex, columnas_detalle, etc.) ─
    def _extract_named_fields(self, block_text: str) -> list[str]:
        """Extrae campo: valor o - Campo: valor en un bloque."""
        fields = []
        for line in block_text.splitlines():
            s = line.strip()
            # "- Tipo_Equipamiento: valor correo"
            m = re.match(r'^-\s+([\w\s/áéíóúÁÉÍÓÚñÑ_]+):\s*(.+)', s)
            if m:
                fields.append(f"{m.group(1).strip()}: {m.group(2).strip()}")
            # "- seccion: X | accion: Y"
            elif re.match(r'^-\s+seccion:\s*.+\|', s):
                fields.append(s[2:])
        return fields

    # ────────────────────────────────────────────────────────────────────────
    # PARSE FORMATO CLÁSICO
    # ────────────────────────────────────────────────────────────────────────
    def parse_classic(self) -> dict:
        proyecto   = self._val(r'proyecto:\s*(.+)')
        titulo     = self._val(r'titulo:\s*(.+)')
        version    = self._val(r'version:\s*(.+)')
        cliente    = self._val(r'cliente:\s*(.+)')
        tecnologia = self._val(r'tecnologia_rpa:\s*(.+)', "Power Automate")

        # Interfaces — para saber tipo de acceso de cada sistema
        interfaces: dict[str, str] = {}
        for m in re.finditer(r'app:\s*([\w]+)\s*\|.*tipo:\s*([\w\s]+)\|.*entorno:\s*([\w\s]+)', self.raw):
            app = m.group(1).strip()
            tipo = m.group(2).strip()
            interfaces[app.upper()] = tipo

        # Excepciones globales
        exc_global: dict[str, list[dict]] = {}
        exc_section_m = re.search(r'EXCEPCIONES_NEGOCIO_CONOCIDAS\n(.+?)(?:\nEXCEPCIONES_|$)', self.raw, re.DOTALL)
        if exc_section_m:
            for line in exc_section_m.group(1).splitlines():
                req_m = re.search(r'req:\s*([\w.]+)', line)
                nom_m = re.search(r'nombre:\s*([^|]+)', line)
                acc_m = re.search(r'accion:\s*(.+)', line)
                if req_m and nom_m and acc_m:
                    rid = req_m.group(1).strip()
                    if rid not in exc_global:
                        exc_global[rid] = []
                    exc_global[rid].append({
                        "condicion": nom_m.group(1).strip(),
                        "accion": acc_m.group(1).strip(),
                        "log": "(ver EXCEPCIONES_NEGOCIO_CONOCIDAS en el PDD)"
                    })

        # Bloques REQ
        req_chunks = re.split(r'\n  REQ_', self.raw)
        requerimientos = []

        for chunk in req_chunks[1:]:
            req_key = "REQ_" + chunk.split('\n')[0].strip()
            req_id  = f"{proyecto}.{req_key}"

            nombre  = self._extract_field(chunk, 'nombre')
            sistema = self._extract_field(chunk, 'sistema')
            accion  = self._extract_field(chunk, 'accion')
            inp     = self._extract_field(chunk, 'input')
            out     = self._extract_field(chunk, 'output')

            if sistema.upper() == "NA": sistema = ""
            if inp.upper()     == "NA": inp     = ""
            if out.upper()     == "NA": out     = ""

            # Limpiar corchetes de inputs/outputs
            inp = inp.strip("[]")
            out = out.strip("[]")

            # Descripción multi-línea
            desc = self._extract_multiline(chunk, 'descripcion')

            # Columnas estructuradas (columnas_log, campos_extraer, columnas_seadex_por_producto...)
            campos_extraer = self._extract_campos_from_block(chunk)

            # Reglas de negocio
            reglas = self._extract_reglas(chunk)

            # Excepciones locales + globales
            exceps = self._extract_excepciones(chunk, req_id)
            for g in exc_global.get(req_id, []):
                exceps.append(g)

            # Sistemas como lista
            sistemas = [s.strip() for s in sistema.split(',') if s.strip()]

            # Acciones del req (construidas desde sub-bloques del .toon)
            acciones_list = self._extract_acciones(chunk, accion, sistema, nombre, desc)

            # Gaps
            criticos, advertencias = self._evaluar_gaps(nombre, sistemas, desc, accion, inp, out)

            requerimientos.append({
                "id":        req_id,
                "nombre":    nombre,
                "plataforma": self._inferir_plataforma(sistemas, interfaces, tecnologia),
                "sistemas":  sistemas,
                "input":     inp,
                "output":    out,
                "accion":    accion,
                "descripcion": desc[:400] if len(desc) > 400 else desc,
                "acciones":  acciones_list,
                "campos_extraer": campos_extraer,
                "reglas_negocio": reglas,
                "excepciones": exceps,
                "gaps": {
                    "criticos":     criticos,
                    "advertencias": advertencias,
                    "puede_generar": len(criticos) == 0,
                },
                "sub_requerimientos": [],
            })

        return {
            "proyecto":   proyecto,
            "tecnologia": tecnologia,
            "es_hibrido": False,
            "clasificacion": {
                "razon": f"Tecnología declarada: {tecnologia}. Interfaces: {interfaces}",
                "plataforma_cloud": None,
                "plataforma_desktop": list(interfaces.keys()) or None,
            },
            "generado": datetime.now(timezone.utc).isoformat(),
            "_meta": {"titulo": titulo, "version": version, "cliente": cliente},
            "requerimientos": requerimientos,
        }

    def _extract_field(self, block: str, key: str) -> str:
        m = re.search(rf'^\s+{key}:\s*(.+)', block, re.MULTILINE)
        return m.group(1).strip() if m else ""

    def _extract_multiline(self, block: str, key: str) -> str:
        m = re.search(rf'\b{key}:\s*>\s*((?:.|\n)+?)(?=\n\s{{4}}\w|\n  REQ_|\Z)', block)
        if not m: return ""
        return " ".join(m.group(1).split())

    def _extract_campos_from_block(self, block: str) -> list[dict]:
        """
        Detecta y extrae campos estructurados del bloque de un req:
        campos_extraer, columnas_log, columnas_seadex_por_producto, campos, etc.
        Retorna lista de {"nombre": str, "fuente": str, "descripcion": str}
        """
        result = []
        # Buscar sub-bloques con nombres que indiquen campos
        patterns = [
            r'campos_extraer\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)',
            r'columnas_log\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)',
            r'columnas_seadex_por_producto\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)',
            r'columnas_detalle\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)',
            r'campos\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)',
            r'campos_seadex\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)',
        ]
        for pat in patterns:
            m = re.search(pat, block, re.MULTILINE)
            if m:
                raw_block = m.group(1)
                for line in raw_block.splitlines():
                    s = line.strip()
                    if not s or s.startswith('#'): continue
                    # "- 01: Serie" or "- Campo: valor | fuente: correo"
                    numbered = re.match(r'^-?\s*(\d+)[:.]\s*(.+)', s)
                    piped    = re.match(r'^-\s+([\w\sáéíóúÁÉÍÓÚñÑ/_]+):\s*([^|]+)\|(.+)', s)
                    simple   = re.match(r'^-\s+([\w\sáéíóúÁÉÍÓÚñÑ_/]+):\s*(.+)', s)
                    dash     = re.match(r'^-\s+([\w\sáéíóúÁÉÍÓÚñÑ_]+)$', s)
                    if numbered:
                        result.append({"nombre": numbered.group(2).strip(), "fuente": "", "descripcion": ""})
                    elif piped:
                        meta   = piped.group(3)
                        fuente = ""
                        fm = re.search(r'fuente:\s*([^|]+)', meta)
                        vf = re.search(r'valor_fijo:\s*([^|]+)', meta)
                        vm = re.search(r'valores:\s*([^|]+)', meta)
                        fd = re.search(r'desc:\s*([^|]+)', meta)
                        if fm: fuente = fm.group(1).strip()
                        elif vf: fuente = "FIJO: " + vf.group(1).strip()
                        elif vm: fuente = "Valores: " + vm.group(1).strip()
                        result.append({
                            "nombre": piped.group(1).strip(),
                            "fuente": fuente,
                            "descripcion": fd.group(1).strip() if fd else "",
                        })
                    elif simple:
                        result.append({"nombre": simple.group(1).strip(), "fuente": simple.group(2).strip(), "descripcion": ""})
                    elif dash:
                        result.append({"nombre": dash.group(1).strip(), "fuente": "", "descripcion": ""})
                break  # usar el primer bloque que encuentre
        return result

    def _extract_acciones(self, block: str, accion_verbo: str, sistema: str,
                            nombre: str, desc: str) -> list[str]:
        """
        Construye el array de acciones del req desde los sub-bloques del .toon.
        Fusiona: descripcion, datos_*, campos_*, adjuntos, reglas, flujo, etc.
        """
        acciones: list[str] = []
        sis = sistema.strip() if sistema else "el sistema"

        # 1. Accion de apertura/validacion desde descripcion
        if desc:
            primer_frase = desc.split('.')[0].strip()
            if primer_frase:
                acciones.append(primer_frase + ".")

        # 2. Sub-bloques de items (datos_piloto, datos_generales, campos_extraer, etc.)
        # Patron: nombre_bloque\n      - item1\n      - item2
        for bloque_m in re.finditer(
            r'\n    (datos_\w+|columnas_\w+|campos_\w+|adjuntos|secciones|'
            r'campo_\w+|campos|flujo|columnas_log|campos_seadex\w*|'
            r'columnas_detalle|fuentes_catalogo|fila_\w+|flujo_\w+|'
            r'validaciones|por_cada_factura|facturas_seadex|consignatario)\s*\n((?:.*\n)*?)(?=\n    \w|\Z)',
            block
        ):
            bloque_nombre = bloque_m.group(1)
            bloque_texto  = bloque_m.group(2)

            # Extraer items de lista (- item)
            items = [
                l.strip()[2:].strip()
                for l in bloque_texto.splitlines()
                if l.strip().startswith('- ') and len(l.strip()) > 3
            ]
            # Extraer pares clave: valor
            pares = [
                f"{m.group(1)}: {m.group(2)}"
                for m in re.finditer(r'^\s+-(\s+[\w\s/áéíóúÁÉÍÓÚñÑ_]+):\s*(.+)', bloque_texto, re.MULTILINE)
            ]

            if bloque_nombre == "adjuntos":
                # adjuntos es multilínea libre
                txt = " ".join(bloque_texto.split())
                if txt:
                    acciones.append(f"Descargar adjuntos: {txt[:200]}.")

            elif bloque_nombre in ("datos_piloto", "datos_generales"):
                # Cada item es un campo a extraer del correo
                for item in items:
                    # Filtrar items que son reglas de negocio (contienen verbo condicional)
                    if not any(x in item.lower() for x in ["puede haber", "si ", "mismo nit", "todas las"]):
                        acciones.append(
                            f"Dentro del cuerpo del correo extraer {item}."
                        )

            elif bloque_nombre.startswith("columnas_seadex") or bloque_nombre in ("campos_seadex", "campos", "secciones"):
                for item in items:
                    acciones.append(f"En {sis}, ingresar/actualizar el campo {item}.")
                for par in pares:
                    acciones.append(f"En {sis}, configurar {par}.")

            elif bloque_nombre.startswith("columnas_log"):
                col_list = ", ".join(items[:5])
                if col_list:
                    acciones.append(f"Escribir en el log las columnas: {col_list}.")
                if len(items) > 5:
                    acciones.append(f"Continuar escribiendo columnas del log: {', '.join(items[5:])}.")

            elif bloque_nombre.startswith("campos_extraer"):
                for item in items:
                    acciones.append(f"Del documento, extraer el campo: {item}.")

            elif bloque_nombre.startswith("fila_"):
                nombre_fila = bloque_nombre.replace("_", " ").capitalize()
                for par in pares:
                    acciones.append(f"En la {nombre_fila}: {par}.")

            elif bloque_nombre in ("flujo", "flujo_general", "flujo_el_salvador"):
                for item in items:
                    acciones.append(f"Paso {sis}: {item}.")

            elif bloque_nombre in ("validaciones",):
                for item in items:
                    acciones.append(f"Validar que {item}.")

            elif bloque_nombre in ("facturas_seadex", "por_cada_factura", "consignatario"):
                for item in items:
                    acciones.append(f"Para cada factura en {sis}: {item}.")

            elif items:
                for item in items[:6]:
                    acciones.append(f"En {sis}, procesar: {item}.")

        # 3. Reglas con condicional SI => accion
        regla_m = re.search(r'\breglas\b[\w_]*\s*\n((?:.*\n)*?)(?=\n    \w|\Z)', block)
        if regla_m:
            for line in regla_m.group(1).splitlines():
                s = line.strip()
                if s.startswith('- ') and s[2:]:
                    regla = s[2:].strip()
                    if '=' in regla or 'si ' in regla.lower() or 'puede' in regla.lower():
                        acciones.append(f"Si {regla}: aplicar logica correspondiente.")

        # 4. Si no se extrajo nada, usar descripcion + accion como fallback
        if not acciones:
            if desc:
                acciones.append(desc[:200])
            if accion_verbo and accion_verbo.upper() not in ("NA", ""):
                acciones.append(f"{accion_verbo} en {sis}: segun descripcion del PDD.")

        return acciones

    def _extract_reglas(self, block: str) -> list[str]:
        """Extrae reglas del bloque de un req."""
        reglas = []
        m = re.search(r'\breglas(?:_criticas)?\s*\n((?:.*\n)*?)(?=\n\s{4}[a-zA-Z_]|\Z)', block)
        if m:
            for line in m.group(1).splitlines():
                s = line.strip()
                if s.startswith('- '):
                    reglas.append("Si " + s[2:] if not s[2:].lower().startswith('si ') else s[2:])
        return reglas

    def _evaluar_gaps(self, nombre, sistemas, desc, accion, inp, out):
        criticos, advertencias = [], []
        if not sistemas:
            criticos.append("SISTEMAS Y ACCESO — Sistema no especificado. Copilot no puede inferir qué aplicación automatizar.")
        if not nombre:
            criticos.append("Nombre del requerimiento no definido.")
        if not desc and not accion:
            criticos.append("Sin descripción ni acción definida. No es posible generar prompts útiles.")
        if not inp:
            advertencias.append("INPUTS — Input no especificado. Confirmar con el equipo de BA.")
        if not out:
            advertencias.append("OUTPUTS — Output no especificado. Confirmar con el equipo de BA.")
        return criticos, advertencias

    def _inferir_plataforma(self, sistemas: list[str], interfaces: dict, tecnologia: str) -> str:
        cloud_signals   = {"sharepoint", "onedrive", "teams", "forms", "dataverse"}
        desktop_signals = {"seadex", "jde", "sap", "siesa", "oracle", "as400", "navision"}
        for s in sistemas:
            key = s.lower()
            if key in desktop_signals: return "Desktop Flow"
            if key in cloud_signals:   return "Cloud Flow"
            iface = interfaces.get(s.upper(), "")
            if "Thick" in iface or "Local" in iface: return "Desktop Flow"
        return "Desktop Flow"  # default conservador

    # ── Parse Annotated (.toon con @accion) ──────────────────────────────────
    def parse_annotated(self) -> dict:
        """Parse básico del formato @document. Extiende clásico con sub-acciones."""
        proyecto   = self._val(r'id_proyecto:\s*(.+)')
        titulo     = self._val(r'titulo:\s*(.+)')
        version    = self._val(r'version:\s*(.+)')
        cliente    = self._val(r'cliente:\s*(.+)')
        tecnologia = self._val(r'tecnologia_rpa:\s*(.+)', "Power Automate")

        requerimientos = []
        # Dividir por @accion[N]
        chunks = re.split(r'@accion\[(\d+)\]', self.raw)
        for i in range(1, len(chunks), 2):
            idx   = chunks[i]
            block = chunks[i + 1] if i + 1 < len(chunks) else ""
            req_id = f"{proyecto}.REQ_{idx.zfill(2)}"

            nombre  = block.split('\n')[0].strip()
            sistema = self._extract_field(block, 'sistema')
            accion  = self._extract_field(block, 'accion')
            inp     = self._extract_field(block, 'input')
            out     = self._extract_field(block, 'output')
            desc    = self._extract_multiline(block, 'descripcion')

            if sistema.upper() == "NA": sistema = ""
            inp = inp.strip("[]")
            out = out.strip("[]")

            sistemas = [s.strip() for s in sistema.split(',') if s.strip()]
            exceps   = self._extract_excepciones(block, req_id)
            campos   = self._extract_campos_from_block(block)
            reglas   = self._extract_reglas(block)
            criticos, advertencias = self._evaluar_gaps(nombre, sistemas, desc, accion, inp, out)

            # Sub-requerimientos
            subs = []
            for sm in re.finditer(r'@subaccion\[(\d+\.\d+)\]\s*(.+?)\n((?:(?!@subaccion\[)[\s\S])*)', block):
                sub_id     = sm.group(1)
                sub_nombre = sm.group(2).strip()
                sub_block  = sm.group(3)
                sub_sis    = self._extract_field(sub_block, 'sistema')
                sub_inp    = self._extract_field(sub_block, 'input')
                sub_out    = self._extract_field(sub_block, 'output')
                sub_accion = self._extract_field(sub_block, 'accion')
                sub_desc   = self._extract_multiline(sub_block, 'descripcion')
                sub_campos = self._extract_campos_from_block(sub_block)
                sub_exceps = self._extract_excepciones(sub_block, f"{req_id}.{sub_id}")
                sub_sis_list = [s.strip() for s in sub_sis.split(',') if s.strip() and s.upper() != 'NA']
                c2, a2 = self._evaluar_gaps(sub_nombre, sub_sis_list, sub_desc, sub_accion, sub_inp, sub_out)
                subs.append({
                    "id": f"{req_id}.{sub_id}",
                    "nombre": sub_nombre,
                    "plataforma": "Desktop Flow",
                    "sistemas": sub_sis_list,
                    "input":  sub_inp.strip("[]"),
                    "output": sub_out.strip("[]"),
                    "accion": sub_accion,
                    "descripcion": sub_desc[:400],
                    "campos_extraer": sub_campos,
                    "reglas_negocio": [],
                    "excepciones": sub_exceps,
                    "gaps": {"criticos": c2, "advertencias": a2, "puede_generar": len(c2) == 0},
                })

            requerimientos.append({
                "id": req_id,
                "nombre": nombre,
                "plataforma": "Desktop Flow",
                "sistemas": sistemas,
                "input":  inp,
                "output": out,
                "accion": accion,
                "descripcion": desc[:400],
                "campos_extraer": campos,
                "reglas_negocio": reglas,
                "excepciones": exceps,
                "gaps": {"criticos": criticos, "advertencias": advertencias, "puede_generar": len(criticos) == 0},
                "sub_requerimientos": subs,
            })

        return {
            "proyecto":   proyecto,
            "tecnologia": tecnologia,
            "es_hibrido": False,
            "clasificacion": {"razon": f"Declarado en PDD: {tecnologia}", "plataforma_cloud": None, "plataforma_desktop": None},
            "generado": datetime.now(timezone.utc).isoformat(),
            "_meta": {"titulo": titulo, "version": version, "cliente": cliente},
            "requerimientos": requerimientos,
        }

    def parse(self) -> dict:
        return self.parse_annotated() if self.formato == "annotated" else self.parse_classic()


# ══════════════════════════════════════════════════════════════════════════════
# 2. CLASIFICACIÓN DE TECNOLOGÍA
# ══════════════════════════════════════════════════════════════════════════════

CLOUD_SIG   = {"sharepoint", "onedrive", "teams", "forms", "dataverse", "power apps"}
DESKTOP_SIG = {"seadex", "jde", "sap", "siesa", "oracle", "as400", "navision"}

def clasificar_tecnologia(analisis: dict) -> dict:
    raw = analisis["tecnologia"].lower()
    todos_sistemas = {s.lower() for r in analisis["requerimientos"] for s in r["sistemas"]}

    has_cloud   = bool(todos_sistemas & CLOUD_SIG)
    has_desktop = bool(todos_sistemas & DESKTOP_SIG)

    if "desktop" in raw and "cloud" in raw:
        tk, label = "hybrid", "Power Automate Híbrido"
    elif "desktop" in raw:
        tk, label = "desktop", "Power Automate Desktop"
    elif "cloud" in raw:
        tk, label = "cloud", "Power Automate Cloud"
    elif has_desktop and has_cloud:
        tk, label = "hybrid", "Power Automate Híbrido"
    elif has_desktop:
        tk, label = "desktop", "Power Automate Desktop"
    elif has_cloud:
        tk, label = "cloud", "Power Automate Cloud"
    else:
        tk, label = "desktop", "Power Automate Desktop"

    analisis["tecnologia"]  = label
    analisis["es_hibrido"]  = tk == "hybrid"
    analisis["_tech_key"]   = tk
    return analisis


# ══════════════════════════════════════════════════════════════════════════════
# 3. GENERADOR DE PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def _placeholder_ruta(inp: str, nombre: str, ext: str = "xlsx") -> str:
    """Devuelve ruta real si parece nombre de archivo, o placeholder descriptivo."""
    if inp and re.search(r'\.\w{2,5}$', inp):
        return inp
    if inp and inp not in ("NA", ""):
        return f"[rutaArchivo\\aqui\\va\\la\\ruta\\{inp}.{ext}]"
    return f"[rutaArchivo\\aqui\\va\\la\\ruta\\{subflow_name(nombre)}.{ext}]"

def _inferir_tipo_sistema(sistemas: list[str]) -> str:
    """Clasifica el tipo de sistema dominante del req."""
    for s in sistemas:
        sl = s.lower()
        if any(x in sl for x in ["seadex", "sap", "jde", "siesa", "oracle", "as400"]): return "ui_legacy"
        if "excel" in sl: return "excel"
        if "outlook" in sl: return "outlook"
        if "sharepoint" in sl: return "sharepoint_ui"
        if "onedrive" in sl: return "onedrive"
    return "generico"


def _accion_to_sentencia(accion: str, sf_name: str, sis_pri: str, var_dt: str, var_estado: str) -> tuple[str, list[str]]:
    """
    Convierte una acción del JSON de análisis a una sentencia de prompt PAD.
    Retorna (sentencia, [variables_referenciadas]).
    """
    a = accion.strip()
    if not a:
        return "", []

    vars_ref: list[str] = []

    # ── Detectar tipo de acción por palabras clave ────────────────────────

    # Validar / filtrar
    if any(w in a.lower() for w in ["validar", "verificar", "identificar correos", "filtrar"]):
        # Extraer condición entre comillas o paréntesis si existe
        cond_m = re.search(r'\(([^)]{5,})\)', a)
        cond   = cond_m.group(1) if cond_m else a[a.lower().index("validar")+7:a.lower().index("validar")+80].strip() if "validar" in a.lower() else a[:80]
        return f"Agregar accion If para validar: {cond[:120]}.", [var_estado]

    # Abrir / navegar
    if any(w in a.lower() for w in ["abrir el correo", "abrir correo"]):
        return f"Usar la accion 'Hacer clic en elemento de la UI' para abrir el correo encontrado en [Lst{sf_name}Correos].", [f"[Lst{sf_name}Correos]"]

    # Extraer campo del cuerpo del correo
    if "extraer" in a.lower() and ("cuerpo" in a.lower() or "correo" in a.lower() or "adjunto" in a.lower()):
        # Obtener el nombre del campo
        campo_m = re.search(r'extraer\s+(.+?)(?:\s*\(|$)', a, re.IGNORECASE)
        campo   = campo_m.group(1).strip() if campo_m else a.replace("extraer", "").strip()[:60]
        # Generar nombre de variable Beecker
        # Evitar doble prefijo si beecker_var ya devuelve uno
        bv = beecker_var(campo)
        var_name = f"[Str{bv}]" if not bv[:3] in ("Str","Int","Bln","Flt","Lst","dt_","Arr","Obj") else f"[{bv}]"
        vars_ref.append(var_name)
        return f"Extraer del cuerpo del correo el campo '{campo}' y guardar en {var_name}.", [var_name]

    # Descargar adjuntos
    if any(w in a.lower() for w in ["descargar adjunto", "descargar archivo"]):
        var_adj = f"[Lst{sf_name}Adjuntos]"
        vars_ref.append(var_adj)
        detalles = a[a.lower().index("descargar")+10:][:100].strip()
        return f"Descargar los adjuntos del correo ({detalles[:80]}) y guardar en {var_adj}.", [var_adj]

    # Leer archivo Excel
    if any(w in a.lower() for w in ["leer", "abrir", "launch excel", "read from excel"]):
        if "excel" in a.lower() or "xlsx" in a.lower():
            arch_m = re.search(r'["\']([^"\']+\.xlsx)["\']', a) or re.search(r'archivo\s+([\w\s\-]+\.xlsx)', a, re.IGNORECASE)
            arch   = arch_m.group(1) if arch_m else f"[Str{sf_name}Ruta]"
            vars_ref.append(var_dt)
            return f"Abrir el archivo Excel '{arch}' con Launch Excel. Leer hoja activa con Read from Excel Worksheet y guardar en {var_dt}.", [var_dt]

    # Escribir en Excel
    if any(w in a.lower() for w in ["escribir", "guardar en excel", "write to excel", "agregar fila"]):
        col_m = re.search(r'columnas?:?\s*(.+)', a, re.IGNORECASE)
        cols  = col_m.group(1).strip()[:120] if col_m else "las columnas definidas en el PDD"
        return f"Escribir en la siguiente fila disponible con Write to Excel Worksheet: {cols}.", []

    # Hacer clic en elemento UI
    if any(w in a.lower() for w in ["hacer clic", "clic en", "seleccionar", "click"]):
        elem_m = re.search(r'en\s+["\']?([^"\']+?)["\']?\s*(?:y|e ingresar|->|$)', a, re.IGNORECASE)
        elem   = elem_m.group(1).strip()[:60] if elem_m else a[:80]
        return f"Usar accion 'Hacer clic en elemento de la UI' sobre '{elem}' en {sis_pri}.", []

    # Ingresar / escribir en campo UI
    if any(w in a.lower() for w in ["ingresar", "escribir en campo", "capturar"]):
        campo_m = re.search(r'(?:ingresar|escribir|capturar)\s+(.+?)(?:\sen\s|\sa\s|$)', a, re.IGNORECASE)
        campo   = campo_m.group(1).strip()[:60] if campo_m else a[:80]
        var_m   = re.search(r'\[([^\]]+)\]', a)
        var_n   = f"[{var_m.group(1)}]" if var_m else f"[Str{beecker_var(campo)}]"
        vars_ref.append(var_n)
        return f"Usar accion 'Rellenar campo de texto en la ventana' con el valor {var_n} en el campo '{campo[:50]}'.", [var_n]

    # Navegar a sección / ruta
    if any(w in a.lower() for w in ["navegar", "ir a", "acceder", "abrir seccion", "ruta_navegacion", "doc. exportacion", "ingreso documento"]):
        sec_m = re.search(r'(?:a|hacia|seccion)\s+["\']?([^"\'>\n]+?)(?:["\']|>|$)', a, re.IGNORECASE)
        sec   = sec_m.group(1).strip()[:80] if sec_m else a[:80]
        return f"Navegar en {sis_pri} a la seccion '{sec}'.", []

    # Esperar
    if any(w in a.lower() for w in ["esperar", "wait"]):
        return f"Usar accion 'Esperar al contenido de la ventana' hasta que {a[:80].lower()}.", []

    # Guardar / actualizar en sistema
    if any(w in a.lower() for w in ["guardar", "actualizar en seadex", "actualizar en jde", "actualizar en sap"]):
        btn_m = re.search(r'(?:boton|clic|accion)\s+["\']?([^"\']+)["\']?', a, re.IGNORECASE)
        btn   = btn_m.group(1).strip()[:40] if btn_m else "Guardar"
        return f"Hacer clic en el boton '{btn}' en {sis_pri} y esperar mensaje de confirmacion.", []

    # Mover archivo
    if any(w in a.lower() for w in ["mover", "move file", "copiar archivo"]):
        return f"Usar accion Move File para mover {a[a.lower().index('mover')+5:a.lower().index('mover')+80].strip()[:60]}.", []

    # Notificar / enviar correo
    if any(w in a.lower() for w in ["notificar", "enviar correo", "send email"]):
        asunto_m = re.search(r"['\"]([^'\"]{5,80})['\"]", a)
        asunto   = asunto_m.group(1) if asunto_m else f"Notificacion de {sf_name}"
        return f"Usar accion Send Email en Outlook con asunto '{asunto}' y adjuntar captura de pantalla.", []

    # Registrar en log
    if any(w in a.lower() for w in ["registrar en log", "registrar 'sin procesar'", "registrar en columna"]):
        return f"Escribir en el log de ejecucion: {a[:100]}.", [var_estado]

    # Si la condicion es compleja (si X → entonces Y)
    if " → " in a or "si " in a.lower()[:10]:
        return f"Agregar accion If para implementar la logica: {a[:120]}.", [var_estado]

    # Fallback: usar la accion textual como sentencia directa
    return f"Ejecutar en {sis_pri}: {a[:120]}.", []


def _bloques_logicos(req: dict) -> list[dict]:
    """
    Descompone un req en su lista de bloques lógicos atómicos leyendo
    el campo 'acciones' del JSON de análisis como fuente principal.
    Cada bloque tiene: tipo, titulo, sentencias[], accion_cubierta, variables[], nota.
    El pipeline _empaquetar_en_prompts los convierte en N prompts respetando el límite.
    """
    nombre   = req["nombre"]
    sistemas = req["sistemas"]
    inp      = req.get("input", req.get("inputs", [""])[0] if req.get("inputs") else "")
    if isinstance(inp, list): inp = ", ".join(inp)
    out      = req.get("output", req.get("outputs", [""])[0] if req.get("outputs") else "")
    if isinstance(out, list): out = ", ".join(out)
    acciones = req.get("acciones", [])      # ← FUENTE PRINCIPAL
    exceps   = req.get("excepciones", [])
    reglas   = req.get("reglas_negocio", [])
    campos   = req.get("campos_extraer", [])
    req_script = req.get("requiere_script", False)
    just_script = req.get("justificacion_script", "")

    sf_name  = subflow_name(nombre)
    tipo_sis = _inferir_tipo_sistema(sistemas)
    sis_pri  = sistemas[0] if sistemas else "el sistema"
    ruta     = _placeholder_ruta(inp, nombre)

    var_ruta   = f"[Str{sf_name}Ruta]"
    var_estado = "[StrEstadoEjecucion]"
    var_modulo = "[StrModulo]"
    var_dt     = f"[dt_{sf_name}]"

    bloques: list[dict] = []

    # ── BLOQUE 0: Variables base (siempre primero) ────────────────────────
    vars_base = [var_ruta, var_estado, var_modulo]
    sentencias_vars = [
        f"Inicializar variable de texto {var_ruta} con la ruta {ruta}.",
        f"Inicializar variable de texto {var_estado} con valor vacio.",
        f"Inicializar variable de texto {var_modulo} con valor '{sf_name}'.",
    ]
    # Variables extra derivadas de inputs múltiples
    for part in inp.split(","):
        p = part.strip()
        if p and p.upper() not in ("NA", ""):
            vn = f"[Str{beecker_var(p)}]"
            if vn not in vars_base:
                sentencias_vars.append(f"Inicializar variable de texto {vn} con valor vacio.")
                vars_base.append(vn)
    # Si requiere script, agregar variable de resultado de script
    if req_script:
        var_script = f"[Str{sf_name}ScriptResult]"
        sentencias_vars.append(f"Inicializar variable de texto {var_script} con valor vacio.")
        vars_base.append(var_script)

    bloques.append({
        "tipo": "init_vars",
        "titulo": "Inicializar variables",
        "sentencias": sentencias_vars,
        "accion_cubierta": "Inicializacion de variables del subflow",
        "variables": vars_base,
        "nota": (
            f"Ajustar {var_ruta} con la ruta real. "
            f"Prefijos Beecker: Str=texto, Int=entero, Bln=booleano, dt_=DataTable, Lst=lista. "
            f"PROHIBIDO hardcode de credenciales, rutas o correos."
            + (f" SCRIPT REQUERIDO: {just_script}" if req_script else "")
        ),
        "instruccion_previa": (
            f"ANTES DE PEGAR: Crear manualmente el subflow '{sf_name}' "
            f"(Menu Subflows > Nuevo subflujo en PAD). "
            f"Copilot no puede crear subflows. Posicionarse dentro. "
            f"Agregar accion Comentario al inicio con: proposito, req {req['id']}, "
            f"precondiciones y postcondiciones."
        ),
    })

    # ── BLOQUES PRINCIPALES: Una sentencia por acción del JSON ────────────
    # Agrupar acciones en lotes de MAX_ACC_PER_BLOQUE acciones afines
    MAX_ACC = 4
    if acciones:
        # Clasificar acciones por afinidad para agruparlas
        grupos_acc: list[list[str]] = []
        grupo_actual: list[str]     = []
        tipo_actual: str            = ""

        def _tipo_acc(a: str) -> str:
            al = a.lower()
            if any(w in al for w in ["extraer", "descargar adjunto"]): return "extraer"
            if any(w in al for w in ["hacer clic", "clic en", "seleccionar"]): return "ui_click"
            if any(w in al for w in ["ingresar", "escribir en campo", "capturar"]): return "ui_type"
            if any(w in al for w in ["navegar", "ir a", "abrir seccion"]): return "navegar"
            if any(w in al for w in ["validar", "verificar", "si ", "si unidad"]): return "validar"
            if any(w in al for w in ["guardar", "actualizar", "write to excel", "agregar fila"]): return "guardar"
            if any(w in al for w in ["notificar", "enviar correo", "send email"]): return "notificar"
            if any(w in al for w in ["mover", "move file"]): return "mover"
            if any(w in al for w in ["leer", "abrir", "launch", "read from"]): return "leer"
            return "generico"

        for acc in acciones:
            t = _tipo_acc(acc)
            if t != tipo_actual or len(grupo_actual) >= MAX_ACC:
                if grupo_actual:
                    grupos_acc.append(grupo_actual)
                grupo_actual = [acc]
                tipo_actual  = t
            else:
                grupo_actual.append(acc)
        if grupo_actual:
            grupos_acc.append(grupo_actual)

        # Convertir cada grupo en un bloque
        for gi, grupo in enumerate(grupos_acc):
            sentencias_bloque: list[str] = []
            vars_bloque:       list[str] = []
            tipo_grupo = _tipo_acc(grupo[0])

            for acc in grupo:
                sent, vs = _accion_to_sentencia(acc, sf_name, sis_pri, var_dt, var_estado)
                if sent:
                    sentencias_bloque.append(sent)
                    vars_bloque.extend(vs)

            if not sentencias_bloque:
                continue

            # Título descriptivo por tipo
            titulo_map = {
                "extraer":  f"Extraer datos del correo — grupo {gi+1}",
                "ui_click": f"Interaccion UI en {sis_pri} — grupo {gi+1}",
                "ui_type":  f"Ingreso de datos en {sis_pri} — grupo {gi+1}",
                "navegar":  f"Navegacion en {sis_pri}",
                "validar":  f"Validaciones — grupo {gi+1}",
                "guardar":  f"Guardar/Actualizar en {sis_pri}",
                "notificar":"Notificacion",
                "mover":    "Mover archivos",
                "leer":     f"Leer datos de {sis_pri}",
                "generico": f"Acciones — grupo {gi+1}",
            }
            titulo_bloque = titulo_map.get(tipo_grupo, f"Acciones {gi+1}")
            # Si solo hay un grupo de este tipo, quitar el número
            if len([g for g in grupos_acc if _tipo_acc(g[0]) == tipo_grupo]) == 1:
                titulo_bloque = titulo_bloque.replace(f" — grupo {gi+1}", "").replace(f" — grupo {gi+1}", "")

            # Nota especial para acciones de script
            nota_bloque = f"Acciones {gi*MAX_ACC+1}-{gi*MAX_ACC+len(grupo)} de {len(acciones)} del req."
            if req_script and tipo_grupo in ("extraer", "validar", "guardar"):
                nota_bloque += f" NOTA SCRIPT: {just_script} — implementar como script externo en PAD."
            if tipo_grupo in ("ui_click", "ui_type", "navegar"):
                nota_bloque += f" ACCION UI: usar el grabador de PAD para {sis_pri}. Habilitar 'Simular accion' donde sea posible."

            bloques.append({
                "tipo":         f"acc_{gi}",
                "titulo":       titulo_bloque,
                "sentencias":   sentencias_bloque,
                "accion_cubierta": f"Acciones {gi*MAX_ACC+1}-{gi*MAX_ACC+len(grupo)} de {len(acciones)}: {grupo[0][:50]}{'...' if len(grupo)>1 else ''}",
                "variables":    list(dict.fromkeys(vars_bloque)),
                "nota":         nota_bloque,
                "instruccion_previa": None,
            })

    # ── FALLBACK si no hay acciones en JSON: usar campos/desc ────────────
    elif campos:
        MAX_COLS = 4
        grupos_c = [campos[i:i+MAX_COLS] for i in range(0, len(campos), MAX_COLS)]
        for gi, grupo in enumerate(grupos_c):
            col_desc = "; ".join(
                f"'{c['nombre']}'" + (f" <- {c['fuente']}" if c.get("fuente") else "")
                for c in grupo
            )
            es_ultimo = gi == len(grupos_c) - 1
            bloques.append({
                "tipo":         f"campos_{gi}",
                "titulo":       f"Procesar columnas ({gi+1}/{len(grupos_c)}) — {sis_pri}",
                "sentencias":   [f"Procesar en {sis_pri} las columnas: {col_desc}."],
                "accion_cubierta": f"Columnas {gi*MAX_COLS+1}-{gi*MAX_COLS+len(grupo)} de {len(campos)}",
                "variables":    [var_dt],
                "nota":         (
                    f"VERIFICAR al terminar: {len(campos)} columnas totales: "
                    + ", ".join(f"'{c['nombre']}'" for c in campos)
                    if es_ultimo else f"Grupo {gi+1} de {len(grupos_c)}."
                ),
                "instruccion_previa": None,
            })

    # ── BLOQUES: Reglas de negocio (si no están ya en acciones) ──────────
    # Solo agregar reglas que NO están cubiertas en los bloques de acciones
    acciones_lower = " ".join(acciones).lower()
    reglas_nuevas  = [r for r in reglas if r[:30].lower() not in acciones_lower]
    if reglas_nuevas:
        MAX_REG = 3
        for gi, grupo in enumerate([reglas_nuevas[i:i+MAX_REG] for i in range(0, len(reglas_nuevas), MAX_REG)]):
            bloques.append({
                "tipo":         f"reglas_{gi}",
                "titulo":       f"Reglas de negocio{f' ({gi+1})' if len(reglas_nuevas)>MAX_REG else ''}",
                "sentencias":   [f"Agregar condicion If para la regla: {r}." for r in grupo],
                "accion_cubierta": f"Reglas de negocio {gi*MAX_REG+1}-{gi*MAX_REG+len(grupo)}",
                "variables":    [var_estado],
                "nota":         "Implementar como bloque If en PAD. Maximo 3 niveles de anidacion (regla Beecker).",
                "instruccion_previa": None,
            })

    # ── BLOQUES: Una excepcion por bloque ────────────────────────────────
    for ei, exc in enumerate(exceps):
        cond       = exc.get("condicion", "error")
        accion_exc = exc.get("accion", "")
        log_exc    = exc.get("log", "")
        msg_m      = re.search(r"['\"]([^'\"]{5,80})['\"]", accion_exc)
        asunto     = msg_m.group(1) if msg_m else f"Error en {nombre}"
        # Extraer sub-acciones de la excepcion
        sentencias_exc = [
            f"Agregar bloque 'On block error' llamado '{sf_name}_Err{ei+1}'.",
            f"Si ocurre '{cond}': establecer {var_estado} en 'Error'.",
            f"Llamar AddToLog con {var_modulo}, nivel 'Error', mensaje '{asunto}'.",
            f"Usar Send Email con asunto '{asunto}' y adjuntar captura de pantalla.",
        ]
        # Sub-acciones adicionales de la excepcion (mover archivos, registrar en columnas, etc.)
        if "mover" in accion_exc.lower() or "carpeta" in accion_exc.lower():
            carpeta_m = re.search(r"carpeta\s+['\"]?([^'\"]+)['\"]?", accion_exc, re.IGNORECASE)
            carpeta   = carpeta_m.group(1) if carpeta_m else "Facturas Procesadas"
            sentencias_exc.append(f"Usar accion Move File para mover los archivos a la carpeta '{carpeta}'.")
        if "sin procesar" in accion_exc.lower() or "columna status" in accion_exc.lower():
            sentencias_exc.append(f"Registrar 'Sin procesar' en la columna Status del log de ejecucion.")
        if "detalle" in accion_exc.lower() or "columna detalle" in accion_exc.lower():
            sentencias_exc.append(f"Registrar el motivo del error en la columna Detalle del log.")

        bloques.append({
            "tipo":         f"excepcion_{ei}",
            "titulo":       f"Excepcion {ei+1}/{len(exceps)}: {cond[:40]}",
            "sentencias":   sentencias_exc,
            "accion_cubierta": f"Excepcion: {cond[:60]}",
            "variables":    [var_estado, var_modulo],
            "nota":         (
                f"Accion completa segun PDD: {accion_exc[:300]}. "
                + (f"Log: {log_exc}. " if log_exc else "")
                + "Destinatarios parametrizables. Adjuntar captura de pantalla. "
                + "REGLA Beecker: al menos un log AddToLog por manejo de error."
            ),
            "instruccion_previa": None,
        })

    # ── BLOQUE: Cierre de aplicacion ─────────────────────────────────────
    if tipo_sis == "excel":
        bloques.append({
            "tipo":         "close_app",
            "titulo":       "Cerrar Excel",
            "sentencias":   ["Guardar y cerrar el archivo Excel con la accion Close Excel."],
            "accion_cubierta": "Cierre del archivo Excel",
            "variables":    [],
            "nota":         "Cerrar siempre el archivo, incluso en caso de error (usar bloque Finally si aplica).",
            "instruccion_previa": None,
        })
    elif tipo_sis == "ui_legacy":
        bloques.append({
            "tipo":         "close_app",
            "titulo":       f"Cerrar sesion en {sis_pri}",
            "sentencias":   [
                f"Hacer clic en el boton Cerrar sesion o Salir de {sis_pri}.",
                "Esperar al cierre de la ventana con la accion 'Esperar al proceso'.",
            ],
            "accion_cubierta": f"Cierre de sesion en {sis_pri}",
            "variables":    [],
            "nota":         f"Cerrar siempre la sesion de {sis_pri} al terminar, aunque haya error.",
            "instruccion_previa": None,
        })

    # ── BLOQUE: Log de ejecucion (siempre al final) ───────────────────────
    log_ruta = r"[rutaLog\LOGS\Log_Ejecucion.xlsx]"
    bloques.append({
        "tipo":         "log",
        "titulo":       "Registro en log de ejecucion",
        "sentencias":   [
            f"Abrir archivo Excel {log_ruta} con Launch Excel.",
            "Usar accion Get Current Date and Time y guardar en [DtFechaEjecucion].",
            f"Escribir en la siguiente fila disponible con Write to Excel Worksheet: "
            f"[DtFechaEjecucion] en col Fecha, '{nombre}' en col Proceso, "
            f"{var_estado} en col Status, {var_modulo} en col Modulo.",
            "Guardar y cerrar con Close Excel.",
        ],
        "accion_cubierta": f"Log de auditoria — output: {out}" if out and out.upper() not in ("NA","") else "Log de auditoria",
        "variables":    [var_estado, var_modulo, "[DtFechaEjecucion]"],
        "nota":         (
            f"Configurar {log_ruta} como variable global en el flow principal. "
            "Columnas del log: Fecha, Modulo, Proceso, Status, Detalle. "
            "Segun Beecker, usar subflujo AddToLog del Framework si existe."
        ),
        "instruccion_previa": None,
    })

    return bloques



def _empaquetar_en_prompts(bloques: list[dict], limit: int) -> list[dict]:
    """
    Toma la lista de bloques lógicos y los empaqueta en prompts
    respetando el límite de caracteres. Si un bloque solo ya supera
    el límite, se parte por sentencias individuales.
    """
    prompts: list[dict] = []
    num = 1

    current_sentencias : list[str] = []
    current_cubiertos  : list[str] = []
    current_variables  : list[str] = []
    current_notas      : list[str] = []
    current_titulo     : str        = ""
    current_instruccion: str | None = None

    def flush():
        nonlocal num, current_sentencias, current_cubiertos, current_variables, current_notas, current_titulo, current_instruccion
        if not current_sentencias:
            return
        texto = " ".join(current_sentencias)
        prompts.append({
            "numero_prompt": num,
            "titulo": current_titulo,
            "instruccion_previa": current_instruccion,
            "prompt": texto,
            "caracteres": len(texto),
            "acciones_cubiertas": current_cubiertos[:],
            "variables_referenciadas": list(dict.fromkeys(current_variables)),
            "nota_desarrollador": " | ".join(current_notas),
        })
        num += 1
        current_sentencias  = []
        current_cubiertos   = []
        current_variables   = []
        current_notas       = []
        current_titulo      = ""
        current_instruccion = None

    for bloque in bloques:
        instruccion = bloque.get("instruccion_previa")
        # Si el bloque tiene instruccion_previa → siempre inicia prompt nuevo
        if instruccion and current_sentencias:
            flush()

        if not current_titulo:
            current_titulo      = bloque["titulo"]
            current_instruccion = instruccion
        elif instruccion:
            current_titulo      = bloque["titulo"]
            current_instruccion = instruccion

        for sentencia in bloque["sentencias"]:
            # Probar si cabe en el prompt actual
            probe = " ".join(current_sentencias + [sentencia])
            if len(probe) > limit and current_sentencias:
                flush()
                current_titulo = bloque["titulo"]
                current_instruccion = bloque.get("instruccion_previa")

            # Si la sentencia sola ya supera el limite, truncar
            if len(sentencia) > limit:
                sentencia = sentencia[:limit - 3] + "..."

            current_sentencias.append(sentencia)

        current_cubiertos.append(bloque["accion_cubierta"])
        current_variables.extend(bloque.get("variables", []))
        if bloque.get("nota"):
            current_notas.append(bloque["nota"])

    flush()
    return prompts


def build_prompts_desktop(req: dict, proyecto: str) -> list[dict]:
    """
    Pipeline dinámico: descompone el req en bloques lógicos atómicos
    y los empaqueta en N prompts segun el contenido real.
    N puede ser 2, 4, 8, 12... lo que el req necesite.
    """
    bloques = _bloques_logicos(req)
    return _empaquetar_en_prompts(bloques, LIMIT_DESKTOP)



def build_sub_prompts(sub: dict, req: dict, proyecto: str) -> dict:
    """Genera el objeto de sub-prompts para un sub-requerimiento."""
    if not sub["gaps"]["puede_generar"]:
        return {
            "id_subflujo": sub["id"],
            "nombre_subflujo": sub["nombre"],
            "plataforma": sub.get("plataforma", "Desktop Flow"),
            "generar_prompt": False,
            "gaps_detectados": {
                "criticos": sub["gaps"]["criticos"],
                "advertencias": sub["gaps"]["advertencias"],
                "impacto": "No se generaron prompts. Resolver gaps criticos.",
            },
            "prompts_secuenciales": [],
            "pasos_manuales_requeridos": [f"Gap a resolver: {c}" for c in sub["gaps"]["criticos"]],
        }

    sub_prompts = build_prompts_desktop(sub, proyecto)
    # Adaptar instruccion_previa del primer prompt para sub-req
    if sub_prompts:
        sf_padre = subflow_name(req["nombre"])
        sub_prompts[0]["instruccion_previa"] = (
            f"ANTES DE PEGAR: Este sub-req {sub['id']} es parte de {req['id']}. "
            f"Posicionarse dentro del subflow '{sf_padre}' del req padre. "
            f"Los prompts de sub-reqs se pegan dentro del mismo subflow del padre."
        )
    return {
        "id_subflujo": sub["id"],
        "nombre_subflujo": sub["nombre"],
        "plataforma": sub.get("plataforma", "Desktop Flow"),
        "generar_prompt": True,
        "gaps_detectados": {
            "criticos": sub["gaps"]["criticos"],
            "advertencias": sub["gaps"]["advertencias"],
            "impacto": "Prompts generados con advertencias." if sub["gaps"]["advertencias"] else "Sin gaps detectados.",
        },
        "prompts_secuenciales": sub_prompts,
        "pasos_manuales_requeridos": [],
    }


def build_prompts_json(analisis: dict) -> dict:
    proyecto  = analisis["proyecto"]
    tech_key  = analisis.get("_tech_key", "desktop")
    prompts_g = []

    for req in analisis["requerimientos"]:
        puede = req["gaps"]["puede_generar"]
        plat  = req.get("plataforma", "Desktop Flow")

        # Generar prompts principales
        if puede:
            if "cloud" in plat.lower():
                # Cloud: por ahora genera estructura básica
                # (extensible: conectar con builder Cloud específico)
                seq_prompts = _build_cloud_basic(req, proyecto)
            else:
                seq_prompts = build_prompts_desktop(req, proyecto)
        else:
            seq_prompts = []

        # Sub-requerimientos
        sub_prs = [build_sub_prompts(sub, req, proyecto) for sub in req.get("sub_requerimientos", [])]

        # Pasos manuales
        manuales = []
        tipo_sis = _inferir_tipo_sistema(req["sistemas"])
        if tipo_sis == "ui_legacy":
            manuales.append(f"Grabar selectores UI de {req['sistemas'][0] if req['sistemas'] else 'el sistema'} con el grabador de PAD.")
        if not puede:
            manuales += ["Resolver gaps criticos antes de generar prompts."] + [f"Gap: {c}" for c in req["gaps"]["criticos"]]
        if req["gaps"]["advertencias"]:
            manuales.append("Revisar advertencias en gaps_detectados con el equipo de BA.")

        prompts_g.append({
            "id_flujo":    req["id"],
            "nombre_flujo": req["nombre"],
            "plataforma":  plat,
            "generar_prompt": puede,
            "gaps_detectados": {
                "criticos":     req["gaps"]["criticos"],
                "advertencias": req["gaps"]["advertencias"],
                "impacto": (
                    "No se generaron prompts. Resolver gaps criticos." if req["gaps"]["criticos"]
                    else "Prompts generados con advertencias." if req["gaps"]["advertencias"]
                    else "Sin gaps detectados."
                ),
            },
            "prompts_secuenciales": seq_prompts,
            "resumen_cobertura": (
                f"{len(seq_prompts)} prompt(s) para {plat}. "
                f"Cubren: variables -> {req['sistemas'][0] if req['sistemas'] else 'sistema'} -> errores -> log."
                if puede else ""
            ),
            "pasos_manuales_requeridos": manuales,
            "sub_prompts": sub_prs,
        })

    total   = sum(len(e["prompts_secuenciales"]) for e in prompts_g)
    total  += sum(len(s["prompts_secuenciales"]) for e in prompts_g for s in e["sub_prompts"])
    con     = sum(1 for e in prompts_g if e["generar_prompt"])
    sin     = len(prompts_g) - con

    return {
        "proyecto":   proyecto,
        "tecnologia": analisis["tecnologia"],
        "es_hibrido": analisis["es_hibrido"],
        "generado":   datetime.now(timezone.utc).isoformat(),
        "_resumen": {
            "total_requerimientos": len(prompts_g),
            "con_prompts":   con,
            "sin_prompts":   sin,
            "total_prompts": total,
        },
        "prompts_generados": prompts_g,
    }


def _build_cloud_basic(req: dict, proyecto: str) -> list[dict]:
    """Builder básico para Cloud Flow. Extensible para conectores específicos."""
    nombre   = req["nombre"]
    sistemas = req["sistemas"]
    sis_pri  = sistemas[0] if sistemas else "el sistema"

    trigger_map = {
        "outlook":    "Cuando llega un nuevo correo electronico (V3) del conector Office 365 Outlook",
        "sharepoint": "Cuando se crea o modifica un elemento del conector SharePoint",
        "forms":      "Cuando se envia una nueva respuesta del conector Microsoft Forms",
        "onedrive":   "Cuando se crea un archivo del conector OneDrive for Business",
    }
    trigger = "trigger manual (Instant Flow)"
    conector = "HTTP"
    for s in sistemas:
        for k, v in trigger_map.items():
            if k in s.lower():
                trigger = v
                conector = k.capitalize()
                break

    p1 = trunc(f"Crear un Cloud Flow automatizado con el trigger {trigger}.", LIMIT_CLOUD)
    p2 = trunc(
        f"Agregar la accion Inicializar variable tres veces: "
        f"StrEstadoEjecucion de tipo texto, StrModulo de tipo texto con valor '{subflow_name(nombre)}', "
        f"ArrResultados de tipo array.",
        LIMIT_CLOUD
    )
    return [
        {"numero_prompt": 1, "titulo": "Trigger", "instruccion_previa": "Pegar en 'Crear tu automatizacion con Copilot' en Power Automate.", "prompt": p1, "caracteres": len(p1), "acciones_cubiertas": ["Trigger del flujo"], "variables_referenciadas": [], "nota_desarrollador": f"Conector: {conector}. Configurar filtros del trigger en el panel de diseno."},
        {"numero_prompt": 2, "titulo": "Variables", "instruccion_previa": "Pegar en el panel Copilot del diseñador.", "prompt": p2, "caracteres": len(p2), "acciones_cubiertas": ["Inicializacion de variables"], "variables_referenciadas": ["StrEstadoEjecucion", "StrModulo", "ArrResultados"], "nota_desarrollador": "Sin corchetes en variables Cloud. Ajustar tipos segun uso real."},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# 4b. GENERADOR DE ARCHIVO .TOON DE PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def build_prompts_toon(prompts_data: dict, analisis: dict) -> str:
    """
    Convierte el dict de prompts en un archivo .toon de lectura directa.
    Estructura diseñada para que el usuario solo copie y pegue cada prompt.
    
    Formato por requerimiento:
      @req[N] NombreReq
        plataforma: Desktop Flow | Cloud Flow
        subflow: NombreSubflow
        total_prompts: N
        [si hay gaps]: gaps_advertencias: texto
        [si no genera]: sin_prompts: motivo
        
        @prompt[N.M] TituloPrompt
          caracteres: N
          acciones_cubiertas: accion1 | accion2
          variables: [Var1] [Var2]
          ---instruccion---
          INSTRUCCION PREVIA: texto
          ---prompt---
          texto del prompt listo para copiar
          ---nota---
          NOTA DESARROLLADOR: texto
          ---fin---
        
        @subreq[N.M] NombreSubreq
          @prompt[N.M.K] TituloPrompt
            ...igual que arriba...
    """
    proyecto   = prompts_data["proyecto"]
    tecnologia = prompts_data["tecnologia"]
    es_hibrido = prompts_data.get("es_hibrido", False)
    r          = prompts_data.get("_resumen", {})
    generado   = prompts_data.get("generado", "")

    lineas: list[str] = []

    def L(texto: str = ""):
        lineas.append(texto)

    # ── ENCABEZADO DEL DOCUMENTO ──────────────────────────────────────────
    L("@document")
    L(f"proyecto: {proyecto}")
    L(f"tecnologia: {tecnologia}")
    L(f"es_hibrido: {str(es_hibrido).lower()}")
    L(f"generado: {generado}")
    L(f"total_requerimientos: {r.get('total_requerimientos', 0)}")
    L(f"con_prompts: {r.get('con_prompts', 0)}")
    L(f"sin_prompts: {r.get('sin_prompts', 0)}")
    L(f"total_prompts: {r.get('total_prompts', 0)}")
    L()

    if es_hibrido:
        nota_h = prompts_data.get("nota_hibrido", {})
        if nota_h:
            L("@nota_hibrido")
            L(f"  explicacion: {nota_h.get('explicacion', '')}")
            for paso in nota_h.get("pasos_implementacion", []):
                L(f"  - {paso}")
            reqs_c = ", ".join(nota_h.get("reqs_cloud", []))
            reqs_d = ", ".join(nota_h.get("reqs_desktop", []))
            if reqs_c: L(f"  reqs_cloud: {reqs_c}")
            if reqs_d: L(f"  reqs_desktop: {reqs_d}")
            L()

    # ── SEPARADOR VISUAL ──────────────────────────────────────────────────
    L("# " + "═" * 70)
    L(f"# PROMPTS DE AUTOMATIZACIÓN — {proyecto} — {tecnologia}")
    L(f"# Uso: copiar el texto entre ---prompt--- y ---fin--- en Copilot de Power Automate")
    L("# " + "═" * 70)
    L()

    # ── REQUERIMIENTOS ────────────────────────────────────────────────────
    for idx_req, entry in enumerate(prompts_data["prompts_generados"], 1):
        req_id    = entry["id_flujo"]
        req_nom   = entry["nombre_flujo"]
        plat      = entry["plataforma"]
        puede     = entry["generar_prompt"]
        gaps      = entry["gaps_detectados"]
        seq       = entry["prompts_secuenciales"]
        sub_prs   = entry.get("sub_prompts", [])
        resumen   = entry.get("resumen_cobertura", "")
        manuales  = entry.get("pasos_manuales_requeridos", [])

        # Nombre del subflow desde el primer prompt si existe
        sf = ""
        if seq and seq[0].get("instruccion_previa"):
            ip = seq[0]["instruccion_previa"]
            m  = re.search(r"subflow\s+'([^']+)'", ip)
            if m: sf = m.group(1)

        L("# " + "─" * 70)
        L(f"@req[{idx_req:02d}] {req_nom}")
        L(f"  id: {req_id}")
        L(f"  plataforma: {plat}")
        if sf:
            L(f"  subflow: {sf}")
        L(f"  total_prompts: {len(seq)}")
        if resumen:
            L(f"  cobertura: {resumen}")

        # Gaps críticos → bloque sin prompts
        if gaps["criticos"]:
            L(f"  estado: SIN_PROMPTS")
            L(f"  motivo: >")
            for c in gaps["criticos"]:
                L(f"    {c}")

        # Advertencias
        if gaps["advertencias"]:
            L(f"  advertencias: >")
            for a in gaps["advertencias"]:
                L(f"    {a}")

        # Pasos manuales
        if manuales and not puede:
            L(f"  pasos_manuales: >")
            for m_paso in manuales:
                L(f"    - {m_paso}")

        L()

        if not puede:
            L(f"  # Sin prompts generados — ver motivo arriba")
            L()
        else:
            # Prompts del requerimiento principal
            _escribir_prompts(seq, idx_req, None, lineas)

        # Sub-requerimientos
        for idx_sub, sub in enumerate(sub_prs, 1):
            sub_id   = sub.get("id_subflujo", "")
            sub_nom  = sub.get("nombre_subflujo", "")
            sub_seq  = sub.get("prompts_secuenciales", [])
            sub_gaps = sub.get("gaps_detectados", {})
            sub_puede = sub.get("generar_prompt", False)

            L(f"  @subreq[{idx_req:02d}.{idx_sub}] {sub_nom}")
            L(f"    id: {sub_id}")
            L(f"    total_prompts: {len(sub_seq)}")
            if sub_gaps.get("criticos"):
                L(f"    estado: SIN_PROMPTS")
                L(f"    motivo: >")
                for c in sub_gaps["criticos"]:
                    L(f"      {c}")
            L()

            if sub_puede and sub_seq:
                _escribir_prompts(sub_seq, idx_req, idx_sub, lineas)

    return "\n".join(lineas)


def _escribir_prompts(seq: list[dict], idx_req: int, idx_sub, lineas: list[str]):
    """Escribe los bloques @prompt[N.M] para una secuencia de prompts."""

    def L(texto: str = ""):
        lineas.append(texto)

    indent = "    " if idx_sub else "  "

    for sp in seq:
        num     = sp["numero_prompt"]
        titulo  = sp["titulo"]
        prompt  = sp["prompt"]
        chars   = sp["caracteres"]
        ip      = sp.get("instruccion_previa") or ""
        nota    = sp.get("nota_desarrollador") or ""
        acciones = sp.get("acciones_cubiertas", [])
        variables = sp.get("variables_referenciadas", [])

        # Etiqueta del prompt: req.sub.num o req.num
        if idx_sub:
            etiqueta = f"{idx_req:02d}.{idx_sub}.{num}"
        else:
            etiqueta = f"{idx_req:02d}.{num}"

        L(f"{indent}@prompt[{etiqueta}] {titulo}")
        L(f"{indent}  caracteres: {chars}")

        if acciones:
            acc_str = " | ".join(str(a)[:60] for a in acciones[:3])
            L(f"{indent}  acciones_cubiertas: {acc_str}")

        if variables:
            L(f"{indent}  variables: {' '.join(str(v) for v in variables[:6])}")

        # Instrucción previa (si existe) — bloque visual propio
        if ip:
            L()
            L(f"{indent}  ---instruccion---")
            # Partir la instruccion en líneas de max 80 chars para legibilidad
            for linea_ip in _wrap(ip, 78):
                L(f"{indent}  {linea_ip}")
            L(f"{indent}  ---fin_instruccion---")

        # El prompt — bloque de copia directa
        L()
        L(f"{indent}  ---prompt---")
        # Partir el prompt en líneas de max 80 chars para legibilidad en el .toon
        # pero el usuario copia todo el bloque como texto continuo
        for linea_p in _wrap(prompt, 78):
            L(f"{indent}  {linea_p}")
        L(f"{indent}  ---fin_prompt---")

        # Nota al desarrollador
        if nota:
            L()
            L(f"{indent}  ---nota_desarrollador---")
            for linea_n in _wrap(nota, 78):
                L(f"{indent}  {linea_n}")
            L(f"{indent}  ---fin_nota---")

        L()


def _wrap(text: str, width: int) -> list[str]:
    """
    Parte el texto en líneas de max width chars respetando espacios.
    Si el texto contiene saltos de línea explícitos los respeta.
    """
    import textwrap
    result = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            result.append("")
            continue
        wrapped = textwrap.wrap(paragraph, width=width, break_long_words=True, break_on_hyphens=False)
        result.extend(wrapped if wrapped else [""])
    return result


# ══════════════════════════════════════════════════════════════════════════════
# 4. MAIN
# ══════════════════════════════════════════════════════════════════════════════

def find_toon(arg: str | None) -> Path:
    if arg:
        # Buscar por nombre exacto, codigo o parcial
        code = re.search(r'[A-Z]{2,5}[\._-]?\d{3}', arg.upper())
        if code:
            norm = code.group(0).replace('.','').replace('-','').replace('_','')
            for f in INPUTS.glob("*.toon"):
                fn = f.name.upper().replace('.','').replace('-','').replace('_','')
                if norm in fn:
                    return f
        p = Path(arg)
        if p.exists(): return p
        p = INPUTS / arg
        if p.exists(): return p
    files = list(INPUTS.glob("*.toon"))
    if not files:
        print(f"ERROR: No hay archivos .toon en {INPUTS}")
        sys.exit(1)
    return files[0]


def main():
    toon_path = find_toon(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"\n Procesando: {toon_path.name}")

    parser  = ToonParser(toon_path)
    analisis = parser.parse()
    analisis = clasificar_tecnologia(analisis)
    proyecto = analisis["proyecto"]
    sid      = safe_id(proyecto)

    # Guardar analisis (sin _tech_key interna)
    analisis_out = {k: v for k, v in analisis.items() if k != "_tech_key"}
    ap = OUTDIR / f"{sid}_analisis.json"
    ap.write_text(json.dumps(analisis_out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f" Analisis: {ap.name}")

    # Guardar prompts como .toon (copia-pega directo) y como JSON (machine-readable)
    prompts = build_prompts_json(analisis)

    # .toon — para el usuario: copia y pega directamente en Copilot
    toon_text = build_prompts_toon(prompts, analisis)
    tp = OUTDIR / f"{sid}_prompts.toon"
    tp.write_text(toon_text, encoding="utf-8")
    print(f" Prompts:  {tp.name}  (copia-pega directo en Copilot)")

    # .json — para el agente y procesamiento posterior
    pp = OUTDIR / f"{sid}_prompts.json"
    pp.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f" Prompts:  {pp.name}  (machine-readable)")

    r = prompts["_resumen"]
    print(f"\n RESUMEN — {proyecto}")
    print(f"  Tecnologia:   {analisis['tecnologia']}")
    print(f"  Reqs:         {r['total_requerimientos']}  |  Con prompts: {r['con_prompts']}  |  Sin prompts (gaps): {r['sin_prompts']}")
    print(f"  Total prompts:{r['total_prompts']}")
    print(f"  Outputs en:   {OUTDIR}/\n")


if __name__ == "__main__":
    main()
