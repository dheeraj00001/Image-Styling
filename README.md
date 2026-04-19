# LA-Stylizer (Linear Algebra Stylizer)

This project implements image styling based on pure linear algebra principles, derived from several classic and modern research papers.

## Mathematical Foundation
- **Reinhard et al. (2001)**: Per-channel statistics matching in decorrelated color space (`lαβ`).
- **Xiao & Ma (2006)**: Global covariance matching using SVD and affine transforms in RGB space.
- **Shao et al. (2007)**: Multiview color correction and PCA/ICA anchors.
- **Zhang et al. (2013)**: Style transfer via image component analysis (Decomposition into Draft, Paint, and Edge).

## Project Structure
- `src/`: Core implementation of the style transfer engine.
- `report/`: Detailed mathematical report and results.
- `assets/`: Test images and examples.

## Features
- [ ] Global Covariance Style Transfer
- [ ] Multiscale Frequency Decomposition
- [ ] Patch-based PCA Texture Transfer
- [ ] Piecewise Affine Stylization
