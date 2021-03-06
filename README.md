# ply_tex2maxima

ply_tex2maxima parses LaTeX math expressions and converts it into the equivalent Maxima form by using PLY.  

Author:Akira Hakuta,  Date: 2017/08/06       

## Installation (windows)

TeX Live:  <http://www.tug.org/texlive/acquire-netinstall.html>

```
\texlive\2017\bin\win32\pythontex.exe
```

Python3: <https://www.python.org/downloads/windows/>  
PLY : <http://www.dabeaz.com/ply/>  
Maxima : <http://maxima.sourceforge.net> (5.39.0-Windows)
```
pip install pygments
pip install ply
```


## Usage
```
tex2maxima_parser.py  
set maxima_bat
maxima_bat='C:\\maxima-5.39.0\\bin\\maxima.bat'

python.exe tex2maxima_parser.py
   --> Generating LALR tables
   
variable : a,b,...,z,A,....,Z,\\alpha,\\beta,\\gamma,\\theta,\\omega
constant : pi --> \\ppi, imaginary unit --> \\ii, napier constant --> \\ee

ply_tex2maxima LaTeX expression style
\\sin{x}
\\cos^{2}{\\theta}
\\log{\\ee}
\\log_{2}{8}
\\frac{d}{dx}{(x^3+x^2+x+1)}
\\int{(x^3+x^2+x+1) dx}
\\int_{1}^{3}{(x-1)(x-3)^2 dx}
\\lim_{x \\to -\\infty} {(\\sqrt{x^2+3x}+x)}
\\sum_{k=1}^{n}{k(k+1)^2}
\\left| 3 - \\ppi \\right|
a_{n}
\\{a-2(b-c)\\}^2  
_{10}\\P_{3}  
_{10}\\C_{3}  
(\\frac{d}{dx})^{3}{x^5}  
\\frac{d^{3}}{dx^{3}}{x^5}  
\\Gamma(5)  
\\zeta(10)  
f(x) function, not f*(x)  

pdflatex.exe -synctex=1 -interaction=nonstopmode example21.tex  
pythontex.exe example21.tex  
pdflatex.exe -synctex=1 -interaction=nonstopmode example21.tex  
```
## Examples

```
[latex_expr, MULT_???, maxima_command] --> tex(maxima_command(maxima_expr))) --> latex_expr
MULT_SP=0
MULT_NSP=1
MULT_CDOT=2
MULT_TIMES=3

['2^3', 1, 'ratsimp'] -->  tex(ratsimp(2^3)) --> 8
['\\frac{2}{6}', 1, 'ratsimp'] --> tex(ratsimp(2*6^-1)) --> \frac{1}{3}
['(x+2y)^5', 0, 'expand'] --> tex(expand((x+2*y)^5)) --> 32\,y^5+80\,x\,y^4+80\,x^2\,y^3+40\,x^3\,y^2+10\,x^4\,y+x^5
['2x-4xy-2y+1', 1, 'factor'] --> tex(factor(2*x-4*x*y+(-2)*y+1)) --> -\left(2 x+1\right) \left(2 y-1\right)
['\\ee^{\\ppi \\ii}', 1, 'ratsimp'] --> tex(ratsimp(%e^(%pi*%i))) --> -1
['\\sin {\\frac{5}{4}\\ppi}', 1, 'ratsimp'] --> tex(ratsimp(sin(5*4^-1*%pi))) --> -\frac{1}{\sqrt{2}}
['\\log{\\ee^3}', 1, 'ratsimp'] --> tex(ratsimp(log(%e^3))) --> 3
['\\frac{d}{dx}{\\log{x}}', 1, 'ratsimp'] --> tex(ratsimp(diff(log(x),x,1))) --> \frac{1}{x}
['\\int{\\cos^{2}{\\theta} d\\theta}', 3, 'ratsimp'] --> tex(ratsimp(integrate(cos(%theta)^2,%theta))) --> \frac{\sin \left(2\times {\theta}\right)+2\times {\theta}}{4}
['\\frac{d}{dx}{f(x)}=f(x)', 2, 'ode2', 'f(x)', 'x'] --> tex(ratsimp(ode2(diff(f(x),x,1) = f(x),f(x),x))) --> f\left(x\right)={\it \%c}\cdot e^{x}
['\\Gamma(6)', 1, 'ratsimp'] --> tex(ratsimp(gamma(6))) --> 120
['\\zeta(2)', 1, 'ratsimp'] --> tex(ratsimp(zeta(2))) --> \frac{\pi^2}{6}
```


### in japanese

#### ply_tex2maxima は LaTeX の数式コードを解析して、Maxima のコードに変換する Python のプログラムツールです。  
Python の構文解析ライブラリ PLY で作ってみました。  

### 各ソフトのインスツール   
#### TeXLive  
<https://www.tug.org/texlive/acquire-netinstall.html>  
install-tl-windows.exe でインスツールする。  
\texlive\2017\bin\win32の中にpythontex.exeがあります。  
これを使う！  

#### Python3  
まず、<https://www.python.org/downloads/windows/> に入って、  
Python3 の好きなバージョン、32bit、64bitを選び、インスツールして下さい。  
コマンドプロンプトで   
pip install pygments  
pip install ply  
と打ち込む。Successfully installed ...　と表示されればOK!    
\Python36\Lib\site-packagesのなかにパッケージのフォルダができる。  
当方は Python 3.6.2 で動作を確認しています。  

#### Maxima  
<http://maxima.sourceforge.net> (5.39.0-Windows)  
bin\maxima.bat を使います。

### 使い方  
tex2maxima_parser.py  
maxima_bat='C:\\\\maxima-5.39.0\\\\bin\\\\maxima.bat'  
のように、ディリクトリを含めて、maxima.batを指定。  
python.exe tex2sym_parser.py  
を実行。出力を見ると  
tex2maxima2tex(texexpr_command_list, batch_dir, test=0)  
が何をしているかか、分かると思います。    

※ LaTeX の数式コード texexpr は  
 ply_tex2maxima LaTeX expression style  の形で入力してください。  
 つまり、関数の引数は { } でくくる。例 '\\\\sin{x}', '\\\\int_{1}^{2}{x^3 dx}'。  

更に  
```
pdflatex.exe -synctex=1 -interaction=nonstopmode example21.tex
pythontex.exe example21.tex
pdflatex.exe -synctex=1 -interaction=nonstopmode example21.tex
```
を実行すると、example21.pdf が作成できます。  

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
これを用いて、定義されたルールに従って、LaTeX の数式コードを Maxima のコードに変換します。  
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
二重根号、繁分数式 等が正しく処理できるように、必要なp\_ 関数を定義していきます。   

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
texexpr_command_listにあるlatexの数式をtex2maxima(texexpr)でMaximaの数式に変換、  
Maximaで数式処理するbatch file(temp.bat)を作成します。  
run_maxima(batch_dir) の返り値(数式処理した結果のlist)に適当な置き換えをし、  
各要素を'&'で区切った文字列の形で返します。  


### example21.tex  
pythontex について  

\begin{pycode}  
code  
\end{pycode}  

codeの部分にPythonのコードを書き込みます。      

\pyc{code}  

はcodeを実行するコマンド。複数のコマンドを実行するのであれば、; を間に入れる。  
pyはPython、cはcommandの意味。  

\py{value}  

は、valueを可能ならば文字列に変えて出力するコマンドのようです。    
\py{'text'}と\pyc{print('text')} は共に、文字列 text を出力します。     

Maximaで処理した結果を貼り付ければよいのですが、  
数式毎にMaximaを立ち上げると、時間が掛かりすぎて実用的ではありません。  
まとめて、1回で処理します。  

tex2maxima2tex()の返り値はファイルresult.texに保存します。  
\input{../result.tex}でそれをLaTeXのコードの間に差し込み、  
更に、arrayjob を使って、配列のように要素を呼び出し、数式処理した結果を貼り付けます。  
The ‘arrayjob’ package Management of arrays in LaTEX.  

Maxima の batch file temp.bat  
数式処理した最終的な LateX のコードの文字列 result.tex  
は共に pythontex が生成するフォルダの中に保存されます。  

分母の有理化については、変形できず、途中で断念。  
不等式については、解にルートがついてしまうと解けない。  


### exampl22.tex 
具体的な使用例  
example12.tex のMaxima 版です。  
多段組enumerateをtabularxで実現しています。  
そのコードの中で、pythonにLaTeXのコードをr'\frac{1}{2}'の形で渡すと、ERRORになることがあります。  
その場合は、'\\\\frac{1}{2}'を使ってください。  

### example23.tex 
具体的な使用例(漸化式)    
4問ともSymPy では解けない(後半２問は誤答を出力)  
Maxima は正解を出力します。  

### example24_emath.tex

具体的な使用例 (platex + emath) です。  
emath <http://emath.s40.xrea.com>  

 ### example25.tex
 高次微分、ガンマ関数、ゼータ関数 、微分方程式の使用例

### pythontex.exe の経過時間の比較  
timeit.exe で pythontex.exe exmaple?.tex の開始から終了までの経過時間を計測してみました。  
PC環境 CPU: Corei7-5600U   RAM: 8.00GB

```
				number of expression	 	Elapsed Time
example21.tex (Maxima)			39			0:00:04.820
example22.tex (Maxima)			 8			0:00:04.195
example23.tex (Maxima)			 4			0:00:04.226

example11.tex ( SymPy)			39			0:00:08.902
example12.tex ( SymPy)			 8			0:00:03.610
```
Maxima は処理する数式の数が増えても、経過時間にはほとんど差がありません。  
batch file に処理するコマンドをまとめ、1回で処理しているので、当然の結果と思われます。  




### モジュールのimport    
他のモジュールと同様に、    
from tex2maxima2_parser import tex2maxima2tex, mylatexstyle   
だけで import できるようにするには、    
まず、ダウンロードしたフォルダー ply_tex2maxima-master を、Python36\Lib\site-packages にコピーまたは移動し,   
Python36\Lib\site-packages に、例えば、  
ply_tex2maxima-master  
の1行だけのファイル ply_tex2maxima-master.pth を作ります。    
Pythonは .pth の付いたファイルを読み込んで path を設定します。絶対path でもOK。    

#### 修正情報
2017/05/23 release  

2017/06/11 

```
多段組enumerateで出る不具合を修正  
```

2017/07/13 

```
\\dfrac を追加  
```

2017/07/19

```
高次微分、ガンマ関数、ゼータ関数 を追加 
微分方程式の使用例を追加
```
2017/08/06

```
Python 3.6.2 で動作確認
```

