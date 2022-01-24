from morpho.reconstruction.factory import ColorModel, Strategy


class Config:
    model: ColorModel
    strategy: Strategy
    
    def __init__(self) -> None:
        self.model = ColorModel.BOOL
        self.strategy = Strategy.EROSION

    def with_model(self, model: ColorModel):
        self.model = model

    def with_strategy(self, strategy: Strategy):
        self.strategy = strategy
