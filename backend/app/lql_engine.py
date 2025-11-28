from lexer import lex
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from intermediate_code_generator import TACGenerator
from optimizer import Optimizer
from code_executer import Executor

import io
import sys

def run_lql(code: str) -> dict:
    """
    Runs the full LQL compilation pipeline and returns
    output of every phase for the FastAPI endpoint.
    """

    phases = {
        "tokens": [],
        "parser": [],
        "semantic": "",
        "tac": [],
        "optimized_tac": [],
        "execution_output": "",
    }

    error_phase = None
    error_message = None

    try:
        # =======================
        # 1. LEXER
        # =======================
        try:
            tokens = lex(code)
            phases["tokens"] = [str(t) for t in tokens]
        except Exception as e:
            error_phase = "lexer"
            error_message = str(e)
            raise

        # =======================
        # 2. PARSER → AST
        # =======================
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            phases["parser"] = [str(node.__dict__) for node in ast]
        except Exception as e:
            error_phase = "parser"
            error_message = str(e)
            raise

        # =======================
        # 3. SEMANTIC ANALYSIS
        # =======================
        try:
            sem = SemanticAnalyzer()
            symbol_table = sem.analyze(ast)
            phases["semantic"] = str(symbol_table)
        except Exception as e:
            error_phase = "semantic"
            error_message = str(e)
            raise

        # =======================
        # 4. GENERATE TAC
        # =======================
        try:
            tacgen = TACGenerator()
            tac = tacgen.generate(ast)
            phases["tac"] = [str(instr) for instr in tac]
        except Exception as e:
            error_phase = "tac"
            error_message = str(e)
            raise

        # =======================
        # 5. OPTIMIZER
        # =======================
        try:
            optimizer = Optimizer(tac)
            optimized_tac = optimizer.optimize()
            phases["optimized_tac"] = [str(instr) for instr in optimized_tac]
        except Exception as e:
            error_phase = "optimizer"
            error_message = str(e)
            raise

        # =======================
        # 6. EXECUTION ENGINE
        # =======================
        try:
            exec_engine = Executor(optimized_tac, symbol_table)
            buffer = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buffer

            try:
                exec_engine.run()
            finally:
                sys.stdout = old_stdout

            phases["execution_output"] = buffer.getvalue()
        except Exception as e:
            error_phase = "execution"
            error_message = str(e)
            raise

        return {
            "success": True,
            "error": None,
            "error_phase": None,
            "phases": phases
        }

    except Exception:
        # On any failure, return outputs of previous phases + error info
        return {
            "success": False,
            "error": error_message,
            "error_phase": error_phase,
            "phases": phases
        }
