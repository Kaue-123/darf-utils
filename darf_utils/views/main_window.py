"""Camada de apresentação: janela Tkinter, sem regra de negócio."""

import tkinter as tk
from collections.abc import Callable
from tkinter import filedialog, messagebox

_TITULO = "Utilitário de Renomeação PDF — DAS Simples Nacional"
_LARGURA_CAMPO = 50


class MainWindow:
    def __init__(self, root: tk.Tk):
        self._root = root
        self._root.title(_TITULO)
        self.on_process: Callable[[], None] = lambda: None

        self._entrada = self._montar_seletor("Diretório de entrada:")
        self._saida = self._montar_seletor("Diretório de saída:")
        tk.Button(root, text="Processar PDF's", command=lambda: self.on_process()).pack(pady=10)

    @property
    def diretorio_entrada(self) -> str:
        return self._entrada.get().strip()

    @property
    def diretorio_saida(self) -> str:
        return self._saida.get().strip()

    def show_info(self, titulo: str, mensagem: str) -> None:
        messagebox.showinfo(titulo, mensagem)

    def show_error(self, titulo: str, mensagem: str) -> None:
        messagebox.showerror(titulo, mensagem)

    def run(self) -> None:
        self._root.mainloop()

    def _montar_seletor(self, rotulo: str) -> tk.Entry:
        tk.Label(self._root, text=rotulo).pack(pady=5)
        campo = tk.Entry(self._root, width=_LARGURA_CAMPO)
        campo.pack(pady=5)
        tk.Button(
            self._root,
            text="Selecionar Pasta",
            command=lambda: self._preencher(campo),
        ).pack(pady=5)
        return campo

    @staticmethod
    def _preencher(campo: tk.Entry) -> None:
        diretorio = filedialog.askdirectory()
        if diretorio:
            campo.delete(0, tk.END)
            campo.insert(0, diretorio)
