import pathlib

from ultralytics import YOLO


def main() -> None:
    model = YOLO("./content/runs/segment/train/weights/best.pt")
    image_path = pathlib.Path("../data/toi/2/RealTime/2_aaeaf257-84b0-4fba-b043-8c1357be1a42.png")

    model.predict(image_path, conf=0.7, verbose=False, save=True, show_boxes=False)


if __name__ == "__main__":
    main()
