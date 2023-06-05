import torch
import torch.nn as nn

# TO ADD
# Fc layer - size of final msa encoding layer to n
# fc layer - n to > n
# output layer/matrix?
# workout how to fix/no_grad the model bits

# Don't think I need this as it ends with a RobertaLMHead

# CONTACT PRED HEAD FROM ESM
class MSAPredictor(nn.Module):
    def __init__(msa_n, msa_m);
        super(msa_transformer, self).__init__()
        self._head1 = torch.nn.Linear(in_features=768, out_features=768)
        self._head2 = torch.nn.Linear(in_features=768, out_features=768)
        self._head3 = torch.nn.Linear(msa_n, msa_m) # msa_topology

        self.model = EfficientNet.from_name(model,include_top=False) #you can notice here, I'm not loading the head, only the backbone
        
    def forward(self, x):
         features = self.model(x)
         res = features.flatten(start_dim=1)
         fc1 = self._head1(res)
         fc2 = self._head1(res)
         fc3 = self._head1(res)
         return rc

    def process_names():
        pretrained_dict = model.state_dict() #pretrained model keys
        model_dict = new_model.state_dict() #new model keys

        processed_dict = {}

        for k in model_dict.keys(): 
            decomposed_key = k.split(".")
            if("model" in decomposed_key):
                pretrained_key = ".".join(decomposed_key[1:])
                processed_dict[k] = pretrained_dict[pretrained_key] #Here we are creating the new state dict to make our new model able to load the pretrained parameters without the head.

        new_model.load_state_dict(processed_dict, strict=False) #strict here is important since the heads layers are missing from the state, we don't want this line to raise an error but load the present keys anyway.
        return new_model

#     """Re-output an MSA, kinda just a decoder/generator"""

#     def __init__(
#         self,
#         in_features: int,
#         prepend_bos: bool,
#         append_eos: bool,
#         bias=True,
#         eos_idx: Optional[int] = None,
#     ):
#         super().__init__()
#         self.in_features = in_features
#         self.prepend_bos = prepend_bos
#         self.append_eos = append_eos
#         if append_eos and eos_idx is None:
#             raise ValueError("Using an alphabet with eos token, but no eos token was passed in.")
#         self.eos_idx = eos_idx
#         self.regression = nn.Linear(in_features, 1, bias)
#         self.activation = nn.Sigmoid()

#     def forward(self, tokens, attentions):
#         # remove eos token attentions
#         if self.append_eos:
#             eos_mask = tokens.ne(self.eos_idx).to(attentions)
#             eos_mask = eos_mask.unsqueeze(1) * eos_mask.unsqueeze(2)
#             attentions = attentions * eos_mask[:, None, None, :, :]
#             attentions = attentions[..., :-1, :-1]
#         # remove cls token attentions
#         if self.prepend_bos:
#             attentions = attentions[..., 1:, 1:]
#         batch_size, layers, heads, seqlen, _ = attentions.size()
#         attentions = attentions.view(batch_size, layers * heads, seqlen, seqlen)

#         # features: B x C x T x T
#         attentions = attentions.to(
#             self.regression.weight.device
#         )  # attentions always float32, may need to convert to float16
#         attentions = apc(symmetrize(attentions))
#         attentions = attentions.permute(0, 2, 3, 1)
#         return self.activation(self.regression(attentions).squeeze(3))