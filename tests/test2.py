import logging
import logging.handlers

"""
logging.basicConfig(
    filename='myapp.log', 
    level=logging.DEBUG,
    format="%(asctime)s - %(created)f - %(filename)s - %(funcName)s - %(levelname)s - %(levelno)s - %(lineno)d - %(message)s - %(module)s - %(msecs)d - %(name)s - %(pathname)s - %(process)d - %(processName)s - %(relativeCreated)d - %(thread)d - %(threadName)s - %(taskName)s"
)
"""

amerique_formater = logging.Formatter("%(asctime)s-%(filename)s-%(message)s")

amerique_filehandler = logging.FileHandler("amerique.log")
amerique_filehandler.setFormatter(amerique_formater)

amerique_logger = logging.getLogger("amerique")
amerique_logger.addHandler(amerique_filehandler)
amerique_logger.setLevel(logging.DEBUG)

amerique_logger.debug("message amerique")


europe_formater = logging.Formatter("%(asctime)s::%(filename)s::%(message)s")

europe_filehandler = logging.FileHandler("europe.log")
europe_filehandler.setFormatter(europe_formater)

europe_logger = logging.getLogger("europe")
europe_logger.addHandler(europe_filehandler)
europe_logger.setLevel(logging.DEBUG)

europe_logger.debug("message europe")