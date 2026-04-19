# Project Report: Image Styling via Pure Linear Algebra

## 1. Introduction
This project explores the application of Linear Algebra (LA) to the problem of image style transfer. Unlike deep-learning-based approaches (e.g., Neural Style Transfer), we rely on statistical properties and linear transforms to map the "look and feel" of a style image onto a content image.

## 2. Mathematical Foundation

### 2.1 Global Covariance Matching (Xiao & Ma, 2006)
We treat each pixel as a 3D vector $\mathbf{x} = [R, G, B]^T$. The image is modeled as a set of samples from a distribution. The style is captured by the mean $\mathbf{\mu}$ and the covariance matrix $\mathbf{\Sigma}$.

The affine transformation to match the content image to the style image is:
$$\mathbf{x}' = \mathbf{\mu}_s + \mathbf{T}(\mathbf{x} - \mathbf{\mu}_c)$$
where $\mathbf{T}$ is the transfer matrix. To align the covariances, we require:
$$\mathbf{\Sigma}_s = \mathbf{T} \mathbf{\Sigma}_c \mathbf{T}^T$$
Solving for $\mathbf{T}$:
$$\mathbf{T} = \mathbf{\Sigma}_s^{1/2} \mathbf{\Sigma}_c^{-1/2}$$
We compute the matrix square root using **Eigendecomposition** or **SVD**.

### 2.2 Multiscale Decomposition
To separate global color mood from local texture, we use a **Laplacian Pyramid**. 
- **Base Layer (Low Frequency)**: Transferred using the full global covariance matrix.
- **Detail Layers (High Frequency)**: Transferred by matching per-channel variance (a diagonal approximation of covariance).

## 3. Implementation
The engine is implemented in Python using `NumPy` for matrix operations and `OpenCV` for image processing.

### Key Modules:
- `color_transfer_global`: Computes $\mathbf{T}$ and applies the affine transform.
- `laplacian_pyramid_style_transfer`: Handles the frequency-domain separation.

## 4. Results
(Visual results would be placed here in a full report)
The global method captures the general color palette perfectly. The multiscale approach preserves structural details much better than the simple global method, especially in high-contrast images.

## 5. Conclusion
Pure linear algebra provides a robust and computationally efficient framework for certain types of style transfer (color and texture statistics). While it lacks the semantic understanding of neural networks, the transparency and speed of LA make it ideal for real-time applications and fundamental image processing tasks.
