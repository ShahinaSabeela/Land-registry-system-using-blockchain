from datetime import time
import hashlib
import json

class blockchain():
    def __init__(self):
        self.f = open('database.json')
        self.blocks = json.load(f)
        
        self.__secret = ''
        self.__difficulty = 4 
        i = 0
        while True:
            _hash = hashlib.sha256(str( str(i)).encode('utf-8')).hexdigest()
            if(_hash[:self.__difficulty] == '0'*self.__difficulty):
                self.__secret = _hash
                break
            i+=1
    def create_block(self, sender:str, information:str):
        block = {
            'index': len(self.blocks),
            'sender': sender,
            'timestamp': time(),
            'info': information
        }
        if(block['index'] == 0): block['previous_hash'] = self.__secret # for genesis block
        else: block['previous_hash'] = self.blocks[-1]['hash']
        i = 0
        while True:
            block['nonce'] = i
            _hash = hashlib.sha256(str(block).encode('utf-8')).hexdigest()
            if(_hash[:self.__difficulty] == '0'*self.__difficulty):
                block['hash'] = _hash
                break
            i+=1
        self.blocks.append(block)
    def validate_blockchain(self):
        valid = True
        n = len(self.blocks)-1
        i = 0
        while(i<n):
            if(self.blocks[i]['hash'] != self.blocks[i+1]['previous_hash']):
                valid = False
                break
            i+=1
        if valid:
            with open("database.json", "w") as outfile:
                self.f.dump(self.blocks, outfile)
            return True
        else: return False
    def show_blockchain(self):
        for block in self.blocks: 
            print(block)
