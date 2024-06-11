from logging import Handler
from tqdm import tqdm


class TqdmConsoleHandler(Handler):
    def emit(self, record) -> None:
        try:
            msg = self.format(record)
            tqdm.write(msg)
        except Exception:
            self.handleError(record)
