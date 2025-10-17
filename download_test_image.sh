#!/bin/bash
# Download a test image to try the model

echo "🖼️  Downloading test image..."
mkdir -p /Users/nestor/armando_new/GroundingDINO/test_images

# Download a sample image from the internet (free to use)
curl -L "https://images.unsplash.com/photo-1560807707-8cc77767d783?w=800" \
  -o /Users/nestor/armando_new/GroundingDINO/test_images/test_image.jpg

if [ $? -eq 0 ]; then
    echo "✅ Test image downloaded to: test_images/test_image.jpg"
    echo ""
    echo "Try running:"
    echo "  python run_model.py -i test_images/test_image.jpg -t 'person . dog .'"
else
    echo "❌ Failed to download image. Please provide your own image."
fi

