from .traceability_creator import Traceability
from config import settings

traceability = Traceability.create_traceability(settings.TRACE_ENGINE)
