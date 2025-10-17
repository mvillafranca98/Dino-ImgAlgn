# 🦕 GroundingDINO - Easy Setup & Usage

**Open-set object detection with text prompts** - Detect any object by describing it in natural language!

This is a simplified, ready-to-use setup of [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) with helper scripts and comprehensive documentation for easy installation and usage on macOS/Linux.

## ✨ Features

- 🚀 **Easy installation** - Automated setup script
- 🖼️ **Simple CLI tool** - Detect objects with one command
- 🎯 **Tuning guide** - Improve accuracy with detailed instructions
- 📦 **Batch processing** - Process multiple images at once
- 💻 **CPU-friendly** - Works great without GPU
- 📖 **Comprehensive docs** - Step-by-step guides for everything

## 🎬 Quick Demo

```bash
# Detect objects in an image
python run_model.py -i photo.jpg -t "person . car . dog ."
```

**Result:** Bounding boxes drawn around detected objects with confidence scores!

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- macOS, Linux, or Windows with WSL

### Quick Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/GroundingDINO.git
cd GroundingDINO

# Run the automated setup (installs dependencies and downloads model)
chmod +x setup_and_run.sh
./setup_and_run.sh

# Activate the environment
source .venv/bin/activate

# Download a sample image
./get_sample_image.sh

# Test it out!
python run_model.py -i sample_cat.jpg -t "cat"
```

## 🚀 Usage

### Basic Detection

```bash
# Activate environment (do this first, every time!)
source .venv/bin/activate

# Detect objects
python run_model.py -i your_image.jpg -t "person . car . dog ."

# View results
open outputs/annotated_result.jpg
```

### Advanced Options

```bash
# Lower threshold for more detections
python run_model.py -i image.jpg -t "person" --box-threshold 0.25

# Higher threshold for fewer false positives
python run_model.py -i image.jpg -t "person" --box-threshold 0.45

# Save results as JSON
python run_model.py -i image.jpg -t "cat . dog ." --save-json

# Batch process multiple images
./batch_detect.sh my_images_folder "person . car ."
```

## 🎯 Tuning for Better Accuracy

If results aren't good, adjust these parameters:

| Parameter | Default | Effect |
|-----------|---------|--------|
| `--box-threshold` | 0.35 | Lower (0.2-0.3) = more detections<br>Higher (0.4-0.5) = fewer false positives |
| `--text-threshold` | 0.25 | Lower (0.15-0.2) = flexible matching<br>Higher (0.3-0.35) = strict matching |

**See `TUNING_GUIDE.md` for comprehensive tuning instructions!**

## 📖 Documentation

- **`START_HERE.md`** - Quick overview and getting started
- **`INSTALLATION_COMPLETE.md`** - Installation guide
- **`HOW_TO_USE_YOUR_IMAGES.md`** - Image usage instructions
- **`TUNING_GUIDE.md`** - Detailed accuracy tuning guide
- **`README.md`** - Main documentation (this file for local use)

## 💡 Tips for Best Results

1. **Use periods** to separate objects: `"cat . dog . bird ."`
2. **Be specific:** `"golden retriever"` > `"dog"` > `"animal"`
3. **Start with defaults** then tune based on results
4. **Use lowercase** in prompts
5. Always **activate the virtual environment** first!

## 📊 Examples

### Detect People in a Photo
```bash
python run_model.py -i street.jpg -t "person"
```

### Detect Multiple Objects
```bash
python run_model.py -i living_room.jpg -t "couch . table . lamp . cat ."
```

### Detect by Description
```bash
python run_model.py -i photo.jpg -t "a red car . a person wearing a hat ."
```

## 🛠️ Project Structure

```
GroundingDINO/
├── run_model.py              # Easy-to-use detection script
├── setup_and_run.sh          # Automated installation
├── batch_detect.sh           # Batch processing script
├── get_sample_image.sh       # Download test image
├── START_HERE.md             # Quick start guide
├── TUNING_GUIDE.md           # Accuracy tuning guide
├── HOW_TO_USE_YOUR_IMAGES.md # Image usage guide
├── repo/                     # Original GroundingDINO code
└── outputs/                  # Detection results
```

## 🔧 Troubleshooting

### Module not found?
```bash
source .venv/bin/activate
```

### No detections?
```bash
python run_model.py -i image.jpg -t "object" --box-threshold 0.2
```

### Too many false positives?
```bash
python run_model.py -i image.jpg -t "object" --box-threshold 0.45
```

**See `TUNING_GUIDE.md` for more solutions!**

## 📚 Original Repository

This is based on the official [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) by IDEA-Research.

### Citation

If you use this in your research, please cite:

```bibtex
@article{liu2023grounding,
  title={Grounding dino: Marrying dino with grounded pre-training for open-set object detection},
  author={Liu, Shilong and Zeng, Zhaoyang and Ren, Tianhe and Li, Feng and Zhang, Hao and Yang, Jie and Li, Chunyuan and Yang, Jianwei and Su, Hang and Zhu, Jun and others},
  journal={arXiv preprint arXiv:2303.05499},
  year={2023}
}
```

## 📝 License

Apache-2.0 License (see LICENSE file)

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

## ⭐ Show Your Support

If this project helped you, please give it a star! ⭐

---

**Made with ❤️ for easy object detection**
