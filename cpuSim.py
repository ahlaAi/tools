from collections import deque

class CPU:
    STAGES = ["Fetch", "Decode", "Execute", "Memory", "WriteBack"]
    
    def __init__(self, instructions):
        self.instructions = instructions  # List of instructions
        self.pipeline = deque(maxlen=5)  # 5-stage pipeline
        self.clock_cycle = 0
        self.pc = 0  # Program counter
        self.pipeline_width = 1  # Single-issue execution
        self.active_instructions = []  # Track active instructions with their progress
        self.results = []  # Store simulation results

    def run(self):
        while self.pc < len(self.instructions) or self.active_instructions:
            self.clock_cycle += 1
            self.advance_pipeline()
            self.record_pipeline_state()
            self.print_pipeline_graph()

    def advance_pipeline(self):
        # Remove completed instructions
        self.active_instructions = [inst for inst in self.active_instructions if inst[1] < 5]
        
        # Move instructions forward in the pipeline
        for i in range(len(self.active_instructions)):
            self.active_instructions[i] = (self.active_instructions[i][0], self.active_instructions[i][1] + 1)
        
        # Fetch one new instruction per cycle
        if self.pc < len(self.instructions):
            inst = self.instructions[self.pc]
            self.active_instructions.append((inst, 1))  # New instruction starts at stage 1
            self.pc += 1
    
    def record_pipeline_state(self):
        pipeline_state = {stage: [] for stage in self.STAGES}
        for inst, stage in self.active_instructions:
            pipeline_state[self.STAGES[stage - 1]].append(inst)
        self.results.append(f"Cycle {self.clock_cycle}: {pipeline_state}")
    
    def print_pipeline_graph(self):
        print(f"Cycle {self.clock_cycle}")
        print("Pipeline:")
        for stage, name in enumerate(self.STAGES, 1):
            instructions_in_stage = [inst for inst, stg in self.active_instructions if stg == stage]
            print(f"{name}: {instructions_in_stage}")
        print("Current Pipeline State:")
        for stage, name in enumerate(self.STAGES, 1):
            print(f"{name}: {', '.join([inst for inst, stg in self.active_instructions if stg == stage])}")
        print("-" * 40)

# Example usage
instructions = [
    "ADD R1, R2, R3", "SUB R4, R5, R6", "LOAD R7, 100(R8)", "STORE R9, 200(R10)", 
    "MUL R11, R12, R13", "ADD R2, R1, R5", "LOAD R5, 300(R6)", "STORE R8, 400(R9)", 
    "DIV R10, R11, R12", "ADD R6, R7, R8"
]

cpu = CPU(instructions)
cpu.run()

