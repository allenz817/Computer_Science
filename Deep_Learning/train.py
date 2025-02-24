import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
from fire import Fire
from model import ConvNet

def train():
    size = (128, 128)
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(size),
        torchvision.transforms.ToTensor(),
    ])