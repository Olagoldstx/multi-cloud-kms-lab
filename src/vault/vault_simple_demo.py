#!/usr/bin/env python3
import os
import base64
import hvac

# Set environment
os.environ['VAULT_ADDR'] = 'http://127.0.0.1:8200'
os.environ['VAULT_TOKEN'] = 'root'

print("🔐 SIMPLE VAULT KMS DEMO")
print("=" * 40)

def main():
    try:
        # Connect to Vault
        client = hvac.Client(url='http://127.0.0.1:8200', token='root')
        
        if client.is_authenticated():
            print("✅ Connected to Vault!")
        else:
            print("❌ Cannot connect to Vault")
            return
        
        # Enable transit engine
        try:
            client.sys.enable_secrets_engine(backend_type='transit', path='transit')
            print("✅ Transit engine enabled")
        except Exception:
            print("ℹ️ Transit engine already enabled")
        
        # Create key
        try:
            client.secrets.transit.create_key('simple-key')
            print("✅ Encryption key created: 'simple-key'")
        except Exception:
            print("ℹ️ Key already exists")
        
        # Encrypt data
        print("\n🔐 ENCRYPTING DATA...")
        secret = "Hello Multi-Cloud KMS World!"
        print(f"Original: {secret}")
        
        encrypted = client.secrets.transit.encrypt_data(
            name='simple-key',
            plaintext=base64.b64encode(secret.encode()).decode()
        )
        ciphertext = encrypted['data']['ciphertext']
        print(f"Encrypted: {ciphertext}")
        
        # Decrypt data
        print("\n🔓 DECRYPTING DATA...")
        decrypted = client.secrets.transit.decrypt_data(
            name='simple-key',
            ciphertext=ciphertext
        )
        decrypted_text = base64.b64decode(decrypted['data']['plaintext']).decode()
        print(f"Decrypted: {decrypted_text}")
        
        # Verify
        if secret == decrypted_text:
            print("\n🎉 SUCCESS! KMS is working perfectly!")
        else:
            print("\n❌ FAILED! Messages don't match")
        
        print("\n" + "=" * 50)
        print("🎓 VAULT KMS BASICS COMPLETE!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
