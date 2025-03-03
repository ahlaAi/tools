import random

class Cache:
    def __init__(self, name, size, latency, next_level=None):
        self.name = name
        self.size = size
        self.latency = latency
        self.next_level = next_level
        self.cache = set()
        self.accesses = 0
        self.hits = 0
        self.misses = 0
    
    def access(self, address):
        self.accesses += 1
        if address in self.cache:
            self.hits += 1
            return self.latency  # Hit
        else:
            self.misses += 1
            if len(self.cache) >= self.size:
                self.cache.pop()  # Remove an old entry (random eviction)
            self.cache.add(address)
            return self.latency + (self.next_level.access(address) if self.next_level else 0)

class Memory:
    def __init__(self, latency):
        self.latency = latency
        self.accesses = 0
    
    def access(self, address):
        self.accesses += 1
        return self.latency

def simulate(cache_hierarchy, address_sequence):
    total_latency = 0
    latencies = []
    for address in address_sequence:
        latency = cache_hierarchy.access(address)
        latencies.append(latency)
        total_latency += latency
    
    avg_latency = total_latency / len(address_sequence)
    max_latency = max(latencies)
    
    return total_latency, avg_latency, max_latency

if __name__ == "__main__":
    # Define latencies
    L1_LATENCY = 2
    L2_LATENCY = 10
    MEM_LATENCY = 200
    
    # Define cache sizes
    L1_SIZE = 64
    L2_SIZE = 256
    
    # Define memory hierarchy
    memory = Memory(MEM_LATENCY)
    L2_cache = Cache("L2", L2_SIZE, L2_LATENCY, memory)
    L1_cache = Cache("L1", L1_SIZE, L1_LATENCY, L2_cache)
    
    # Generate a sequence of 1000 random addresses
    ADDRESS_SPACE = 1000
    address_sequence = [random.randint(0, ADDRESS_SPACE - 1) for _ in range(1000)]
    
    # Simulate performance
    total_latency, avg_latency, max_latency = simulate(L1_cache, address_sequence)
    
    # Report statistics
    print("--- Simulation Results ---")
    print(f"Total Latency: {total_latency} cycles")
    print(f"Average Latency: {avg_latency:.2f} cycles")
    print(f"Max Latency: {max_latency} cycles")
    print(f"L1 - Accesses: {L1_cache.accesses}, Hits: {L1_cache.hits}, Misses: {L1_cache.misses}")
    print(f"L2 - Accesses: {L2_cache.accesses}, Hits: {L2_cache.hits}, Misses: {L2_cache.misses}")
    print(f"Memory - Accesses: {memory.accesses}")

