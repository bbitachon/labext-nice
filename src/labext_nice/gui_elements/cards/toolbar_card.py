from labext_nice.gui_elements.cards.base_card import BaseCard
from nicegui import ui


class MeasurementControlCard(BaseCard):

    def build(self):
        with ui.card():
            with ui.row():
                # Action buttons
                ui.button(
                    "＋ New Single Measurement",
                )
                ui.button(
                    "📂 Load Measurements",
                )
                ui.button(
                    "🔁 Repeat Last",
                )
                # Start / Abort
                self._measure_btn = ui.button(
                    "▶ Measure",
                ).classes("bg-green-700 text-white")
                self._abort_btn = ui.button(
                    "■ Abort",
                ).classes("bg-red-700 text-white")
                self._abort_btn.disable()
