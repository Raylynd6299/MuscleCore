from .Authentication import MuscleCoreAPIAuthenticationHandler

class MuscleCoreAPIHandler:
    def __init__(self, muscle_core_handler):
        self.muscle_core_handler = muscle_core_handler

        self.authentication = MuscleCoreAPIAuthenticationHandler(self)