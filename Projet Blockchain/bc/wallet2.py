from bitcoin import*
private_key = random_key()
print(privkey_to_address)
public_key = privtopub(private_key)
print(public_key)
address = pubtoaddr(public_key)
print("your address is : " + address)