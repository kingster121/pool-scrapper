def get_price(*protocols):
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
            raise ValueError("Each protocol must be a tuple with two elements: a string and a dictionary.")
        protocol_name, protocol_dict = protocol
        if not isinstance(protocol_name, str):
            raise TypeError("Protocol name must be a string.")
        if not isinstance(protocol_dict, dict):
            raise TypeError("Protocol dictionary must be a dictionary.")
    

    # Create dictionary with keys associated to unique token