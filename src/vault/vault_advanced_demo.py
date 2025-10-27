#!/usr/bin/env python3
import os
import base64
import hvac

# Set environment
os.environ['VAULT_ADDR'] = 'http://127.0.0.1:8200'
os.environ['VAULT_TOKEN'] = 'root'

print("🔐 ADVANCED VAULT KMS DEMO")
print("=" * 45)

def main():
    try:
        # Connect to Vault
        client = hvac.Client(url='http://127.0.0.1:8200', token='root')
        
        if not client.is_authenticated():
            print("❌ Cannot connect to Vault")
            return
        
        print("✅ Connected to Vault!")
        
        # Enable transit engine
        try:
            client.sys.enable_secrets_engine(backend_type='transit', path='transit')
            print("✅ Transit engine enabled")
        except Exception:
            print("ℹ️ Transit engine already enabled")
        
        # Create key
        try:
            client.secrets.transit.create_key('advanced-key')
            print("✅ Encryption key created: 'advanced-key'")
        except Exception:
            print("ℹ️ Key already exists")
        
        print("\n🎓 LESSON 1: MULTIPLE ENCRYPTIONS")
        print("-" * 35)
        
        secrets = [
            "Credit Card: 4111-1111-1111-1111",
            "API Key: sk_live_abcdef123456",
            "Database Password: SuperSecret123!",
            "SSH Private Key: -----BEGIN RSA PRIVATE KEY-----"
        ]
        
        ciphertexts = []
        
        for i, secret in enumerate(secrets, 1):
            print(f"\n🔐 Secret {i}: {secret[:30]}...")
            
            # Encrypt
            encrypted = client.secrets.transit.encrypt_data(
                name='advanced-key',
                plaintext=base64.b64encode(secret.encode()).decode()
            )
            ciphertext = encrypted['data']['ciphertext']
            ciphertexts.append(ciphertext)
            print(f"   🔒 Encrypted: {ciphertext[:40]}...")
            
            # Decrypt
            decrypted = client.secrets.transit.decrypt_data(
                name='advanced-key',
                ciphertext=ciphertext
            )
            decrypted_text = base64.b64decode(decrypted['data']['plaintext']).decode()
            print(f"   🔓 Decrypted: {decrypted_text[:30]}...")
            
            # Verify
            if secret == decrypted_text:
                print("   ✅ Success!")
            else:
                print("   ❌ Failed!")
        
        print("\n🎓 LESSON 2: KEY ROTATION")
        print("-" * 25)
        
        print("🔄 Rotating encryption key...")
        client.secrets.transit.rotate_key('advanced-key')
        print("✅ Key rotated to new version!")
        
        print("\n🔍 Testing backward compatibility...")
        for i, ciphertext in enumerate(ciphertexts, 1):
            try:
                decrypted_after_rotation = client.secrets.transit.decrypt_data(
                    name='advanced-key',
                    ciphertext=ciphertext
                )
                still_works = base64.b64decode(decrypted_after_rotation['data']['plaintext']).decode()
                print(f"   Secret {i}: ✅ Still decrypts after rotation")
            except Exception as e:
                print(f"   Secret {i}: ❌ Failed after rotation: {e}")
        
        print("\n🎓 LESSON 3: KEY INFORMATION")
        print("-" * 25)
        
        try:
            key_info = client.secrets.transit.read_key('advanced-key')
            if key_info and 'data' in key_info:
                info = key_info['data']
                print(f"   Key Name: advanced-key")
                print(f"   Latest Version: {info.get('latest_version', 'N/A')}")
                print(f"   Type: {info.get('type', 'N/A')}")
                print(f"   Keys: {list(info.get('keys', {}).keys())}")
        except Exception as e:
            print(f"   ℹ️ Could not read key info: {e}")
        
        print("\n" + "=" * 60)
        print("🎓 ADVANCED VAULT KMS MASTERY ACHIEVED!")
        print("=" * 60)
        print("You've demonstrated:")
        print("✓ Multiple encryption/decryption operations")
        print("✓ Key rotation and version management")
        print("✓ Backward compatibility testing")
        print("✓ Key metadata inspection")
        print("\n🚀 Ready for production KMS operations!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
