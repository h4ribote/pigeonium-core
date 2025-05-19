from funcHint import *

# Currency deposit system

if not getSelfCurrency():
    createCurrency("TestCurrency","TC",1000_000000)

depo_amount = getVariable(selfAddress,transaction.source)
depo_time = getVariable(selfAddress,md5(transaction.source))
if depo_amount and depo_time:
    depoTime = int.from_bytes(depo_time,'big')
    depoAmount = int.from_bytes(depo_amount,'big')
    depoPeriod = transaction.timestamp - depoTime
    if depoPeriod < 60*60*24:
        transferFromContract(transaction.source,getSelfCurrency().currencyId,depo_amount)
    else:
        interestRate = 1 + depoPeriod/(60*60*24) * 0.01
        transferFromContract(transaction.source,getSelfCurrency().currencyId,int(depo_amount*(interestRate)))

if transaction.currencyId == getSelfCurrency().currencyId:
    setVariable(transaction.source,transaction.amount.to_bytes(8,'big')) # depo_amount
    setVariable(md5(transaction.source),transaction.timestamp.to_bytes(8,'big')) # depo_time
else: # Unsupported currencies
    transferFromContract(transaction.source,transaction.currencyId,transaction.amount)
