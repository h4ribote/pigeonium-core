import hashlib
import requests
from typing import overload
from decimal import Decimal

class Utils:
    @staticmethod
    def dictFormat(data: dict):
        for dKey in list(data.keys()):
            dValue = data[dKey]
            if type(dValue) == bytes:
                data[dKey] = dValue.hex()
        return data
    
    @staticmethod
    def hex2bytes(hex: str, length: int = None) -> bytes:
        b = bytes.fromhex(hex)
        if length and len(b) < length:
            b = bytes(length - len(b)) + b
        return b
    
    @overload
    @staticmethod
    def convertAmount(amount: int) -> str:
        pass

    @overload
    @staticmethod
    def convertAmount(amount: float) -> int:
        pass

    @staticmethod
    def convertAmount(amount):
        if isinstance(amount, int):
            return str(f"{amount / 1000000:,.6f}".rstrip('0').rstrip('.'))
        elif isinstance(amount, float):
            return int(Decimal(str(amount)) * 1000000)
        else:
            raise ValueError()
    
    @staticmethod
    def contraction(bytesObj: bytes, length: int = 6):
        hexObj = bytesObj.hex()
        return f"{hexObj[:length]}....{hexObj[-length:]}"

    @staticmethod
    def sha256(string: bytes) -> bytes:
        return hashlib.sha256(string).digest()

    @staticmethod
    def md5(string: bytes) -> bytes:
        return hashlib.md5(string, usedforsecurity=False).digest()
