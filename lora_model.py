from model_def import GPT,MultiHeadAttention,LayerNorm,FeedForward,Block,Head,n_embd,n_head,dropout
import torch
import torch.nn as nn
import torch.nn.functional as F


class LoraHead(Head):
    """
    Extends MultiHeatAttention with LoRA (Low-Rank Adaptation) matrices.
    LoRA enhances efficiency by only updating the query and value matrices.
    This class adds LoRA matrices and applies LoRA logic in the forward method.

    Parameters:
    - r (int): Rank for LoRA matrices.
    - config: Configuration of the Roberta Model.
    """
    
    def __init__(self, r=8):  
        head_size = n_embd // n_head
        super().__init__(head_size=head_size)
        self.lora_query_matrix_B = nn.Parameter(torch.zeros(head_size, r))
        self.lora_query_matrix_A = nn.Parameter(torch.randn(r, head_size))
        self.lora_value_matrix_B = nn.Parameter(torch.zeros(head_size, r))
        self.lora_value_matrix_A = nn.Parameter(torch.randn(r, head_size))
        
    def lora_query(self, x):
        """
        Applies LoRA to the query component. Computes a modified query output by adding 
        the LoRA adaptation to the standard query output. Requires the regular linear layer 
        to be frozen before training.
        """
        lora_query_weights = torch.matmul(self.lora_query_matrix_B, self.lora_query_matrix_A)
        return self.query(x) + F.linear(x, lora_query_weights)

    def lora_value(self, x):
        """
        Applies LoRA to the value component. Computes a modified value output by adding 
        the LoRA adaptation to the standard value output. Requires the regular linear layer 
        to be frozen before training.
        """
        lora_value_weights = torch.matmul(self.lora_value_matrix_B, self.lora_value_matrix_A)
        return self.value(x) + F.linear(x, lora_value_weights)
        
        
    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x)
        q=self.lora_query(x)
        v=self.lora_value(x)
        out = torch.nn.functional.scaled_dot_product_attention(q, k, v, attn_mask=None, dropout_p=dropout if self.training else 0, is_causal=True)
        
        return out
        
        
class LoraGPT(nn.Module):
    
    
    def __load_model(self)->GPT:
        model_path = "./10M_2024-07-21_08-16.pth"


        model = GPT()
        print("Compiling the model...\n")
        try:
            model = torch.compile(model)  # requires PyTorch 2.0
        except Exception as e:
            pass
        model.load_state_dict(torch.load(model_path,map_location=self.device))

        m = model.to(self.device)
        return m
    
    def __init__(self,  r=8,device='cuda'):
        
        
        super().__init__()
        self.lora_rank = r
        self.device = device
        self.model=self.__load_model()
        self.replace_multihead_attention_recursion(self.model)
        self.freeze_parameters_except_lora_and_bias()
        
        
    def forward(self, x,targets=None):
        return self.model(x,targets)
   
        
    def replace_multihead_attention_recursion(self,model):
        """
        Replaces RobertaSelfAttention with LoraRobertaSelfAttention in the model.
        This method applies the replacement recursively to all sub-components.

        Parameters
        ----------
        model : nn.Module
            The PyTorch module or model to be modified.
        """
        for name, module in model.named_children():
            if isinstance(module, Head):
                # Replace RobertaSelfAttention with LoraRobertaSelfAttention
                new_layer = LoraHead(r=self.lora_rank)
                new_layer.load_state_dict(module.state_dict(), strict=False)
                setattr(model, name, new_layer)
            else:
                # Recursive call for child modules
                self.replace_multihead_attention_recursion(module)
                
                
    def freeze_parameters_except_lora_and_bias(self):
        """
        Freezes all model parameters except for specific layers and types based on the configuration.
        Parameters in LoRA layers, the finetune head, bias parameters, embeddings, and layer norms 
        can be set as trainable based on class settings.
        """
        for name, param in self.model.named_parameters():
            print(name)
            is_trainable = (
                "lora_" in name 
                
                #(self.train_layer_norms and "LayerNorm" in name)
            )
            param.requires_grad = is_trainable
        