from .utils import Utils
from .config import Config
from .wallet import Wallet
from .contract import Contract
from .struct import Transaction as TransactionStruct
from time import time
from .state import State
from .error import *

class Transaction(TransactionStruct):
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return super().__str__()
    
    def __repr__(self):
        return super().__repr__()

    @classmethod
    def create(cls, source:Wallet, dest:bytes, currencyId:bytes, amount:int, feeAmount:int = 0, inputData:bytes = bytes(), isContract:bool = False) -> "Transaction":
        tx = cls()
        tx.networkId = Config.NetworkId
        tx.source = source.address
        tx.dest = dest
        tx.currencyId = currencyId
        tx.amount = amount
        tx.feeAmount = feeAmount
        tx.inputData = inputData
        tx.isContract = isContract
        if isContract:
            try:
                tx.publicKey = source.publicKey
                tx.signature = source.sign(tx.networkId.to_bytes(8,'big')+tx.source+tx.dest+tx.currencyId+tx.amount.to_bytes(8,'big')+tx.feeAmount.to_bytes(8,'big')+tx.inputData)
            except:
                tx.publicKey = bytes(64)
                tx.signature = bytes(64)
        else:
            tx.publicKey = source.publicKey
            tx.signature = source.sign(tx.networkId.to_bytes(8,'big')+tx.source+tx.dest+tx.currencyId+tx.amount.to_bytes(8,'big')+tx.feeAmount.to_bytes(8,'big')+tx.inputData)
        return tx

    @classmethod
    def genesis(cls, adminWallet:Wallet, dest:bytes, currencyId:bytes, amount:int, timestamp:int) -> "Transaction":
        tx = cls()
        tx.indexId = 0
        tx.networkId = Config.NetworkId
        tx.source = bytes(16)
        tx.dest = dest
        tx.currencyId = currencyId
        tx.amount = amount
        tx.feeAmount = 0
        tx.inputData = bytes()
        tx.publicKey = bytes(64)
        tx.signature = bytes(64)
        tx.isContract = True
        tx.timestamp = timestamp
        txData = (tx.indexId.to_bytes(8,'big')+tx.networkId.to_bytes(8,'big')+tx.source+tx.dest+
                  tx.currencyId+tx.amount.to_bytes(8,'big')+tx.feeAmount.to_bytes(8,'big')+tx.inputData+tx.timestamp.to_bytes(8,'big'))
        tx.adminSignature = adminWallet.sign(txData)
        return tx
    
    def adminSign(self, indexId:int, adminWallet:Wallet = Wallet.fromPrivate(Config.AdminPrivateKey), timestamp:int = int(time())):
        txData = (indexId.to_bytes(8,'big')+self.networkId.to_bytes(8,'big')+
                  self.source+self.dest+self.currencyId+self.amount.to_bytes(8,'big')+self.feeAmount.to_bytes(8,'big')+self.inputData+
                  self.signature+timestamp.to_bytes(8,'big'))
        self.adminSignature = adminWallet.sign(txData)
        self.indexId = indexId
        self.timestamp = timestamp

    def verify(self) -> tuple[bool,bool]:
        sourceSignature = False
        adminSignature = False
        if self.isContract:
            txData = (self.indexId.to_bytes(8,'big')+self.networkId.to_bytes(8,'big')+self.source+self.dest+
                      self.currencyId+self.amount.to_bytes(8,'big')+self.feeAmount.to_bytes(8,'big')+self.inputData+self.timestamp.to_bytes(8,'big'))
            if Wallet.fromPublic(Config.AdminPublicKey).verifySignature(txData, self.adminSignature):
                sourceSignature = True
                adminSignature = True
        else:
            sourceWallet = Wallet.fromPublic(self.publicKey)
            txData = (self.networkId.to_bytes(8,'big')+self.source+self.dest+self.currencyId+self.amount.to_bytes(8,'big')+self.feeAmount.to_bytes(8,'big')+self.inputData)
            if sourceWallet.verifySignature(txData, self.signature):
                sourceSignature = True
            txData = (self.indexId.to_bytes(8,'big')+self.networkId.to_bytes(8,'big')+self.source+self.dest+
                      self.currencyId+self.amount.to_bytes(8,'big')+self.feeAmount.to_bytes(8,'big')+self.inputData+self.timestamp.to_bytes(8,'big'))
            if Wallet.fromPublic(Config.AdminPublicKey).verifySignature(txData, self.adminSignature):
                adminSignature = True
        return sourceSignature, adminSignature

    def execute(self):
        state = State(self.source, self.dest)
        if state.getBalance(self.source, self.currencyId) < self.amount:
            raise InsufficientBalance()
        state.cursor.execute(self.toSql())
        state.cursor.execute("UPDATE balance SET amount = amount - %s WHERE address = %s AND currencyId = %s", (self.amount, self.source, self.currencyId))
        if self.dest == bytes(16):
            state.cursor.execute("UPDATE currency SET supply = supply - %s WHERE currencyId = %s", (self.amount, self.currencyId))
        else:
            state.cursor.execute("INSERT INTO balance (address,currencyId,amount) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE amount=amount+%s",
                             (self.dest, self.currencyId, self.amount, self.amount))
        if state.isContract(self.dest):
            contract = Contract(state.getScript(self.dest))
            contract.execute(self, state)
