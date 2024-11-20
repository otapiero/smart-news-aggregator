import os
from typing import Final


DB_ACCESSOR_APP_ID: Final = os.getenv("DB_ACCESSOR_APP_ID", "users_db_accessor")
DB_ACCESSOR_PORT: Final = int(os.getenv("DB_ACCESSOR_PORT", "50052"))
LOG_LEVEL: Final = os.getenv("LOG_LEVEL", "INFO")
DAPR_GRPC_PORT: Final = int(os.getenv("DAPR_GRPC_PORT", "50000"))
DAPR_HTTP_PORT: Final = int(os.getenv("DAPR_HTTP_PORT", "3500"))
APP_PORT: Final = int(os.getenv("APP_PORT", "50050"))
