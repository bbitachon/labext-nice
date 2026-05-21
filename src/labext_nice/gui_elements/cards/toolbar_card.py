from labext_nice.gui_elements.cards.base_card import BaseCard
from nicegui import ui


class MeasurementControlCard(BaseCard):

    def build(self):
        with ui.card():
            with ui.grid(columns=3):
                with ui.row().classes("col-span-3 items-center gap-2"):
                    self._save_path_input = ui.input("Save Path").classes("flex-grow")
                    ui.button("…")
                    self._save_checkbox = ui.checkbox("Save Measurement")
                ui.label("Quick Access").classes("col-span-3 font-bold")
                ui.button("＋ New Single Measurement")
                ui.button("📂 Load Measurements")
                ui.button("🔁 Repeat Last")

                # Start / Abort
                ui.label("Measurement Control").classes("col-span-3 font-bold")
                with ui.row().classes("col-span-3 justify-center gap-4"):
                    self._measure_btn = ui.button("▶ Measure").classes("w-50")
                    self._abort_btn = ui.button("■ Abort").classes("w-50")
                    self._abort_btn.disable()
