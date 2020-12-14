from userinterface import *
import config as cfg



web3,contract=initialize_contract(cfg.ganache_URL,cfg.address,cfg.abi)

main_loop(web3,contract,cfg.function_info)

