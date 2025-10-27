#!/usr/bin/env python3
import os
import base64

# Set environment
os.environ['VAULT_ADDR'] = 'http://127.0.0.1:8200'
os.environ['VAULT_TOKEN'] = 'root'

print("🔐 KMS LEARNING LAB - LET'S GO!")
print("=" * 40)

try:
    import hvac
    print("✅ Libraries loaded successfully")
    
    # Connect to Vault
    client = hvac.Client(url='http://127.0.0.1:8200', token='root')
    
    if client.is_authenticated():
        print("✅ Connected to Vault!")
    else:
        print("❌ Cannot connect to Vault")
        exit(1)
    
    # Enable transit
    try:
        client.sys.enable_secrets_engine(backend_type='transit', path='transit')
        print("✅ Transit engine enabled")
    except Exception as e:
        if "already in use" in str(e):
            print("ℹ️ Transit engine already enabled")
        else:
            print(f"❌ Failed to enable transit: {e}")
            exit(1)
    
    # Create key
    try:
        client.secrets.transit.create_key('my-key')
        print("✅ Encryption key created: 'my-key'")
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ Key already exists")
        else:
            print(f"❌ Failed to create key: {e}")
            exit(1)
    
    # ENCRYPT
    print("\n🎯 ENCRYPTING DATA...")
    secret = "Hello Multi-Cloud KMS World!"
    print(f"Original: {secret}")
    
    encrypted = client.secrets.transit.encrypt_data(
        name='my-key',
        plaintext=base64.b64encode(secret.encode()).decode()
    )
    ciphertext = encrypted['data']['ciphertext']
    print(f"Encrypted: {ciphertext}")
    
    # DECRYPT
    print("\n🎯 DECRYPTING DATA...")
    decrypted = client.secrets.transit.decrypt_data(
        name='my-key',
        ciphertext=ciphertext
    )
    decrypted_text = base64.b64decode(decrypted['data']['plaintext']).decode()
    print(f"Decrypted: {decrypted_text}")
    
    # VERIFY
    if secret == decrypted_text:
        print("\n🎉 SUCCESS! KMS is working perfectly!")
        print("Encryption → Decryption: ✅")
    else:
        print("\n❌ FAILED! Messages don't match")
        exit(1)
    
    # KEY ROTATION
    print("\n🔄 DEMONSTRATING KEY ROTATION...")
    client.secrets.transit.rotate_key('my-key')
    print("✅ Key rotated to new version")
    
    # Test backward compatibility
    still_works = client.secrets.transit.decrypt_data(
        name='my-key',
        ciphertext=ciphertext
    )
    still_works_text = base64.b64decode(still_works['data']['plaintext']).decode()
    
    if still_works_text == secret:
        print("✅ Backward compatibility: OLD data works with NEW key")
    else:
        print("❌ Backward compatibility failed")
    
    print("\n" + "=" * 50)
    print("🎓 CONGRATULATIONS! YOU'VE LEARNED:")
    print("✓ Key Management System fundamentals")
    print("✓ Data encryption and decryption")
    print("✓ Key rotation and versioning")
    print("✓ HashiCorp Vault operations")
    print("\n🚀 Next: Add AWS KMS and Google Cloud KMS!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
