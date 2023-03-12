import torch

from torch_geometric.nn import ComplEx

def test_complex_scoring():
  model = ComplEx(5, 2, 1)
  model.node_emb.weight.data = torch.Tensor([[2.], [3.], [5.], [1.], [2.]])
  model.node_emb_im.weight.data  = torch.Tensor([[4.], [1.], [3.], [1.], [2.]])
  model.rel_emb.weight.data  = torch.Tensor([[2.], [3.]])
  model.rel_emb_im.weight.data = torch.Tensor([[3.], [1.]])
  
  score = model(torch.IntTensor([1, 3]), torch.IntTensor([1, 0]), torch.IntTensor([2, 4]))
  
  assert torch.all(torch.eq(score, torch.tensor([58, 8])))
  
def test_complex():
    model = ComplEx(num_nodes=10, num_relations=5, hidden_channels=32)
    assert str(model) == 'ComplEx(10, num_relations=5, hidden_channels=32)'

    head_index = torch.tensor([0, 2, 4, 6, 8])
    rel_type = torch.tensor([0, 1, 2, 3, 4])
    tail_index = torch.tensor([1, 3, 5, 7, 9])

    loader = model.loader(head_index, rel_type, tail_index, batch_size=5)
    for h, r, t in loader:
        out = model(h, r, t)
        assert out.size() == (5, )

        loss = model.loss(h, r, t)
        assert loss >= 0.

        mean_rank, hits_at_10 = model.test(h, r, t, batch_size=5)
        assert mean_rank <= 10
        assert hits_at_10 == 1.0
