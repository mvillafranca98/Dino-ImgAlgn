#!/bin/bash
# Batch process multiple images with GroundingDINO
# Usage: ./batch_detect.sh "input_folder" "text_prompt"

if [ $# -lt 2 ]; then
    echo "Usage: ./batch_detect.sh INPUT_FOLDER 'text prompt'"
    echo ""
    echo "Example:"
    echo "  ./batch_detect.sh my_images 'person . car . dog .'"
    exit 1
fi

INPUT_FOLDER="$1"
TEXT_PROMPT="$2"
OUTPUT_BASE="batch_outputs"

# Check if input folder exists
if [ ! -d "$INPUT_FOLDER" ]; then
    echo "❌ Error: Folder '$INPUT_FOLDER' does not exist"
    exit 1
fi

# Activate virtual environment
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

echo "🦕 Batch Processing with GroundingDINO"
echo "======================================="
echo "Input folder: $INPUT_FOLDER"
echo "Text prompt: $TEXT_PROMPT"
echo "Output folder: $OUTPUT_BASE"
echo ""

# Count images
IMAGE_COUNT=$(find "$INPUT_FOLDER" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l | tr -d ' ')
echo "Found $IMAGE_COUNT images to process"
echo ""

# Process each image
COUNTER=0
for img in "$INPUT_FOLDER"/*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
    # Skip if no files match
    [ -e "$img" ] || continue
    
    COUNTER=$((COUNTER + 1))
    BASENAME=$(basename "$img" | sed 's/\.[^.]*$//')
    OUTPUT_DIR="$OUTPUT_BASE/$BASENAME"
    
    echo "[$COUNTER/$IMAGE_COUNT] Processing: $img"
    
    python /Users/nestor/armando_new/GroundingDINO/run_model.py \
        -i "$img" \
        -t "$TEXT_PROMPT" \
        -o "$OUTPUT_DIR" \
        --save-json
    
    if [ $? -eq 0 ]; then
        echo "  ✅ Success! Output saved to: $OUTPUT_DIR"
    else
        echo "  ❌ Failed to process $img"
    fi
    echo ""
done

echo "======================================="
echo "🎉 Batch processing complete!"
echo "Processed $COUNTER images"
echo "Results saved to: $OUTPUT_BASE/"
echo ""
echo "To view results:"
echo "  open $OUTPUT_BASE/*/annotated_result.jpg"

