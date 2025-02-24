import os
from config import settings

metrics_file_path: str = os.path.join(settings.LOGS_DIR, settings.METRICS_FILE_NAME)