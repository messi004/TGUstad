import importlib
import pkgutil
import logging

logger = logging.getLogger(__name__)


def load_features(app):
    """
    Automatically loads all feature modules that expose setup(app).
    """
    package_name = "features"
    package = importlib.import_module(package_name)

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue

        try:
            module = importlib.import_module(f"{package_name}.{module_name}")

            if hasattr(module, "setup"):
                module.setup(app)
                logger.info("Loaded feature: %s", module_name)
            else:
                logger.warning(
                    "Feature %s has no setup(app) function",
                    module_name
                )

        except Exception as e:
            logger.exception(
                "Failed to load feature %s: %s",
                module_name,
                e
            )