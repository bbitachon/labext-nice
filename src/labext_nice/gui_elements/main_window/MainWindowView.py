#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
File    :   MainWindowView.py
"""

import logging
from typing import Optional

from nicegui import app, ui

from labext_nice.gui_elements.cards.toolbar_card import MeasurementControlCard


class MainWindowView:
    """
    Constructs and manages the NiceGUI main window.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        # self._model = model

        # UI element references (set during build)
        self._queue_table: Optional[ui.table] = None
        self._log_area: Optional[ui.log] = None
        self._progress: Optional[ui.linear_progress] = None
        self._measure_btn: Optional[ui.button] = None
        self._abort_btn: Optional[ui.button] = None
        self._clear_btn: Optional[ui.button] = None
        self._up_btn: Optional[ui.button] = None
        self._down_btn: Optional[ui.button] = None
        self._save_path_input: Optional[ui.input] = None
        self._save_toggle: Optional[ui.checkbox] = None

        self._build()

    # =========================================================================
    # UI construction
    # =========================================================================

    def _build(self):
        """Register the '/' page and build all widgets inside it."""

        @ui.page("/")
        def index():
            with ui.column().classes("w-full"):
                MeasurementControlCard()  # self._build_toolbar()
            # with ui.row().classes("w-full gap-4 mt-2"):
            #     self._build_queue_panel()
            #     self._build_plot_panel()
            # self._build_log_panel()

    # ── Toolbar ───────────────────────────────────────────────────────────────

    def _build_toolbar(self):
        with ui.card():
            with ui.row().classes("items-center gap-3 flex-wrap"):

                # Title
                ui.label("SPLAT").classes("text-xl font-bold text-cyan-400 mr-4")

                # Action buttons
                ui.button(
                    "＋ New Experiment",
                ).classes("bg-cyan-700 text-white")
                ui.button(
                    "📂 Load Queue",
                ).classes("bg-gray-700 text-white")
                ui.button(
                    "🔁 Repeat Last",
                ).classes("bg-gray-700 text-white")

                ui.separator().classes("h-8 border-gray-600")

                # Start / Abort
                self._measure_btn = ui.button(
                    "▶ Measure",
                ).classes("bg-green-700 text-white")
                self._abort_btn = ui.button(
                    "■ Abort",
                ).classes("bg-red-700 text-white")
                self._abort_btn.disable()

                ui.separator().classes("h-8 border-gray-600")

                ui.button(
                    "📁",
                ).classes(
                    "bg-gray-700 text-gray-300"
                ).props("flat dense")

    # ── Queue panel ───────────────────────────────────────────────────────────

    def _build_queue_panel(self):
        with ui.card():
            with ui.row().classes("items-center justify-between p-2"):
                ui.label("Measurement Queue").classes("font-semibold text-gray-300")
                with ui.row().classes("gap-1"):
                    self._up_btn = (
                        ui.button(
                            "▲",
                        )
                        .props("flat dense")
                        .classes("text-gray-400")
                    )
                    self._down_btn = (
                        ui.button("▼").props("flat dense").classes("text-gray-400")
                    )
                    self._clear_btn = (
                        ui.button("🗑 Clear").props("flat dense").classes("text-red-400")
                    )

            columns = [
                {
                    "name": "type",
                    "label": "Device Type",
                    "field": "type",
                    "align": "left",
                },
                {"name": "id", "label": "Device ID", "field": "id", "align": "left"},
                {
                    "name": "measurement",
                    "label": "Measurement",
                    "field": "measurement",
                    "align": "left",
                },
                {
                    "name": "progress",
                    "label": "Progress",
                    "field": "progress",
                    "align": "left",
                },
            ]
            self._queue_table = (
                ui.table(columns=columns, rows=[], row_key="hash")
                .classes("w-full text-sm")
                .props("dense flat")
            )

            # Progress bar for the first (running) row
            self._progress = ui.linear_progress(value=0, show_value=False).classes(
                "mt-1 hidden"
            )

        # self._update_queue_buttons()

    # ── Plot panel ────────────────────────────────────────────────────────────

    def _build_plot_panel(self):
        with ui.card():
            with ui.tabs().classes("text-cyan-400") as tabs:
                tab_1d = ui.tab("1D")
                tab_2d = ui.tab("2D")

            with ui.tab_panels(tabs, value=tab_1d).classes("w-full"):
                with ui.tab_panel(tab_1d):
                    self._plot_1d = ui.plotly(
                        {
                            "data": [],
                            "layout": {
                                # "title": self._model.plot_title_1d,
                                "title": "test",
                                # "xaxis": {"title": self._model.axis_label_1d[0]},
                                "xaxis": {"title": "test"},
                                # "yaxis": {"title": self._model.axis_label_1d[1]},
                                "yaxis": {"title": "test"},
                                "paper_bgcolor": "#0f1117",
                                "plot_bgcolor": "#1a1f2e",
                                "font": {"color": "#e2e8f0"},
                            },
                        }
                    ).classes("w-full h-64")

                with ui.tab_panel(tab_2d):
                    self._plot_2d = ui.plotly(
                        {
                            "data": [],
                            "layout": {
                                "title": "test",
                                "xaxis": {"title": "test"},
                                "yaxis": {"title": "test"},
                                "paper_bgcolor": "#0f1117",
                                "plot_bgcolor": "#1a1f2e",
                                "font": {"color": "#e2e8f0"},
                            },
                        }
                    ).classes("w-full h-64")

    # ── Log panel ─────────────────────────────────────────────────────────────

    def _build_log_panel(self):
        with ui.card():
            ui.label("Log").classes("text-xs text-gray-500 px-2 pt-1")
            self._log_area = ui.log(max_lines=200).classes(
                "w-full h-36 text-xs text-green-400 font-mono bg-gray-950"
            )

        # Route Python logging → NiceGUI log widget
        class NiceGuiLogHandler(logging.Handler):
            def __init__(self_inner, log_widget: ui.log):
                super().__init__()
                self_inner._widget = log_widget

            def emit(self_inner, record):
                self_inner._widget.push(self_inner.format(record))

        handler = NiceGuiLogHandler(self._log_area)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logging.getLogger().addHandler(handler)
