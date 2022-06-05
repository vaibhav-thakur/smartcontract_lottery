1. Users can enter Lottery with ETH based on a USD Fee.
2. An Admin will choose when a Lottery is over.
3. The Lottery will select a Random winner.

How do we want to test this?
1. 'mainnet-fork'
2. 'development' with mocks
3. 'testnet'


# Commands
 brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/LfPiUNGG1yFRDuEFPgWwYd1BRwKye4K8 accounts=10 mnemonic=brownie port=8545