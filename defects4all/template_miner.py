from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig


def get_template_miner(config_file, persistent_file):
    config = TemplateMinerConfig()
    config.load(config_file)
    config.profiling_enabled = False

    from drain3.file_persistence import FilePersistence

    persistence = FilePersistence(str(persistent_file))

    template_miner = TemplateMiner(persistence, config=config)
    return template_miner
