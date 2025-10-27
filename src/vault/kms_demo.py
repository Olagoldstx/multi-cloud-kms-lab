#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def run_command(cmd, check=True):
    """Run a shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"   Error: {result.stderr}")
            return False
        return result
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python
    python_check = run_command("python3 --version")
    if python_check:
        print(f"✅ {python_check.stdout.strip()}")
    
    # Check Vault
    vault_check = run_command("vault --version")
    if vault_check:
        print(f"✅ Vault: {vault_check.stdout.strip()}")
    else:
        print("❌ Vault not found. Please install HashiCorp Vault.")
        return False
        
    # Check Python packages
    try:
        import hvac
        print("✅ hvac package available")
    except ImportError:
        print("❌ hvac package missing. Run: pip3 install hvac")
        return False
        
    return True

def start_vault():
    """Start Vault development server"""
    print("\n🚀 Starting Vault server...")
    
    # Check if Vault is already running
    status_check = run_command("vault status", check=False)
    if status_check and status_check.returncode == 0:
        print("✅ Vault is already running")
        return True
    
    # Start Vault in development mode
    vault_process = subprocess.Popen([
        "vault", "server", "-dev", "-dev-root-token-id=root",
        "-dev-listen-address=127.0.0.1:8200"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for Vault to start
    time.sleep(3)
    
    # Check if Vault started successfully
    status_check = run_command("vault status", check=False)
    if status_check and status_check.returncode == 0:
        print("✅ Vault server started successfully")
        print("   Address: http://127.0.0.1:8200")
        print("   Token: root")
        return True
    else:
        print("❌ Failed to start Vault server")
        return False

def run_kms_demo():
    """Run the main KMS demonstration"""
    print("\n🎓 KMS LEARNING LAB - CORE CONCEPTS")
    print("=" * 50)
    
    import hvac
    import base64
    
    # Connect to Vault
    client = hvac.Client(url='http://127.0.0.1:8200', token='root')
    
    if not client.is_authenticated():
        print("❌ Cannot authenticate with Vault")
        return False
        
    print("✅ Connected to Vault!")
    
    # Enable transit engine
    try:
        client.sys.enable_secrets_engine(backend_type='transit', path='transit')
        print("✅ Transit engine enabled")
    except Exception:
        print("ℹ️ Transit engine already enabled")
    
    # Create a key
    try:
        client.secrets.transit.create_key(name='demo-key', type='aes256-gcm96')
        print("✅ Created encryption key: 'demo-key'")
    except Exception:
        print("ℹ️ Key already exists")
    
    # DEMO 1: Basic Encryption
    print("\n1. 🔐 BASIC ENCRYPTION")
    print("-" * 30)
    
    secret_data = "My confidential data: Password123!"
    print(f"   Original: {secret_data}")
    
    # Encrypt
    encrypted = client.secrets.transit.encrypt_data(
        name='demo-key',
        plaintext=base64.b64encode(secret_data.encode()).decode()
    )
    ciphertext = encrypted['data']['ciphertext']
    print(f"   Encrypted: {ciphertext[:60]}...")
    
    # DEMO 2: Basic Decryption
    print("\n2. 🔓 BASIC DECRYPTION")
    print("-" * 30)
    
    decrypted = client.secrets.transit.decrypt_data(
        name='demo-key',
        ciphertext=ciphertext
    )
    decrypted_data = base64.b64decode(decrypted['data']['plaintext']).decode()
    print(f"   Decrypted: {decrypted_data}")
    
    # Verify
    if secret_data == decrypted_data:
        print("   ✅ Encryption/Decryption successful!")
    else:
        print("   ❌ Encryption/Decryption failed!")
        return False
    
    # DEMO 3: Key Rotation
    print("\n3. 🔄 KEY ROTATION")
    print("-" * 30)
    
    client.secrets.transit.rotate_key(name='demo-key')
    print("   ✅ Key rotated to new version")
    
    # Show backward compatibility
    still_decrypts = client.secrets.transit.decrypt_data(
        name='demo-key',
        ciphertext=ciphertext
    )
    still_works = base64.b64decode(still_decrypts['data']['plaintext']).decode()
    
    if still_works == secret_data:
        print("   ✅ Backward compatibility maintained")
    else:
        print("   ❌ Backward compatibility broken!")
    
    return True

def main():
    print("🔐 WELCOME TO MULTI-CLOUD KMS LEARNING LAB")
    print("==========================================")
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix the requirements above and try again.")
        return
    
    # Start Vault
    if not start_vault():
        return
    
    # Run the demo
    if run_kms_demo():
        print("\n" + "=" * 50)
        print("🎉 CONGRATULATIONS! You've completed:")
        print("   ✓ Key Management System fundamentals")
        print("   ✓ Data encryption and decryption") 
        print("   ✓ Key rotation concepts")
        print("   ✓ HashiCorp Vault basics")
        print("\n🚀 Ready for the next level: Cloud KMS integration!")
    else:
        print("\n❌ Demo failed. Please check the errors above.")

if __name__ == "__main__":
    main()
