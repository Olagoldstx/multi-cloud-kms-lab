#!/usr/bin/env python3
import boto3
import base64
import os

print("🔐 AWS KMS INTEGRATION")
print("=" * 40)

def setup_aws_kms():
    """Set up and demonstrate AWS KMS"""
    try:
        # Initialize AWS KMS client
        kms_client = boto3.client('kms', region_name='us-east-1')
        print("✅ AWS KMS client initialized")
        
        # Create a KMS key
        response = kms_client.create_key(
            Description='Multi-Cloud KMS Lab Key',
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS'
        )
        
        key_id = response['KeyMetadata']['KeyId']
        print(f"✅ AWS KMS Key Created: {key_id}")
        
        # Encrypt data
        plaintext = "Secret data for AWS KMS"
        encrypt_response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext.encode()
        )
        ciphertext = base64.b64encode(encrypt_response['CiphertextBlob']).decode()
        print(f"🔒 Encrypted with AWS KMS: {ciphertext[:50]}...")
        
        # Decrypt data
        decrypt_response = kms_client.decrypt(
            CiphertextBlob=base64.b64decode(ciphertext)
        )
        decrypted = decrypt_response['Plaintext'].decode()
        print(f"🔓 Decrypted with AWS KMS: {decrypted}")
        
        # Verify
        if plaintext == decrypted:
            print("✅ AWS KMS encryption/decryption successful!")
        else:
            print("❌ AWS KMS failed!")
            
        return key_id
        
    except Exception as e:
        print(f"❌ AWS KMS setup failed: {e}")
        return None

if __name__ == "__main__":
    setup_aws_kms()
