from code_executer import Executor
from intermediate_code_generator import TACGenerator
from lexer import lex
from optimizer import Optimizer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from lql_code_examples import code


# list data = [1, 2, 3, 4]
# list big = filter data >= 3
# list sq = map data $0 => $0 * $0 + (10 + 7) % 18, 21, 26, 33
# list result = sq + [5, 6, 1, 3] % 23, 27, 27, 36
# sort result desc
# print result
# print mean result

# list union_res = data union [3,4,59,10]
# print union_res


# snippet = code[18];

# for i in range(0, len(code)):
    
#     # if not i == 5:
#     #     continue; 

#     print(f"\n{i + 1} - CODE: ");
#     snippet = code[i];
#     tokens = lex(snippet);


#     print("-----------");
#     print(" TOKENS: ");
#     print("-----------");
#     for tok in tokens:
#         print(tok);
        
#     print();

#     print("-----------");
#     print(" PARSER: ");
#     print("-----------");
#     parser = Parser(tokens)
#     ast = parser.parse()

#     for node in ast:
#         print(node.__dict__)

#     print();

#     print("-----------");
#     print(" SEMANTIC: ");
#     print("-----------");
        
#     sem = SemanticAnalyzer()
#     symbol_table = sem.analyze(ast)

#     print("Semantic OK! Symbol Table:")
#     print(symbol_table)

#     print();

#     print("-----------");
#     print(" TAC: ");
#     print("-----------");

#     tacgen = TACGenerator()
#     tac = tacgen.generate(ast)
#     TACGenerator.pretty_print(tac)

#     print();

#     print("-----------");
#     print(" Optimizer: ");
#     print("-----------");

#     optimizer = Optimizer(tac)
#     optimized_tac = optimizer.optimize()

#     TACGenerator.pretty_print(optimized_tac)

#     print();



#     print("-----------");
#     print(" CODE: ");
#     print("-----------");
#     print(snippet);

#     print("-----------");
#     print(" Executer: ");
#     print("-----------");

#     exec_engine = Executor(tac, symbol_table)
#     exec_engine.run()


output_file = "result.txt"

# open file in write mode every time you run the tests
with open(output_file, "w", encoding="utf-8") as f:

    for i in range(len(code)):

        snippet = code[i]

        # Header for this test case
        f.write(f"\n{i+1} - CODE:\n")
        f.write(snippet + "\n\n")

        # ========== TOKENS ==========
        tokens = lex(snippet)
        f.write("-----------\n TOKENS:\n-----------\n")
        for tok in tokens:
            f.write(str(tok) + "\n")
        f.write("\n")

        # ========== PARSER ==========
        f.write("-----------\n PARSER:\n-----------\n")
        parser = Parser(tokens)
        ast = parser.parse()
        for node in ast:
            f.write(str(node.__dict__) + "\n")
        f.write("\n")

        # ========== SEMANTIC ANALYSIS ==========
        f.write("-----------\n SEMANTIC:\n-----------\n")
        sem = SemanticAnalyzer()
        symbol_table = sem.analyze(ast)
        f.write("Semantic OK! Symbol Table:\n")
        f.write(str(symbol_table) + "\n\n")

        # ========== TAC ==========
        f.write("-----------\n TAC:\n-----------\n")
        tacgen = TACGenerator()
        tac = tacgen.generate(ast)
        for instr in tac:
            f.write(str(instr) + "\n")
        f.write("\n")

        # ========== OPTIMIZER ==========
        f.write("-----------\n Optimizer:\n-----------\n")
        optimizer = Optimizer(tac)
        optimized_tac = optimizer.optimize()
        for instr in optimized_tac:
            f.write(str(instr) + "\n")
        f.write("\n")

        # ========== EXECUTION ==========
        f.write("-----------\n Executer:\n-----------\n")

        # Write code again inside executer section  
        f.write("CODE:\n")
        f.write(snippet + "\n\n")

        # Execute and capture printed output
        exec_engine = Executor(optimized_tac, symbol_table)

        import io, sys
        buffer = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer
        
        try:
            exec_engine.run()
        finally:
            sys.stdout = old_stdout

        exec_output = buffer.getvalue()

        f.write("OUTPUT:\n")
        f.write(exec_output + "\n")

        # ========== END SEPARATOR ==========
        f.write("============================================================================\n")


        # ========== END SEPARATOR ==========
        f.write("============================================================================\n")
