import logging
from logging.handlers import RotatingFileHandler

# Configurar o logger
logger = logging.getLogger("fastapi")
logger.setLevel(logging.ERROR) 

# Criar um manipulador de arquivos (log rotativo para evitar arquivos gigantes)
file_handler = RotatingFileHandler("errors.log", maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
file_handler.setLevel(logging.ERROR)

# Definir formato do log
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Adicionar o manipulador ao logger
logger.addHandler(file_handler)
