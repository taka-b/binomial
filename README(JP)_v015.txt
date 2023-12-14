Binomial

-- Natural Number Simulation for Complex Systems --

　　複雑反応系研究室

    Copyright (c) 2022 Takashi Sato
    
    This software is released under the MIT License. http://opensource.org/licenses/mit-license.php*/


説明

  このプログラムは、複雑な反応システムを探索するための自然数シミュレーションを提供します。 
  この計算の数は、分子数、細胞数、生きている個体数などを意味します。
  このプログラムは、これらの自然数を計算するための時間発展アルゴリズムが含まれています。 
  このプログラムは、従来の通常の微分方程式（OED）の代わりに使用できます。 OEDは、膨大な数理系の現象に対処できます。 
  数シミュレーションも、二項確率によるランダムな自然数に基づいて、これらの反応系や数理系モデルを解くことができます。 
  このプログラムは、止まらない計算と入力ファイル書き込みにより、簡単な使用を可能にします。 
  このスマートなシミュレーターをお楽しみください。
  

カテゴリー

 複雑系, システムバイオロジー, A-life, シミュレーション
 
 
ファイル構成

 このプログラムを動かすためには、6つのPythonファイルと、１つの入力ファイルが必要です。

    1. binomial_v015.py (メインプログラム)
        メインコードで、入力ファイルの読み込みと、計算の実行プロセスが含まれています。 
    2. element_32.py
        計算要素を定義するコードが含まれています。 入力ファイルの*Elementで定義される要素名、初期の数などを元に
        要素オブイジェクトが作られます。
    3. reaction_42.py
        反応式を計算するためのコードが含まれています。入力ファイルの*Reactionで反応式が定義されます。
    4. utility_49.py
    　　結果グラフの出力や、csvファイルへの出力などのユーティリティ関係のコードが含まれます。
    5. setting_14.py
         入力ファイルの読み込みに関係したコードが含まれます。
    6. reactionManage_05.py  
         このファイルは、反応計算をサポートするコードが含まれています。
    7. polymer_12.py
         工事中です。
    8. binomial_parameters.json
         計算上の条件と、結果の設定を決めるパラメータが含まれている。

 これらのコードは、2023年3月時点、Ubuntu 22.04.1 LTS　上の Spyder IDE 5.3.3で作りました。  
 WindowsとLinuxで動作可能です。
 
はじめに

     上記の6つのdot（.）-pyファイルと1つの入力ファイルでプログラムを実行できます。
   入力ファイルは、拡張子が.txtのプレーンテキストで記述されています。
   ファイルには、* Time、* Element、* Reaction、および*Plotの4つのセクションが必要です。
   
   メイン-プロジェクト-フォルダを1つ作成します。
   プログラム-ファイル-ホルダーをメインホルダーの中に作り、
   上記6つのdot（.）-pyファイルを格納します。
   メイン-プロジェクト-フォルダの中に別のホルダーを作成して、入力ファイルを格納します。(参照："Folder structure.pdf")
      
    Spyderで実行するには、binomial_v015.pyの中の入力ファイル名を変更する必要があります。
   binomial_v015.pyを実行すると、計算が開始され、プロットがプロットウィンドウに表示されます。
   以下のテストファイルの説明は、inp_immune_323.txtのものです。 以下に4つのセクションの説明を示します。
   * Time、* Element、* Reaction、および*Plotです。
   
    1.*Time
            開始時間、終了時間を書きます。
          コンソールの出力時間感覚、プロット出力時間間隔、csvファイル出力時間間隔、および単位です。
          数値は、０を含む自然数のみが利用可能です。
          計算は1間隔ごとに実行されます。
          以下、すべての場合、**は、コメント行を意味します。

         Format:
           *Time
            start time, end time, console out interval, plot out interval, csv-file out interval, time unit
         
         Example:
           *Time, 
           ** start, end, console out, plot out, csv, out, time unit
                  0, 14400, 1440, 14400, 1440,  min

    2.*Element
          　シミュレートする要素アイテムを記述します。
          要素名、初期要素数が最低限必要です。要素名は、重複がないように付けてください。
          その他、プロットの色、マーカーが設定可能です。
          色とマーカーを指定しないと、任意の色とマーカーが割当てられます。色は、下記などが設定できます。
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
           virus, 500, Black, 8
           cell, 100000, Green, s
           virusCell, 0, p
           macrophage, 5000, 
           macrophageActive, 0,
           macrophageWithVirus, 0, 
           dendricCell, 2000, Blue,  
           dendricMHC, 0, Red,  
           naiveTh1, 10000, Green
           activeTh1, 0, 
           IFN, 0, Blue
           IL-12, 0
          
    3.*Reaction
           上記の要素間、もしくは単体要素の反応を定義します。
         以下のように多くの反応タイプが利用可能です。
         反応マルチ(rM)は、多くの種類の要素に関係する反応を定義できます。
 
              r1_0 : ある１種類の要素の一定割合で減少
              r1_1 : ある１種類の要素が、別の１要素に変化
              r1_2 : ある１種類の要素が、別の２種類の要素に変化
              r1_3 : ある１種類の要素が、別の３種類の要素に変化
              r2_1 : ある２種類の要素が、別の１種類の要素に変化
              r2_2 : ある２種類の要素が、別の２種類の要素に変化
              r2_3 : ある２種類の要素が、別の３種類の要素に変化
              r3_1 : ある３種類の要素が、別の１種類の要素に変化
              r3_2 : ある３種類の要素が、別の２種類の要素に変化
              r3_3 : ある３種類の要素が、別の３種類の要素に変化
              rM   : 多種類の要素が、別の多種類の要素に変化
              r1_+ : ある１種類の要素の数が、一定数ずつ増加する（線形増加）
              r1_- : ある１種類の要素の数が、一定数ずつ減少する（線形減少）            
 
　　　　すべての反応定義には、基本的に反応要素と生成要素、および要素の反応次数に関する情報と、
　　　　反応確率パラメーターの数値設定が必要です。
　　　　r1_1以上（上記、r1_1からrMまで）の反応では。反応要素と生成要素に同じ要素が含まれていてもかまいません。
　　　　記述の仕方は、以下のとおりです。
　　　　
　　　　r1_2を例とすると、1種類の要素Aが2種類の要素XとYになるので、定義式は、
　　　　1つのAが2つのXと3つのYになるとすると、以下のようになります。 
 
              r1_2, 001, 1, A, 0.5, 2, X, 3, Y 
 
　　　　最初の項で反応タイプを定義します。2番目は識別用の名前です。１番目と２番目の名前て「r1_2_001」のように
　　　　固有の反応名になるので、重複がないように２番目の名前を決めてください。
        3番目と4番目の項「1、A」は反応次数と要素名です。
        5番目の0.5は、この反応の確率パラメーターです。
        6番目と7番目の「2、X」は反応次数と、生成される要素名です。
        8番目と9番目の「3、Y」は反応次数と、もうひとつの生成される要素名です。 
        
　　　　反応次数は自然数でなければなりません。
        要素名は*Elementで定義されている必要があります。
        確率パラメーターは、小数と自然数が使えます。
       
       rMは、反応定義の前後に多数の種類の要素を定義できます。
        例えば以下のように、3行使って1つの反応を定義します。
 
            　　rM,   002,  1, A, 10, B, 10, C, 2, D, 100, E
                         1000
                        1, X, 1, Y, 10, Z, 3, W
                       
　　　　上記は、5種類の要素が反応し、4種類の要素が生成します。
        要素名の前の数字は、他の反応定義と同様に反応次数です。 
        最初の行は、反応する要素を定義します。  2行目は、反応確率パラメーターです。
        3行目は、作成された要素を定義します。 
        このように、行には多くの要素を記述できます。
        
　　　　*Reactionの定義には、同じ行にグローバル正規化パラメーターが必要です。
　　　　このパラメーターは、反応系中の全要素数と同程度の値が望ましいと考えられます。
　　　　r2_1、r2_2、r2_3、r3_1、r3_2、r3_3、rMの反応が、この正規化パラメーターによって、
　　　　反応確率パラメーターと共にアルゴリズムを通じて反応率に関わります。
 
　　　　反応確率パラメーターとグローバル正規化パラメーターは小数にすることができます。
　　　　以下の形式では、A、B、X、Yは*Element項目で定義された要素名です。
　　　　 pi（p1, p2, ・・・等）は、各反応の確率パラメーターを表します。

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

    4. *Plot
　　　　このセクションでは、プロット条件を定義します。 
　　　　同じ行に書かれた要素が1つの図に表示されます。 
　　　　プロットの縦軸タイプは線形または対数です。記載がないときは、デフォルトの"linear"で表示されます。

         Format:
          *Plot, plot-type
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
           
    5. binomial_parameters.json
          このファイルでは、２つのパラメータを定義できます。
          デフォルトは、すべて"YES"です。
             "EntropyCalc": "YES" or "NO": エントロピーの計算は、大きな数では負荷がかかるため切り替えができます。
                                        　　　　　もし、計算させない場合は "NO"を選択してください。
             "CSV_OUTPUT":"YES" or "NO" :  CSVファイルには、すべての要素の指定時間での値が出力されます。    
　　　　　　　　　　　　　　　　　　　　　　　　　もし、計算させない場合は "NO"を選択してください。
             "FIG_OUTPUT":"YES" or "NO" :  図のファイルタイプは、pngです。
             　　　　　　　　　　　　　　　　　　*Plotで定義された図が、指定時間で出力されます。 
　　　　　　　　　　　　　　　　　　　　　　　　　もし、計算させない場合は "NO"を選択してください。

プログラムの実行

     2つの実行プロセスが利用可能です。
   少なくともマスターホルダーには2つのホルダーが必要です。 1つのホルダーには6つのプログラムファイルが含まれています。
   もう一方のホルダーには、上記のような入力ファイルが含まれている必要があります。(参照："Folder structure.pdf")

　　　　1.Spyder
        
           実行方法の1つは、anaconda3でspyderを使用します。 Spyderからメインのプログラムファイルbinomial_v015.pyを開きます。
          次のように、適切な行に入力ファイル名を書き込む必要があります。
         
               fName ='inp_test_038.txt'
         
         Spyderの「ファイルの実行」コマンドで計算を実行します。 
          結果ファイル等は、入力ファイルのあるフォルダ中に新しいホルダーが作成され、その中に配置されます。
          
　　　　2.コマンドライン、端末
     
            ホルダーの準備は1.Spyderケースと同じです。
            ターミナル(windowsの場合はコマンドプロンプト)を開き、ディレクトリをプログラムファイルのあるディレクトリに変更します。
            次のように端末にコマンドラインを記述します。
           
                   $ python binomial_v015.py inp_test_038.txt
                  
               行を返すと、プログラムが開始されます。
               結果ファイルは、1.spyderのように新しく作成されたホルダーに配置されます。




 
 
 
