from typing import Union
import pathlib
import dataclasses

import cv2
from cv2.typing import MatLike
from ultralytics import YOLO
from ultralytics.engine.results import Results
import numpy as np

from . import img_manipulation as imgm


@dataclasses.dataclass
class ProcessedImg:
    image: MatLike
    images: list[MatLike]


class AiModule:
    @staticmethod
    def predict_image(model: YOLO, image: Union[str, MatLike], conf) -> list[Results]:
        result = model.predict(image, conf=conf, verbose=False)
        return result

    @staticmethod
    def process_image(model: YOLO, image: Union[str, MatLike], conf: float=0.6) -> ProcessedImg:
        img: MatLike
        if isinstance(image, str):
            img = cv2.imread(image)
        else:
            img = image
        image = imgm.ImgManipulation.defish(img)
        results = AiModule.predict_image(model, image, conf)

        out_imgs: list[MatLike] = []
        for result in results:
            masks = result.masks.data.numpy() # type: ignore
            mask = masks[0]
            mask = mask.astype("uint8") * 255
            mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
            imgc = cv2.bitwise_and(img, img, mask=mask)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[0]
            
            rect = cv2.minAreaRect(cnt) 
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            
            box_mask = np.zeros_like(imgc)
            cv2.drawContours(box_mask, [box], 0, (255, 255, 255), thickness=cv2.FILLED) # type: ignore

            masked_img = cv2.bitwise_and(imgc, box_mask)

            x, y, w, h = cv2.boundingRect(box) # type: ignore
            outp = masked_img[y:y+h, x:x+w]

            out_imgs += [outp]
                    
            image = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) 

            # cv2.imwrite("out.png", outp)

            # cv2.imshow("out", outp)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        
        out = ProcessedImg(
            image=image,
            images=out_imgs,
        )
        
        return out


def main() -> None:
    model = YOLO("./content/runs/segment/train/weights/best.pt")
    image_path = pathlib.Path("../data/toi/2/RealTime/2_aaeaf257-84b0-4fba-b043-8c1357be1a42.png")
    
    image = cv2.imread(str(image_path))

    result = AiModule.process_image(model, image, 0.6)
    # def mat_to_bytes(mat: MatLike) -> bytes:
    #     _, buffer = cv2.imencode(".png", mat)
    #     return buffer.tobytes()
    # imgs = [mat_to_bytes(mat) for mat in results]
    
    
    # for i, img in enumerate(imgs):
    #     with open(f"{i}.png", "wb") as f:
    #         f.write(img)


if __name__ == "__main__":
    main()
