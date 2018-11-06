import ply.lex as lex

# Reserved Words
# reserved = {
#     'new_project': 'NEW_PROJECT', #Done
#     'add_member': 'ADD_MEMBER', #Done
#     'delete_member' : 'DELETE_MEMBER', #Done
#     'view_members' : 'VIEW_MEMBERS', #Done
#     'create_brainstorm':'CREATE_BRAINSTORM', #Done
#     'add_idea':'ADD_IDEA', #Done
#     'add_task': 'ADD_TASK', #Done
#     'edit_task': 'EDIT_TASK', #Done
#     'delete_task': 'DELETE_TASK', #Done
#     'completed_task': 'COMPLETED_TASK', #Done
#     'assign_task': 'ASSIGN_TASK', #Done
#     'view_brainstorm':'VIEW_BRAINSTORM', #Done
#     'view_schedule': 'VIEW_SCHEDULE', #Done
#     'view_tasks' : 'VIEW_TASKS', #Done
#     'list_today' : 'LIST_TODAY', #Done
#     'list_week' : 'LIST_WEEK', #Done
#     'list_overdue' : 'LIST_OVERDUE', #Done
#     'generate_project' : 'GENERATE_PROJECT', #Done
#     'generate_pie' : 'GENERATE_PIE',
#     'generate_bar' : 'GENERATE_BAR',
#     'generate_line' : 'GENERATE_LINE'
# }

reserved = {
    'define': 'DEFINE',
    'as': 'AS',
    'addWatermark': 'ADD_WATERMARK',
}

#Tokens
tokens = ["NAME","NUMBER","PHRASE","NUMBERLIST","NAMELIST",'LPAREN', 'RPAREN', 'COMMA',"ID","FILE"] + list(reserved.values())


# Simple Regular Expressions
t_ignore = ' \t'
t_NAME = r'[a-zA-Z]+'
t_PHRASE = r'[a-zA-Z ]+'
t_NUMBER = r'[\d+]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'
## NEED regular expression to accept characters and spaces - for tasks

# Define a rule for reserved words
def t_ID(t):
    r'[a-zA-Z]+_[a-zA-Z]+'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Regular expression for list of numbers
def t_LIST(t):
    r'[-?0-9,]+[-?0-9]'
    t.type = 'NUMBERLIST'
    return t
    
# Regular expression for list of words
def t_LIST2(t):
    r'[\'a-zA-z\']+[,\'a-zA-Z\']*'
    t.type = 'NAMELIST'
    return t

def t_LEFTPAREN(t):
    r'[(]'
    t.type = 'LPAREN'
    return t

def t_RIGHTPAREN(t):
    r'[)]'
    t.type = 'RPAREN'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print('Illegal character %s', t.value[0])
    t.lexer.skip(1)
    return t

# Build the lexer
lexer = lex.lex()


testInput = '''addWatermark JVG 535 (fdf)'''
test2= '''(jkl)'''

# input text to test
lexer.input(test2)

# divide input into tokens
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)