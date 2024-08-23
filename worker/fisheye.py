import cv2
from cv2.typing import MatLike
import numpy as np


def defish(image: MatLike) -> MatLike:
    height, width = image.shape[:2]

    K = np.array([[width, 0, width // 2],
                [0, width, height // 2],
                [0, 0, 1]], dtype=np.float32)

    D = np.array([-0.5, 0.5, 0, 0], dtype=np.float32)

    new_K, _ = cv2.getOptimalNewCameraMatrix(K, D, (width, height), 0)
    map1, map2 = cv2.initUndistortRectifyMap(K, D, np.eye(3), new_K, (width, height), cv2.CV_16SC2)
    undistorted_image = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    return undistorted_image


image_path = "data/toi/8/RealTime/8_0cc969d9-3c24-498c-841e-d776504dbcbe.png"
image = cv2.imread(image_path)

defished = defish(image)

# cv2.imwrite("corrected_fisheye_image.png", defished)

cv2.imshow(
    "image",
    cv2.vconcat(
        (
            image,
            defished,
        )
    ),
)
cv2.waitKey(0)
cv2.destroyAllWindows()
