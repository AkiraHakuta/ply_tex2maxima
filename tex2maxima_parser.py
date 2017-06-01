# tex2maxima_parser.py   Author: Akira Hakuta, Date: 2017/05/27
# python.exe tex2maxima_parser.py

from ply import yacc
# Get the token map
from tex2maxima_lexer import tokens, lexer

import subprocess
import re

# set maxima_bat
maxima_bat='C:\\maxima-5.39.0\\bin\\maxima.bat'

MULT_SP=0
MULT_NSP=1
MULT_CDOT=2
MULT_TIMES=3

# variable : a,b,...,z,A,...,Z,\alpha,\beta,\gamma,\theta,\omega
# constant : pi --> \ppi, imaginary unit --> \ii, napier constant --> \ee

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UPLUS', 'UMINUS'),  
    ('right', 'EXPONENT'),    
    )


# Parsing rules
# Functions should be start with `p_`.

# statement : expr
def p_statement(p):
    'statement : expr'
    p[0] = p[1]

# expr : expr^expr
def p_expr_exponent(p):
    'expr : expr EXPONENT expr'
    #p[0]  p[1] p[2]   p[3]
    p[0] = '({})^({})'.format(p[1], p[3])
    
# expr : expr !
def p_expr_factorial(p):
    'expr : expr FACTORIAL'
    p[0] = 'factorial({})'.format(p[1])
    
    
# expr : expr*expr | expr \times expr | expr CDOT expr
def p_expr_mult(p):
    'expr : expr MULT expr'
    p[0] = '{}*{}'.format(p[1],p[3])
    
# expr : expr expr    
def p_expr_exprexpr(p):
    'expr : expr expr'
    p[0] = '{}*{}'.format(p[1],p[2])
              
# expr : expr \div expr
def p_expr_div(p):
    'expr : expr DIV expr'
    p[0] = '{}*(({})^(-1))'.format(p[1],p[3])
    

# expr : expr+expr
def p_expr_plus(p):
    'expr : expr PLUS expr'
    p[0] = '{}+{}'.format(p[1], p[3])


# expr : expr-expr
def p_expr_minus(p):
    'expr : expr MINUS expr'
    p[0] = '{}-{}'.format(p[1], p[3])
    
# expr : {expr}
def p_expr_brace(p):
    'expr : LBRACE expr RBRACE'
    p[0] = '({})'.format(p[2])

# expr : (expr)
def p_expr_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = '({})'.format(p[2])

# expr : [a-zA-Z]
def p_expr_symbol(p):
    'expr : ALPHABET'
    p[0] = p[1]
    
# expr : %alpha|%beta|%Gamma|%theta|%omega
def p_expr_greek_ch(p):
    'expr : GREEK_CH'
    p[0] = p[1]

# expr : +expr
def p_expr_plus_expr(p):
    'expr : PLUS expr %prec UPLUS' # override precedence of PLUS by `%prec UPLUS`
    p[0] = p[2]

# expr : -expr
def p_expr_minus_expr(p):
    'expr : MINUS expr %prec UMINUS' # override precedence of MINUS by `%prec UMINUS`
    p[0] = '(-1)*({})'.format(p[2])
    
# expr : pi
def p_expr_pi(p):
    'expr : PI'
    p[0] = '%pi'
 
# expr : imaginary_unit    
def p_expr_imaginary_unit(p):
    'expr : IMAGINARY_UNIT'
    p[0] = '%i'

# expr : napier_constant
def p_expr_napier_constant(p):
    'expr : NAPIER_CONSTANT'
    p[0] = '%e'   

# expr : infty
def p_expr_infty(p):
    'expr : INFTY'
    p[0] = 'inf'

# expr :  \d+  
def p_expr_integer(p):
    'expr : NN_INTEGER'
    p[0] = p[1]
 
# expr :  \d*\.\d+ 
def p_expr_float(p):
    'expr : NN_FLOAT'
    #p[0] = 'nsimplify(Rational({}))'.format(p[1])
    p[0] = 'ratsimp({})'.format(p[1])
        
# expr : \sqrt{expr}
def p_expr_sqrt1(p):
    'expr : F_SQRT LBRACE expr RBRACE'
    p[0] = 'sqrt({})'.format(p[3])    
    
# expr : \sqrt[expr]{expr}
def p_expr_sqrt2(p):
    'expr : F_SQRT LBRACKET expr RBRACKET LBRACE expr RBRACE'
    #p[0] = '(root(({}),({})))'.format(p[6],p[3])
    p[0] = '(({})^(({})^(-1)))'.format(p[6],p[3])

# expr : \frac{expr}{expr}
def p_expr_frac(p):
    'expr : F_FRAC LBRACE expr RBRACE LBRACE expr RBRACE'
    p[0] = '({}) * ({})^(-1)'.format(p[3], p[6])   

# expr : \sin{expr} | \cos{expr} | \tan{expr} 
def p_expr_f_trigonometric(p):
    'expr : F_TRIG LBRACE expr RBRACE'
    p[0] = '{}({})'.format(p[1][1:], p[3])
     
# expr : \log{expr}
def p_expr_f_log(p):
    'expr : F_LOG LBRACE expr RBRACE'
    p[0] = 'log({})'.format(p[3])

# expr : \sin^{expr}{expr} | \cos^{expr}{expr} | \tan^{expr}{expr} 
def p_expr_f_trigonometric_car(p):
    'expr : F_TRIG_CAR LBRACE expr RBRACE LBRACE expr RBRACE'
    p[0] = '({}({}))^({})'.format(p[1][1:4],p[6],p[3])  

# expr : \log_{expr}{expr}
def p_expr_f_log_ub(p):
    'expr : F_LOG_UB LBRACE expr RBRACE LBRACE expr RBRACE '
    p[0] = 'log({})*(log({})^(-1))'.format(p[6],p[3])
    
# expr : \sum_{k=expr}^{expr}{expr}
def p_expr_sum(p):
    'expr : F_SUM  UB LBRACE ALPHABET EQUAL expr  RBRACE EXPONENT LBRACE expr RBRACE LBRACE expr RBRACE'
    p[0] = 'nusum({},{},{},{})'.format(p[13],p[4],p[6],p[10])
 
# expr : \frac{d}{dx} {expr}
def p_expr_diff(p):
    'expr : DIFF LBRACE DX RBRACE LBRACE expr RBRACE'
    x=p[3][1:]    
    if x=='%alpha' or x=='%beta' or x=='%Gamma' or x=='%theta' or x=='%omega':
        p[0] = 'diff({},{},1)'.format(p[6], p[3][1:])
    else:
        p[0] = 'diff({},{},1)'.format(p[6], p[3][1]) 
    
# expr : \int{expr dx}
def p_expr_int(p):
    'expr : F_INT LBRACE expr DX RBRACE'
    x=p[4][1:]
    if x=='%alpha' or x=='%beta' or x=='%Gamma' or x=='%theta' or x=='%omega':
        p[0] = 'integrate({},{})'.format(p[3],p[4][1:])
    else:
        p[0] = 'integrate({},{})'.format(p[3],p[4][1])    

# expr : \int^{expr}_{expr}{expr dx}
def p_expr_definite_int(p):
    'expr : F_INT UB LBRACE expr RBRACE EXPONENT LBRACE expr RBRACE LBRACE expr DX RBRACE'
    x=p[8][1:]
    if x=='%alpha' or x=='%beta' or x=='%Gamma' or x=='%theta' or x=='%omega':
        p[0] = 'integrate({},{},{},{})'.format(p[11],p[12][1:],p[4],p[8])
    else:
        p[0] = 'integrate({},{},{},{})'.format(p[11],p[12][1],p[4],p[8])
    
# expr : \lim_{expr->expr}{expr}
def p_expr_lim(p):
    'expr : LIM UB LBRACE expr TO expr RBRACE LBRACE expr RBRACE'
    p[0] = 'limit({}, {}, {})'.format(p[9],p[4],p[6])
    
# expr : a_{expr}
def p_expr_seq_term(p):
    'expr : F_SEQ_TERM LBRACE expr RBRACE'
    p[0] = 'a({})'.format(p[3]) 
          
# expr : _{expr}C_{expr} |  _{expr}P_{expr}
def p_expr_combi_or_permutation(p):
    'expr : UB LBRACE expr RBRACE COMBI_PERMU UB LBRACE expr RBRACE'
    if p[5] == r'\C':
        p[0] = 'combination({},{})'.format(p[3],p[8])
    elif p[5] == r'\P':
        p[0] = 'permutation({},{})'.format(p[3],p[8])
        
# expr : \left| expr \right|
def p_expr_abs(p):
    'expr : LPIPE expr RPIPE'
    p[0] = 'abs({})'.format(p[2])        
       


# statement : expr = expr
def p_statement_equal_expr(p):
    'statement : expr EQUAL expr'
    p[0] = '({})=({})'.format(p[1],p[3])
  
# statement : expr > expr | expr < expr | expr >= expr | expr <= expr |
def p_statement_relation_expr(p):
    'statement : expr RELATION expr'
    if p[2] == '>':
        p[0] = '{}>{}'.format(p[1],p[3])
    elif p[2] == '<':
        p[0] = '{}<{}'.format(p[1],p[3])
    elif p[2] == '\\geqq':
        p[0] = '{}>={}'.format(p[1],p[3])
    elif p[2] == '\\leqq':
        p[0] = '{}<={}'.format(p[1],p[3])   
        
# statement : statement , statement    
def p_statement_statemant_comma_statement(p):
    'statement : statement COMMA statement'
    p[0] = '{},{}'.format(p[1],p[3])


# Rule for error handling
def p_error(t):
    print("syntax error at '%s'" % (t.value))



# Generating LALR tables
#parser = yacc.yacc()
parser=yacc.yacc(errorlog=yacc.NullLogger())# to completely silence warnings

import logging
logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)



def tex2maxima(texexpr):
    replace_list=[['~',''],['\,',''],['\:',''],['\;',''],['\!',''], [r'\{','('],[r'\}', ')'],[r'\left(','('],[r'\right)', ')'],  
        [r'\alpha','%alpha'],[r'\beta','%beta'],[r'\gamma','%Gamma'],[r'\omega','%omega'],[r'\theta','%theta']]
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1]) 
    
    lexer.input(texexpr)
    maximaexpr = parser.parse(texexpr, lexer=lexer)
    #parser.parse(texexpr, debug=logging.getLogger()) # debug!
    return maximaexpr
 
    
def mylatexstyle(texexpr):
    replace_list=[[r'\ii',' i'],[r'\ee',' e'],[r'\ppi',r'\pi '],[r'\C',r'\mathrm{C}'],[r'\P',r'\mathrm{P}']]
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1]) 
    return texexpr
    
    
def run_maxima(batch_dir):    
    maxima_cmd = maxima_bat +' -b '+ batch_dir + 'temp.bat'
    try:
        maxima_ret = subprocess.check_output(maxima_cmd)
    except:
        print('set maxima_bat')
        return 1
    maxima_ret = str(maxima_ret)
    maxima_ret = re.sub(r'\s+false(\\r)?(\\n)\(%i\d+\)\s','',maxima_ret)
    maxima_ret = re.sub(r'(\\r)?(\\n)\s*','',maxima_ret)
    #print(maxima_ret) 
    replace_list= [['\\\\','\\'],['\\it \\%alpha','\\alpha'],['\\it \\%beta','\\beta'],['\\it \\%Gamma','\\gamma'],['\\it \\%theta','\\theta'],['\\it \\%omega','\\omega']
        ,['\\lor','~or~']]
    for el in replace_list:
        maxima_ret = maxima_ret.replace(el[0],el[1]) 
    maxima_ret_list = re.findall(r'.*begin\(%i\d+\)(.*)\$\$\(%o\d+\)end.*', maxima_ret)
    #print(maxima_ret_list)
    maxima_ret_list = re.split(r'\$\$\(%o\d+\)', maxima_ret_list[0])
    #print(maxima_ret_list)
    latex_result_list = []
    for el in maxima_ret_list:
        rl = re.split(r'\$\$',el)
        latex_result_list.append(rl)
    #print(latex_result_list)
    return latex_result_list
    
    
def tex2maxima2tex(texexpr_command_list, batch_dir, test=0):    
    #print(texexpr_command_list)
    maxima_command = ''
    maxima_command += '\r'
    maxima_command += 'load("mactex-utilities.lisp");\r'# LaTeX output
    maxima_command += 'load(functs);\r'
    maxima_command += 'load(solve_rec);\r'
    maxima_command += 'load(sqdnst);\r'
    maxima_command += 'load(fourier_elim);\r'
    maxima_command += 'begin;\r'
    for el in texexpr_command_list:
        command = el[2]
        maximaexpr = tex2maxima(el[0])
        #print(maximaexpr)
        if command == 'ratsimp':
            maxima_command += 'tex(ratsimp({:s}))'.format(maximaexpr)+';\r'
        if command == 'expand':
            maxima_command += 'tex(expand({:s}))'.format(maximaexpr)+';\r'
        elif command == 'factor':
            maxima_command += 'tex(factor({:s}))'.format(maximaexpr)+';\r'
        elif command == 'solve_rec_2':
            maxima_command += 'tex(ratsimp(solve_rec({:s},a(n),a(1)={:s})))'.format(maximaexpr,tex2maxima(el[3]))+';\r'
        elif command == 'solve_rec_3':
            maxima_command += 'tex(ratsimp(solve_rec({:s},a(n),a(1)={:s},a(2)={:s})))'.format(maximaexpr,tex2maxima(el[3]),tex2maxima(el[4]))+';\r'
        elif command == 'solve':
            maxima_command += 'tex(solve([{:s}],[{:s}]))'.format(maximaexpr,el[3])+';\r'
        elif command == 'fourier_elim':
            maxima_command += 'tex(fourier_elim([{:s}],[{:s}]))'.format(maximaexpr,el[3])+';\r'            
        elif command == 'rat':
            maxima_command += 'tex(rat({:s}),algebraic:true)'.format(maximaexpr)+';\r'
        elif command == 'sqrtdenest':
            maxima_command += 'tex(sqrtdenest({:s}))'.format(maximaexpr)+';\r'
        elif command == 'radcan':
            maxima_command += 'tex(radcan({:s}))'.format(maximaexpr)+';\r'
        elif command == 'rootscontract':
            maxima_command += 'tex(rootscontract({:s}))'.format(maximaexpr)+';\r'
        elif command == 'logcontract':
            maxima_command += 'tex(logcontract({:s}))'.format(maximaexpr)+';\r'
        elif command == 'trigsimp':
            maxima_command += 'tex(trigsimp({:s}))'.format(maximaexpr)+';\r'
                           
    maxima_command += 'end;\r'
    maxima_command += '\r'
    try:
        f = open(batch_dir+'temp.bat', 'w')
        f.write(maxima_command)
        f.close()
    except:
        return 1    
    latex_result_list = run_maxima(batch_dir)
    if latex_result_list == 1:
        return 1
    for i in range(len(texexpr_command_list)):
        mult_code=texexpr_command_list[i][1]
        if mult_code == MULT_CDOT:
            latex_result_list[i][1]=latex_result_list[i][1].replace(r'\,',r'\cdot ')
        elif mult_code == MULT_NSP:
            latex_result_list[i][1]=latex_result_list[i][1].replace(r'\,',' ')
        elif mult_code == MULT_TIMES:
            latex_result_list[i][1]=latex_result_list[i][1].replace(r'\,',r'\times ')            
    #print(latex_result_list)
    latex_result_str = ''
    if test == 1:
        for i in range(len(latex_result_list)):
            print('{} --> {:s} --> {:s}'.format(texexpr_command_list[i], latex_result_list[i][0], latex_result_list[i][1]))
        return 0
    else:
        for el in latex_result_list:
            latex_result_str += el[1]+'&'
        return latex_result_str
 
        
if __name__ == '__main__':   
    texexpr_comand_list = [
    [r'2^3',MULT_NSP,'ratsimp'], 
    [r'1.234',MULT_NSP,'ratsimp'],
    [r'\frac{2}{6}',MULT_NSP,'ratsimp'],
    [r'(x+2y)^2',MULT_SP,'expand'],
    [r'2x-4xy-2y+1',MULT_NSP,'factor'],
    [r'%alpha^2-9%beta^2',MULT_CDOT,'factor'],
    [r'\ee^{\ppi \ii}',MULT_NSP,'ratsimp'],
    [r'\sin {\frac{5}{4}\ppi}',MULT_NSP,'ratsimp'],
    [r'\log{\ee^3}',MULT_NSP,'ratsimp'],
    [r'\log_{2}{8}',MULT_NSP,'radcan'],
    [r'\left|\sqrt{7} -3 \right|',MULT_NSP,'ratsimp'],
    [r'\frac{d}{dx}{\log{x}}',MULT_NSP,'ratsimp'],
    [r'\int{\cos^{2}{\theta} d\theta}',MULT_TIMES,'ratsimp'],
    [r'\int_{1}^{2}{t^2 dt}',MULT_NSP,'ratsimp'],
    [r'a_{n+1}=3a_{n}+8',MULT_CDOT,'solve_rec_2','2'],
    [r'a_{n+2}-6a_{n+1}+9a_{n}=0',MULT_CDOT,'solve_rec_3','1','6'],    
    [r'2x+y=13,x-2y=-6',MULT_NSP,'solve','x,y'],
    [r'x^2-3x-4 \leqq 0',MULT_CDOT,'fourier_elim','x'],
    [r'\sqrt{8-2\sqrt{15}}',MULT_NSP, 'sqrtdenest'],
    [r'\sqrt{x^2}',MULT_NSP, 'ratsimp'],
    ]

    test = 1
    tex2maxima2tex(texexpr_comand_list, '', test)
    #print(tex2maxima2tex(texexpr_comand_list, ''))
    
    
    
