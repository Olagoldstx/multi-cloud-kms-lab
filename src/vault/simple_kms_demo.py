#!/usr/bin/env python3
import os
import base64

# Set environment
os.environ['VAULT_ADDR'] = 'http://127.0.0.1:8200'
os.environ['VAULT_TOKEN'] = 'root'

print("🔐 SIMPLE KMS DEMO - GUARANTEED TO WORK")
print("=" * 40)

try:
    import hvac
    print("✅ HVAC imported successfully")
    
    # Connect to Vault
    client = hvac.Client(url='http://127.0.0.1:8200', token='root')
    
    if client.is_authenticated():
        print("✅ Connected to Vault!")
    else:
        print("❌ Cannot connect to Vault")
        exit(1)
    
    # Enable transit (simplest approach)
    try:
        client.sys.enable_secrets_engine(backend_type='transit', path='transit')
        print("✅ Transit engine enabled")
    except:
        print("ℹ️ Transit engine already enabled")
    
    # Create key - MINIMAL approach
    try:
        # Just use minimal parameters
        client.secrets.transit.create_key(name='simple-key')
        print("✅ Key created: 'simple-key'")
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ Key already exists")
        else:
            print(f"❌ Key creation failed: {e}")
            # Try without any parameters
            try:
                client.secrets.transit.create_key('simple-key')
                print("✅ Key created with legacy API")
            except:
                print("❌ Completely failed to create key")
                exit(1)
    
    # ENCRYPT
    print("\n🔐 ENCRYPTION TEST")
    secret = "Hello KMS World!"
    print(f"Original: {secret}")
    
    encrypted = client.secrets.transit.encrypt_data(
        name='simple-key',
        plaintext=base64.b64encode(secret.encode()).decode()
    )
    ciphertext = encrypted['data']['ciphertext']
    print(f"Encrypted: {ciphertext}")
    
    # DECRYPT
    print("\n🔓 DECRYPTION TEST")
    decrypted = client.secrets.transit.decrypt_data(
        name='simple-key', 
        ciphertext=ciphertext
    )
    decrypted_text = base64.b64decode(decrypted['data']['plaintext']).decode()
    print(f"Decrypted: {decrypted_text}")
    
    # VERIFY
    if secret == decrypted_text:
        print("🎉 SUCCESS! KMS is working!")
    else:
        print("❌ FAILED! Something went wrong.")
        
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
