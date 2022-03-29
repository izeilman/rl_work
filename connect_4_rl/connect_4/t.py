import numpy as np
a = np.zeros((6,7))
a[2][1] = 1
a[4][1] = 1
a[5][1] = 1
a[2][3] = 1
a[3][3] = 1
a[4][3] = 1
a[5][3] = 1

from scipy.signal import convolve2d

def winning_move(board):
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    horizontal_kernel = np.array([[ 1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
    for kernel in detection_kernels:
        if (convolve2d(board, kernel, mode="valid") == 4).any():
            return True
    return False
print(winning_move(a))
