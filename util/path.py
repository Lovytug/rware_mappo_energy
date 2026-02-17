from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Папка с json-конфигами
CONFIGURATION_DIR = PROJECT_ROOT / "configuration"

# Конкретный набор конфигов
CONFIG_EPISODE_RUN = (
    PROJECT_ROOT / "run"
)
