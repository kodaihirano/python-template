OntCversion = '2.0.0'
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.App import RegisterAppCall, DynamicAppCall
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash, GetScriptContainer
from ontology.interop.Ontology.Native import Invoke
from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat, state
from ontology.interop.System.Transaction import GetTransactionHash
from ontology.libont import str, AddressFromVmCode

SelfContractAddr = GetExecutingScriptHash()
ONTAddress = Base58ToAddress("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV")
ONGAddress = Base58ToAddress("AFmseVrdL9f9oyCzZefL9tG6UbvhfRZMHJ")

ONT_BALANCE_PREFIX = 'ont'
ONG_BALANCE_PREFIX = 'ong'


def Main(operation, args):
    if operation == "depositOnt":
        assert (len(args) == 2)
        account = args[0]
        amount = args[1]
        return depositOnt(account, amount)
    if operation == "withdrawOnt":
        assert (len(args) == 2)
        account = args[0]
        amount = args[1]
        return withdrawOnt(account, amount)
    if operation == "depositOng":
        assert (len(args) == 2)
        account = args[0]
        amount = args[1]
        return depositOng(account, amount)
    if operation == "withdrawOng":
        assert (len(args) == 2)
        account = args[0]
        amount = args[1]
        return withdrawOng(account, amount)
    if operation == "getOntBalance":
        assert (len(args) == 1)
        account = args[0]
        return getOntBalance(account)
    if operation == "getOngBalance":
        assert (len(args) == 1)
        account = args[0]
        return getOngBalance(account)
    return False



def depositOnt(account, amount):
    """

    :param account: the account who wants to deposit ont into the contract.
    :param amount: the amount of ont. If you want to deposit 1 ONT, you need to pass amount as 1.
    :return:
    """
    assert (CheckWitness(account))
    assert (_transferONT(account, SelfContractAddr, amount))
    Put(GetContext(), _concatKey(ONT_BALANCE_PREFIX, account), getOntBalance(account) + amount)
    Notify(["depositOnt", account, amount])
    return True

def withdrawOnt(account, amount):
    """

    :param account: the account who wants to deposit ont into the contract.
    :param amount: the amount of ont. If you want to withdraw 1 ONT, you need to pass amount as 1.
    :return:
    """
    assert (CheckWitness(account))
    ontBalance = getOntBalance(account)
    assert (ontBalance >= amount)
    assert (_transferONT(SelfContractAddr, account, amount))
    Put(GetContext(), _concatKey(ONT_BALANCE_PREFIX, account), ontBalance - amount)
    Notify(["withdrawOnt", account, amount])
    return True


def depositOng(account, amount):
    """

    :param account: the account who wants to deposit ont into the contract.
    :param amount: the amount of ong. If you want to deposit 1 ONG, you need to pass amount as 1 * 10 ** 9.
    :return:
    """
    assert (CheckWitness(account))
    assert (_transferONG(account, SelfContractAddr, amount))
    Put(GetContext(), _concatKey(ONG_BALANCE_PREFIX, account), getOngBalance(account) + amount)
    Notify(["depositOng", account, amount])
    return True


def withdrawOng(account, amount):
    """

    :param account: the account who wants to deposit ont into the contract.
    :param amount: the amount of ong. If you want to withdraw 1 ONG, you need to pass amount as 1 * 10 ** 9.
    :return:
    """
    assert (CheckWitness(account))
    ongBalance = getOngBalance(account)
    assert (ongBalance >= amount)
    assert (_transferONG(SelfContractAddr, account, amount))
    Put(GetContext(), _concatKey(ONG_BALANCE_PREFIX, account), ongBalance - amount)
    Notify(["withdrawOng", account, amount])
    return True

def getOntBalance(account):
    return Get(GetContext(), _concatKey(ONT_BALANCE_PREFIX, account))

def getOngBalance(account):
    return Get(GetContext(), _concatKey(ONG_BALANCE_PREFIX, account))

def _transferONG(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False

def _transferONT(fromAcct, toAcct, amount):
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONTAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False


def _concatKey(str1,str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)