# ply_tex2maxima

ply_tex2maxima parses LaTeX math expressions and converts it into the equivalent Maxima form by using PLY.  

Author:Akira Hakuta,  Date: 2017/05/23    

## Installation (windows)

TeX Live:  <http://www.tug.org/texlive/acquire-netinstall.html>

```
\texlive\2016\bin\win32\pythontex.exe
```

Python3: <https://www.python.org/downloads/windows/>  
PLY : <http://www.dabeaz.com/ply/>  
Maxima : <http://maxima.sourceforge.net>  
```
pip install ply
```


## Usage
```
tex2maxima_parser.py  
set maxima_bat
maxima_bat='C:\\maxima-5.39.0\\bin\\maxima.bat'

python.exe tex2maxima_parser.py
   --> Generating LALR tables
   
variable : a,b,...,z,A,....,Z,\alpha,\beta,\gamma,\theta,\oomega
constant : pi --> \ppi, imaginary unit --> \ii, napier constant --> \ee

ply_tex2maxima LaTeX expression style
\sin{x}
\cos^{2}{\theta}
\log{2}
\log_{2}{8}
\frac{d}{dx}{(x^3+x^2+x+1)}
\int{(x^3+x^2+x+1) dx}
\int_{1}^{3}{(x-1)(x-3)^2 dx}
\lim_{x \to -\infty} {(\sqrt{x^2+3x}+x)}
\sum_{k=1}^{n}{k(k+1)^2}
\left| 3 - \ppi \right|
a_{n}
\{a-2(b-c)\}^2  
_{10}\P_{3}  
_{10}\C_{3}  

pdflatex.exe -synctex=1 -interaction=nonstopmode example3.tex  
pythontex.exe example3.tex  
pdflatex.exe -synctex=1 -interaction=nonstopmode example3.tex  
```
## Examples

```
[latex_expr, MULT_???, maxima_command] --> tex(maxima_command(maxima_expr))) --> latex_expr

['2^3', 1, 'ratsimp'] --> tex(ratsimp(2^3)) --> 8
['1.234', 1, 'ratsimp'] --> tex(ratsimp(ratsimp(1.234)))rat:replaced1.234by617/500=1.234 --> \frac{617}{500}
['\\frac{2}{6}', 1, 'ratsimp'] --> tex(ratsimp(2*6^-1)) --> \frac{1}{3}
['(x+2y)^2', 1, 'expand'] --> tex(expand((x+2*y)^2)) --> 4y^2+4xy+x^2
['2x-4xy-2y+1', 2, 'factor'] --> tex(factor(2*x-4*x*y+(-2)*y+1)) --> -(2\cdot x+1)\cdot (2\cdot y-1)
['\\ee^{\\ppi \\ii}', 1, 'ratsimp'] --> tex(ratsimp(%e^(%pi*%i))) --> -1
['\\sin {\\frac{5}{4}\\ppi}', 1, 'ratsimp'] --> tex(ratsimp(sin(5*4^-1*%pi))) --> -\frac{1}{\sqrt{2}}
['\\log{\\ee^3}', 1, 'ratsimp'] --> tex(ratsimp(log(%e^3))) --> 3
['\\log_{2}{8}', 1, 'radcan'] --> tex(radcan(log(8)*log(2)^-1)) --> 3
['\\left|\\sqrt{7} -3 \\right|', 1, 'ratsimp'] --> tex(ratsimp(abs(sqrt(7)-3))) --> 3-\sqrt{7}
['\\frac{d}{dx}{\\log{x}}', 1, 'ratsimp'] --> tex(ratsimp(diff(log(x),x,1))) --> \frac{1}{x}
['\\int_{1}^{2}{t^2 dt}', 1, 'ratsimp'] --> tex(ratsimp(integrate(t^2,t,1,2))) --> \frac{7}{3}
['a_{n+1}=3a_{n}+8', 2, 'solve_rec_2', '2'] --> tex(ratsimp(solve_rec(a(n+1)=3*a(n)+8,a(n),a(1)=2))) --> a(n)=2\cdot 3^{n}-4
['\\sqrt{8-2\\sqrt{15}}', 1, 'sqrtdenest'] --> tex(sqrtdenest(sqrt(8-2*sqrt(15)))) --> \sqrt{5}-\sqrt{3}
```


### in japanese

#### ply_tex2maxima は LaTeX の数式コードを解析して、Maxima のコードに変換する Python のプログラムツールです。  
すでに、antlr4 で作られたLaTeX2SymPy <https://github.com/augustt198/latex2sympy> があります。  
今回、Python の構文解析ライブラリ PLY で作ってみました。  

### 各ソフトのインスツール   
#### TexLive  
<https://www.tug.org/texlive/acquire-netinstall.html>  
install-tl-windows.exe でインスツールする。  
\texlive\2016\bin\win32の中にpythontex.exeがあります。  
これを使う！  

#### Python3  
まず、<https://www.python.org/downloads/windows/> に入って、  
Python3 の好きなバージョン、32bit、64bitを選び、インスツールして下さい。  
コマンドプロンプトで   
pip install ply  
と打ち込む。Successfully installed ...　と表示されればOK!    
\Python35\Lib\site-packagesのなかにパッケージのフォルダができる。    

#### Maxima  
<http://maxima.sourceforge.net>  
bin\maxima.bat を使います。

### 使い方  
tex2maxima_parser.py  
maxima_bat='C:\\\\maxima-5.39.0\\\\bin\\\\maxima.bat'  
のように、ディリクトリを含めて、maxima.batを指定。  
python.exe tex2sym_parser.py  
を実行。出力を見ると  
tex2maxima2tex(texexpr_command_list, batch_dir, test=0)  
が何をしているかか、分かると思います。    

更に  
```
pdflatex.exe -synctex=1 -interaction=nonstopmode example3.tex
pythontex.exe example3.tex
pdflatex.exe -synctex=1 -interaction=nonstopmode example3.tex
```
を実行すると、example3.pdf が作成できます。  

### 各ファイルの説明  
### tex2maxima_lexer.py 
ply.lex.lex() は字句解析機を構築します。  
これを用いて、文字列をtokenの並びへと変換します。  
python.exe tex2sym_lexer.py  
を実行して下さい。  
どんな単語をtokenとして認識しているのかが分かります。  
tokenの定義する方法は２つあります。  
例えば、非負整数のtokenの名前を'NN_INTEGER'とします。  
```
t_NN_INTEGER(t)= r'\d+'

def t_NN_INTEGER(t):
	r'\d+'
    return t
```
どちらでもtokenを定義できるのですが、  
関数で定義すると、定義された順に高い優先度を与えられます。  
例えば、  
```
def t_NN_INTEGER(t):
    r'\d+'
    return t
    
def t_NN_FLOAT(t):
    r'\d*\.\d+'
    return t
```
の順序で定義すると、  
'123.456'は  
[('123', 'NN_INTEGER'), ('.456', 'NN_FLOAT')] のように２つのtokenと認識してしまいます。  
定義の順序を入れ替えると   
[('123.456', 'NN_FLOAT')]となります。  
このように、順序に気を付けながらtokenを定義します。  

### tex2maxima_parser.py   
ply.yacc.yacc() は 構文解析器を構築します。  
これを用いて、定義されたルールに従って、LaTex の数式コードを Maxima のコードに変換します。  
```
# expr : expr^expr
def p_expr_exponent(p):
    'expr : expr EXPONENT expr'
    # p[0]  p[1]  p[2]    p[3]
    p[0] = '({})＾({})'.format(p[1], p[3])
    
で tex2sym(r'2^3') --> (2)＾(3) となります。
```
  
’expr : expr EXPONENT expr' は意味のある文字列で、  
上記コメントのように、配列pの各要素とシンボル expr,EXPONENT の値が対応しています。  
二重根号、繁分数式 等が正しく処理できるように、必要なp_ 関数を定義していきます。  
高校数学レベルの数式を対象としました。  

絶対値の記号 |expr| は曖昧な記号です。  
次の式は2通りに解釈できます。  
```
| 2|-3+4|-5 | = | 2-5 | = 3
| 2|-3+4|-5 | = 2 - 3 + 20 = 19
```
\left| expr \right| で定義をすることにします。  

#### run_maxima(batch_dir)  
maxima.bat -b batch_dir/temp.bat を実行し、 
subprocess.check_output(maxima_cmd)で出力を表示、  
そこから数式処理した結果を抜き取り、listとして返します。 

#### tex2maxima2tex(texexpr_command_list, batch_dir, test=0)  
texexpr_command_listにあるlatexの数式をtex2maxima(texexpr)でmaximaの数式に変換、  
maximaで数式処理するbatch file(temp.bat)を作成します。  
run_maxima(batch_dir) の返り値(数式処理した結果のlist)に適当な置き換えをし、  
各要素を&で繋げた文字列として返します。  


### example3.tex  
pythontex について    
\begin{pycode}    
code    
\end{pycode}    
codeの部分にPythonのコードを書き込みます。    

\pyc{code}はcodeを実行するコマンド。複数のコマンドを実行するのであれば、; を間に入れる。    
pyはpython、cはcommandの意味。  

\py{value}は、valueを可能ならば文字列に変えて出力するコマンドのようです。     
\py{'text'}と\pyc{print('text')} は共に、文字列 text を出力します。    

maximaで処理した結果を貼り付ければよいのですが、  
数式毎にmaximaを立ち上げると、時間が掛かりすぎて実用的ではありません。  
まとめて、1回で処理します。  

tex2maxima2tex()の返り値はファイルresult.texに保存します。  
\input{../result.tex}でそれをtexのコードの間に貼り付けます。  
更に、arrayjob を使って、配列のように要素を呼び出し、数式処理した結果を貼り付けます。  
The ‘arrayjob’ package Management of arrays in LaTEX.  

maxima の batch file temp.bat  
数式処理した最終的な LateX のコードの文字列 result.tex  
は共に pythontex が生成するフォルダの中に保存されます。  

分母の有理化については、変形できず、途中で断念。  
不等式については、解にルートがついてしまうと解けない。  


### example4.tex 
具体的な使用例(因数分解)  
example2.tex のmaxima 版です。  

### example5.tex 
具体的な使用例(漸化式)    
4問ともSymPy では解けない(後半２問は誤答を出力)  
maxima は正解を出力します。  




### pythontex.exe の経過時間の比較  
timeit.exe で pythontex.exe exmaple?.tex の開始から終了までの経過時間を計測してみました。  
PC環境 CPU: Corei7-5600U   RAM: 8.00GB

```
				number of expression	 		Elapsed Time
example3.tex (Maxima)			39				0:00:04.820
example4.tex (Maxima)			 8				0:00:04.669
example5.tex (Maxima)			 4				0:00:04.777

example1.tex ( SymPy)			39				0:00:08.902
example2.tex ( SymPy)			 8				0:00:03.324
```
maxima は処理する数式の数が増えても、経過時間にはほとんど差がありません。  
batch file に処理するコマンドをまとめ、1回で処理しているので、当然の結果と思われます。  




### モジュールのimport    
他のモジュールと同様に、    
from tex2maxima_parser import tex2sym, mylatexstyle   
だけで import できるようにするには、    
まず、ダウンロードしたフォルダー ply_tex2maxima-master を、Python35\Lib\site-packages にコピーまたは移動し,   
Python35\Lib\site-packages に、例えば、  
ply_tex2maxima-master  
の1行だけのファイル ply_tex2maxima-master.pth を作ります。    
Pythonは .pth の付いたファイルを読み込んで path を設定します。絶対path でもOK。    








