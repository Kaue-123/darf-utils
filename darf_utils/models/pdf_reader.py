"""Leitura do texto bruto de arquivos PDF."""

from pathlib import Path

import fitz

from darf_utils.models.errors import PdfReadError


class PdfReader:
    """Adaptador sobre o PyMuPDF, isolando a dependência externa do domínio."""

    def read_text(self, caminho: Path) -> str:
        try:
            with fitz.open(caminho) as documento:
                return "".join(pagina.get_text() for pagina in documento)
        except (RuntimeError, OSError) as erro:
            raise PdfReadError(str(erro)) from erro
