Binomial

-- Natural Number Simulation for Complex Systems --

　　複雑反応系研究室

    Copyright (c) 2023- Takashi Sato
    
    This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/


0. 説明

0.1 概要：
  このプログラムは、複雑な反応システムを解析するための自然数シミュレーション(NNS)を提供します。 
  この計算での数は、分子数、細胞数、生きている個体数などで、すべての数は0を含む自然数となります。
  このプログラムは、これらの自然数を計算するための時間発展アルゴリズムが含まれています。 
  このプログラムは、従来の通常の微分方程式ODEやペトリネットに対して補足的に使用できます。 
  NNSは、二項確率によるランダムな自然数計算によって、化学反応系や数理系モデルをシミュレーションします。 
  このプログラムは、止まらない計算アルゴリズムにより、簡便なモデル定義を可能にします。 
　
0.2 シミュレーション：
　以下のような反応系における分子の“数”の時間発展をシミュレーショすることができます。
　lA　+　mB　+　nC　+ ・・・　→　sX　+　tY　+　uZ　+ ・・・
　ここで、A、B、C、X、Y、Zはそれぞれ反応要素、ｌ、ｍ、ｎ、ｓ、ｔ、uはそれぞれ反応の量的次数を表す係数です。　
  詳細は、論文（bioRxiv:「Application of a Novel Numerical Simulation to Biochemical Reaction systems」
　Takashi Sato, doi: https://doi.org/10.1101/2023.08.10.552732）に譲るが、上記の量論式について
　任意の数の要素、および次数をもつ時間発展式を、任意の数の量論式について同時に計算することが出来ます。

0.3 カテゴリー:
  複雑系、 システムバイオロジー, バイオインフォマティクス、A-life、 シミュレーション
 
 
1. ファイル構成

 このプログラムを動かすためには、以下の9つのPythonファイルと、１つのjsonファイル、
それから１つの入力ファイルが必要です。以下の、ファイル群を今後、プログラムファイルと呼びます。


    1.1 binomial_v016.py (メインプログラム)
        メインコードで、入力ファイルの読み込みと、計算の実行プロセスが含まれています。 
    1.2 binomial_parameters_02.json
         計算上の条件と、結果の設定を決めるパラメータが含まれている。
    1.3 element_35.py
        計算要素を定義するコードが含まれています。 入力ファイルの*Elementで定義される要素名、初期の数などを元に
        要素オブイジェクトが作られます。
    1.4 reaction_63.py
        反応式を計算するためのコードが含まれています。入力ファイルの*Reactionで反応式が定義されます。
    1.5 utility_55.py
    　　結果グラフの出力や、csvファイルへの出力などのユーティリティ関係のコードが含まれます。
    1.6 setting_30.py
         入力ファイルの読み込みに関係したコードが含まれます。
    1.7 utility_functions.py
         設定に必要な関数が含まれています。
    1.8 polymer_12.py
         工事中です。
    1.9 setManage_01.py
         工事中です。

 これらのコードは、2023年9月時点、Ubuntu 22.04.2 LTS　上の Spyder IDE 5.4.3で作りました。  
 WindowsとLinuxで動作可能です。(一部の入力ファイルは、Linuxのみ対応)

 
2. フォルダの準備

   メインホルダーを1つ作成します。
   そのメインホルダーの中にプログラムホルダーを作り、上記プログラムファイルを格納します。
   メインホルダーの中に別の入力ファイル用のホルダーを作成して、入力ファイルを格納します。(参照："Folder_structure.pdf")
　　入力ファイルホルダーはいくつ作ってもよいですが、同じ名前の入力ファイルは複数作らないようにしてください。   
　　

3. 入力ファイルの構成 1

     このプログラムは、上記プログラムファイルと1つの入力ファイルを準備すると実行できます。
   入力ファイルは、拡張子が.txtのプレーンテキストで記述し、
   *Time、*Element、*Reaction、および*Plotの4つのセクションを準備します。

   以下のExampleの説明は、inp_immune_323.txtのものです。 以下に4つのセクションの説明を示します。
   * Time、* Element、* Reaction、および*Plotです。以下、すべての場合、**は、コメント行を意味します。
   コメントは、#でも可能です。
   
3.1 *Time
            まず、開始時間、終了時間を書きます。それから、コンソールの出力時間間隔、
          プロット出力時間間隔、csvファイル出力時間間隔、および単位を１行で書きます。
          数値は、0を含む自然数のみが利用可能です。
          計算は1単位間隔ごとに実行されます。以下の例では、0から始まり14400まで、１増えるごとに計算が実行されます。
          コンソールには1440毎に途中経過を出力し、図の表示は7200毎に（従って2回）、ファイルへの要素の値の出力が1400毎になされます。
          単位は、この場合”min”となっていますが、速度定数との関係を注意して、ユーザーが定義する仕様になっています。
          

         Format:
           *Time
            start time, end time, console out interval, plot out interval, csv-file out interval, time unit
         
         Example:
           *Time, 
           ** start, end, console out, plot out, csv out, time unit
           0, 14400, 1440, 7200, 1440,  min

3.2 *Element
          　シミュレートする要素アイテムを定義します。
          要素名、初期要素数が最低限必要です。要素名は、重複がないように気を付けてください。
          また、下記の例のように要素の初期数は、0を含む自然数で設定する必要があります。
          ただし、1e5や1.1e4のように指数表示も可能です。
          その他、プロットの色、マーカーが設定可能です。
          色とマーカーを指定しないと、任意の色とマーカーが割当てられます。色は、下記やmatplotlibで利用可能な色が設定できます。
         ['Black', 'Green' ,'Yellow', 'Gray', 'Blue', 'Red', 'Orange']や、matplotlib.colors.cnames中の色。
          マーカーは、下記のようなものが設定できます。
          ["o", "v", "^", "<", ">","1", "2", "3", "4", "8",  \
           "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"]
            
          
         Format:
           *Element
            element name, initial number, plot color, plot marker
               --- --- --- 
               --- --- --- 

         Example:
           *Element
           ** 0:element name, 1:initial number, 2:plot color
           virus,               500, Black, 8
           cell,                1e5, Green, s
           virusCell,             0, p
           macrophage,         5000, 
           macrophageActive,      0,
           macrophageWithVirus,   0, 
           dendricCell,        2000, Blue,  
           dendricMHC,            0, Red,  
           naiveTh1,          1.1e4, Green
           activeTh1,             0, 
           IFN,                   0, Blue
           IL-12,                 0
          
3.3 *Reaction
           上記の要素間、もしくは単体要素の反応を定義します。
         以下のように多くの反応タイプが利用可能です。
         反応マルチ(rM)は、4種類以上の要素に関係する反応を定義できます。
 
              r1_0 : ある1種類の要素の一定割合で減少
              r1_1 : ある1種類の要素が、別の1要素に変化
              r1_2 : ある1種類の要素が、別の2種類の要素に変化
              r1_3 : ある1種類の要素が、別の3種類の要素に変化
              r2_1 : ある2種類の要素が、別の1種類の要素に変化
              r2_2 : ある2種類の要素が、別の2種類の要素に変化
              r2_3 : ある2種類の要素が、別の3種類の要素に変化
              r3_1 : ある3種類の要素が、別の1種類の要素に変化
              r3_2 : ある3種類の要素が、別の2種類の要素に変化
              r3_3 : ある3種類の要素が、別の3種類の要素に変化
              rM   : 4種類以上の要素が、別の4種類以上の要素に変化（後述）
              r1_+ : ある1種類の要素の数が、一定数ずつ増加する（線形増加）
              r1_- : ある1種類の要素の数が、一定数ずつ減少する（線形減少)
              r+-= : "="の左辺にある要素の加減を計算して、右辺の要素の値とする（計算確認用等に使用する）         
 
　　　　反応定義には、基本的に反応要素と生成要素、および要素の反応次数に関する情報と、
　　　　速度定数（反応確率パラメーター）の数値設定が必要です。
　　　　r1_1以上（上記、r1_1からrMまで）の反応では、反応要素と生成要素に同じ要素が含まれていてもかまいません。
　　　　記述の仕方は、以下のとおりです。
　　　　
　　　　r1_2の例を示します。下記は、要素Aが2種類の要素XとYになる例です。定義式は、
　　　　1つのAが2つのXと3つのYになるとすると、以下のようになります。 
 
              r1_2, 001, 1, A, 0.5, 2, X, 3, Y
 
　　　　最初の項で反応タイプを定義します。2番目は識別用の名前です。１番目と２番目の名前て「r1_2_001」のように
　　　　固有の反応名になるので、重複がないように2番目の名前を決めてください。
        3番目と4番目の項「1、A」は反応次数と要素名です。
        5番目の0.5は、この反応の速度定数（反応確率パラメーター）です。
        6番目と7番目の「2、X」は反応次数と、生成される要素名です。
        8番目と9番目の「3、Y」は反応次数と、もうひとつの生成される要素名です。 
        
　　　　反応次数は自然数でなければなりません。
        要素名は*Elementで定義されている必要があります。
        速度定数（反応確率パラメーター）は、少数か自然数で、指数表示が使えます。
       
       rMは、反応定義の前後に多数の種類の要素を定義できます。
        例えば以下のように、3行使って1つの反応を定義します。
 
            　　rM,   002,  1, A, 10, B, 10, C, 2, D, 100, E
                            1000
                            1, X, 1, Y, 10, Z, 3, W
                       
　　　　上記は、5種類の要素が反応し、4種類の要素が生成します。
        要素名の前の数字は、他の反応定義と同様に反応次数です。 
        最初の行は、反応する要素を定義します。2行目は、速度定数（反応確率パラメーター）です。
        3行目は、生成された要素を定義します。 
        このように、行には多くの要素を記述でき、基本的に制限はありません。
        
　　　　*Reactionの定義には、同じ行に正規化パラメーターが必要です。
　　　　このパラメーターは、反応系中の全要素数と同程度の値が望ましいですが、特に制限はありません。
　　　　この値が大きいと反応する確率が小さくなり、小さいと逆に反応する確率が大きくなります。
　　　　r2_1、r2_2、r2_3、r3_1、r3_2、r3_3、rMの反応が、この正規化パラメーターによって、
　　　　反応確率パラメーターと共にアルゴリズムを通じて反応率に関わります。
        (詳細は、論文「bioRxiv:「Application of a Novel Numerical Simulation to Biochemical Reaction systems」
　　　　Takashi Sato, doi: https://doi.org/10.1101/2023.08.10.552732」)
        を参照ください）
 
　　　　速度定数（反応確率パラメーター）と正規化パラメーターは小数にすることができます。
　　　　以下の形式では、A、B、X、Yは*Element項目で定義された要素名です。
　　　　 pi（p1, p2, ・・・等）は、各反応の速度定数（反応確率パラメーター）を表します。

         Format:
          *Reaction, global normalization parameter
           r1_2, name, a, A, p1, x, X, y, Y
           r1_1, name, a, A, p2, x, X
           r1_0, name, a, A, p3
           r2_2, name, a, A, b, B, p4, x, X, y, Y
           r2_1, name, a, A, b, B, p5, x, X
           rM,   name, a, A, b, B, c, C, d, D, e, E, -------
                       p6
                       x, X, y, Y, z, Z, w, W, -------
           --- --- --- 
           --- --- --- 

         Example:
           *Reaction, 100000000
           r2_1, 001,  10, virus, 1, cell, 0.04, 1, virusCell
           r1_1, 002,   1, virusCell, 0.001, 100, virus
           r2_1, 003,   1, macrophage, 1, virus, 0.9, 1, macrophageWithVirus
           rM,   004,   1, macrophageWithVirus,  
                        0.9, 
                        1, macrophageWithVirus, 10, IFN, 10, IL-12
           r1_1, 005,   1, macrophageWithVirus, 0.1, 1, macrophage
           r2_1, 006,   1, virus, 1, dendricCell, 10, 1, dendricMHC
           rM,   007,   1, naiveTh1, 1, dendricMHC, 10, IFN, 10, IL-12
                        10000,
                        1, activeTh1, 1, dendricMHC
           r1_2, 013,   1, activeTh1, 1, 10, IFN, 1, activeTh1
           r2_1, 014,   1, macrophage, 2, IFN, 10, 1, macrophageActive 
           r2_1, 015,   1, macrophageActive, 10, virus, 1, 1, macrophageWithVirus
           r1_1, 018,   1, dendricMHC, 0.0002, 1, dendricCell
           r1_1, 019,   1, macrophageActive, 0.002, 1, macrophage
           r1_1, 020,   1, activeTh1, 0.001, 1, naiveTh1
           r1_0, 021,   1, IFN, 0.01

3.4 *Plot
　　　　このセクションでは、プロット条件を定義します。 
　　　　同じ行に書かれた要素が1つの図に表示されます。 
　　　　プロットの縦軸タイプは線形または対数です。記載がないときは、デフォルトの"linear"(線形)で表示されます。

        Format:
          *Plot, plot-type (linear or log)
          ** second item is "linear" or "log".
           A, X, Y
           B, W
           F
           --- --- --- 
           --- --- ---          
    
        Example:
         *Plot, log
           virus, virusCell, macrophageWithVirus
           cell, virusCell
           macrophage, macrophageActive, macrophageWithVirus
           dendricMHC, dendricCell
           IFN, IL-12
           activeTh1, naiveTh1
           
3.5 binomial_parameter_02.json
          このファイルでは、5つのパラメータを定義できます。
          "EntropyCalc": "YES" or "NO": エントロピーの計算は、大きな数では負荷がかかるため切り替えができます。
                                        計算する場合は"YES"、計算させない場合は "NO"を選択してください。
          "CSV_OUTPUT":  "YES" or "NO": CSVファイルには、すべての要素の指定時間での値が出力されます。    
　　　　　　　　　　　　　　　　　　　　計算する場合は"YES"、計算させない場合は "NO"を選択してください。
          "FIG_OUTPUT":  "YES" or "NO": 図のファイルタイプは、pngです。
             　　　　　　　　　　　　　 *Plotで定義された図が、指定時間で出力されます。 
　　　　　　　　　　　　　　　　　　　　もし、計算させない場合は "NO"を選択してください。
          "RestartFile": "YES" or "NO": "YES"の場合、要素の計算された最後の値を初期値とした、リスタート用のファイルが作成されます。
　　　　　　　　　　　　　　　　　　　　例えば、test_059.txtに対しては、test_059_Re.txt
                                        が、入力ファイルと同じフォルダ内に作成されます。
　　　　　　　　　　　　　　　　　　　　"NO"の場合、ファイルは作られません。
             　　　　　　　　　　　　　 このリスタートファイル名を使って再度計算が可能です。
          "ProcessPoolExecutor":  "NO": 現在は、未設定。


4. 入力ファイルの構成 2　（オプションの設定項目） (例. test_059.txt)

4.1 *ElementInOut

   計算領域対して要素の流入・流出を表現するためのに、*ElenemtInOutが定義できます。
   これにより、計算途中で要素の流入・流出を表現できます。

          Format:    
          *ElementInOut
      element name, initial number, plot color, marker, <brank>, type-0, at time, amaunt, at time, amaunt, -> -> 
      element name, initial number, plot color, marker, <brank>, type-1, interval, amaunt
      element name, initial number, plot color, marker, <brank>, type-2, const, amplitude, period-time, add-interval
           --- --- --- 
           --- --- ---   
        
     Example:
     *ElementInOut
      Q,      270, blue, s, ,    type-0, 10, 300, 40, 100, 50, 50, 60, 500, 70, 500
      T-in,     0, blue, h, ,    type-1, 2, 1e2
      T-out,  1e5, magenta, 4, , type-1, 2, -5e2
      B,        0,  purple, 2, , type-2, 100, 10, 10,  50


5. プログラムの実行

   2つの実行プロセスが利用可能になっています。
   一つは、spyderから直接プログラムを実行する方法で、もう一つは、コマンドラインから実行する方法です。

　　　1.Spyder
          「2. フォルダの準備」を参考に入力ファイルを準備します。
          実行方法の1つは、anaconda3でSpyderを使用します。 Spyderからメインのプログラムファイルbinomial_v016.pyを開きます。
          次のように、適切な行に入力ファイル名を書き込みます。メインプログラムには、すでにfNameが記述されているので、
　　　　　それを書き換えてください。
         
               fName ='inp_immune_323.txt'
         
          Spyderの「ファイルの実行」コマンドで計算を実行します。 
          結果ファイル等は、入力ファイルのあるフォルダ中に新しいホルダーが作成され、その中に配置されます。
          
　　　2.コマンドライン、端末
     
          ホルダーの準備は1.Spyderと同じです。
          ターミナル(例えば、Anaconda Powershell Prompt)を開き、ディレクトリをプログラムファイルのあるディレクトリに変更します。
          次のように端末にコマンドラインを記述します。
           
               > python binomial_v016.py inp_immune_323.txt
                  
          改行を返すと、プログラムが開始されます。
          結果ファイルは、1.spyderのように新しく作成されたホルダーに配置されます。


6. 結果ファイル

   結果ファイルフォルダは、入力ファイルと同じディレクトリに作成されます。例えば：

      inp_immune_323.txt の結果ファイルは、"inp_immune_323_yyyy-mm-dd hh-mm-ss" のフォルダ内に入ります。

   このフォルダには入力ファイルで定義された要素数の時系列のプロット図（PNGファイル）と、
   CSVファイルが保存されます。CSVファイルには以下の3種類があります。

      inp_immune_323_all.csv：設定された時間での要素数を行ごとの時間で記録します。
      inp_immune_323_all_02.csv：設定された時間での要素数を列ごとの時間で記録します。
      inp_immune_323_information.csv：瞬間反応(IR)、累積IR、および反応エントロピーに関する情報を、設定された時間で行ごとの時間で提供します。


7. SBMLファイルのNNS用テキストファイルへの変換

   convert_SBML_to_NNS_004.pyを使って、SBMLで書かれたxmlファイルを、NNS用のテキストファイルに変換できます。
   実行方法は、次の2つです。どちらの場合も、変更するファイルとプログラムは同じフォルダ内に配置してください。
   プログラムファイルといくつかの例が、"convert"フォルダ内にあります。

　　　7.1 Spyder
        
          実行方法の1つは、anaconda3でSpyderを使用します。 Spyderからconvert_SBML_to_NNS_004.pyを開きます。
          filenameに、変換したいファイル名を代入します。
         
               filename = "binding_A_B.xml"
         
          Spyderの「ファイルの実行」コマンドで計算を実行します。 
          結果ファイルが、以下のようになって同じホルダー内に配置されます。

              binding_A_B_NNS.txt
          
　　　7.2 コマンドライン、端末

          ターミナル(例えば、Anaconda Powershell Prompt)を開き、ディレクトリをプログラムファイルのあるディレクトリに変更します。
          次のように端末にコマンドラインを記述します。
           
               > python convert_SBML_to_NNS_004.py binding_A_B.xml
                  
          改行し実行すると、以下のファイルが同じフォルダ内に作成されます。
          
              binding_A_B_NNS.txt

      7.3 設定事項

　　　上記実行の際、以下の事項はプログラム内で変更可能です。
      (出力されたテキストファイルを直接書き換えることでも変更可能です)

      7.3.1 計算時間に関する設定は、デフォルトで以下の行が入ります。
         変更したい場合は、出力されたファイルを変更するか、プログラム内のTIME_SCHEDULEを変更してください。
         構文は、*Timeと同じです。

              TIME_SCHEDULE = "0, 100, 10, 50, 1, seconds\n\n"

      7.3.2 要素の初期数の設定は、デフォルトではSBMLから取得することを試みます。うまくいくとそのままの値が設定されます。
         取得できない場合は、999が設定されます。この時の設定は以下の通りです。
         ただし、NNSでは要素の数が0を含む正整数である必要があるため、小数を読み込むとプログラムはエラーで止まることに
         注意してください。

              ELEMENT_SETTING = "NO"
              INITIAL_NUMBERS = 999 

         以下のように設定すると、強制的に指定したINITIAL_NUMBERSの値が割り当てられます。

              ELEMENT_SETTING = "YES"
              INITIAL_NUMBERS = 999 

         INITIAL_NUMBERSは、変更できますが、0もしくは正整数としてください。また、この設定はすべての要素に適用されます。
         もし個別に変更したい場合は出力されたテキストファイルを変更してください。
         また、プロットの色やマーカーはNNS内でランダムに設定されます。もし、決まったものを使いたい場合は、
         やはりテキストファイルを変更してください。

      7.3.3 反応式は、優先してSBMLから取得することを試みます。もし、反応の各要素の次数がうまく取得できない場合は、１が割り当てられます。
         また、速度定数がうまく取得できないときは、以下の定数が割り当てられます。

              RATE_CONSTANT = 999

         さらに、規格化定数は、NNS独自の定数なので以下のように割り当てられます。

              NORMALIZATION_CONSTANT = 9.9e9

         上記の各定数は系の性質や、反応の特性に従って適切に変更することをお勧めします。

      7.3.4 *Plotには、SBMLから取得した各要素をすべて記述することがデフォルトになっています。NUMBER_TO_PLOTでは、
         一つのグラフに入る要素の数を指定できます。もしなにも出力したくない場合は、PLOT_CONDITION = "NO"としてください。

              PLOT_CONDITION = "YES" 
              NUMBER_TO_PLOT = 5






 
 
 
