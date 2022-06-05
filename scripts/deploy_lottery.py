from tracemalloc import start
from scripts.helpful_scripts import getAccount, getContract, fund_with_link
from brownie import Lottery, accounts, network, config
import time


def deploy_lottery():
    account = getAccount()
    # id="fcc-acc"
    lottery = Lottery.deploy(
        getContract("eth_usd_price_feed").address,
        getContract("vrf_coordinator").address,
        getContract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery!")
    return lottery


def start_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    startingTxn = lottery.startLottery({"from": account})
    startingTxn.wait(1)
    print("The Lottery is started!")


def enter_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    txn = lottery.enter({"from": account, "value": value})
    txn.wait(1)
    print("You have entered Lottery!")


def end_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    txn = fund_with_link(lottery.address)
    txn.wait(1)
    print("here1")
    ending_txn = lottery.endLottery({"from": account})
    print("here2")
    ending_txn.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the Lottery winner.")
    # Fund contract
    # End Lottery


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
