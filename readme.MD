# Summary of Workflow
1. Scrap data from all the relevant websites such as *pool_address*, *pool_description*
2. With the *pool_address* from above, get information on how much token is in each pool using Web3 call.
3. Store the information in the format of:
    - {(pool0, token0): [amt_of_token0_in_pool0_for_time0, amt_of_token10_in_pool0_for_time1], 
    <br>(pool0, token1): [amt_of_token1_in_pool0_for_time0, amt_of_token1_in_pool0_for_time1], ...}
    - E.g. {(0x5777d92f208679db4b9778590fa3cab3ac9e2168, 0x6b175474e89094c44da98b954eedeac495271d0f): [59M, 60M], ...}
4. Find the unique tokens and use coingecko API to get the historical price.
5. Combine the information on prices, and the token to get the TVL. And how much TVL change