# base_card.py
from abc import ABC, abstractmethod
from nicegui import ui


class BaseCard(ABC):
    """Each card owns its UI fragment and knows how to refresh itself."""

    def __init__(self):
        # self._model = model
        # self._connect_signals()  # wire model signals in subclass
        self.build()  # render the card

    @abstractmethod
    def build(self):
        """Construct the NiceGUI elements inside a ui.card."""
        ...

    # @abstractmethod
    # def _connect_signals(self):
    #     """Wire model signals to refresh callbacks."""
    #     ...

    # @ui.refreshable
    # @abstractmethod
    # def _content(self):
    #     """The refreshable inner content of the card."""
    #     ...
