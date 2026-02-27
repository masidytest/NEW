# plugins/example_math.py
# Example plugin: Extended math operations

def register(cap_registry):
    """Register math plugin capabilities"""
    
    def tool_double(x: float) -> float:
        """Double a number"""
        return x * 2
    
    def tool_square(x: float) -> float:
        """Square a number"""
        return x ** 2
    
    def tool_factorial(n: int) -> int:
        """Calculate factorial"""
        if n < 0:
            return 0
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    # Register capabilities
    cap_registry.register(
        name="double_number",
        func=tool_double,
        tags=["math", "utility", "plugin"],
        input_schema={"x": "float"},
        output_schema={"result": "float"},
        description="Double a number (plugin)"
    )
    
    cap_registry.register(
        name="square_number",
        func=tool_square,
        tags=["math", "utility", "plugin"],
        input_schema={"x": "float"},
        output_schema={"result": "float"},
        description="Square a number (plugin)"
    )
    
    cap_registry.register(
        name="factorial",
        func=tool_factorial,
        tags=["math", "utility", "plugin"],
        input_schema={"n": "int"},
        output_schema={"result": "int"},
        description="Calculate factorial of a number (plugin)"
    )
