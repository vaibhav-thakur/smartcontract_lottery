from os import access
from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    getAccount,
    fund_with_link,
)
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = getAccount()
    lottery.startLottery({"from": account})
    print("lottery.getEntranceFee()")
    print(lottery.getEntranceFee())
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # lottery.enter({"from": getAccount(index=1), "value": lottery.getEntranceFee()})
    txn = fund_with_link(lottery)
    # txn.wait(1)
    ending_txn = lottery.endLottery({"from": account})
    # ending_txn.wait(1)
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
