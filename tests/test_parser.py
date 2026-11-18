from darf_utils.models.parser import DarfParser

TEXTO_GUIA = """
Documento de Arrecadação do Simples Nacional
CNPJ Matriz
12.345.678/0001-99
ACME Comércio de Peças LTDA
Período de Apuração
Razão Social
Janeiro/2024
"""


def test_extrai_cnpj_razao_social_e_periodo():
    darf = DarfParser().parse(TEXTO_GUIA)

    assert darf is not None
    assert darf.cnpj == "12345678000199"
    assert darf.razao_social == "ACME Comércio de Peças LTDA"
    assert darf.periodo_apuracao == "Janeiro-2024"


def test_retorna_none_sem_cnpj():
    assert DarfParser().parse("documento qualquer") is None


def test_retorna_none_sem_periodo():
    texto = "12.345.678/0001-99\nACME LTDA\nPeríodo de Apuração\n"

    assert DarfParser().parse(texto) is None
