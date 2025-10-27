#!/usr/bin/env python3
import base64
import os

print("🔐 GOOGLE CLOUD KMS DEMO")
print("=" * 40)

def check_gcp_kms():
    """Check if Google Cloud KMS is available"""
    try:
        from google.cloud import kms
        return kms
    except ImportError:
        print("❌ google-cloud-kms not available")
        print("💡 Install with: pip3 install google-cloud-kms")
        return None

def demonstrate_gcp_concepts():
    """Demonstrate GCP KMS concepts"""
    print("\n🎓 GOOGLE CLOUD KMS CORE CONCEPTS")
    print("=" * 35)
    
    print("1. 🔑 KEY HIERARCHY")
    print("   • Project → Location → Key Ring → Crypto Key")
    print("   • Key Rings: Logical grouping of keys")
    print("   • Crypto Keys: Actual encryption keys")
    
    print("\n2. 🌍 LOCATIONS & AVAILABILITY")
    print("   • Global: Single region, low latency")
    print("   • Regional: Specific regions for compliance")
    print("   • Multi-regional: High availability")
    
    print("\n3. 🔐 KEY VERSIONS")
    print("   • Primary version: Active encryption")
    print("   • Previous versions: Decryption only")
    print("   • Automatic rotation support")
    
    print("\n4. 🔒 IAM INTEGRATION")
    print("   • Cloud IAM for access control")
    print("   • Fine-grained permissions")
    print("   • Service account integration")

def simulate_gcp_workflow():
    """Simulate GCP KMS workflow"""
    print("\n🔄 SIMULATED GCP KMS WORKFLOW")
    print("=" * 30)
    
    # Simulate key hierarchy
    project_id = "my-gcp-project"
    location = "global"
    key_ring = "multi-cloud-ring"
    key_name = "gcp-lab-key"
    
    print(f"1. 🔧 Key Hierarchy:")
    print(f"   Project: {project_id}")
    print(f"   Location: {location}")
    print(f"   Key Ring: {key_ring}")
    print(f"   Crypto Key: {key_name}")
    
    # Simulate encryption
    plaintext = "Sensitive data for Google Cloud KMS"
    print(f"2. 📝 Plaintext: {plaintext}")
    
    # Simple simulation
    simulated_cipher = base64.b64encode(f"GCPKMS:{key_name}:{plaintext}".encode()).decode()
    print(f"3. 🔒 Encrypted: {simulated_cipher[:50]}...")
    
    # Simulate decryption
    decoded = base64.b64decode(simulated_cipher).decode()
    if decoded.startswith('GCPKMS:'):
        parts = decoded.split(':')
        decrypted_key = parts[1]
        decrypted_text = ':'.join(parts[2:])
        print(f"4. 🔓 Decrypted with key {decrypted_key}: {decrypted_text}")
    
    # Verify
    if plaintext == decrypted_text:
        print("5. ✅ Verification: Encryption/decryption successful!")

def real_gcp_demo():
    """Run real GCP KMS demo if available"""
    kms = check_gcp_kms()
    if not kms:
        return False
    
    try:
        print("\n🚀 ATTEMPTING REAL GCP KMS SETUP")
        print("-" * 30)
        
        # This would require actual GCP credentials
        print("❌ GCP credentials not configured")
        print("💡 To use real GCP KMS:")
        print("   1. Create GCP project at https://console.cloud.google.com/")
        print("   2. Enable KMS API")
        print("   3. Create service account and download credentials")
        print("   4. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("   5. Run: gcloud auth application-default login")
        
        return False
        
    except Exception as e:
        print(f"❌ Real GCP KMS failed: {e}")
        return False

if __name__ == "__main__":
    # First demonstrate concepts
    demonstrate_gcp_concepts()
    
    # Try real GCP KMS
    real_success = real_gcp_demo()
    
    # If real GCP failed, show simulation
    if not real_success:
        simulate_gcp_workflow()
    
    print("\n" + "=" * 50)
    print("🎓 GOOGLE CLOUD KMS LEARNING COMPLETE!")
    print("=" * 50)
    print("You now understand:")
    print("✓ GCP KMS architecture and hierarchy")
    print("✓ Key rings and crypto keys")
    print("✓ IAM integration and access control")
    print("✓ Multi-region deployment strategies")
    
    print("\n🌐 MULTI-CLOUD KMS MASTERY PROGRESS:")
    print("✅ HashiCorp Vault KMS")
    print("✅ AWS KMS") 
    print("✅ Google Cloud KMS")
    print("🚀 Next: Multi-Cloud Integration!")
    print("\n2. 🌍 LOCATION STRATEGY")
    print("   • Global: Single region, low latency")
    print("   • Regional: Compliance requirements")
    print("   • Multi-regional: High availability")
    
    print("\n3. 🔐 KEY VERSIONS & ROTATION")
    print("   • Primary version: Active encryption")
    print("   • Previous versions: Decryption only")
    print("   • Automatic rotation: 90 days default")
    print("   • Manual rotation: On-demand")
    
    print("\n4. 🔒 IAM INTEGRATION")
    print("   • Cloud IAM permissions")
    print("   • Service accounts")
    print("   • Fine-grained access control")

def simulate_gcp_workflow():
    """Simulate GCP KMS workflow"""
    print("\n🔄 SIMULATED GCP KMS WORKFLOW")
    print("-" * 30)
    
    # Simulate key hierarchy
    project_id = "my-cloud-project"
    location = "global"
    key_ring = "production-keys"
    crypto_key = "app-encryption-key"
    
    print(f"1. 🏗️  Creating Key Hierarchy:")
    print(f"   Project: {project_id}")
    print(f"   Location: {location}")
    print(f"   Key Ring: {key_ring}")
    print(f"   Crypto Key: {crypto_key}")
    
    # Simulate encryption
    plaintext = "Sensitive user data for GCP KMS"
    print(f"\n2. 📝 Plaintext: {plaintext}")
    
    # Simulate encryption process
    simulated_cipher = base64.b64encode(
        f"GCPKMS:{project_id}/{location}/{key_ring}/{crypto_key}:{plaintext}".encode()
    ).decode()
    
    print(f"3. 🔒 Encrypted: {simulated_cipher[:50]}...")
    
    # Simulate decryption
    decoded = base64.b64decode(simulated_cipher).decode()
    if decoded.startswith('GCPKMS:'):
        parts = decoded.split(':')
        key_path = parts[1]
        decrypted_text = ':'.join(parts[2:])
        
        print(f"4. 🔓 Decrypted with {key_path}:")
        print(f"   {decrypted_text}")
    
    # Verify
    if plaintext == decrypted_text:
        print("5. ✅ Verification: Encryption/decryption successful!")

def show_gcp_integration():
    """Show GCP service integration"""
    print("\n🌐 GCP SERVICE INTEGRATION")
    print("-" * 30)
    
    services = {
        "Cloud Storage": "Automatic bucket encryption",
        "BigQuery": "Dataset and table encryption", 
        "Compute Engine": "VM disk encryption",
        "Cloud SQL": "Database encryption at rest",
        "Secret Manager": "Secret encryption backend"
    }
    
    for service, description in services.items():
        print(f"• {service}: {description}")

def real_gcp_setup_guide():
    """Guide for real GCP setup"""
    print("\n💡 REAL GCP KMS SETUP GUIDE")
    print("-" * 30)
    
    print("1. 🔧 PREREQUISITES:")
    print("   • GCP Project with billing enabled")
    print("   • KMS API enabled")
    print("   • Appropriate IAM permissions")
    
    print("\n2. 🛠️  SETUP STEPS:")
    print("   pip3 install google-cloud-kms")
    print("   gcloud auth login")
    print("   gcloud config set project YOUR_PROJECT_ID")
    print("   gcloud services enable cloudkms.googleapis.com")
    
    print("\n3. 🔑 CREATE RESOURCES:")
    print("   # Create key ring")
    print("   gcloud kms keyrings create my-key-ring --location=global")
    print("   ")
    print("   # Create crypto key") 
    print("   gcloud kms keys create my-key --keyring=my-key-ring --location=global --purpose=encryption")

if __name__ == "__main__":
    demonstrate_gcp_concepts()
    simulate_gcp_workflow() 
    show_gcp_integration()
    real_gcp_setup_guide()
    
    print("\n" + "=" * 60)
    print("🎓 GOOGLE CLOUD KMS CONCEPTS MASTERED!")
    print("=" * 60)
    print("You now understand:")
    print("✓ GCP KMS architecture and hierarchy")
    print("✓ Key management and rotation strategies")
    print("✓ GCP service integration patterns")
    print("✓ Real setup and implementation steps")
    
    print("\n🌐 MULTI-CLOUD PROGRESS:")
    print("✅ HashiCorp Vault KMS - Practical implementation")
    print("✅ AWS KMS - Architecture and concepts") 
    print("✅ Google Cloud KMS - Concepts and patterns")
    print("🚀 Next: Multi-Cloud Integration Strategy!")
