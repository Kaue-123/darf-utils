"""Erros do domínio."""


class PdfReadError(Exception):
    """PDF ausente, corrompido ou protegido."""


class DarfNaoReconhecidaError(Exception):
    """O texto do PDF não contém os dados esperados de uma guia."""
