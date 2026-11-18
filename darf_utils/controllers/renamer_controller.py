"""Controlador: valida a entrada da view, aciona o modelo e devolve o resultado."""

from pathlib import Path

from darf_utils.models.renamer import DarfRenamer, RenameReport
from darf_utils.views.main_window import MainWindow

_LIMITE_DETALHES = 10


class RenamerController:
    def __init__(self, view: MainWindow, renamer: DarfRenamer):
        self._view = view
        self._renamer = renamer
        self._view.on_process = self.process

    def process(self) -> None:
        entrada, saida = Path(self._view.diretorio_entrada), Path(self._view.diretorio_saida)

        erro = _validar(entrada, saida)
        if erro:
            self._view.show_error("Erro", erro)
            return

        try:
            report = self._renamer.rename_all(entrada, saida)
        except OSError as falha:
            self._view.show_error("Erro", f"Não foi possível concluir o processo: {falha}")
            return

        self._view.show_info("Processo concluído", _resumir(report))


def _validar(entrada: Path, saida: Path) -> str | None:
    if not entrada.name or not saida.name:
        return "Selecione os diretórios de entrada e de saída."
    if not entrada.is_dir():
        return f"Diretório de entrada não encontrado: {entrada}"
    return None


def _resumir(report: RenameReport) -> str:
    if report.total == 0:
        return "Nenhum PDF encontrado no diretório de entrada."

    linhas = [f"{len(report.renomeados)} arquivo(s) renomeado(s)."]
    if report.ignorados:
        linhas.append(f"\n{len(report.ignorados)} arquivo(s) ignorado(s):")
        linhas += [f"• {item.nome}: {item.motivo}" for item in report.ignorados[:_LIMITE_DETALHES]]
        restantes = len(report.ignorados) - _LIMITE_DETALHES
        if restantes > 0:
            linhas.append(f"… e mais {restantes}.")
    return "\n".join(linhas)
