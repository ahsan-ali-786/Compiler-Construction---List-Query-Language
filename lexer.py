# import re

# TOKEN_SPEC = [
#     ('NUMBER',   r'\d+(\.\d+)?'),
#     ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
#     ('OP',       r'<=|>=|==|!=|<|>|\+|-|\*|/'),
#     ('ASSIGN',   r'='),
#     ('ARROW',    r'->'),
#     ('LBRACK',   r'\['),
#     ('RBRACK',   r'\]'),
#     ('COMMA',    r','),
#     ('NEWLINE',  r'\n'),
#     ('SKIP',     r'[ \t]+'),
# ]

# KEYWORDS = {
#     'list', 'filter', 'sort', 'asc', 'desc', 'map',
#     'mean', 'sum', 'median', 'variance', 'std', 'min',
#     'max', 'count', 'print', 'union', 'intersection',
#     'difference', 'and', 'or', 'xor'
# }

# def lex(code):
#     tokens = []
#     regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
#     for match in re.finditer(regex, code):
#         kind = match.lastgroup
#         value = match.group()
#         if kind == 'ID' and value in KEYWORDS:
#             tokens.append(('KEYWORD', value))
#         elif kind not in ('SKIP', 'NEWLINE'):
#             tokens.append((kind, value))
#     return tokens


import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'col'])

# ── Token specification ───────────────────────────────────────
TOKEN_REGEX = re.compile(r"""
    (?P<NUMBER>\d+(\.\d+)?)              |  # positive numbers only
    (?P<DOLLAR0>\$0)                     |  # $0
    (?P<ARROW>=>)                        |  # arrow for map
    (?P<COMP>>=|<=|==|!=)                |  # two-char comparisons first
    (?P<GT>>)                            |  # then single >
    (?P<LT><)                            |  # then single 
    (?P<ASSIGN>=)                        |  # assignment
    (?P<PLUS>\+)                         |  # arithmetic operators
    (?P<MINUS>-)                         |
    (?P<STAR>\*)                         |
    (?P<SLASH>/)                         |
    (?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)       |  # identifiers & keywords
    (?P<LBRACK>\[)                       |
    (?P<RBRACK>\])                       |
    (?P<LPAREN>\()                       |
    (?P<RPAREN>\))                       |
    (?P<COMMA>,)                         |
    (?P<COMMENT>%[^\n]*)                 |  # comment to end of line
    (?P<WS>[ \t]+)                       |
    (?P<NEWLINE>\r?\n+)                    
""", re.VERBOSE)

# Keywords that become specific token types
KEYWORDS = {
    'list', 'filter', 'sort', 'asc', 'desc', 'map', 'print',
    'mean', 'sum', 'median', 'variance', 'std', 'min', 'max', 'count',
    'union', 'intersection', 'difference',
    'and', 'or', 'xor'  # logical/bitwise operators
}

def lex(source):
    tokens = []
    line, col = 1, 1

    for mo in TOKEN_REGEX.finditer(source):
        kind = mo.lastgroup
        value = mo.group()

        if kind in ('WS', 'COMMENT'):
            pass  # skip whitespace and comments
        elif kind == 'NEWLINE':
            line += value.count('\n')
            col = 1
            continue
        elif kind == 'ID':
            # Check if it's a keyword
            if value in KEYWORDS:
                tokens.append(Token('KEYWORD', value, line, col))
            else:
                tokens.append(Token('ID', value, line, col))
        elif kind in ('PLUS', 'MINUS', 'STAR', 'SLASH'):
            # Unify arithmetic operators as OP
            tokens.append(Token('OP', value, line, col))
        elif kind in ('GT', 'LT', 'COMP'):
            # Unify comparison operators
            tokens.append(Token('COMP', value, line, col))
        else:
            # Keep original token type for others
            tokens.append(Token(kind, value, line, col))

        col += len(value)

    tokens.append(Token('EOF', None, line, col))
    return tokens