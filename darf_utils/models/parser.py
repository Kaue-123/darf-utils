"""Extração dos dados da guia a partir do texto do PDF."""

import re

from darf_utils.models.darf import Darf

_CNPJ = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")
_PERIODO = re.compile(r"Razão Social\s*\n\s*(\w+/\d{4})")


class DarfParser:
    """Converte o texto de uma guia em uma entidade `Darf`."""

    def parse(self, texto: str) -> Darf | None:
        cnpj = _CNPJ.search(texto)
        if cnpj is None:
            return None

        razao_social = self._buscar_razao_social(texto, cnpj.group())
        periodo = _PERIODO.search(texto)
        if razao_social is None or periodo is None:
            return None

        return Darf(
            cnpj=self._somente_digitos(cnpj.group()),
            razao_social=razao_social,
            periodo_apuracao=periodo.group(1).replace("/", "-"),
        )

    @staticmethod
    def _buscar_razao_social(texto: str, cnpj_formatado: str) -> str | None:
        padrao = re.compile(
            re.escape(cnpj_formatado) + r"\s*(.*?)\s*Período de Apuração",
            re.DOTALL,
        )
        encontrado = padrao.search(texto)
        return encontrado.group(1).strip() if encontrado else None

    @staticmethod
    def _somente_digitos(cnpj_formatado: str) -> str:
        return re.sub(r"\D", "", cnpj_formatado)
