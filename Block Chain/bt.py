import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transaction_details, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transaction_details = transaction_details
        self.hash = hash
        self.nonce = nonce

class StudentRecordBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        self.students = {}

    def create_genesis_block(self):
        genesis_block = Block(0, "0", int(time.time()), "Genesis Block", self.calculate_hash(0, "0", int(time.time()), "Genesis Block", 0), 0)
        self.chain.append(genesis_block)

    def add_transaction(self, transaction_details):
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = int(time.time())
        previous_hash = previous_block.hash
        nonce = self.proof_of_work(index, previous_hash, timestamp, transaction_details)
        new_hash = self.calculate_hash(index, previous_hash, timestamp, transaction_details, nonce)
        new_block = Block(index, previous_hash, timestamp, transaction_details, new_hash, nonce)
        self.chain.append(new_block)

    def proof_of_work(self, index, previous_hash, timestamp, transaction_details):
        nonce = 0
        while True:
            new_hash = self.calculate_hash(index, previous_hash, timestamp, transaction_details, nonce)
            if new_hash[:4] == "0000":  # Difficulty level
                return nonce
            nonce += 1

    def calculate_hash(self, index, previous_hash, timestamp, transaction_details, nonce):
        value = str(index) + str(previous_hash) + str(timestamp) + str(transaction_details) + str(nonce)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_student(self, student_id, name):
        self.students[student_id] = {"name": name, "records": []}
        self.add_transaction(f"Added Student: {student_id}, Name: {name}")

    def update_student_record(self, student_id, record):
        if student_id in self.students:
            self.students[student_id]["records"].append(record)
            self.add_transaction(f"Updated Student: {student_id}, Record: {record}")
        else:
            print(f"Student {student_id} not found.")

    def print_chain(self):
        for block in self.chain:
            print(vars(block))

    def print_student_records(self):
        for student_id, details in self.students.items():
            print(f"Student ID: {student_id}, Name: {details['name']}, Records: {details['records']}")

if __name__ == '__main__':
    student_blockchain = StudentRecordBlockchain()

    # Adding students to the blockchain
    student_blockchain.add_student("S1234", "Alice Smith")
    student_blockchain.add_student("S5678", "Bob Johnson")

    # Updating student records
    student_blockchain.update_student_record("S1234", "Math: A")
    student_blockchain.update_student_record("S1234", "Science: B+")
    student_blockchain.update_student_record("S5678", "Math: B")
    student_blockchain.update_student_record("S5678", "History: A-")

    # Printing student records
    student_blockchain.print_student_records()

    # Printing the blockchain
    student_blockchain.print_chain()