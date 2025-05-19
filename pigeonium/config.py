from mysql.connector import MySQLConnection as MySqlConnection
from .struct import Currency

class Config:
    NetworkName: str = "Pigeonium"
    NetworkId: int = 0
    ContractDeployCost: int = 100
    ContractExecutionCost: int = 10
    InputDataCost: int = 10

    AdminPrivateKey: bytes = None
    AdminPublicKey: bytes = None

    BaseCurrency = Currency()
    BaseCurrency.currencyId = bytes(16)
    BaseCurrency.name = "Pigeon"
    BaseCurrency.symbol = "Pigeon"
    BaseCurrency.issuer = bytes(16)
    BaseCurrency.supply = 1000000_000000 # = 1000000.000000

    MySQLConnection: MySqlConnection = None

    class Server:
        Host: str = "0.0.0.0"
        Port: int = 8000
        RootPath: str = "/"
