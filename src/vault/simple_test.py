#!/usr/bin/env python3
print("🎉 Python is working!")
print("Testing basic imports...")

try:
    import hvac
    print("✅ hvac (Vault client) imported successfully")
except ImportError as e:
    print(f"❌ hvac import failed: {e}")

try:
    import boto3
    print("✅ boto3 (AWS) imported successfully") 
except ImportError as e:
    print(f"❌ boto3 import failed: {e}")

try:
    import cryptography
    print("✅ cryptography imported successfully")
except ImportError as e:
    print(f"❌ cryptography import failed: {e}")

print("\n🎯 Next: We'll start Vault and run the KMS demo!")
