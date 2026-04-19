import numpy as np
import cv2
from scipy.linalg import sqrtm

def resize_image_if_needed(image, max_dimension=1024):
    """
    Resize image if its largest dimension exceeds max_dimension,
    maintaining aspect ratio.
    """
    height, width = image.shape[:2]
    if max(height, width) <= max_dimension:
        return image
    
    # Calculate scaling factor
    scale = max_dimension / max(height, width)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Resize using INTER_AREA for shrinking (better quality)
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized

def get_stats(image_data):
    """
    Computes mean and covariance matrix for an image.
    image_data: (N, 3) array of pixels
    """
    mu = np.mean(image_data, axis=0)
    cov = np.cov(image_data.T)
    return mu, cov

def color_transfer_global(content_pixels, style_pixels):
    """
    Implements the global covariance transfer from Xiao & Ma (2006).
    Formula: x' = mu_s + (Sigma_s^1/2)(Sigma_c^-1/2)(x - mu_c)
    """
    mu_c, cov_c = get_stats(content_pixels)
    mu_s, cov_s = get_stats(style_pixels)

    # Compute transfer matrix T = Sigma_s^0.5 * Sigma_c^-0.5
    try:
        sigma_c_inv_sqrt = sqrtm(np.linalg.inv(cov_c + np.eye(3)*1e-6))
        sigma_s_sqrt = sqrtm(cov_s + np.eye(3)*1e-6)
        T = sigma_s_sqrt @ sigma_c_inv_sqrt
    except np.linalg.LinAlgError:
        # Fallback to simple scaling if covariance is singular
        std_c = np.std(content_pixels, axis=0) + 1e-6
        std_s = np.std(style_pixels, axis=0)
        T = np.diag(std_s / std_c)

    centered_c = content_pixels - mu_c
    transferred = (T @ centered_c.T).T + mu_s
    return transferred

def laplacian_pyramid_style_transfer(content_img, style_img, levels=3):
    """
    Decomposes images into multiscale frequency bands.
    Applies global transfer to the low-frequency base,
    and scale-specific transfer to high-frequency details.
    """
    # Resize style to match content for band-wise comparison
    style_img_res = cv2.resize(style_img, (content_img.shape[1], content_img.shape[0]))
    
    # 1. Build Pyramids
    def build_pyramid(img, levels):
        pyramid = []
        temp = img.astype(np.float64)
        for i in range(levels):
            low = cv2.GaussianBlur(temp, (0, 0), sigmaX=2)
            high = temp - low
            pyramid.append(high)
            temp = low
        pyramid.append(temp) # Base
        return pyramid

    cp = build_pyramid(content_img, levels)
    sp = build_pyramid(style_img_res, levels)
    
    # 2. Process bands
    # Base layer (lowest frequency): Global color transfer
    base_c = cp[-1].reshape(-1, 3)
    base_s = sp[-1].reshape(-1, 3)
    styled_base = color_transfer_global(base_c, base_s)
    styled_base = styled_base.reshape(cp[-1].shape)
    
    # Detail layers: Match variance/scale per band
    styled_pyramid = []
    for i in range(levels):
        detail_c = cp[i]
        detail_s = sp[i]
        
        # Linear Algebra: scaling factor is ratio of standard deviations
        # This is a simplified per-channel 1D covariance matching
        std_c = np.std(detail_c, axis=(0,1)) + 1e-6
        std_s = np.std(detail_s, axis=(0,1))
        scale = std_s / std_c
        
        styled_detail = detail_c * scale
        styled_pyramid.append(styled_detail)
        
    # 3. Reconstruct
    res = styled_base
    for i in reversed(range(levels)):
        res += styled_pyramid[i]
        
    return np.clip(res, 0, 255).astype(np.uint8)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python style_transfer.py <content> <style> <output> [--multiscale]")
        sys.exit(1)
        
    # Read images
    c = cv2.imread(sys.argv[1])
    s = cv2.imread(sys.argv[2])
    
    if c is None or s is None:
        print("Error: Could not read images.")
        sys.exit(1)
    
    # Resize large images to prevent memory issues
    c = resize_image_if_needed(c)
    s = resize_image_if_needed(s)
    
    if "--multiscale" in sys.argv:
        res = laplacian_pyramid_style_transfer(c, s)
    else:
        # Simple global
        pixels_c = c.reshape(-1, 3).astype(np.float64)
        pixels_s = s.reshape(-1, 3).astype(np.float64)
        res_pixels = color_transfer_global(pixels_c, pixels_s)
        res = np.clip(res_pixels.reshape(c.shape), 0, 255).astype(np.uint8)

    cv2.imwrite(sys.argv[3], res)
    print(f"Successfully saved styled image to {sys.argv[3]}")
