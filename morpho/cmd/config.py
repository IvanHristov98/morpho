from morpho.reconstruction import Config as RecConfig


class Config:
    rec_cfg: RecConfig
    
    def __init__(self) -> None:
        self.rec_cfg = RecConfig()
