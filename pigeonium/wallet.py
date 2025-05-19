from ecdsa import SigningKey, VerifyingKey, NIST256p
import hashlib
from .utils import Utils
from .struct import Wallet as WalletStruct

class Wallet(WalletStruct):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return super().__str__()
    
    def __repr__(self):
        return super().__repr__()
    
    @classmethod
    def generate(cls):
        wallet = cls()
        private_key = SigningKey.generate(NIST256p,None,hashlib.sha256)
        public_key = private_key.get_verifying_key().to_string()
        wallet.privateKey = private_key.to_string()
        wallet.publicKey = public_key
        wallet.address = Utils.md5(Utils.sha256(public_key))

        return wallet
    
    @classmethod
    def fromPrivate(cls,privateKey:bytes):
        wallet = cls()
        private_key = SigningKey.from_string(privateKey,NIST256p,hashlib.sha256)
        public_key = private_key.get_verifying_key().to_string()
        wallet.privateKey = private_key.to_string()
        wallet.publicKey = public_key
        wallet.address = Utils.md5(Utils.sha256(public_key))
        return wallet
    
    @classmethod
    def fromPublic(cls,publicKey:bytes):
        wallet = cls()
        wallet.privateKey = None
        wallet.publicKey = publicKey
        wallet.address = Utils.md5(Utils.sha256(publicKey))
        return wallet
    
    def sign(self,data:bytes) -> bytes:
        private_key = SigningKey.from_string(self.privateKey,NIST256p,hashlib.sha256)
        signature = private_key.sign(data)
        return signature

    def verifySignature(self,data:bytes,signature:bytes):
        public_key = VerifyingKey.from_string(self.publicKey,NIST256p,hashlib.sha256)
        try:
            if public_key.verify(signature,data):
                return True
            else:
                return False
        except:
            return False
    
    def detail(self):
        return f"privateKey | {self.privateKey.hex()}\npublicKey  | {self.publicKey.hex()}\naddress    | {self.address.hex()}"
