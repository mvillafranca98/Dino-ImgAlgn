# 🦕 Dino-ImgAlgn - GroundingDINO Object Detection

A ready-to-use setup for GroundingDINO object detection with helper scripts, comprehensive documentation, and easy tuning options. Detect objects in images using natural language descriptions!

## 📦 What's Inside

- **`repo/`** - The cloned GroundingDINO repository
- **`setup_and_run.sh`** - Automated setup script (run this first!)
- **`run_model.py`** - Easy-to-use Python script with tuning options
- **`TUNING_GUIDE.md`** - Comprehensive guide for improving accuracy
- **`.venv/`** - Virtual environment (created after setup)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Clone and Run Setup
```bash
git clone https://github.com/mvillafranca98/Dino-ImgAlgn.git
cd Dino-ImgAlgn
./setup_and_run.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Download the pretrained model weights (~700MB)

### Step 2: Activate Environment
```bash
source .venv/bin/activate
```

### Step 3: Run Detection
```bash
python run_model.py -i YOUR_IMAGE.jpg -t "person . car . dog ."
```

**Example output:**
```
✅ Detection complete! Found 2 objects.
1. person: confidence = 0.892
2. car: confidence = 0.856
```

That's it! Results will be saved to the `outputs/` folder.

---

## 💡 Usage Examples

### Basic Detection
```bash
# Detect people in an image
python run_model.py -i photo.jpg -t "person"

# Detect multiple objects
python run_model.py -i photo.jpg -t "person . car . bicycle . dog ."

# Save results as JSON
python run_model.py -i photo.jpg -t "cat" --save-json
```

### Tuning for Better Accuracy
```bash
# Missing detections? Lower the box threshold
python run_model.py -i photo.jpg -t "person" --box-threshold 0.25

# Too many false positives? Raise the box threshold
python run_model.py -i photo.jpg -t "person" --box-threshold 0.45

# Wrong labels? Adjust text threshold
python run_model.py -i photo.jpg -t "cat" --text-threshold 0.15
```

### Using the Original Demo Script
```bash
cd repo
python demo/inference_on_a_image.py \
  -c groundingdino/config/GroundingDINO_SwinT_OGC.py \
  -p weights/groundingdino_swint_ogc.pth \
  -i YOUR_IMAGE.jpg \
  -o outputs \
  -t "person . car ." \
  --cpu-only
```

---

## 🎯 Not Getting Good Results?

See **`TUNING_GUIDE.md`** for detailed instructions on:
- Adjusting thresholds for better detection
- Writing effective text prompts
- Common scenarios and solutions
- Troubleshooting tips

Quick tips:
- **Lower `--box-threshold`** (e.g., 0.25) to detect more objects
- **Raise `--box-threshold`** (e.g., 0.45) to reduce false positives
- **Use specific prompts:** "red car" instead of "vehicle"
- **Separate objects with periods:** "person . cat . dog ."

---

## 📝 Command Reference

### `run_model.py` Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--image` | `-i` | Path to input image (required) | - |
| `--text` | `-t` | Text prompt (required) | - |
| `--output` | `-o` | Output directory | `outputs` |
| `--box-threshold` | - | Box confidence (0.0-1.0) | `0.35` |
| `--text-threshold` | - | Text matching (0.0-1.0) | `0.25` |
| `--config` | `-c` | Config file path | `GroundingDINO_SwinT_OGC.py` |
| `--checkpoint` | `-p` | Checkpoint file path | `groundingdino_swint_ogc.pth` |
| `--save-json` | - | Save results as JSON | `False` |
| `--gpu` | - | Use GPU (if available) | `False` (uses CPU) |

### Get Help
```bash
python run_model.py --help
```

---

## 🔧 Troubleshooting

### Virtual environment not activating?
```bash
# Create it manually
python3 -m venv /Users/nestor/armando_new/GroundingDINO/.venv
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
cd /Users/nestor/armando_new/GroundingDINO/repo
pip install -e .
```

### Model weights not downloaded?
```bash
cd /Users/nestor/armando_new/GroundingDINO/repo
mkdir -p weights
curl -L -o weights/groundingdino_swint_ogc.pth \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
```

### Import errors?
```bash
# Make sure you're in the virtual environment
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# Reinstall the package
cd /Users/nestor/armando_new/GroundingDINO/repo
pip install -e .
```

### No detections at all?
```bash
# Try very low thresholds
python run_model.py -i image.jpg -t "object" \
  --box-threshold 0.15 \
  --text-threshold 0.15
```

---

## 📚 Additional Resources

- **Tuning Guide:** `TUNING_GUIDE.md` - Detailed accuracy improvement guide
- **Official Repo:** [github.com/IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO)
- **Paper:** [arxiv.org/abs/2303.05499](https://arxiv.org/abs/2303.05499)
- **Jupyter Notebook:** `repo/test.ipynb` - Interactive examples
- **Gradio Web UI:** `repo/demo/gradio_app.py` - Run in browser

---

## 🎓 Example Workflow

```bash
# 1. Activate environment
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# 2. Test with default settings
python run_model.py -i test.jpg -t "person . car ." -o test1

# 3. If results aren't good, adjust thresholds
python run_model.py -i test.jpg -t "person . car ." -o test2 --box-threshold 0.25

# 4. Try different prompts
python run_model.py -i test.jpg -t "a person standing . a red car ." -o test3 --box-threshold 0.25

# 5. Save best configuration
python run_model.py -i test.jpg -t "a person standing . a red car ." -o final \
  --box-threshold 0.25 --text-threshold 0.2 --save-json

# 6. Check results
open final/annotated_result.jpg
cat final/results.json
```

---

## 🌟 Tips for Best Results

1. **Be Specific:** "golden retriever dog" > "dog" > "animal"
2. **Use Periods:** "cat . dog . bird ." not "cat dog bird"
3. **Start with Defaults:** Then tune based on results
4. **Test Incrementally:** Change one parameter at a time
5. **Save Configurations:** Use `--save-json` to track what works

---

## 📊 Performance Notes

- **Model Size:** ~700MB (SwinT variant)
- **Speed on CPU:** ~5-10 seconds per image (MacBook)
- **Accuracy:** COCO zero-shot: 48.5 AP

For better accuracy (but larger model), you can download the SwinB variant:
```bash
cd repo/weights
curl -L -o groundingdino_swinb_cogcoor.pth \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth

# Use it with -p flag
python ../run_model.py -i image.jpg -t "person" \
  -c repo/groundingdino/config/GroundingDINO_SwinB_cfg.py \
  -p repo/weights/groundingdino_swinb_cogcoor.pth
```

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Activate (do this first, every time)
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# Basic detection
python run_model.py -i IMAGE.jpg -t "OBJECTS ."

# More detections
python run_model.py -i IMAGE.jpg -t "OBJECTS ." --box-threshold 0.25

# Fewer false positives
python run_model.py -i IMAGE.jpg -t "OBJECTS ." --box-threshold 0.45

# With JSON output
python run_model.py -i IMAGE.jpg -t "OBJECTS ." --save-json

# Help
python run_model.py --help
```

---

## 📞 Need More Help?

1. Check **`TUNING_GUIDE.md`** for detailed tuning instructions
2. Look at example notebooks in `repo/demo/`
3. Read the official README in `repo/README.md`
4. Check GitHub issues: https://github.com/IDEA-Research/GroundingDINO/issues

---

**Happy Detecting! 🦕**

