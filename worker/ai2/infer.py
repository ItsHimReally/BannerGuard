import base64
import io

import torch.nn as nn
import torchvision.models as models
import torch
from torchvision import transforms
from PIL import Image


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DualEfficientnetClassifier(nn.Module):
    def __init__(self) -> None:
        super(DualEfficientnetClassifier, self).__init__()

        efficientnet = models.efficientnet_b0(pretrained=True)

        self.feature_extractor = nn.Sequential(*list(efficientnet.children())[:-1])

        self.fc = nn.Sequential(
            nn.Linear(2560, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, img1, img2):
        feat1 = self.feature_extractor(img1)
        feat2 = self.feature_extractor(img2)

        feat1 = feat1.view(feat1.size(0), -1)
        feat2 = feat2.view(feat2.size(0), -1)

        combined_features = torch.cat((feat1, feat2), dim=1)
        output = self.fc(combined_features)

        return output
    
    def predict(self, img1, img2):
        imgs = self.processing_imgs(img1, img2)

        ans = self.forward(imgs[0][None, :, :, :], imgs[1][None, :, :, :]).squeeze()
        return ans > 0.5

    def processing_imgs(self, target: io.BytesIO, fact: io.BytesIO):
        image_size = (256, 256)

        transform = transforms.Compose([
            transforms.Resize(image_size),
        ])

        target_img = Image.open(target)
        fact_img = Image.open(fact)

        target_img = transform(target_img)
        fact_img = transform(fact_img)

        transform = transforms.ToTensor()
        target_img = transform(target_img)
        fact_img = transform(fact_img)

        if target_img.shape[0] == 4:
            target_img = target_img[:-1]
        if fact_img.shape[0] == 4:
            fact_img = fact_img[:-1]

        return target_img, fact_img

model = DualEfficientnetClassifier()
model.to(device)


def process_img(img1, img2) -> bool:
    out = model.predict(img1, img2)
    return bool(out)


# img1 = "./contents/18340_F1x1.png"
# img2 = "./imgs/5_22b586db-3350-48f4-b5e6-5bcff27a5067.png"

# out = process_img(image_file1, image_file2)
# print("out", out)
