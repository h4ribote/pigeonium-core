from .utils import Utils
from .config import Config
from .wallet import Wallet
from .state import State
from typing import Literal
from .struct import Transaction
from .error import *
from asteval import Interpreter
import json


class Contract:
    def __init__(self, script:str) -> None:
        self.script = script
        self.address = Utils.md5(Utils.sha256(script.encode()))
        self.deployCost = len(script.encode()) * Config.ContractDeployCost
        self.excutionCost = len(script.encode()) * Config.ContractExecutionCost

    def __str__(self):
        return f"<Contract {self.address.hex()}>"
    
    def __repr__(self):
        return self.__str__()
    
    def verify(self):
        return self.address == Utils.md5(Utils.sha256(self.script.encode()))

    def execute(self, transaction:Transaction, state:State):
        try:
            state.payFee(self.excutionCost)
        
            aeval = Interpreter(minimal=True)
            aeval.config['augassign'] = True
            aeval.config['if'] = True
            aeval.config['ifexp'] = True
            aeval.config['try'] = True

            aeval.symtable['cancelTx'] = False
            aeval.symtable['exception'] = None

            aeval.symtable['transaction'] = transaction

            aeval.symtable['hex2bytes'] = Utils.hex2bytes
            aeval.symtable['md5'] = Utils.md5
            aeval.symtable['sha256'] = Utils.sha256

            aeval.symtable['getBalance'] = state.getBalance
            aeval.symtable['getCurrency'] = state.getCurrency
            aeval.symtable['getSelfCurrency'] = state.getSelfCurrency
            aeval.symtable['getTransaction'] = state.getTransaction
            aeval.symtable['getTransactions'] = state.getTransactions
            aeval.symtable['getVariable'] = state.getVariable
            # aeval.symtable['getVariables'] = state.getVariables
            aeval.symtable['setVariable'] = state.setVariable
            aeval.symtable['transferFromUser'] = state.transferFromUser
            aeval.symtable['transferFromContract'] = state.transferFromContract
            aeval.symtable['burn'] = state.burn
            aeval.symtable['mint'] = state.mint
            aeval.symtable['createCurrency'] = state.createCurrency
            aeval.symtable['nextIndexId'] = state.nextIndexId

            aeval(self.script)
        
            if aeval.symtable['cancelTx'] == True:
                if isinstance(aeval.symtable['exception'], Exception):
                    raise aeval.symtable['exception']
                else:
                    raise ContractError("Transaction canceled")
        except Exception as e:
            raise e
