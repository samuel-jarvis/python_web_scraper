import logging
from pathlib import Path

# 1. Create module-specific logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Logger passes all DEBUG+ to handlers

# 2. Handlers
console = logging.StreamHandler()
console.setLevel(logging.INFO)   # Only show INFO+ on console

log_path = Path(__file__).resolve().parents[2] / "output" / "logger.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
file = logging.FileHandler(log_path, mode="a")
file.setLevel(logging.DEBUG)     # Capture everything in file

# 3. Formatter
fmt = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console.setFormatter(fmt)
file.setFormatter(fmt)

# 4. Attach
logger.addHandler(console)
logger.addHandler(file)

# Usage
logger.debug("Loaded config: %s", log_path)
logger.info("Server listening on port %d", 8080)
