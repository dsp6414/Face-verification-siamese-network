from torch import nn
import torch.nn.functional as F

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(1, 4, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(4),
            nn.Dropout2d(p=.2),
            
            nn.ReflectionPad2d(1),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),
            nn.Dropout2d(p=.2),

            nn.ReflectionPad2d(1),
            nn.Conv2d(8, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),
            nn.Dropout2d(p=.2),
            
            # nn.ReflectionPad2d(1),
            # nn.Conv2d(16, 16, kernel_size=3),
            # nn.ReLU(inplace=True),
            # nn.BatchNorm2d(16),
            # nn.Dropout2d(p=.2),

        )

        self.fc1 = nn.Sequential(
            nn.Linear(8*100*100, 256),
            nn.ReLU(inplace=True),

            # nn.Linear(512, 512),
            # nn.ReLU(inplace=True),

            nn.Linear(256, 128))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        output = F.normalize(output)
        return output

    def forward(self, anchor_input, pos_input, neg_input):
        anchor_output = self.forward_once(anchor_input)
        pos_output = self.forward_once(pos_input)
        neg_output = self.forward_once(neg_input)
        return anchor_output, pos_output, neg_output