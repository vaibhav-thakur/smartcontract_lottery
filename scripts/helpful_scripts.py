from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    interface,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def getAccount(index=None, id=None):
    # account[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def getContract(contract_name):
    """This function will grab the contract addressed from brownie config
    when defined, otherwise it will deploy and return a mock version of that contract.
     Args:
         contract_name (String)

     Returns
         brownie.network.contract.ProjectContract : The most recenty deployed version
         of the Contract.

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INTITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INTITIAL_VALUE):
    account = getAccount()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    linkToken = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(linkToken.address, {"from": account})
    print("Deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, default_amt=100000000000000000
):  # 0.1 LINK -- It is supposed to be 0.25 LINK not 0.1. This caused the VirtualMachineError
    account = account if account else getAccount()
    link_token = link_token if link_token else getContract("link_token")
    txn = link_token.transfer(contract_address, default_amt, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # txn = link_token_contract.transfer(contract_address, default_amt, {"from": acccount})
    txn.wait(1)
    print("Funded Contract!")
    return txn
