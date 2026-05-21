#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
File    :   test_gui_smoke.py
Desc    :   Smoke test — verifies the SPLAT GUI starts and renders
            the main page without raising any exceptions.

Run with:
    uv run pytest tests/test_gui_smoke.py -v
"""

from nicegui.testing import User


async def test_page_loads(user: User):
    await user.open("/")
