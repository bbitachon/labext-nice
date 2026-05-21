#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
File    :   labext.py
Desc    :   LabExT NiceGUI — application entry point.
            Run with:  python labext.py
            Or natively (desktop window):  python labext.py --native
"""

import logging
import click
from logging.handlers import RotatingFileHandler

from nicegui import ui, app
from labext_nice.gui_elements.main_window.MainWindowView import MainWindowView
from labext_nice.Utilities.Utilities import setup_user_settings_directory


def setup_logging(log_level: str):
    level = getattr(logging, log_level.upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(level)

    fmt = logging.Formatter("%(asctime)s [%(levelname)-8s] %(name)s — %(message)s")

    # Rotating file handler
    fh = RotatingFileHandler("labext.log", maxBytes=5 * 1024 * 1024, backupCount=3)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    root.addHandler(ch)


@click.command()
@click.option(
    "--native", is_flag=True, default=False, help="Run as native desktop window"
)
@click.option(
    "--port", default=8080, help="Port for the web server (ignored in native mode)"
)
@click.option(
    "--log-level", default="INFO", help="Logging level (DEBUG/INFO/WARNING/ERROR)"
)
def main(native: bool, port: int, log_level: str):
    setup_logging(log_level)
    setup_user_settings_directory(makedir_if_needed=True)

    logger = logging.getLogger(__name__)
    logger.info("Starting LabExT…")

    # Build model and view
    # director = ExperimentDirector()
    # model = MainWindowModel(experiment_director=director)
    view = MainWindowView()  # registers the '/' page

    logger.info("LabExT GUI ready.")

    if native:
        ui.run(
            title="LabExT",
            native=True,
            window_size=(1400, 900),
            reload=False,
        )
    else:
        ui.run(
            title="LabExT",
            port=port,
            reload=False,
            show=True,
        )


if __name__ in {"__main__", "__mp_main__"}:
    main()
