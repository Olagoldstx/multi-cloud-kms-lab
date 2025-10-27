#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def setup_environment():
    """Set up the proper environment for Vault"""
    print("🔧 Setting up environment...")
    
    # Set Vault address to HTTP for development
    os.environ['VAULT_ADDR'] = 'http://127.0.0.1:8200'
    os.environ['VAULT_TOKEN'] = 'root'
    
    print("✅ Set VAULT_ADDR=http://127.0.0.1:8200")
    print("✅ Set VAULT_TOKEN=root")

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

def check_vault_status():
    """Check if Vault is running and accessible"""
    print("🔍 Checking Vault status...")
    
    # Make sure environment is set
    os.environ['VAULT_ADDR'] = 'http://127.0.0.1:8200'
    
    result = run_command("vault status", check=False)
    
    if result and result.returncode == 0:
        print("✅ Vault is running and accessible")
        return True
    elif result and result.returncode == 2:
        print("ℹ️ Vault is not running")
        return False
    else:
        print(f"❓ Vault status check failed: {result.stderr if result else 'Unknown error'}")
        return False

def start_vault():
    """Start Vault development server"""
    print("\n🚀 Starting Vault server...")
    
    # Kill any existing Vault processes
    print("🔄 Cleaning up any existing Vault processes...")
    run_command("pkill -f 'vault server'", check=False)
    time.sleep(2)
    
    # Start Vault in development mode
    print("📝 Starting Vault development server on http://127.0.0.1:8200...")
    
    try:
        # Start Vault in the background
        vault_process = subprocess.Popen([
            "vault", "server", "-dev", "-dev-root-token-id=root",
            "-dev-listen-address=127.0.0.1:8200"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for Vault to start
        time.sleep(3)
        
        # Check if process is still running
        if vault_process.poll() is not None:
            stdout, stderr = vault_process.communicate()
            print(f"❌ Vault process ended:")
            print(f"   stdout: {stdout.decode() if stdout else 'None'}")
            print(f"   stderr: {stderr.decode() if stderr else 'None'}")
            return False
        
        # Check if Vault is accessible
        if check_vault_status():
            print("✅ Vault server started successfully!")
            return True
        else:
            print("❌ Vault started but not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start Vault: {e}")
        return False

def run_kms_demo():
    """Run the main KMS demonstration"""
    print("\n🎓 KMS LEARNING LAB - CORE CONCEPTS")
    print("=" * 50)
    
    import hvac
    import base64
    
    # Connect to Vault with explicit settings
    print("🔗 Connecting to Vault...")
    client = hvac.Client(url='http://127.0.0.1:8200', token='root')
    
    try:
        if not client.is_authenticated():
            print("❌ Cannot authenticate with Vault")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
        
    print("✅ Connected to Vault!")
    
    # Enable transit engine
    try:
        client.sys.enable_secrets_engine(backend_type='transit', path='transit')
        print("✅ Transit engine enabled")
    except Exception as e:
        if "path is already in use" in str(e):
            print("ℹ️ Transit engine already enabled")
        else:
            print(f"❌ Failed to enable transit engine: {e}")
            return False
    
    # Create a key - COMPATIBLE VERSION
    print("🔑 Creating encryption key...")
    try:
        # Try the newer API first
        try:
            # For newer HVAC versions
            create_response = client.secrets.transit.create_key(
                name='demo-key',
                key_type='aes256-gcm96',
                exportable=True,
                allow_plaintext_backup=True
            )
            print("✅ Created encryption key: 'demo-key' (new API)")
        except TypeError:
            # Fallback to older API
            create_response = client.secrets.transit.create_key(
                name='demo-key'
            )
            print("✅ Created encryption key: 'demo-key' (legacy API)")
            
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ Key already exists")
        else:
            print(f"❌ Failed to create key: {e}")
            return False
    
    # DEMO 1: Basic Encryption
    print("\n1. 🔐 BASIC ENCRYPTION")
    print("-" * 30)
    
    secret_data = "My confidential data: Password123!"
    print(f"   Original: {secret_data}")
    
    try:
        # Encrypt
        encrypted = client.secrets.transit.encrypt_data(
            name='demo-key',
            plaintext=base64.b64encode(secret_data.encode()).decode()
        )
        ciphertext = encrypted['data']['ciphertext']
        print(f"   Encrypted: {ciphertext}")
    except Exception as e:
        print(f"❌ Encryption failed: {e}")
        return False
    
    # DEMO 2: Basic Decryption
    print("\n2. 🔓 BASIC DECRYPTION")
    print("-" * 30)
    
    try:
        decrypted = client.secrets.transit.decrypt_data(
            name='demo-key',
            ciphertext=ciphertext
        )
        decrypted_data = base64.b64decode(decrypted['data']['plaintext']).decode()
        print(f"   Decrypted: {decrypted_data}")
    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        return False
    
    # Verify
    if secret_data == decrypted_data:
        print("   ✅ Encryption/Decryption successful!")
    else:
        print("   ❌ Encryption/Decryption failed!")
        return False
    
    # DEMO 3: Key Rotation
    print("\n3. 🔄 KEY ROTATION")
    print("-" * 30)
    
    try:
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
            
    except Exception as e:
        print(f"❌ Key rotation failed: {e}")
        return False
    
    # DEMO 4: List keys to show what we created
    print("\n4. 📋 KEY MANAGEMENT")
    print("-" * 30)
    try:
        keys = client.secrets.transit.list_keys()
        if keys and 'data' in keys and 'keys' in keys['data']:
            print(f"   Available keys: {', '.join(keys['data']['keys'])}")
        else:
            print("   No keys found or unable to list keys")
    except Exception as e:
        print(f"   ℹ️ Could not list keys: {e}")
    
    return True

def main():
    print("🔐 WELCOME TO MULTI-CLOUD KMS LEARNING LAB")
    print("==========================================")
    
    # Setup environment first
    setup_environment()
    
    # Check Vault status
    if not check_vault_status():
        print("\n🔄 Vault not running. Starting now...")
        if not start_vault():
            print("\n❌ Could not start Vault.")
            print("💡 Try running this command manually in another terminal:")
            print("   vault server -dev -dev-root-token-id=root -dev-listen-address=127.0.0.1:8200")
            print("\nThen run this script again.")
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
