"""Entidade de domínio: os dados que identificam uma guia DARF/DAS."""

import re
from dataclasses import dataclass

_CARACTERES_INVALIDOS = re.compile(r'[<>:"/\\|?*]')
_ESPACOS = re.compile(r"\s+")


@dataclass(frozen=True)
class Darf:
    cnpj: str
    razao_social: str
    periodo_apuracao: str

    @property
    def nome_arquivo(self) -> str:
        """Nome do PDF no padrão `CNPJ - Razão Social - Período.pdf`."""
        partes = (self.cnpj, self.razao_social, self.periodo_apuracao)
        return f"{' - '.join(_sanitizar(parte) for parte in partes)}.pdf"


def _sanitizar(valor: str) -> str:
    """Remove quebras de linha e caracteres proibidos em nomes de arquivo."""
    return _ESPACOS.sub(" ", _CARACTERES_INVALIDOS.sub("", valor)).strip()
