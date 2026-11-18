"""Caso de uso: renomear em lote as guias de um diretório."""

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from darf_utils.models.errors import DarfNaoReconhecidaError, PdfReadError
from darf_utils.models.parser import DarfParser

_MOTIVO_NAO_RECONHECIDA = "não foi possível identificar CNPJ, razão social e período"


class TextExtractor(Protocol):
    def read_text(self, caminho: Path) -> str: ...


@dataclass(frozen=True)
class ArquivoIgnorado:
    nome: str
    motivo: str


@dataclass
class RenameReport:
    renomeados: list[str] = field(default_factory=list)
    ignorados: list[ArquivoIgnorado] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.renomeados) + len(self.ignorados)


class DarfRenamer:
    """Lê cada PDF do diretório de entrada e copia para a saída já renomeado."""

    def __init__(self, reader: TextExtractor, parser: DarfParser | None = None):
        self._reader = reader
        self._parser = parser or DarfParser()

    def rename_all(self, entrada: Path, saida: Path) -> RenameReport:
        saida.mkdir(parents=True, exist_ok=True)

        report = RenameReport()
        for pdf in _listar_pdfs(entrada):
            try:
                report.renomeados.append(self._renomear(pdf, saida))
            except (DarfNaoReconhecidaError, PdfReadError, OSError) as erro:
                report.ignorados.append(ArquivoIgnorado(pdf.name, str(erro)))
        return report

    def _renomear(self, pdf: Path, saida: Path) -> str:
        darf = self._parser.parse(self._reader.read_text(pdf))
        if darf is None:
            raise DarfNaoReconhecidaError(_MOTIVO_NAO_RECONHECIDA)

        destino = _caminho_disponivel(saida / darf.nome_arquivo)
        shutil.copy2(pdf, destino)
        return destino.name


def _listar_pdfs(diretorio: Path) -> list[Path]:
    return sorted(
        arquivo
        for arquivo in diretorio.iterdir()
        if arquivo.is_file() and arquivo.suffix.lower() == ".pdf"
    )


def _caminho_disponivel(destino: Path) -> Path:
    """Acrescenta um sufixo numérico quando o nome já existe no destino."""
    candidato, sequencia = destino, 1
    while candidato.exists():
        candidato = destino.with_name(f"{destino.stem} ({sequencia}){destino.suffix}")
        sequencia += 1
    return candidato
