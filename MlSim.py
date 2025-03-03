import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class MLAccelerator:
    def __init__(self, cores=1024, peak_flops_per_core=512, sram_size=32, hbm_bandwidth=1, 
                 systolic_array_size=256, utilization_factor=0.8):
        self.cores = cores  # Number of compute cores
        self.peak_flops_per_core = peak_flops_per_core  # TFLOPs per core
        self.sram_size = sram_size  # On-chip memory (MB)
        self.hbm_bandwidth = hbm_bandwidth  # TB/s
        self.systolic_array_size = systolic_array_size  # Matrix mult efficiency
        self.utilization_factor = utilization_factor  # Effective compute usage
        
        self.total_peak_flops = self.cores * self.peak_flops_per_core  # TFLOPs
        self.effective_flops = self.total_peak_flops * self.utilization_factor
        self.stage_cycles = []  # Track cycles per stage
        
    def memory_latency(self, access_size):
        """ Estimate memory latency based on access size """
        if access_size <= self.sram_size:
            return 2  # SRAM latency in cycles
        else:
            return 100  # HBM latency in cycles (simplified)
    
    def compute_time(self, ops):
        """ Compute execution time in cycles """
        return ops / (self.effective_flops * 1e12 / 1e9)  # Convert FLOPs to cycles
    
    def transformer_layer_cycles(self, seq_len, hidden_dim):
        """ Estimate cycles for a single transformer layer """
        
        matmul_ops = 2 * seq_len * hidden_dim ** 2  # QK^T, QV, MLP
        softmax_ops = seq_len * hidden_dim  # Softmax complexity
        layernorm_ops = seq_len * hidden_dim  # LayerNorm complexity
        
        compute_cycles = self.compute_time(matmul_ops + softmax_ops + layernorm_ops)
        memory_cycles = self.memory_latency(hidden_dim * seq_len)
        
        total_cycles = compute_cycles + memory_cycles
        
        # Log detailed cycle breakdown
        self.stage_cycles.append({
            "MatMul": compute_cycles,
            "Softmax": self.compute_time(softmax_ops),
            "LayerNorm": self.compute_time(layernorm_ops),
            "Memory": memory_cycles
        })
        
        return total_cycles
    
    def run_model(self, num_layers=24, seq_len=1024, hidden_dim=4096):
        """ Estimate total cycles for a full transformer model """
        total_cycles = 0
        self.stage_cycles.clear()  # Reset log
        
        for _ in range(num_layers):
            total_cycles += self.transformer_layer_cycles(seq_len, hidden_dim)
        
        return total_cycles
    
    def log_cycles(self):
        """ Print detailed cycle breakdown """
        for i, stage in enumerate(self.stage_cycles):
            print(f"Layer {i}: MatMul={stage['MatMul']:.2f} cycles, Softmax={stage['Softmax']:.2f} cycles, \
                  LayerNorm={stage['LayerNorm']:.2f} cycles, Memory={stage['Memory']:.2f} cycles")

class LlamaModel:
    def __init__(self, num_layers=32, seq_len=2048, hidden_dim=4096):
        self.num_layers = num_layers
        self.seq_len = seq_len
        self.hidden_dim = hidden_dim
        self.graph = nx.DiGraph()
        self.build_graph()
    
    def build_graph(self):
        """ Construct a computation graph representing a LLaMA-like model """
        for layer in range(self.num_layers):
            self.graph.add_node(f"Layer {layer}", ops=2 * self.seq_len * self.hidden_dim ** 2)
            if layer > 0:
                self.graph.add_edge(f"Layer {layer - 1}", f"Layer {layer}")
    
    def visualize_graph(self):
        """ Visualize the computation graph """
        plt.figure(figsize=(12, 6))
        nx.draw(self.graph, with_labels=True, node_size=3000, node_color="lightblue")
        plt.title("LLaMA Model Computation Graph")
        plt.show()

# Example Usage
accelerator = MLAccelerator()
total_cycles = accelerator.run_model()
print(f"Total cycles to run transformer model: {total_cycles:.2f}")
accelerator.log_cycles()

llama = LlamaModel()
llama.visualize_graph()

