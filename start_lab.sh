#!/bin/bash

# Set the environment variables
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

echo "🔐 Multi-Cloud KMS Lab Starter"
echo "==============================="

# Check if Vault is running
if vault status > /dev/null 2>&1; then
    echo "✅ Vault is already running"
else
    echo "🚀 Starting Vault server..."
    # Start Vault in background
    vault server -dev -dev-root-token-id=root -dev-listen-address=127.0.0.1:8200 > vault.log 2>&1 &
    
    # Wait for startup
    sleep 3
    
    # Check if started successfully
    if vault status > /dev/null 2>&1; then
        echo "✅ Vault started successfully"
    else
        echo "❌ Failed to start Vault. Check vault.log for details."
        exit 1
    fi
fi

echo ""
echo "🎯 Running KMS Demo..."
python3 kms_demo_final.py
