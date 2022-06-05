from asyncio import exceptions
from importlib.metadata import entry_points
from os import O_TEXT
from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    getAccount,
    fund_with_link,
    getContract,
)
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 2000 ETH/USD
    # USD Entry Fee is 50
    # 2000/1 = 50/x. x = 0.025
    expected_entrace_fee = Web3.toWei(0.025, "ether")
    entrace_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrace_fee == entrace_fee


def test_cant_enter_unless_started():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    #  Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": getAccount(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    #  Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    #  Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # Assert
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    #  Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    txn = lottery.endLottery({"from": account})
    requestID = txn.events["RequestedRandomness"]["requestID"]
    STATIC_RNG = 777
    getContract("vrf_coordinator").callBackWithRandomness(
        requestID, STATIC_RNG, lottery.address, {"from": account}
    )
    # Assert
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    # 777 % 3 =  259 so 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
