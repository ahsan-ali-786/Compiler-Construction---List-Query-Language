📘 Lexer (Tokenizer) Documentation

The Lexer (also called a scanner or tokenizer) is responsible for converting raw program text into a sequence of tokens that the parser can understand.
It uses regular expressions to match keywords, identifiers, operators, numbers, and symbols.

# 🔹 1. Token Structure

Tokens are represented with a namedtuple:

Token = namedtuple('Token', ['type', 'value', 'line', 'col'])

Each token contains:

Field Meaning
type Category of the token (e.g., NUMBER, KEYWORD, ID, OP)
value Actual lexeme matched
line Line number in the source
col Column number where the token begins

# 🔹 2. Token Specification (Regex Rules)

The lexer uses a single combined regex (TOKEN_REGEX) with named groups to match lexemes:

### ✔ Supported Token Types

Token Meaning
NUMBER Integers and decimals (optional -)
DOLLAR0 Special variable $0 for mapping
ARROW => used in map expressions
COMP Comparison operators: >= <= == !=
GT >
LT <
ASSIGN =
PLUS / MINUS / STAR / SLASH / MOD Arithmetic operators
ID Identifiers or keywords
LBRACK / RBRACK [ and ]
LPAREN / RPAREN ( and )
COMMA ,
COMMENT Line comments starting with @
WS Whitespace
NEWLINE \n or \r\n

# 🔹 3. Keyword Handling

Identifiers matched as ID are further categorized:

KEYWORDS = {
'list', 'filter', 'sort', 'asc', 'desc', 'map', 'print',
'mean', 'sum', 'median', 'variance', 'std', 'min', 'max', 'count',
'union', 'intersection', 'difference',
'and', 'or', 'xor'
}

If an identifier matches one of these, it becomes:

Token('KEYWORD', value, line, col)

Else it remains:

Token('ID', value, line, col)

# 🔹 4. The lex() Function

This is the main entry point for tokenizing source code.

def lex(source):
tokens = []
line, col = 1, 1
pos = 0

It scans the entire program and builds a token stream for the parser.

## ✔ 4.1 Matching Tokens

The lexer iterates over all regex matches:

for mo in TOKEN_REGEX.finditer(source):

For each match:

It checks for unmatched text (invalid lexeme).

Determines the token type (mo.lastgroup).

Converts identifiers to keywords if necessary.

Handles whitespace, comments, and newlines.

Appends valid tokens to the token list.

## ✔ 4.2 Line & Column Tracking

Every lexeme updates column position:

col += len(value)

Newlines reset column and increment line count:

line += value.count('\n')
col = 1

## ✔ 4.3 Handling Errors

If the regex skips text (invalid characters):

raise SyntaxError(
f"Invalid lexeme '{invalid_text}' at line {line}, col {col}"
)

Same for any unmatched trailing text at the end.

## ✔ 4.4 Token Normalization

The lexer converts certain tokens:

👉 Arithmetic Operators

+, -, \*, /, % → Token('OP', value)

👉 Comparison Operators

> =, <=, ==, !=, >, < → Token('COMP', value)

👉 Whitespace & Comments

Discarded automatically.

# 🔹 5. End-of-File Token

Finally, the lexer appends:

Token('EOF', None, line, col)

The parser uses this to detect the end of input.

# 🔹 6. Example Output

Input:

list x = [1,2,3]

Lexer produces:

KEYWORD list
ID x
ASSIGN =
LBRACK [
NUMBER 1
COMMA ,
NUMBER 2
COMMA ,
NUMBER 3
RBRACK ]
EOF

🎉 Summary

The lexer is responsible for:

✔ Tokenizing the input
✔ Converting identifiers into keywords
✔ Handling operators, numbers, arrays, map syntax
✔ Tracking line/column positions
✔ Error reporting for invalid lexemes
✔ Producing a clean, structured token stream for the parser

This completes the lexical analysis phase of your compiler.
