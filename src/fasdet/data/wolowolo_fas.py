

from mmpretrain.datasets import BaseDataset
from mmpretrain.registry import DATASETS


@DATASETS.register_module()
class WolowoloFAS(BaseDataset):
    """Wolowolo FAS Dataset"""

    def __init__(self, data_root, ann_file, metainfo, **kwargs):
        pass
    
    def load_data_list(self):
        pass




