"""Composição da aplicação: liga view, controlador e modelo."""

import tkinter as tk

from darf_utils.controllers.renamer_controller import RenamerController
from darf_utils.models.parser import DarfParser
from darf_utils.models.pdf_reader import PdfReader
from darf_utils.models.renamer import DarfRenamer
from darf_utils.views.main_window import MainWindow


def run() -> None:
    view = MainWindow(tk.Tk())
    RenamerController(view, DarfRenamer(PdfReader(), DarfParser()))
    view.run()
