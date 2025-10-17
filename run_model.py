#!/usr/bin/env python3
"""
Enhanced GroundingDINO Runner with Tuning Options
This script makes it easy to run and tune the model for better accuracy.
"""

import argparse
import os
import sys
import json
from pathlib import Path

# Add repo to path
sys.path.insert(0, '/Users/nestor/armando_new/GroundingDINO/repo')

import torch
import cv2
import numpy as np
from PIL import Image

# Import from the util.inference module for easier usage
try:
    from groundingdino.util.inference import load_model, load_image, predict, annotate
    USE_UTIL_INFERENCE = True
except ImportError:
    USE_UTIL_INFERENCE = False
    print("⚠️  Warning: Could not import utility functions. Using fallback method.")


def run_detection(
    image_path,
    text_prompt,
    config_path="groundingdino/config/GroundingDINO_SwinT_OGC.py",
    checkpoint_path="weights/groundingdino_swint_ogc.pth",
    box_threshold=0.35,
    text_threshold=0.25,
    output_dir="outputs",
    cpu_only=True,
    save_json=False,
):
    """
    Run GroundingDINO detection on an image.
    
    Args:
        image_path: Path to input image
        text_prompt: Text description of objects to detect (e.g., "person . cat . dog .")
        config_path: Path to model config file
        checkpoint_path: Path to model checkpoint
        box_threshold: Confidence threshold for bounding boxes (0.0-1.0)
        text_threshold: Confidence threshold for text matching (0.0-1.0)
        output_dir: Directory to save outputs
        cpu_only: Run on CPU only
        save_json: Save detection results as JSON
    
    Returns:
        Dictionary with detection results
    """
    
    print(f"\n🦕 Running GroundingDINO Detection")
    print(f"{'='*50}")
    print(f"Image: {image_path}")
    print(f"Prompt: {text_prompt}")
    print(f"Box threshold: {box_threshold}")
    print(f"Text threshold: {text_threshold}")
    print(f"Device: {'CPU' if cpu_only else 'CUDA'}")
    print(f"{'='*50}\n")
    
    # Make output directory absolute if it's relative
    if not Path(output_dir).is_absolute():
        output_dir = str(Path.cwd() / output_dir)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"💾 Output will be saved to: {output_dir}\n")
    
    # Save original working directory for finding the image
    original_cwd = Path.cwd()
    
    # Change to repo directory to ensure relative paths work
    repo_dir = Path("/Users/nestor/armando_new/GroundingDINO/repo")
    
    # Handle image path BEFORE changing directory - try multiple locations
    image_path_obj = Path(image_path)
    if not image_path_obj.is_absolute():
        # Try relative to original working directory first
        cwd_image = original_cwd / image_path
        if cwd_image.exists():
            image_path = str(cwd_image.absolute())
        else:
            # Try relative to GroundingDINO parent directory
            parent_image = original_cwd.parent / image_path if original_cwd.name == "repo" else original_cwd / image_path
            if parent_image.exists():
                image_path = str(parent_image.absolute())
            else:
                # Try relative to repo directory
                repo_image = repo_dir / image_path
                if repo_image.exists():
                    image_path = str(repo_image.absolute())
    else:
        image_path = str(Path(image_path).absolute())
    
    # Make config and checkpoint paths absolute
    config_path = repo_dir / config_path if not Path(config_path).is_absolute() else Path(config_path)
    checkpoint_path = repo_dir / checkpoint_path if not Path(checkpoint_path).is_absolute() else Path(checkpoint_path)
    
    # Now change to repo directory
    os.chdir(repo_dir)
    
    # Check if files exist
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found!")
        print(f"   Searched for: {image_path}")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Please provide the full path to your image.")
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    
    try:
        # Load model
        print("📦 Loading model...")
        if USE_UTIL_INFERENCE:
            model = load_model(str(config_path), str(checkpoint_path))
            if cpu_only:
                model = model.cpu()
        else:
            # Fallback: use direct imports
            from groundingdino.models import build_model
            from groundingdino.util.slconfig import SLConfig
            from groundingdino.util.utils import clean_state_dict
            
            args = SLConfig.fromfile(str(config_path))
            args.device = "cpu" if cpu_only else "cuda"
            model = build_model(args)
            checkpoint = torch.load(str(checkpoint_path), map_location="cpu")
            model.load_state_dict(clean_state_dict(checkpoint["model"]), strict=False)
            model.eval()
        
        print("✅ Model loaded successfully!\n")
        
        # Load image
        print("🖼️  Loading image...")
        if USE_UTIL_INFERENCE:
            image_source, image = load_image(image_path)
        else:
            from groundingdino.datasets import transforms as T
            image_pil = Image.open(image_path).convert("RGB")
            transform = T.Compose([
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])
            image, _ = transform(image_pil, None)
            image_source = image_pil
        
        print("✅ Image loaded successfully!\n")
        
        # Run detection
        print("🔍 Running detection...")
        device = "cpu" if cpu_only else "cuda"
        if USE_UTIL_INFERENCE:
            boxes, logits, phrases = predict(
                model=model,
                image=image,
                caption=text_prompt,
                box_threshold=box_threshold,
                text_threshold=text_threshold,
                device=device
            )
        else:
            # Fallback method
            from groundingdino.util.inference import get_grounding_output
            device = "cpu" if cpu_only else "cuda"
            model = model.to(device)
            image = image.to(device)
            
            with torch.no_grad():
                outputs = model(image[None], captions=[text_prompt])
            
            logits = outputs["pred_logits"].sigmoid()[0]
            boxes = outputs["pred_boxes"][0]
            
            # Filter by threshold
            filt_mask = logits.max(dim=1)[0] > box_threshold
            boxes = boxes[filt_mask].cpu()
            logits = logits[filt_mask].cpu().max(dim=1)[0]
            phrases = [f"obj_{i}" for i in range(len(boxes))]
        
        print(f"✅ Detection complete! Found {len(boxes)} objects.\n")
        
        # Print results
        print("📊 Detection Results:")
        print(f"{'='*50}")
        for i, (box, phrase, conf) in enumerate(zip(boxes, phrases, logits)):
            print(f"{i+1}. {phrase}: confidence = {conf:.3f}")
            print(f"   Box: [{box[0]:.3f}, {box[1]:.3f}, {box[2]:.3f}, {box[3]:.3f}]")
        print(f"{'='*50}\n")
        
        # Annotate and save image
        print("💾 Saving annotated image...")
        if USE_UTIL_INFERENCE:
            annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
        else:
            # Manual annotation
            annotated_frame = np.array(image_source)
            h, w = annotated_frame.shape[:2]
            for box, phrase in zip(boxes, phrases):
                # Convert normalized coords to pixel coords
                x1, y1, x2, y2 = box
                x1, y1, x2, y2 = int(x1*w), int(y1*h), int(x2*w), int(y2*h)
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, phrase, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        output_path = os.path.join(output_dir, "annotated_result.jpg")
        # Ensure output directory exists (in case we changed directories)
        os.makedirs(output_dir, exist_ok=True)
        success = cv2.imwrite(output_path, annotated_frame)
        if success:
            print(f"✅ Saved to: {output_path}")
            print(f"   File size: {os.path.getsize(output_path) / 1024:.1f} KB\n")
        else:
            print(f"❌ Failed to save image to: {output_path}\n")
        
        # Save JSON if requested
        if save_json:
            results = {
                "image": image_path,
                "prompt": text_prompt,
                "box_threshold": box_threshold,
                "text_threshold": text_threshold,
                "detections": [
                    {
                        "phrase": phrase,
                        "confidence": float(conf),
                        "box": box.tolist()
                    }
                    for box, phrase, conf in zip(boxes, phrases, logits)
                ]
            }
            json_path = os.path.join(output_dir, "results.json")
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Saved JSON to: {json_path}\n")
        
        return {
            "boxes": boxes,
            "logits": logits,
            "phrases": phrases,
            "output_path": output_path
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Run GroundingDINO with easy tuning options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python run_model.py -i image.jpg -t "person . car . dog ."
  
  # Adjust thresholds for better accuracy
  python run_model.py -i image.jpg -t "cat" --box-threshold 0.3 --text-threshold 0.2
  
  # Save results as JSON
  python run_model.py -i image.jpg -t "objects" --save-json
  
  # Use GPU (if available)
  python run_model.py -i image.jpg -t "person" --gpu

Tuning Tips:
  - Lower box_threshold (e.g., 0.2-0.3) to detect more objects (may include false positives)
  - Raise box_threshold (e.g., 0.4-0.5) to only detect high-confidence objects
  - Lower text_threshold (e.g., 0.15-0.2) for more flexible text matching
  - Use specific, clear text prompts: "a red car . a person ." works better than "stuff"
  - Separate multiple objects with periods: "cat . dog . chair ."
        """
    )
    
    parser.add_argument("-i", "--image", required=True, help="Path to input image")
    parser.add_argument("-t", "--text", required=True, help="Text prompt (e.g., 'person . car . dog .')")
    parser.add_argument("-o", "--output", default="outputs", help="Output directory (default: outputs)")
    parser.add_argument("-c", "--config", default="groundingdino/config/GroundingDINO_SwinT_OGC.py",
                        help="Path to config file")
    parser.add_argument("-p", "--checkpoint", default="weights/groundingdino_swint_ogc.pth",
                        help="Path to checkpoint file")
    parser.add_argument("--box-threshold", type=float, default=0.35,
                        help="Box confidence threshold (default: 0.35, range: 0.0-1.0)")
    parser.add_argument("--text-threshold", type=float, default=0.25,
                        help="Text matching threshold (default: 0.25, range: 0.0-1.0)")
    parser.add_argument("--gpu", action="store_true", help="Use GPU instead of CPU")
    parser.add_argument("--save-json", action="store_true", help="Save results as JSON")
    
    args = parser.parse_args()
    
    result = run_detection(
        image_path=args.image,
        text_prompt=args.text,
        config_path=args.config,
        checkpoint_path=args.checkpoint,
        box_threshold=args.box_threshold,
        text_threshold=args.text_threshold,
        output_dir=args.output,
        cpu_only=not args.gpu,
        save_json=args.save_json
    )
    
    if result:
        print("🎉 Success! Check the output directory for results.")
    else:
        print("❌ Detection failed. See error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

