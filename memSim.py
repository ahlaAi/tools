import random
import matplotlib.pyplot as plt

class DRAM:
    def __init__(self, page_size=4096, req_size=256, policy='open', hit_latency=50, miss_latency=100, banks=4, ranks=2):
        self.page_size = page_size
        self.req_size = req_size
        self.policy = policy
        self.banks = banks
        self.ranks = ranks
        self.row_buffers = [[None for _ in range(banks)] for _ in range(ranks)]
        self.hits = 0
        self.misses = 0
        self.hit_latency = hit_latency
        self.miss_latency = miss_latency
    
    def access(self, address):
        rank = (address // (self.page_size * self.banks)) % self.ranks
        bank = (address // self.page_size) % self.banks
        row_address = address // self.page_size
        
        if self.row_buffers[rank][bank] == row_address:
            self.hits += 1  # Row buffer hit
        else:
            self.misses += 1  # Row buffer miss
            self.row_buffers[rank][bank] = row_address if self.policy == 'open' else None  # Update row buffer if open
    
    def reset(self):
        self.hits = 0
        self.misses = 0
        self.row_buffers = [[None for _ in range(self.banks)] for _ in range(self.ranks)]
    
    def compute_latency(self):
        access_latencies = [self.hit_latency] * self.hits + [self.miss_latency] * self.misses
        average_latency = sum(access_latencies) / len(access_latencies)
        max_latency = max(access_latencies)
        return average_latency, max_latency, access_latencies

# Initialize DRAM with Open Page policy
dram = DRAM(page_size=4096, req_size=256, policy='open', hit_latency=50, miss_latency=100, banks=4, ranks=2)

# Generate sequential access pattern
base_address = 0x100000  # Arbitrary base address for simulation
stride = 512  # 512B stride

for i in range(500):
    address = base_address + i * stride
    dram.access(address)

# Generate random access pattern
random_addresses = [random.randint(0x100000, 0x200000) for _ in range(500)]
for address in random_addresses:
    dram.access(address)

# Compute latency statistics
average_latency, max_latency, access_latencies = dram.compute_latency()

# Plot latency distribution
plt.figure(figsize=(8, 5))
plt.hist(access_latencies, bins=[49, 51, 99, 101], align='mid', rwidth=0.8)
plt.xticks([50, 100], ['Hit (50 cycles)', 'Miss (100 cycles)'])
plt.xlabel("Access Latency (cycles)")
plt.ylabel("Number of Requests")
plt.title("Memory Access Latency Distribution")
plt.show()

# Print results
print(f"Row Buffer Hits: {dram.hits}")
print(f"Row Buffer Misses: {dram.misses}")
print(f"Average Latency: {average_latency} cycles")
print(f"Max Latency: {max_latency} cycles")

