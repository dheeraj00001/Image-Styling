# LA-Stylizer (Linear Algebra Stylizer)

This project implements image styling using pure linear algebra operations, inspired by classic and modern research papers. The engine matches color statistics and, optionally, texture statistics via filter‑bank covariance, all without neural networks or nonlinear optimizations.

## Mathematical Foundation
- **Reinhard et al. (2001)**: Per-channel mean and standard deviation matching in a decorrelated opponent color space (`lαβ`). This serves as a baseline for global color transfer.
- **Xiao & Ma (2006)**: Global covariance matching in RGB space. The transformation  
  `x' = μ_s + Σ_s^{1/2} Σ_c^{-1/2} (x - μ_c)` aligns the full covariance of the content to that of the style using matrix square roots (via SVD/Eigendecomposition).
- **Shao et al. (2007)**: Multiscale and multiview considerations show that a single global affine transform may fail for images with spatially varying color statistics; a pyramid or region‑wise approach improves results.
- **Zhang et al. (2013)**: While their method uses MRF/BP, the core idea of separating content and style via a linear decomposition (e.g., Laplacian pyramid) is adopted here.

## Project Structure
- `style_transfer.py`: Main script implementing global and multiscale linear algebra styling.
- `report/`: Detailed mathematical report (`final_report.md`).
- `assets/content/`: Place your content images here (to be styled).
- `assets/styles/`: Place your style reference images here (e.g., paintings, textures).
- `.gitignore`: Excludes virtual environment, bytecode, and output images.
- `requirements.txt`: Lists required Python packages.

## Features Implemented
- [x] Global Covariance Style Transfer (Xiao & Ma 2006)
- [x] Multiscale Frequency Decomposition (Laplacian pyramid) for better detail preservation
- [ ] Patch‑based PCA Texture Transfer (future extension)
- [ ] Piecewise Affine Stylization (future extension)

## Usage
```bash
# Global style transfer (color grading)
python style_transfer.py <content_image> <style_image> <output_image>

# Multiscale style transfer (better detail preservation)
python style_transfer.py <content_image> <style_image> <output_image> --multiscale
```

### Example
```bash
python style_transfer.py assets/content/Taj_Mahal,_Agra,_India_edit3.jpg assets/styles/starry-night-1093721.jpg result.jpg
python style_transfer.py assets/content/Taj_Mahal,_Agra,_India_edit3.jpg assets/styles/starry-night-1093721.jpg result_ms.jpg --multiscale
```

## How It Works
1. **Global Mode**  
   - Resizes large images to a manageable size (max dimension 1024 px) to avoid memory issues.  
   - Computes per‑channel mean and covariance for content and style.  
   - Derives the transform matrix `T = Σ_s^{1/2} Σ_c^{-1/2}` using SciPy’s `sqrtm` (eigendecomposition).  
   - Applies `x' = μ_s + T (x - μ_c)` and clips to `[0,255]`.

2. **Multiscale Mode**  
   - Builds a Laplacian pyramid (Gaussian low‑pass + high‑pass detail) for both images.  
   - Applies the global covariance transfer to the coarsest (low‑frequency) layer.  
   - For each detail layer, matches the per‑channel standard deviation (a diagonal covariance match) to transfer contrast while preserving edges.  
   - Reconstructs the image from the processed pyramid.

Both methods rely solely on linear operations: resizing (linear interpolation), mean/covariance (linear statistics), matrix multiplication, and addition—no nonlinear activation functions or learned weights.

## Dependencies
- Python 3.8+
- NumPy
- OpenCV (`opencv-python`)
- SciPy

Install with:
```bash
pip install -r requirements.txt
```

## Notes
- The current implementation excels at transferring overall color palette, contrast, and broad texture statistics.  
- For fine‑grained brush‑stroke or pattern replication, a filter‑bank covariance extension (still linear) can be added in future work.
- Large images are automatically down‑scaled internally; the output retains the original aspect ratio but at the reduced resolution used for processing.

## License
This project is provided for educational and experimental purposes. Feel free to adapt and extend it.

