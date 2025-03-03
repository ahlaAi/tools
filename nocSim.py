import random
from collections import deque

class Packet:
    def __init__(self, src, dest, cycle_created):
        self.src = src  # (x, y) coordinates
        self.dest = dest
        self.cycle_created = cycle_created
        self.cycle_delivered = None

class Node:
    def __init__(self, x, y, is_memory=False):
        self.x, self.y = x, y
        self.is_memory = is_memory
        self.queue = deque()
        self.received_packets = []

    def inject_packet(self, grid_size, cycle):
        if random.random() < 0.3:  # 30% chance to inject a packet
            dest = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
            if dest != (self.x, self.y):  # Ensure it's not the same node
                packet = Packet((self.x, self.y), dest, cycle)
                self.queue.append(packet)

    def receive_packet(self, packet, cycle, memory_delay=200):
        packet.cycle_delivered = cycle + memory_delay  # Simulate memory access delay
        self.received_packets.append(packet)

class NoCSimulator:
    def __init__(self, grid_size=4, memory_delay=200):
        self.grid_size = grid_size
        self.memory_delay = memory_delay
        self.nodes = [[Node(x, y, is_memory=(random.random() < 0.2)) for y in range(grid_size)] for x in range(grid_size)]
        self.total_packets = 0
        self.total_latency = 0
        
    def route_packet(self, packet):
        src_x, src_y = packet.src
        dest_x, dest_y = packet.dest
        
        if src_x < dest_x:
            src_x += 1
        elif src_x > dest_x:
            src_x -= 1
        elif src_y < dest_y:
            src_y += 1
        elif src_y > dest_y:
            src_y -= 1
        
        if (src_x, src_y) == packet.dest:
            return (src_x, src_y), True
        return (src_x, src_y), False
    
    def run(self, cycles=20):
        for cycle in range(cycles):
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    node = self.nodes[x][y]
                    node.inject_packet(self.grid_size, cycle)
                    
                    new_queue = deque()
                    while node.queue:
                        packet = node.queue.popleft()
                        next_pos, delivered = self.route_packet(packet)
                        
                        if delivered:
                            self.nodes[next_pos[0]][next_pos[1]].receive_packet(packet, cycle, self.memory_delay)
                            self.total_packets += 1
                            self.total_latency += (packet.cycle_delivered - packet.cycle_created)
                        else:
                            self.nodes[next_pos[0]][next_pos[1]].queue.append(packet)
        
        avg_latency = self.total_latency / self.total_packets if self.total_packets > 0 else 0
        print(f"Total Packets Delivered: {self.total_packets}")
        print(f"Average Latency: {avg_latency:.2f} cycles")

if __name__ == "__main__":
    simulator = NoCSimulator(grid_size=8, memory_delay=200)
    simulator.run(cycles=1000)

