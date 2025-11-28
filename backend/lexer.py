import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'col'])

# ── Token specification ───────────────────────────────────────
TOKEN_REGEX = re.compile(r"""
    (?P<NUMBER>-?\d+(\.\d+)?)            |
    (?P<DOLLAR0>\$0)                     |  # $0
    (?P<ARROW>=>)                        |  # arrow for map
    (?P<COMP>>=|<=|==|!=)                |  # two-char comparisons first
    (?P<GT>>)                            |  # then single >
    (?P<LT><)                            |  # then single 
    (?P<ASSIGN>=)                        |  # assignment
    (?P<PLUS>\+)                         |  # arithmetic operators
    (?P<MINUS>-)                         |
    (?P<STAR>\*)                         |
    (?P<MOD>%)                           |
    (?P<SLASH>/)                         |
    (?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)       |  # identifiers & keywords
    (?P<LBRACK>\[)                       |
    (?P<RBRACK>\])                       |
    (?P<LPAREN>\()                       |
    (?P<RPAREN>\))                       |
    (?P<COMMA>,)                         |
    (?P<COMMENT>@[^\n]*)                 |  # comment to end of line
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
    pos = 0  # track current position in source

    for mo in TOKEN_REGEX.finditer(source):
        if mo.start() > pos:
            # There is unmatched text before this match → invalid lexeme
            invalid_text = source[pos:mo.start()]
            raise SyntaxError(f"Invalid lexeme '{invalid_text}' at line {line}, col {col}")

        kind = mo.lastgroup
        value = mo.group()

        if kind in ('WS', 'COMMENT'):
            pass
        elif kind == 'NEWLINE':
            line += value.count('\n')
            col = 1
            pos = mo.end()
            continue
        elif kind == 'ID':
            if value in KEYWORDS:
                tokens.append(Token('KEYWORD', value, line, col))
            else:
                tokens.append(Token('ID', value, line, col))
        elif kind in ('PLUS', 'MINUS', 'STAR', 'SLASH', 'MOD'):
            tokens.append(Token('OP', value, line, col))
        elif kind in ('GT', 'LT', 'COMP'):
            tokens.append(Token('COMP', value, line, col))
        else:
            tokens.append(Token(kind, value, line, col))

        col += len(value)
        pos = mo.end()  # update position

    if pos < len(source):
        # trailing unmatched text
        invalid_text = source[pos:]
        raise SyntaxError(f"Invalid lexeme '{invalid_text}' at line {line}, col {col}")

    tokens.append(Token('EOF', None, line, col))
    return tokens
