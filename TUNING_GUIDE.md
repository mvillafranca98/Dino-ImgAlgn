# 🎯 GroundingDINO Tuning Guide

This guide helps you improve detection accuracy when the model isn't performing well.

## 📋 Quick Start

### 1. Basic Setup
```bash
# Run the setup script first
cd /Users/nestor/armando_new/GroundingDINO
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### 2. Activate Environment
```bash
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
```

### 3. Run Detection
```bash
# Using the easy runner script
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i YOUR_IMAGE.jpg \
  -t "person . car . dog ." \
  -o outputs

# Or using the original demo script
cd /Users/nestor/armando_new/GroundingDINO/repo
python demo/inference_on_a_image.py \
  -c groundingdino/config/GroundingDINO_SwinT_OGC.py \
  -p weights/groundingdino_swint_ogc.pth \
  -i YOUR_IMAGE.jpg \
  -o outputs \
  -t "person . car ." \
  --cpu-only
```

---

## 🔧 Tuning Parameters for Better Accuracy

### **1. Box Threshold (`--box-threshold` or `--box_threshold`)**

Controls the minimum confidence score for detecting objects.

**Default:** `0.35`

#### When to Adjust:
- **Missing detections?** → **Lower it** (try `0.25`, `0.2`, or even `0.15`)
- **Too many false positives?** → **Raise it** (try `0.40`, `0.45`, or `0.5`)

#### Examples:
```bash
# Detect more objects (lower threshold)
python run_model.py -i image.jpg -t "person" --box-threshold 0.25

# Only high-confidence detections (higher threshold)
python run_model.py -i image.jpg -t "person" --box-threshold 0.45
```

---

### **2. Text Threshold (`--text-threshold` or `--text_threshold`)**

Controls how closely the detected object must match your text prompt.

**Default:** `0.25`

#### When to Adjust:
- **Not detecting the right objects?** → **Lower it** (try `0.2` or `0.15`)
- **Detecting unrelated objects?** → **Raise it** (try `0.3` or `0.35`)

#### Examples:
```bash
# More flexible text matching
python run_model.py -i image.jpg -t "cat" --text-threshold 0.15

# Stricter text matching
python run_model.py -i image.jpg -t "cat" --text-threshold 0.35
```

---

### **3. Text Prompt Format**

The way you write your prompt significantly affects results.

#### Best Practices:
✅ **DO:**
- Use periods to separate objects: `"person . car . dog ."`
- Use lowercase: `"cat"` instead of `"Cat"`
- Be specific: `"red car"` instead of `"vehicle"`
- Use articles: `"a person . a dog ."` can work better than `"person . dog ."`

❌ **DON'T:**
- Use vague terms: `"things"`, `"stuff"`
- Use very long sentences
- Forget the periods between objects

#### Examples:
```bash
# Good prompts
python run_model.py -i image.jpg -t "person . car . bicycle ."
python run_model.py -i image.jpg -t "a cat sitting on a couch ."
python run_model.py -i image.jpg -t "red apple . green banana ."

# Not as good
python run_model.py -i image.jpg -t "person car bicycle"  # Missing periods
python run_model.py -i image.jpg -t "PERSON"  # Uppercase
python run_model.py -i image.jpg -t "things in the room"  # Too vague
```

---

## 🎨 Common Scenarios & Solutions

### Scenario 1: **Model finds nothing**
```bash
# Solution: Lower both thresholds significantly
python run_model.py -i image.jpg -t "object" \
  --box-threshold 0.2 \
  --text-threshold 0.15
```

### Scenario 2: **Model finds too many false positives**
```bash
# Solution: Raise box threshold
python run_model.py -i image.jpg -t "person" \
  --box-threshold 0.45
```

### Scenario 3: **Model detects objects but wrong labels**
```bash
# Solution: Be more specific in prompt and adjust text threshold
python run_model.py -i image.jpg -t "a tabby cat . a golden retriever dog ." \
  --text-threshold 0.2
```

### Scenario 4: **Small objects not detected**
```bash
# Solution: Lower box threshold significantly
python run_model.py -i image.jpg -t "small bird . tiny insect ." \
  --box-threshold 0.15
```

### Scenario 5: **Need multiple variations of same object**
```bash
# Solution: List variations explicitly
python run_model.py -i image.jpg -t "red car . blue car . white truck . motorcycle ."
```

---

## 📊 Recommended Starting Points

| Use Case | Box Threshold | Text Threshold | Notes |
|----------|---------------|----------------|-------|
| General detection | `0.35` | `0.25` | Default, balanced |
| High precision (few false positives) | `0.45-0.5` | `0.3-0.35` | Only confident detections |
| High recall (catch everything) | `0.2-0.25` | `0.15-0.2` | May include false positives |
| Small objects | `0.15-0.25` | `0.2` | Lower threshold for small/distant objects |
| Specific objects | `0.3` | `0.15` | Flexible text matching |

---

## 🧪 Testing Strategy

1. **Start with defaults:** Run with `box_threshold=0.35` and `text_threshold=0.25`
2. **Adjust box threshold first:** If too many/few detections, modify box_threshold
3. **Then adjust text threshold:** If labels are wrong, modify text_threshold
4. **Refine the prompt:** Make it more specific or try different phrasings
5. **Save results:** Use `--save-json` to compare different configurations

### Example Testing Workflow:
```bash
# Test 1: Default
python run_model.py -i test.jpg -t "person" -o test1 --save-json

# Test 2: Lower box threshold
python run_model.py -i test.jpg -t "person" -o test2 --save-json --box-threshold 0.25

# Test 3: Different prompt
python run_model.py -i test.jpg -t "a person standing" -o test3 --save-json --box-threshold 0.25

# Compare JSON files to see which works best
cat test1/results.json
cat test2/results.json
cat test3/results.json
```

---

## 💡 Advanced Tips

### 1. **Use Token Spans for Precise Detection**
If you need exact phrase matching:
```bash
cd /Users/nestor/armando_new/GroundingDINO/repo
python demo/inference_on_a_image.py \
  -c groundingdino/config/GroundingDINO_SwinT_OGC.py \
  -p weights/groundingdino_swint_ogc.pth \
  -i image.jpg \
  -o outputs \
  -t "There is a cat and a dog in the image ." \
  --token_spans "[[[9, 10], [11, 14]], [[19, 20], [21, 24]]]" \
  --cpu-only
```

### 2. **Batch Processing Multiple Images**
Create a simple script:
```bash
for img in images/*.jpg; do
  python run_model.py -i "$img" -t "person . car ." -o "outputs/$(basename $img .jpg)"
done
```

### 3. **Compare Different Models**
You can download and test the larger SwinB model for potentially better accuracy:
```bash
cd /Users/nestor/armando_new/GroundingDINO/repo
curl -L -o weights/groundingdino_swinb_cogcoor.pth \
  https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth

python run_model.py \
  -i image.jpg \
  -t "person" \
  -c groundingdino/config/GroundingDINO_SwinB_cfg.py \
  -p weights/groundingdino_swinb_cogcoor.pth
```

---

## 🐛 Troubleshooting

### Issue: "CUDA out of memory"
**Solution:** Use `--cpu-only` flag or the default CPU mode in `run_model.py`

### Issue: "Model not loading"
**Solution:** Check that checkpoint exists:
```bash
ls -lh /Users/nestor/armando_new/GroundingDINO/repo/weights/
```

### Issue: "Import errors"
**Solution:** Make sure virtual environment is activated:
```bash
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate
cd /Users/nestor/armando_new/GroundingDINO/repo
pip install -e .
```

### Issue: "No objects detected at all"
**Solution:** Try the most permissive settings:
```bash
python run_model.py -i image.jpg -t "object . thing ." \
  --box-threshold 0.1 \
  --text-threshold 0.1
```

---

## 📚 Additional Resources

- **Official Demo Notebook:** `/Users/nestor/armando_new/GroundingDINO/repo/test.ipynb`
- **GitHub Repository:** https://github.com/IDEA-Research/GroundingDINO
- **Paper:** https://arxiv.org/abs/2303.05499

---

## 🎓 Quick Reference

```bash
# Activate environment
source /Users/nestor/armando_new/GroundingDINO/.venv/bin/activate

# Basic run (recommended for testing)
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i IMAGE.jpg \
  -t "OBJECTS_TO_DETECT ." \
  -o outputs

# Full parameter example
python /Users/nestor/armando_new/GroundingDINO/run_model.py \
  -i IMAGE.jpg \
  -t "person . car . dog ." \
  -o outputs \
  --box-threshold 0.35 \
  --text-threshold 0.25 \
  --save-json
```

**Remember:** Start simple, then tune incrementally! 🚀

