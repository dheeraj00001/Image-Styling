# LA-Stylizer (Linear Algebra Stylizer)

This project implements image styling based on pure linear algebra principles, derived from several classic and modern research papers.

## Mathematical Foundation
- **Reinhard et al. (2001)**: Per-channel statistics matching in decorrelated color space (`lαβ`).
- **Xiao & Ma (2006)**: Global covariance matching using SVD and affine transforms in RGB space.
- **Shao et al. (2007)**: Multiview color correction and PCA/ICA anchors.
- **Zhang et al. (2013)**: Style transfer via image component analysis (Decomposition into Draft, Paint, and Edge).

## Project Structure
- `style_transfer.py`: The main script for applying image styles.
- `report/`: Detailed mathematical report and results.
- `assets/content/`: Folder for images to be styled.
- `assets/styles/`: Folder for style images (e.g., paintings, themes).

## Features
- [ ] Global Covariance Style Transfer
- [ ] Multiscale Frequency Decomposition
- [ ] Patch-based PCA Texture Transfer
- [ ] Piecewise Affine Stylization
