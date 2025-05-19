class ContractError(Exception):
    pass

class PigeoniumError(Exception):
    pass


class InvalidSignature(ContractError):
    pass

class InsufficientBalance(ContractError):
    pass

class InvalidTransaction(ContractError):
    pass

class InvalidCurrency(ContractError):
    pass

class SelfTransaction(ContractError):
    pass

class DuplicateSignature(ContractError):
    pass

class InvalidAdminSignature(PigeoniumError):
    pass
