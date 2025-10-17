# 🚀 START HERE - GroundingDINO Quick Setup

## ⚡ 3-Step Quick Start

```bash
# Step 1: Setup (one-time only)
cd /Users/nestor/armando_new/GroundingDINO
./setup_and_run.sh

# Step 2: Activate environment (every time)
source .venv/bin/activate

# Step 3: Run detection
python run_model.py -i YOUR_IMAGE.jpg -t "person . car . dog ."
```

---

## 📚 Complete Guide Structure

| File | Purpose | When to Read |
|------|---------|--------------|
| **START_HERE.md** (this file) | Quick overview | Read first |
| **README.md** | Complete guide | After setup |
| **TUNING_GUIDE.md** | Improve accuracy | When results aren't good |
| **SETUP_COMPLETE.txt** | Reference sheet | Quick command lookup |

---

## 🎯 What You Can Do

GroundingDINO detects objects in images using **text descriptions**. You describe what you want to find, and it finds it!

**Examples:**
- "Find all people and cars" → Detects people and cars
- "Detect a cat on a couch" → Finds cats on couches
- "red car . blue bicycle ." → Finds red cars and blue bicycles

**No training needed** - just describe what you want to detect!

---

## 📖 Documentation Overview

### 1. **Setup (10 minutes)**
Run `./setup_and_run.sh` - it will:
- Create a Python virtual environment
- Install all required packages
- Download pretrained model (~700MB)

### 2. **Basic Usage**
```bash
# Simple detection
python run_model.py -i photo.jpg -t "person"

# Multiple objects (separate with periods!)
python run_model.py -i photo.jpg -t "person . car . dog ."

# Save results as JSON
python run_model.py -i photo.jpg -t "cat" --save-json
```

### 3. **Tuning for Better Results**
See `TUNING_GUIDE.md` for detailed instructions. Quick tips:

**Missing detections?**
```bash
python run_model.py -i photo.jpg -t "person" --box-threshold 0.25
```

**Too many false positives?**
```bash
python run_model.py -i photo.jpg -t "person" --box-threshold 0.45
```

**Wrong labels?**
```bash
python run_model.py -i photo.jpg -t "cat" --text-threshold 0.15
```

---

## 🎨 Example Prompts

✅ **Good Prompts:**
- `"person . car . bicycle ."`
- `"a cat sitting on a couch ."`
- `"red apple . green banana ."`
- `"golden retriever dog . tabby cat ."`

❌ **Bad Prompts:**
- `"person car bicycle"` (missing periods)
- `"PERSON"` (uppercase)
- `"things in the image"` (too vague)
- `"stuff"` (not specific)

**Rule of thumb:** Be specific, use lowercase, separate with periods!

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| No detections | Lower `--box-threshold` to 0.25 or 0.2 |
| Too many false positives | Raise `--box-threshold` to 0.45 or 0.5 |
| Wrong labels | Adjust `--text-threshold` to 0.15 or 0.2 |
| Import errors | `source .venv/bin/activate` then `cd repo && pip install -e .` |
| Model not found | Run `./setup_and_run.sh` again |

---

## 📦 What's Installed

After running setup:
- **PyTorch** - Deep learning framework
- **GroundingDINO** - The detection model
- **Transformers** - BERT text encoder
- **OpenCV** - Image processing
- **Model weights** - Pretrained checkpoint (~700MB)

Total size: ~2-3 GB

---

## 🌟 Common Use Cases

### 1. **Detect Specific Objects**
```bash
python run_model.py -i street.jpg -t "person . car . bicycle . traffic light ."
```

### 2. **Find Objects by Description**
```bash
python run_model.py -i living_room.jpg -t "a red couch . a wooden table . a lamp ."
```

### 3. **Batch Process Multiple Images**
```bash
./batch_detect.sh my_photos "person . dog . cat ."
```

### 4. **Save Results for Analysis**
```bash
python run_model.py -i photo.jpg -t "person" --save-json
cat outputs/results.json
```

---

## 🎓 Learning Path

### Day 1: Setup & Basic Usage
1. Run `./setup_and_run.sh`
2. Try detecting simple objects: `python run_model.py -i image.jpg -t "person"`
3. Experiment with different prompts

### Day 2: Tuning & Optimization
1. Read `TUNING_GUIDE.md`
2. Learn about `--box-threshold` and `--text-threshold`
3. Practice writing better prompts

### Day 3: Advanced Features
1. Try batch processing with `batch_detect.sh`
2. Explore the Jupyter notebooks in `repo/demo/`
3. Try the Gradio web UI

---

## 💡 Pro Tips

1. **Always activate the virtual environment first!**
   ```bash
   source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
   ```

2. **Start with default settings, then tune based on results**

3. **Use specific descriptions:** "golden retriever" beats "dog"

4. **Separate objects with periods:** "cat . dog . bird ."

5. **Use `--save-json` to compare different configurations**

6. **Lower thresholds = more detections** (but more false positives)

7. **Higher thresholds = fewer detections** (but higher confidence)

---

## 📊 Parameter Quick Reference

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--box-threshold` | 0.35 | 0.0-1.0 | Minimum detection confidence |
| `--text-threshold` | 0.25 | 0.0-1.0 | Text matching strength |

**Lower box-threshold (0.2-0.3):**
- ✅ Catches more objects
- ❌ More false positives

**Higher box-threshold (0.4-0.5):**
- ✅ Only high confidence
- ❌ Might miss objects

**Lower text-threshold (0.15-0.2):**
- ✅ More flexible matching
- ❌ Less precise labels

**Higher text-threshold (0.3-0.35):**
- ✅ More precise labels
- ❌ Stricter matching

---

## 🎬 Video Tutorial (Step-by-Step)

```bash
# 1. Navigate to the folder
cd /Users/nestor/armando_new/GroundingDINO

# 2. Run setup (wait ~5-10 minutes for downloads)
./setup_and_run.sh

# 3. Activate environment
source .venv/bin/activate

# 4. (Optional) Download a test image
./download_test_image.sh

# 5. Run detection
python run_model.py -i test_images/test_image.jpg -t "person . dog ."

# 6. Check results
open outputs/annotated_result.jpg

# 7. Try different thresholds
python run_model.py -i test_images/test_image.jpg -t "person . dog ." \
  --box-threshold 0.25 -o outputs2

# 8. Compare results
open outputs2/annotated_result.jpg
```

---

## 🚨 Important Notes

1. **Virtual Environment:** Always activate before running!
   ```bash
   source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
   ```

2. **CPU Mode:** By default runs on CPU (fine for macOS)

3. **First Run:** Will be slower (model loading), subsequent runs faster

4. **Prompts:** Always use lowercase and periods!

5. **Thresholds:** Start with defaults (0.35, 0.25) then adjust

---

## 📞 Need Help?

**Quick Fixes:** See troubleshooting table above

**Accuracy Issues:** Read `TUNING_GUIDE.md` (comprehensive guide)

**General Usage:** Read `README.md` (complete documentation)

**Advanced Features:** Check `repo/README.md` (original docs)

**GitHub Issues:** https://github.com/IDEA-Research/GroundingDINO/issues

---

## ✅ Next Steps

1. ✅ Read this file (you're here!)
2. ⏭️ Run `./setup_and_run.sh`
3. ⏭️ Try detection on your first image
4. ⏭️ Read `TUNING_GUIDE.md` if results aren't good
5. ⏭️ Explore advanced features in `README.md`

---

## 🎉 Ready to Start?

```bash
cd /Users/nestor/armando_new/GroundingDINO
./setup_and_run.sh
```

**That's it! Have fun detecting! 🦕**

---

*For more details, see:*
- **README.md** - Complete guide
- **TUNING_GUIDE.md** - Accuracy improvement
- **SETUP_COMPLETE.txt** - Command reference

