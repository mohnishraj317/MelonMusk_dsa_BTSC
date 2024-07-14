import hashlib

def hash(message):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    return sha256_hash.hexdigest()

def verify(received_message, received_hash):
    computed_hash = hash(received_message)
    return computed_hash == received_hash

def send_hash(hash):
    return hash

def send_message(message):
    return message

alice_message = input("Enter Alice's message: ")
alice_hash = hash(alice_message)

print("Alice's Message: ",alice_message)
print("Alice's Hash: ",alice_hash)

bob_message = send_message(alice_message)
bob_hash = send_hash(alice_hash)

print("Bob's Message: ",bob_message)
print("Bob's Hash: ",bob_hash)
print("Decoded Hash: ",hash(bob_message))

is_equal = verify(bob_message, bob_hash)
if(is_equal):
    print("Transmission Not Tampered")
