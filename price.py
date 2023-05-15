import requests
import time


def get_closest_time_price(timestamp: float, data: list):
    closest_ts = None
    closest_price = None
    min_time_diff = float("inf")

    for ts, price in data:
        time_diff = abs(ts - timestamp)
        if time_diff < min_time_diff:
            closest_ts = ts
            closest_price = price
            min_time_diff = time_diff

    return closest_ts, closest_price


def price_from_cid(unique_tokens_list: list, unix_times: list):
    THROTTLE_RATE = 10  # 10s per API request

    token_time_price_dict = {}
    unix_times = [x * 1000 for x in unix_times]  # Convert time to ms unix
    for token_address in unique_tokens_list:
        coingecko_url = f"https://api.coingecko.com/api/v3/coins/eth/contract/{token_address}/market_chart/?vs_currency=usd&days=5"
        try:
            data = requests.get(coingecko_url).json()["prices"]

            # Yesterdays data
            for timestamp in unix_times:
                timestamp_real, price = get_closest_time_price(
                    timestamp=timestamp, data=data
                )
                token_time_price_dict[(token_address, timestamp)] = price

        except Exception as e:
            print(coingecko_url)
            print(f"Token CID cant be found: {token_address}")

        # Throttle before moving onto next request
        time.sleep(THROTTLE_RATE)

    return token_time_price_dict


def get_token_price(*protocols, unix_times: list):
    """
    Input structure: (protocol_name, pools_tokens_dict)
        pools_tokens_dict -> {
            (pool0, token0): num_of_token0_in_pool0,
            (pool0, token1): num_of_token1_in_pool0...
        }
    Output structure: (protocol_name, pools_TVL_dict)
        pools_TVL_dict ->{
            pool0: TVL,
            pool1: TVL ...
        }
    """

    # Basic check to ensure right data is being passed
    for protocol in protocols:
        if len(protocol) != 2:
            raise ValueError(
                "Each protocol must be a tuple with two elements: a string and a dictionary."
            )
        protocol_name, protocol_dict = protocol
        if not isinstance(protocol_name, str):
            raise TypeError("Protocol name must be a string.")
        if not isinstance(protocol_dict, dict):
            raise TypeError("Protocol dictionary must be a dictionary.")

    # Create a list of pools_tokens_dict
    pools_tokens_list = []
    for protocol in protocols:
        protocol_name, pools_tokens_dict = protocol
        pools_tokens_list.append(pools_tokens_dict)

    # Create list of unique tokens
    unique_tokens_list = []
    for pools_tokens_dict in pools_tokens_list:
        for key in pools_tokens_dict:
            token_address = key[1]
            if token_address not in unique_tokens_list:
                unique_tokens_list.append(token_address)

    # Get token's price based on closest timestamp
    token_time_price_dict = price_from_cid(unique_tokens_list, unix_times)

    return token_time_price_dict


### Testing Corner ###
token0 = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # WETH
token1 = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
token2 = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"  # WBTC
token3 = "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # DAI
get_token_price(
    (
        "uniswap",
        {
            ("pool0", token0): 100,
            ("pool0", token1): 110,
            ("pool1", token0): 120,
            ("pool1", token2): 130,
        },
    ),
    ("curve", {("cpool0", token0): 140, ("cpool0", token3): 150}),
    unix_times=[1681948800, 1682035200],
)
### End Testing Corner ###
