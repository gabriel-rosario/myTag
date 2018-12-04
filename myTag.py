import ply.lex as lex
import ply.yacc as yacc
from handlers.videos import Video
from handlers.audio import Audio
from handlers.documents import PDF

tokens = [
            'TYPE',
            'ID',
            'PATH',
            'EQUALS',
            'TAG',
            'STRING',
            'GET',
            'SET',
            'ADD',
            'SAVE',
            'CLEAR'
]

t_EQUALS = r'\='
t_ignore = r' '

def t_TYPE(t):
    r'vid | aud | img | doc'
    t.type = 'TYPE'
    return t

def t_GET(t):
    r'get | GET'
    t.type = 'GET'
    return t

def t_SET(t):
    r'set | SET'
    t.type = 'SET'
    return t

def t_ADD(t):
    r'add | ADD'
    t.type = 'ADD'
    return t

def t_SAVE(t):
    r'save | SAVE'
    t.type = 'SAVE'
    return t

def t_CLEAR(t):
    r'clear | CLEAR'
    t.type = 'CLEAR'
    return t

#TODO: no se puede tener un ID con las palabras TYPE. (ex: audio, vidabuena)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'ID'
    return t

def t_PATH(t):
    r'(/[^:]+)+'
    t.type = "PATH"
    return t

def t_TAG(t):
    r'\< \w+ \>'
    t.type = 'TAG'
    return t

def t_STRING(t):
    r'\"[a-zA-Z0-9_?!@#$%&*-+().~, \t\n]*\"'
    t.type = 'STRING'
    return t

def t_error(t):
    print("Illegal character!")
    t.lexer.skip(len(s))

lexer = lex.lex()


var = {}


def p_mytag(p):
     '''
     mytag : assign
           | function
           | empty
     '''

#TODO: se supone que si no existe el id en type_value solo puede aceptar path
def p_var_assign(p):
    '''
    assign : TYPE ID EQUALS type_value
           | ID EQUALS id_value
    '''
    obj = None
    if(len(p) == 5):
        if p[4] in var:
            value = var[p[4]][1] #if var exists, the value of the var is assigend as the value of new var
        else:
             value = p[4] #if var does not exist, the input is assigend as the value of the new var
        type = p[1]
        if(type == 'vid'):
            try:
                obj = Video(str(value))
            except AssertionError as e:
                print(e)
        elif(type == 'aud'):
            try:
                obj = Audio(str(value))
            except AssertionError as e:
                print(e)
        elif(type == 'img'):
            try:
                obj = Image(str(value))
            except AssertionError as e:
                print(e)
        elif(type == 'doc'):
            try:
                obj = PDF(str(value))
            except AssertionError as e:
                print(e)
        var[p[2]] = [type, obj]
    else:
        var[p[1]] = [None, p[3].replace('"', '')]

def p_function(p):
    '''
    function : get_function
             | set_function
             | add_function
             | show_function
             | save_function
             | clear_function
    '''

def p_get_function(p):
    '''
    get_function : GET ID
                 | GET ID TAG
    '''
    if p[2] in var:
        if(len(p) == 3):
            print(var[p[2]])
        else:
            type = var[p[2]][0]
            obj = var[p[2]][1]
            tag = str(p[3]).replace('<', '').replace('>', '')
            if(type == 'vid'):
                try:
                    print(obj.get_tag(tag))
                except AssertionError as e:
                    print(e)
            elif(type == 'aud'):
                try:
                    print(obj.get_tag(tag))
                except AssertionError as e:
                    print(e)
            elif(type == 'img'):
                print("test")
            elif(type == 'doc'):
                try:
                    print(obj.get_tag(tag))
                except AssertionError as e:
                    print(e)
            else:
                print(p[2] + ' is not a valid ID for GET')
    else:
        print(p[2] + ' is not a valid ID')

def p_set_func(p):
    '''
    set_function : SET ID TAG EQUALS set_value
    '''
    if p[2] in var:
        type = var[p[2]][0]
        obj = var[p[2]][1]
        tag = p[3].replace('<', '').replace('>', '')
        value = p[5].replace('"', '')
        if(type == 'vid'):
            if(tag == 'artwork'):
                try:
                    obj.set_artwork(value)
                except AssertionError as e:
                    print(e)
            else:
                try:
                    obj.set_tag(tag, value)
                except AssertionError as e:
                    print(e)
        elif(type == 'aud'):
            if(tag == 'artwork'):
                try:
                    obj.set_artwork(value)
                except AssertionError as e:
                    print(e)
            else:
                try:
                    obj.set_tag(tag, value)
                except AssertionError as e:
                    print(e)
        elif(type == 'img'):
            #obj.set
            print('test')
        elif(type == 'doc'): #TODO: toc
            if(tag == 'watermark'):
                obj.set_watermark(value)
            if(tag == 'toc'):
                obj.set_toc(value)
            else:
                try:
                    obj.set_tag(tag, value)
                except AssertionError as e:
                    print(e)
        else:
            print(p[2] + ' is not a valid ID for SET')
    else:
        print(p[2] + ' is not a valid ID')

def p_add_function(p):
    '''
    add_function : ADD ID TAG EQUALS set_value
                 | ADD ID TAG EQUALS set_value set_value
    '''
    if p[2] in var:
        type = var[p[2]][0]
        obj = var[p[2]][1]
        tag = p[3].replace('<', '').replace('>', '')
        value = p[5].replace('"', '')
        if(type == 'vid'):
            if(tag == 'sub'):
                try:
                    if(len(p) == 7):
                        lang = p[6]
                    obj.add_subs(value, lang)
                except AssertionError as e:
                    print(e)
            elif(tag == 'chapter'):
                obj.chapter_split(int(value))
        elif(type == 'aud'):
            #obj.set
            print('test')
        elif(type == 'img'):
            #obj.set
            print('test')
        elif(type == 'doc'):
            #obj.set
            print('test')
        else:
            print(p[2] + ' is not a valid ID for ADD')
    else:
        print(p[2] + ' is not a valid ID')

def p_show_function(p):
    '''
    show_function : ID
    '''
    if p[1] in var:
        print('Type: ' + str(var[p[1]][0]) + '\nValue: ' + var[p[1]][1])
    else:
        print("NameError: name \'" + p[1] + "\' is not defined")

def p_save_func(p):
    '''
    save_function : SAVE ID
    '''
    if p[2] in var:
        type = var[p[2]][0]
        obj = var[p[2]][1]
        if(type == 'vid'):
            obj.save()
        elif(type == 'aud'):
            obj.save()
        elif(type == 'img'):
            #obj.save()
            print('test')
        elif(type == 'doc'):
            obj.save()
    else:
        print(p[2] + ' is not a valid ID')

def p_clear_func(p):
    '''
    clear_function : CLEAR ID
    '''
    if p[2] in var:
        type = var[p[2]][0]
        obj = var[p[2]][1]
        if(type == 'vid'):
            obj.clear()
        elif(type == 'aud'):
            obj.clear()
    else:
        print(p[2] + ' is not a valid ID')

def p_type_value(p):
    '''
    type_value : PATH
               | ID
    '''
    p[0] = p[1]

def p_set_value(p):
    '''
    set_value : ID
              | STRING
              | PATH
    '''
    p[0] = p[1]

def p_id_value(p):
    '''
    id_value : PATH
             | STRING
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None
    #print(var) #for testing purposes

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

while True:
    try:
        s = input(">>> ")
        if s == "exit":
            break
    except EOFError:
        break
    parser.parse(s)
