from torch import nn
import torch

class AttentionPooling(nn.Module):

    def __init__(self, dim):
        super().__init__()
        self.score = nn.Linear(dim, 1)

    def forward(self, x, mask=None):
        scores = self.score(x).squeeze(-1)

        if mask is not None:
            scores = scores.masked_fill(~mask, -1e9)

        w = torch.softmax(scores, dim=0)
        return (x * w.unsqueeze(-1)).sum(dim=0)