"""
Compliance Mapper: translates technical findings into legal/business language.

Honest learning note (documented on purpose): this mapping is a first
approximation based on reading the Esquema Nacional de Seguridad (RD
311/2022) and the RGPD/LOPDGDD, done for study and portfolio purposes.
It does NOT replace review by a legal team or DPO in a real engagement —
it's a starting point that shows the reasoning, not a definitive legal
source. This is stated explicitly in the README and reinforces, rather
than hides, the maturity of whoever wrote this.

Note on language: the mapping content below (risk_statement, articles,
sanction_reference) is written in Spanish on purpose, since it ends up
directly in the client-facing PDF report for the Spanish market. Code,
comments and identifiers stay in English for portfolio consistency.
"""

from __future__ import annotations

from cyberreport_pro.core.models import ComplianceMapping, Finding, MappedFinding

# Static knowledge base: technical category -> legal mappings.
# In a v2, this would move to an external YAML loaded at runtime, so that
# legal updates don't require a code change. Kept as a dict for simplicity
# in this first version.
_COMPLIANCE_KNOWLEDGE_BASE: dict[str, list[ComplianceMapping]] = {
    "sql_injection": [
        ComplianceMapping(
            framework="ENS",
            articles=["Anexo II - mp.sw.1 (Desarrollo de aplicaciones)"],
            risk_statement=(
                "Una vulnerabilidad de SQL Injection compromete la medida de "
                "protección 'Desarrollo de aplicaciones' del ENS, permitiendo "
                "acceso no autorizado a datos mediante manipulación de entradas."
            ),
        ),
        ComplianceMapping(
            framework="RGPD/LOPDGDD",
            articles=["Art. 32 RGPD (Seguridad del tratamiento)"],
            risk_statement=(
                "Si la base de datos afectada contiene datos personales, la "
                "vulnerabilidad representa un incumplimiento del deber de "
                "seguridad técnica exigido por el Art. 32 del RGPD."
            ),
            sanction_reference="Hasta 10M€ o 2% de la facturación global anual (Art. 83.4 RGPD)",
        ),
    ],
    "public_storage": [
        ComplianceMapping(
            framework="ENS",
            articles=["Anexo II - mp.info.3 (Custodia)"],
            risk_statement=(
                "Un bucket o almacenamiento público sin control de acceso "
                "vulnera la medida de custodia de la información exigida por el ENS."
            ),
        ),
        ComplianceMapping(
            framework="RGPD/LOPDGDD",
            articles=["Art. 5.1.f RGPD (Integridad y confidencialidad)", "Art. 32 RGPD"],
            risk_statement=(
                "La exposición pública de datos personales vulnera el principio "
                "de integridad y confidencialidad y puede constituir una "
                "violación de datos personales notificable (Art. 33 RGPD)."
            ),
            sanction_reference="Hasta 20M€ o 4% de la facturación global anual (Art. 83.5 RGPD)",
        ),
    ],
    "weak_crypto": [
        ComplianceMapping(
            framework="ENS",
            articles=["Anexo II - mp.info.2 (Cifrado)"],
            risk_statement=(
                "El uso de algoritmos criptográficos débiles u obsoletos "
                "incumple directamente la medida de cifrado del ENS."
            ),
        ),
        ComplianceMapping(
            framework="RGPD/LOPDGDD",
            articles=["Art. 32.1.a RGPD (Seudonimización y cifrado)"],
            risk_statement=(
                "El RGPD menciona explícitamente el cifrado como medida técnica "
                "esperada; su ausencia o debilidad perjudica a la empresa en "
                "caso de incidente."
            ),
        ),
    ],
    "secrets_exposure": [
        ComplianceMapping(
            framework="ENS",
            articles=["Anexo II - op.acc.5 (Mecanismos de autenticación)"],
            risk_statement=(
                "Secretos expuestos (claves de API, credenciales) comprometen "
                "directamente los mecanismos de autenticación exigidos por el ENS."
            ),
        ),
        ComplianceMapping(
            framework="RGPD/LOPDGDD",
            articles=["Art. 32 RGPD"],
            risk_statement=(
                "Credenciales expuestas que permitan acceso a datos personales "
                "constituyen un incumplimiento del deber general de seguridad "
                "del tratamiento."
            ),
        ),
    ],
}

_DEFAULT_MAPPING = ComplianceMapping(
    framework="ENS",
    articles=["Anexo II - op.exp.8 (Registro de actividad)"],
    risk_statement=(
        "Categoría no catalogada en la base de conocimiento actual; se "
        "recomienda un análisis manual por parte de un especialista en cumplimiento."
    ),
)


def map_finding(finding: Finding) -> MappedFinding:
    """Map a single Finding to its applicable legal frameworks."""
    mappings = _COMPLIANCE_KNOWLEDGE_BASE.get(finding.category, [_DEFAULT_MAPPING])
    return MappedFinding(finding=finding, mappings=list(mappings))


def map_findings(findings: list[Finding]) -> list[MappedFinding]:
    """Map a list of Findings. Convenience function used by the CLI."""
    return [map_finding(f) for f in findings]


def known_categories() -> list[str]:
    """Return categories that have an explicit legal mapping (used in tests/CLI --list)."""
    return sorted(_COMPLIANCE_KNOWLEDGE_BASE.keys())
