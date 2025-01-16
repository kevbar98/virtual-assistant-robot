""" import torch
from torchvision.models import vgg16

class FaceTracker(torch.nn.Module):
    def __init__(self):
        super(FaceTracker, self).__init__()
        self.feature_extractor = vgg16(pretrained=True).features
        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(512 * 7 * 7, 2048),
            torch.nn.ReLU(),
            torch.nn.Linear(2048, 1),
            torch.nn.Sigmoid()
        )
        self.regressor = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(512 * 7 * 7, 2048),
            torch.nn.ReLU(),
            torch.nn.Linear(2048, 4),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        features = self.feature_extractor(x)
        class_out = self.classifier(features)
        bbox_out = self.regressor(features)
        return class_out, bbox_out

def load_model(model_path):

    model = FaceTracker()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model
 """