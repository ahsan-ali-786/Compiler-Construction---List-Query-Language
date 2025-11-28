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


snippet = code[7];
tokens = lex(snippet);


print("-----------");
print(" TOKENS: ");
print("-----------");
for tok in tokens:
    print(tok);
    
print();

print("-----------");
print(" PARSER: ");
print("-----------");
parser = Parser(tokens)
ast = parser.parse()

for node in ast:
    print(node.__dict__)

print();

print("-----------");
print(" SEMANTIC: ");
print("-----------");
    
sem = SemanticAnalyzer()
symbol_table = sem.analyze(ast)

print("Semantic OK! Symbol Table:")
print(symbol_table)

print();

print("-----------");
print(" TAC: ");
print("-----------");

tacgen = TACGenerator()
tac = tacgen.generate(ast)
TACGenerator.pretty_print(tac)

print();

print("-----------");
print(" Optimizer: ");
print("-----------");

optimizer = Optimizer(tac)
optimized_tac = optimizer.optimize()

TACGenerator.pretty_print(optimized_tac)

print();



print("-----------");
print(" CODE: ");
print("-----------");
print(snippet);

print("-----------");
print(" Executer: ");
print("-----------");

exec_engine = Executor(tac, symbol_table)
exec_engine.run()
