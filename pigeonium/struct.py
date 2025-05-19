from time import time
from .utils import Utils
from typing import overload

class Transaction:
    def __init__(self) -> None:
        self.indexId:int = None
        self.networkId:int = None
        self.source:bytes = None
        self.dest:bytes = None
        self.currencyId:bytes = None
        self.amount:int = None
        self.feeAmount:int = None
        self.inputData:bytes = None
        self.publicKey:bytes = None
        self.isContract:bool = False
        self.signature:bytes = None
        self.timestamp:int = None
        self.adminSignature:bytes = None
        
    def __str__(self):
        source = Utils.contraction(self.source)
        dest = Utils.contraction(self.dest)
        return f"<Transaction {source} -> {dest}>"
    
    def __repr__(self):
        return self.__str__()
    
    def toDict(self) -> dict[str,str|int|bytes]:
        return {
            "indexId": self.indexId,
            "networkId": self.networkId,
            "source": self.source,
            "dest": self.dest,
            "currencyId": self.currencyId,
            "amount": self.amount,
            "feeAmount": self.feeAmount,
            "inputData": self.inputData,
            "publicKey": self.publicKey,
            "isContract": int(self.isContract),
            "signature": self.signature,
            "timestamp": self.timestamp,
            "adminSignature": self.adminSignature
        }
    
    def toHexDict(self) -> dict[str,str|int]:
        return {
            "indexId": self.indexId,
            "networkId": self.networkId,
            "source": self.source.hex(),
            "dest": self.dest.hex(),
            "currencyId": self.currencyId.hex(),
            "amount": self.amount,
            "feeAmount": self.feeAmount,
            "inputData": self.inputData.hex(),
            "publicKey": self.publicKey.hex(),
            "isContract": int(self.isContract),
            "signature": self.signature.hex(),
            "timestamp": self.timestamp,
            "adminSignature": self.adminSignature.hex()
        }
    
    @classmethod
    def fromDict(cls, data:dict) -> "Transaction":
        tx = cls()
        tx.indexId = data.get("indexId", None)
        tx.networkId = data.get("networkId", None)
        tx.source = data.get("source", None)
        tx.dest = data.get("dest", None)
        tx.currencyId = data.get("currencyId", None)
        tx.amount = data.get("amount", None)
        tx.feeAmount = data.get("feeAmount", None)
        tx.inputData = data.get("inputData", None)
        tx.publicKey = data.get("publicKey", None)
        tx.isContract = bool(data.get("isContract", 0))
        tx.signature = data.get("signature", None)
        tx.timestamp = data.get("timestamp", None)
        tx.adminSignature = data.get("adminSignature", None)
        return tx
    
    @classmethod
    def fromHexDict(cls, data:dict) -> "Transaction":
        tx = cls()
        tx.indexId = data.get("indexId", None)
        tx.networkId = data.get("networkId", None)
        tx.source = bytes.fromhex(data.get("source", None))
        tx.dest = bytes.fromhex(data.get("dest", None))
        tx.currencyId = bytes.fromhex(data.get("currencyId", None))
        tx.amount = data.get("amount", None)
        tx.feeAmount = data.get("feeAmount", None)
        tx.inputData = bytes.fromhex(data.get("inputData", None))
        tx.publicKey = bytes.fromhex(data.get("publicKey", None))
        tx.isContract = bool(data.get("isContract", 0))
        tx.signature = bytes.fromhex(data.get("signature", None))
        tx.timestamp = data.get("timestamp", None)
        tx.adminSignature = bytes.fromhex(data.get("adminSignature", None))
        return tx
    
    @classmethod
    def create(cls, source:"Wallet", dest:bytes, currencyId:bytes, amount:int, feeAmount:int = 0, inputData:bytes = bytes(), isContract:bool = False) -> "Transaction":
        pass

    @classmethod
    def genesis(cls, adminWallet:"Wallet", dest:bytes, currencyId:bytes, amount:int, timestamp:int) -> "Transaction":
        pass
    
    def adminSign(self, indexId:int, adminWallet:"Wallet", timestamp:int = int(time())):
        pass

    def verify(self) -> tuple[bool,bool]:
        pass

    def toSql(self) -> tuple[str,str]:
        sql = "INSERT INTO transaction (indexId,source,dest,currencyId,amount,feeAmount,inputData,publicKey,isContract,signature,timestamp,adminSignature) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (self.indexId, self.source, self.dest, self.currencyId, self.amount, self.feeAmount, self.inputData, self.publicKey, int(self.isContract), self.signature, self.timestamp, self.adminSignature)
        return sql, params

class Currency:
    def __init__(self) -> None:
        self.currencyId:bytes = None
        self.name:str = None
        self.symbol:str = None
        self.issuer:bytes = None
        self.supply:int = None
    
    def __str__(self):
        idhex = self.currencyId.hex()
        return f"<Currency {self.name}({self.symbol}): {idhex[:6]}....{idhex[-6:]}>"
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def create(cls,name:str,symbol:str,issuer:bytes,supply:int=0) -> "Currency":
        pass
    
    def verify(self):
        pass

class Wallet:
    def __init__(self) -> None:
        self.privateKey:bytes = None
        self.publicKey:bytes = None
        self.address:bytes = None
    
    def __str__(self) -> str:
        return f"<Wallet {self.address.hex()}>"
    
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def generate(cls) -> "Wallet":
        pass
    
    @classmethod
    def fromPrivate(cls,privateKey:bytes) -> "Wallet":
        pass
    
    @classmethod
    def fromPublic(cls,publicKey:bytes) -> "Wallet":
        pass
    
    def sign(self,data:bytes) -> bytes:
        pass

    def verifySignature(self,data:bytes,signature:bytes):
        pass
    
    def detail(self):
        pass
