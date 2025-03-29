import torch

def attention_mask(seq_len, learned_embedding: torch.Tensor):
    # learned_embedding: [embed_0, embed_1, ..., embed_n]
    
    embed = learned_embedding.new_full((*learned_embedding.shape[:-1], seq_len, seq_len), float("-inf"))
    pos = torch.arange(seq_len)
    rel_pos = pos[:, None] - pos[None, :]
    valid_pos = (rel_pos >= 0) & (rel_pos < learned_embedding.shape[-1])
    
    embed[..., valid_pos] = learned_embedding[..., rel_pos[valid_pos]]
    return embed

class TransformerLayer(torch.nn.Module):
    def __init__(self, embed_dim, num_heads, res_pos_length=512):
        super().__init__()
        
        self.res_pos = torch.nn.Parameter(torch.zeros(num_heads, res_pos_length))
        self.self_att = torch.nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.mlp = torch.nn.Sequential(
            torch.nn.Linear(embed_dim, 4 * embed_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(4 * embed_dim, embed_dim)
        )
        self.in_norm = torch.nn.LayerNorm(embed_dim)
        self.mlp_norm = torch.nn.LayerNorm(embed_dim)
    
    def forward(self, x):
        x_norm = self.in_norm(x)
        attn_mask = attention_mask(x.shape[1], self.res_pos)
        x = x + self.self_att(x_norm, x_norm, x_norm, attn_mask=attn_mask)[0]
        x = x + self.mlp(self.mlp_norm(x))
        return x
    
class Transformer(torch.nn.Module):
    def __init__(self, embed_dim, num_heads, num_layers):
        super().__init__()
        self.network = torch.nn.Sequential(
            torch.nn.Embedding(128, embed_dim), # a set of learned features
            *[
                TransformerLayer(embed_dim, num_heads) for _ in range(num_layers)
                ],
            torch.nn.Linear(embed_dim, 128),
        )

    def forward(self, x):
        return self.network(x)
    
def train():
    with open(__file__) as f:
        code = f.read()
    
    tokens = torch.as_tensor([127] + [ord(c) for c in code] + [0]).cuda()
    #print(torch.unique(tokens))
    
    net = Transformer(256, 8, 4)
    #print(net(tokens[None, :10]).shape)
    
    net.cuda()
    optim = torch.optim.AdamW(net.parameters(), lr=1e-3)
    for it in range(1000):
        pred = net(tokens[None, :-1])[0]
        loss = torch.nn.functional.cross_entropy(pred, tokens[1:])
        
        optim.zero_grad()
        loss.backward()
        optim.step()
        
        if it % 10 == 0:
            print(float(loss))
            pred = net(tokens[None, :])[0]
            print(tokens[1:11])
            print(pred.argmax(-1))
            print([int(net(tokens[None, :n+1])[0,-1].argmax()) for n in range(10)])
        #break
    net.eval()
    net.cpu()
    torch.save(net, "transformer.pth")
    
def sample():
    import sys
    net = torch.load("transformer.pth")
    net.eval()
    net.cuda()
    data = [127]
    for i in range(1000):
        tokens = torch.as_tensor(data[-500:]).cuda()
        pred = net(tokens[None, :])[0]
        next_char = pred.argmax(-1)
        if next_char == 0:
            break
        data.append(int(next_char))
        sys.stdout.write(chr(int(next_char)))  
        sys.stdout.flush()
    
    #print(code)

if __name__ == "__main__":
    train()
    sample()
    #learned_embed = torch.arange(6).float().view(2, 3)
    #print(attention_mask(5, learned_embed))