
import logging

logger = logging.getLogger('MeowCore')
logger.setLevel(logging.DEBUG)


class MeowCore:
    def __init__(self, TOKEN: str):
        self.token = TOKEN
        return
