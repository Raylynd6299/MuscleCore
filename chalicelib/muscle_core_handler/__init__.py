from .API import MuscleCoreAPIHandler

class MuscleCoreHandler:
    def __init__(self):
        self.api = MuscleCoreAPIHandler(self)

muscle_core_handler = MuscleCoreHandler()