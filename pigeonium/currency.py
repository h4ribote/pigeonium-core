from .utils import Utils
from .config import Config
from .struct import Currency as CurrencyStruct

class Currency(CurrencyStruct):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return super().__str__()
    
    def __repr__(self):
        return super().__repr__()

    @classmethod
    def create(cls,name:str,symbol:str,issuer:bytes,supply:int=0):
        cu = cls()
        cu.currencyId = Utils.md5(Utils.sha256(name.encode()+symbol.encode()+issuer))
        cu.name = name
        cu.symbol = symbol
        cu.issuer = issuer
        cu.supply = supply
        return cu
    
    def verify(self):
        if self.currencyId == bytes(16):
            return (self.name == Config.BaseCurrency.name) and (self.symbol == Config.BaseCurrency.symbol) and (self.issuer == Config.BaseCurrency.issuer)
        return Utils.md5(Utils.sha256(self.name.encode()+self.symbol.encode()+self.issuer)) == self.currencyId
