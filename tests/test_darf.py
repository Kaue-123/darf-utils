from darf_utils.models.darf import Darf


def test_nome_arquivo_segue_o_padrao():
    darf = Darf("12345678000199", "ACME LTDA", "Janeiro-2024")

    assert darf.nome_arquivo == "12345678000199 - ACME LTDA - Janeiro-2024.pdf"


def test_nome_arquivo_remove_caracteres_invalidos_e_quebras_de_linha():
    darf = Darf("12345678000199", "ACME / Filial\n  Norte", "Janeiro-2024")

    assert darf.nome_arquivo == "12345678000199 - ACME Filial Norte - Janeiro-2024.pdf"
