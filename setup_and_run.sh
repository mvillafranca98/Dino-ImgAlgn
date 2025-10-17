#!/bin/bash
# GroundingDINO Setup and Installation Script
# This script will set up everything needed to run the model

set -e  # Exit on error

echo "🦕 GroundingDINO Setup Script"
echo "=============================="

# Navigate to the repo directory
cd /Users/nestor/armando_new/GroundingDINO/repo

# Step 1: Check Python version
echo ""
echo "Step 1: Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Step 2: Create virtual environment if it doesn't exist
VENV_PATH="/Users/nestor/armando_new/GroundingDINO/.venv"
if [ ! -d "$VENV_PATH" ]; then
    echo ""
    echo "Step 2: Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
else
    echo ""
    echo "Step 2: Virtual environment already exists, skipping..."
fi

# Step 3: Activate virtual environment
echo ""
echo "Step 3: Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Step 4: Upgrade pip
echo ""
echo "Step 4: Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Step 5: Install PyTorch (CPU version for macOS)
echo ""
echo "Step 5: Installing PyTorch..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Step 6: Install the package
echo ""
echo "Step 6: Installing GroundingDINO..."
pip install -e .

# Step 7: Download pretrained weights
echo ""
echo "Step 7: Downloading pretrained weights..."
mkdir -p weights
if [ ! -f "weights/groundingdino_swint_ogc.pth" ]; then
    echo "Downloading GroundingDINO-T checkpoint..."
    curl -L -o weights/groundingdino_swint_ogc.pth \
      https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
    echo "✅ Checkpoint downloaded successfully!"
else
    echo "Checkpoint already exists, skipping download..."
fi

# Step 8: Download sample image if needed
echo ""
echo "Step 8: Checking for sample images..."
if [ ! -d ".asset" ] || [ ! -f ".asset/cat_dog.jpeg" ]; then
    echo "Sample images not found. You'll need to provide your own images."
else
    echo "Sample images found!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment and run the model:"
echo "  source $VENV_PATH/bin/activate"
echo "  cd /Users/nestor/armando_new/GroundingDINO/repo"
echo ""
echo "Quick test command:"
echo "  python demo/inference_on_a_image.py \\"
echo "    -c groundingdino/config/GroundingDINO_SwinT_OGC.py \\"
echo "    -p weights/groundingdino_swint_ogc.pth \\"
echo "    -i YOUR_IMAGE.jpg \\"
echo "    -o outputs \\"
echo "    -t 'objects you want to detect' \\"
echo "    --cpu-only"

