#!/bin/bash

# Exit on error
set -e

# Check if image name and tag are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <image_name> <image_tag>"
    exit 1
fi

# Read parameters
IMAGE_NAME=$1
IMAGE_TAG=$2

# Read config file
CONFIG_FILE="config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

# Parse config file
ACR_NAME=$(jq -r '.acrName' "$CONFIG_FILE")
ACR_URL=$(jq -r '.acrUrl' "$CONFIG_FILE")
RESOURCE_GROUP=$(jq -r '.resourceGroup' "$CONFIG_FILE")
CONTAINER_APP_NAME=$(jq -r '.containerAppName' "$CONFIG_FILE")

# Check for required tools
for cmd in docker az jq; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed."
        exit 1
    fi
done

# Check if already logged into Azure
if az account show > /dev/null 2>&1; then
    echo "Already logged into Azure."
else
    echo "Not logged into Azure. Logging in..."
    az login
fi

# Enable ACR admin credentials (if not already enabled)
echo "Enabling ACR admin credentials..."
az acr update -n $ACR_NAME --admin-enabled true > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to enable ACR admin credentials."
    exit 1
fi

# Retrieve ACR credentials
echo "Retrieving ACR credentials..."
ACR_USERNAME=$(az acr credential show -n $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR_NAME --query "passwords[0].value" -o tsv)

# Login to ACR
echo "Logging in to Azure Container Registry..."
echo "$ACR_PASSWORD" | docker login $ACR_URL -u $ACR_USERNAME --password-stdin
if [ $? -ne 0 ]; then
    echo "Failed to log in to Azure Container Registry."
    exit 1
fi

# Build the image
echo "Building Docker image..."
docker build -t $ACR_URL/$IMAGE_NAME:$IMAGE_TAG .

# Push the image to ACR
echo "Pushing Docker image to ACR..."
docker push $ACR_URL/$IMAGE_NAME:$IMAGE_TAG

# Update the Azure Container App with the new image
echo "Updating Azure Container App..."
az containerapp update \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --image $ACR_URL/$IMAGE_NAME:$IMAGE_TAG > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to update Azure Container App."
    exit 1
fi

echo "Azure Container App updated successfully."

# Clean up ACR image locally
echo "Removing local ACR image..."
docker rmi $ACR_URL/$IMAGE_NAME:$IMAGE_TAG || echo "Warning: Failed to remove local ACR image."