# 🖼️ How to Use Your Own Images with GroundingDINO

## ✅ **It Works!** 
The model just successfully detected a cat with 94.9% confidence!

---

## 🚀 Using Your Own Images

### Method 1: Use Full Absolute Path (Recommended)
```bash
# Activate environment
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# Run with FULL path to your image
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /Users/nestor/path/to/your/image.jpg \
  -t "person . car . dog ."
```

### Method 2: Copy Image to GroundingDINO Directory
```bash
# Copy your image to the GroundingDINO folder
cp /path/to/your/image.jpg /Users/nestor/armando_new/GroundingDINO/

# Then run with just the filename
cd /Users/nestor/armando_new/GroundingDINO
source .venv/bin/activate
python run_model.py -i image.jpg -t "objects to detect"
```

### Method 3: Navigate to Image Directory
```bash
# Go to where your image is
cd /Users/nestor/Documents/Photos  # or wherever your image is

# Activate environment
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# Run with relative path
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i my_photo.jpg \
  -t "person . car ."
```

---

## 📋 Quick Examples

### Example 1: Detect People in a Photo
```bash
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /Users/nestor/Desktop/photo.jpg \
  -t "person"
```

### Example 2: Detect Multiple Objects
```bash
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /Users/nestor/Downloads/street.jpg \
  -t "person . car . bicycle . traffic light ."
```

### Example 3: Using the Sample Cat Image
```bash
cd /Users/nestor/armando_new/GroundingDINO
source .venv/bin/activate
python run_model.py -i sample_cat.jpg -t "cat"
```

---

## 🎯 Adjust for Better Results

### More Detections (Lower Threshold)
```bash
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /path/to/image.jpg \
  -t "person" \
  --box-threshold 0.25
```

### Fewer False Positives (Higher Threshold)
```bash
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /path/to/image.jpg \
  -t "person" \
  --box-threshold 0.45
```

### Save Results as JSON
```bash
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /path/to/image.jpg \
  -t "cat . dog ." \
  --save-json
```

---

## 📊 Where Are the Results?

Results are saved in the `outputs/` directory:
- **Image:** `outputs/annotated_result.jpg` (with bounding boxes)
- **JSON:** `outputs/results.json` (if you used `--save-json`)

View the result:
```bash
open outputs/annotated_result.jpg
```

---

## 💡 Pro Tips

1. **Always use full paths** for images outside the GroundingDINO folder
2. **Use periods** to separate objects: `"cat . dog . bird ."`
3. **Be specific:** `"tabby cat"` works better than `"animal"`
4. **Start with default thresholds** (0.35), then adjust
5. **First detection is slow** (~10-15 seconds), then faster

---

## 🐛 Common Issues

### Issue: "Image not found: test.jpg"
**Solution:** Use the full path to your image:
```bash
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /Users/nestor/Desktop/test.jpg \
  -t "objects"
```

### Issue: "Module not found"
**Solution:** Activate the virtual environment:
```bash
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
```

### Issue: No detections found
**Solution:** Lower the box threshold:
```bash
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i image.jpg \
  -t "object" \
  --box-threshold 0.2
```

---

## 📚 For More Help

- **Detailed tuning:** Read `TUNING_GUIDE.md`
- **Complete guide:** Read `README.md`
- **Installation info:** Read `INSTALLATION_COMPLETE.md`

---

## ✨ Quick Command Template

Copy and customize this:
```bash
# 1. Activate
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# 2. Run (change the path and objects!)
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i /FULL/PATH/TO/YOUR/IMAGE.jpg \
  -t "objects you want to detect ."

# 3. View results
open outputs/annotated_result.jpg
```

---

**Happy Detecting! 🦕**

