"""Point d'entrée principal de l'application."""

import logging
import sys

from .api.app import create_app

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = create_app()
    logger.info("Démarrage de l'application")
    app.run(host="0.0.0.0", port=5000, debug=False)

