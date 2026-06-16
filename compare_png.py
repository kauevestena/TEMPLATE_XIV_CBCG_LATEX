import cv2
import numpy as np
import sys

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def main():
    img1 = cv2.imread(sys.argv[1])
    img2 = cv2.imread(sys.argv[2])

    if img1.shape != img2.shape:
        print(f"Shapes differ: {img1.shape} vs {img2.shape}")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    m = mse(img1, img2)
    print(f"MSE: {m}")

if __name__ == '__main__':
    main()
