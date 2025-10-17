#!/bin/bash
# Download a sample image to test GroundingDINO

echo "🖼️  Downloading sample image..."

cd /Users/nestor/armando_new/GroundingDINO

# Download a public domain image
curl -L "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/800px-Cat03.jpg" \
  -o sample_cat.jpg

if [ $? -eq 0 ]; then
    echo "✅ Sample image downloaded: sample_cat.jpg"
    echo ""
    echo "Now run:"
    echo "  source .venv/bin/activate"
    echo "  python run_model.py -i sample_cat.jpg -t 'cat'"
else
    echo "❌ Failed to download. You can use any .jpg/.png image on your computer instead."
    echo ""
    echo "Run with full path:"
    echo "  python run_model.py -i /full/path/to/your/image.jpg -t 'objects to detect'"
fi

