from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price to feed address to our fundme contract

    # if we are in a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address  # newest address

    fund_me = FundMe.deploy(
        # "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e",
        price_feed_address,
        {"from": account},
        # .get("verify") can be written as ["verify"] but index errors
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # publish_source=True to verify
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
