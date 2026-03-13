import torch
import torchvision
import torchvision.transforms as transforms

from torch.utils.data import DataLoader
from model import GreenWashNet

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

dataset = torchvision.datasets.ImageFolder(
"dataset",
transform=transform
)

loader = DataLoader(dataset,batch_size=32,shuffle=True)

model = GreenWashNet()

loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.0005)

for epoch in range(15):

    for images,labels in loader:

        outputs = model(images)

        loss = loss_fn(outputs,labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print("Epoch",epoch,"Loss",loss.item())

torch.save(model.state_dict(),"models/model.pth")