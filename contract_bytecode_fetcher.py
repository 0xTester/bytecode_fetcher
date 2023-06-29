from web3 import Web3
import os
from datetime import datetime

exact_time = datetime.now()
fmt_time = exact_time.strftime('%d%m%y') 
file_time = exact_time.strftime('%H%M%S')
current_dir = os.getcwd() #We get the current directory to save our results
results_dir = os.path.join(current_dir, 'results', '{}'.format(fmt_time)) #We set our results directory (we will store our results here)
if not os.path.exists(results_dir):
    os.makedirs(results_dir) #We create our results folders here

#We get wss endpoint and credentials from the virtual environment ./activate file. (We could also set a .env file but we preferred the activate file)
USERNAME = os.environ['USERNAME']
PSWD = os.environ['ENDPOINT_PASSWORD']
WSS = os.environ['WSS_ENDPOINT']

#Try to connect using our auth credentials.
connection_url = f"wss://{USERNAME}:{PSWD}@{WSS}"
w3 = Web3(Web3.WebsocketProvider(connection_url))

#Verify if we are connected 
print('Connected: ' + str(w3.is_connected()))

#We get the latest block info
block = w3.eth.get_block('latest')

#Set the range of blocks to analyze. 
initial = block.number - 400 #The number of blocks you want to analyze (starting points from the latest block). You can also set specific block numbers
final = block.number
a_block = w3.eth.get_block(initial)

tx_list = [] #We create a list of contract creation txns, we use this for improved UX
print('Checking transactions from block: ' + str(initial) + ' to ' + str(final))
while initial <= final:
    print('Block: ' + str(initial))
    for tx_hash in a_block ['transactions']: #We iterate the block's txns
        tx = w3.eth.get_transaction(tx_hash) #we get each specific tx_hash
        tx_obj = {'From': tx['from'], 'To': tx['to'], 'value': tx['value']} #Easy format to identify txn objects: From: To: value: 
        if (tx_obj['To'] == None): #We verify if the txn was a contract deployment (To: should be None) 
            dep_hash = str((tx['hash'].hex())) #We catch the txn hash and convert it to hex
            receipt = w3.eth.get_transaction_receipt(dep_hash) #We get the receipt to check if it was a succesful or a failed txn and also to get contract address
            if (receipt['status'] == 1): #We check txn status, if status = 1 then it was successful, if failed then status = 0
                print('Successful contract deployment detected at txn: ' + dep_hash)  
                tx_list.append(dep_hash) #Used for UX
                contract_address = receipt['contractAddress'] #we get the contract address
                contract_bytecode = w3.eth.get_code(contract_address).hex()[2:] #We fetch the bytecode and strip the leading 0x
                filepath = os.path.join(results_dir, contract_address + '.txt') #We create a file for each succesful contract deployment
                file = open(filepath, 'w') #We open the file to wrtie on it
                file.write('Contract address: ' + contract_address + '\n') 
                file.write(f"Contract bytecode: {contract_bytecode}")
            else:
                print('There was a failed contract deployment in this block')
    if not tx_list: #This is what we use the tx_list[] for our UX
        print('No contract deployments found in this block') 
    tx_list = [] #We reset the tx_list 
    initial += 1
    a_block = w3.eth.get_block(initial)
