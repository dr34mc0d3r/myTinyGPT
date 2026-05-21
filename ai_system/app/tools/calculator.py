from app.tools.base import Tool

class CalculatorTool(Tool):
    """
    Simple calculator tool.
    """
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluates mathematical expressions. Input: 'expression' (str)."

    def execute(self, expression: str) -> str:
        try:
            # Note: eval is used here for simplicity in an educational project,
            # but should be restricted or replaced by a safer parser in production.
            # We restrict globals and locals for a bit of safety.
            allowed_names = {
                "abs": abs, "round": round, "max": max, "min": min, "pow": pow,
                "sum": sum, "len": len
            }
            return str(eval(expression, {"__builtins__": None}, allowed_names))
        except Exception as e:
            return f"Error: {str(e)}"
