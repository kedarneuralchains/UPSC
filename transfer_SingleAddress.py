# Import required libraries
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Connect to an Ethereum node
web3 = Web3(Web3.HTTPProvider('https://rpc.url.com')) # secure rpc url for network of choice
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Set sender and recipient addresses
sender_address = web3.to_checksum_address('0xSenderAddress')
recipient_address = web3.to_checksum_address('0xReceiverAddress')

# Set private key for the sender's account. 
private_key = '0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # DO NOT SHARE YOUR PRIVATE KEY.

# Fetch balance data (optional)
balance_sender = web3.from_wei(web3.eth.get_balance(sender_address), 'ether')
balance_recipient = web3.from_wei(web3.eth.get_balance(recipient_address), 'ether')

print(f'The balance of { sender_address } is: { balance_sender } ETH')
print(f'The balance of { recipient_address } is: { balance_recipient } ETH')

# Static gas price setup
gas_price = web3.to_wei(5, 'gwei')  # set gas price, 5 Gwei here

# Define the transaction parameters
transaction_params = {
    'from': sender_address,
    'to': recipient_address,
    'value': web3.to_wei(0.01, 'ether'),  # set amount to be sent (0.01 Ether in this example)
    'nonce': web3.eth.get_transaction_count(sender_address),
    'gas': 21000,  # Gas limit for the transaction
    'gasPrice': gas_price,  # Static gas price of 5 Gwei
    'chainId': 1234 # ChainId for network of choice
}

# Sign the transaction
transaction = web3.eth.account.sign_transaction(transaction_params, private_key)

# Send the transaction
transaction_hash = web3.eth.send_raw_transaction(transaction.rawTransaction)

# Wait for the transaction to be mined
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

# Check the transaction status (optional)
if transaction_receipt.status:
    print('Transaction successful!')
    print('Transaction hash:', transaction_hash.hex())
    print(f'Explorer link: https://explorer.chain.com/tx/{transaction_hash.hex()}') # set explorer url
else:
    print('Transaction failed.')

# Fetch balance data after the transaction (optional)
balance_sender = web3.from_wei(web3.eth.get_balance(sender_address), 'ether')
balance_recipient = web3.from_wei(web3.eth.get_balance(recipient_address), 'ether')

print(f'The balance of { sender_address } is: { balance_sender } ETH')
print(f'The balance of { recipient_address } is: { balance_recipient } ETH')
