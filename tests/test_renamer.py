from pathlib import Path

import pytest

from darf_utils.models.errors import PdfReadError
from darf_utils.models.renamer import DarfRenamer

from tests.test_parser import TEXTO_GUIA


class FakeReader:
    def __init__(self, textos: dict[str, str]):
        self._textos = textos

    def read_text(self, caminho: Path) -> str:
        texto = self._textos.get(caminho.name)
        if texto is None:
            raise PdfReadError("arquivo corrompido")
        return texto


@pytest.fixture
def diretorios(tmp_path: Path) -> tuple[Path, Path]:
    entrada, saida = tmp_path / "entrada", tmp_path / "saida"
    entrada.mkdir()
    return entrada, saida


def _criar_pdfs(entrada: Path, *nomes: str) -> None:
    for nome in nomes:
        (entrada / nome).write_bytes(b"%PDF-1.4")


def test_renomeia_pdf_reconhecido(diretorios):
    entrada, saida = diretorios
    _criar_pdfs(entrada, "guia.pdf")

    report = DarfRenamer(FakeReader({"guia.pdf": TEXTO_GUIA})).rename_all(entrada, saida)

    assert report.renomeados == ["12345678000199 - ACME Comércio de Peças LTDA - Janeiro-2024.pdf"]
    assert report.ignorados == []


def test_nao_sobrescreve_guias_de_mesmo_nome(diretorios):
    entrada, saida = diretorios
    _criar_pdfs(entrada, "a.pdf", "b.pdf")
    reader = FakeReader({"a.pdf": TEXTO_GUIA, "b.pdf": TEXTO_GUIA})

    report = DarfRenamer(reader).rename_all(entrada, saida)

    assert len(report.renomeados) == 2
    assert len(list(saida.iterdir())) == 2


def test_ignora_arquivo_ilegivel_e_segue_o_lote(diretorios):
    entrada, saida = diretorios
    _criar_pdfs(entrada, "ok.pdf", "ruim.pdf")

    report = DarfRenamer(FakeReader({"ok.pdf": TEXTO_GUIA})).rename_all(entrada, saida)

    assert len(report.renomeados) == 1
    assert [item.nome for item in report.ignorados] == ["ruim.pdf"]


def test_ignora_arquivos_que_nao_sao_pdf(diretorios):
    entrada, saida = diretorios
    (entrada / "nota.txt").write_text("x")

    report = DarfRenamer(FakeReader({})).rename_all(entrada, saida)

    assert report.total == 0
