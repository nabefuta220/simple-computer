# simple-computer

1word8bit,256wardによるアセンブリ言語の疑似実行環境です。

- [simple-computer](#simple-computer)
  - [スペック](#スペック)
  - [状態レジスタ](#状態レジスタ)
  - [命令一覧](#命令一覧)
    - [引数一覧](#引数一覧)
      - [R(数字)](#r数字)
      - [VALUE](#value)
      - [ADDRESS](#address)
      - [LABLE](#lable)
      - [OP](#op)
      - [CONDITION](#condition)
      - [DEVICE](#device)
    - [ニモニック一覧](#ニモニック一覧)
      - [MOV](#mov)
      - [FUNC (for resister)](#func-for-resister)
      - [LDI](#ldi)
      - [FNCI](#fnci)
      - [LOAD](#load)
      - [STA](#sta)
      - [FUNC (for memory)](#func-for-memory)
      - [JMP](#jmp)
      - [CAL](#cal)
      - [RET](#ret)
      - [SET](#set)
      - [IN](#in)
      - [OUT](#out)
      - [HALT](#halt)

## スペック

- 1ワード8bit
- 256ワード構成
- データレジスタ:7個
- 演算子:加算、減算、1増加、1減少、bitwiseOR,bitwiseAND,bitwiseXOR,Inverterの計8種類
- 状態レジスタ:Sign,oVerflow,Carry,Zeroの4つ

## 状態レジスタ

これは、[MOV](#mov)、[FUNC (for resister)](#func-for-resister)、[LDI](#ldi)、[FNCI](#fnci)、[LOAD](#load)、[STA](#sta)、[FUNC (for memory)](#func-for-memory)によって変更され、

[JMP](#jmp)、[CAL](#cal)、[RET](#ret)のときに条件分岐に使われます。

- Sign : 直前の代入値の最上位ビットが1(=符号付き整数型で捉えたとき、負の値になる)ときにたちます。
- oVerflow : 直前の代入値を符号付き整数型で捉えたとき、表示範囲を超えたときに立ちます。
- Carry : 直前の代入値を符号なし整数型で捉えたとき、表示範囲を超えたときに立ちます。
- Zero : 直前の代入値のビットがすべて0のときに立ちます。

## 命令一覧

### 引数一覧

以下、これらの引数は、次の意味です。

#### R(数字)

- 意味 : (数字)番目のレジスタです。
- 例 : R2 , R6

#### VALUE

- 意味 : オペランド(10進数、もしくは16進数)
  
- 例 : 35 , 1AH , ffH

- 注意 : 数値については、後ろに`H`をつけることで16進数に、それ以外は10進数で解釈されます。

#### ADDRESS

- 意味 : メモリの番地(10進数、もしくは16進数)
  
- 例 : 35 , 1AH , ffH

#### LABLE
  
- 意味 : ラベル(英数字、ただし、最初に数字はおけない)
- 例 : IF , LB1 , STR2INT

- 注意 : `3IF`など、数字が先頭にくるものはラベルとしては解釈されません。また、`FUNC`、`HALT`など、他のコマンドと同じ文字列もラベルとしては解釈されません。

  また、ラベルをつけるには、LABELの最後に`:`をつける必要があります。

#### OP

- 意味 : 演算子

- 一覧

  | A OP B | 効果               |
  |--------|--------------------|
  | A 0 B  | A+1                |
  | A 1 B  | A+B                |
  | A 2 B  | A-1                |
  | A 3 B  | A-B                |
  | A 4 B  | A\|B (論理和)      |
  | A 5 B  | A^B (排他的論理和) |
  | A 6 B  | A&1 (論理積)       |
  | A 7 B  | ~A  (ビット反転)   |

#### CONDITION

- 意味 : 条件

- 一覧

  | CONDITION | 条件                 |
  |-----------|----------------------|
  | 0         | 無条件               |
  | 1         | V=1 (オーバーフロー) |
  | 2         | Z=1 (ゼロ)           |
  | 3         | Z=0 (ゼロ以外)       |
  | 4         | S=1 (負)             |
  | 5         | S=0 (正)             |
  | 6         | C=1 (キャリー)       |
  | 7         | C=0 (ノンキャリー)   |

#### DEVICE

- 意味 : デバイス番号(10進数、もしくは16進数)

- 例 : 35 , 1AH , ffH

### ニモニック一覧

#### MOV

- 引数 : MOV [R_D](#r数字) , [R_S](#r数字)
- 効果 : R_DにR_Sの値を代入します。
- 例 : `MOV R3 R4` : レジスタ3にレジスタ4の値を代入します。

#### FUNC (for resister)

- 引数 : FUNC [OP](#op) [R](#r数字)
- 効果 : レジスタ1にRの値 OP レジスタ1 の結果を格納します。
  
  また、その時の結果に応じて、[状態フラグ](#状態レジスタ)を変化させます。
- 例 : `FUNC 2 R4` : レジスタ1にレジスタ4 - レジスタ1 の結果を格納します。

#### LDI

- 引数 : LDI [R](#r数字) [VALUE](#value)
- 効果 : RにVALUEを代入します。
  
  また、その時の代入値に応じて、[状態フラグ](#状態レジスタ)を変化させます。
- 例 : `LDI R2 10H` : レジスタ2に10H=16を代入します。

#### FNCI

- 引数 : FNCI [OP](#op) [VALUE](#value)
- 効果 : レジスタ1にVALUE OP レジスタ1の結果を代入します。
  
  また、その時の結果に応じて、[状態フラグ](#状態レジスタ)を変化させます。
- 例 : `FNCI 4 21H` : レジスタ1に21Hとレジスタ1の値の論理和の結果を格納します。

#### LOAD

- 引数 : LOAD [R](#r数字) [ADDRESS](#address)
- 効果 : レジスタRにメモリのADDRESS番地の値を代入します。
  
  また、その時の代入値に応じて、[状態フラグ](#状態レジスタ)を変化させます。
- 例 : `LOAD R2 10H` : レジスタ2にメモリの10H=16番地の値を代入します。

#### STA

- 引数 : LOAD [R](#r数字) [ADDRESS](#address)
- 効果 : ADDRESS番地の値にレジスタRの値を代入します。
  
  また、その時の代入値に応じて、[状態フラグ](#状態レジスタ)を変化させます。
- 例 : `LOAD R2 10H` : メモリの10H=16番地の値にレジスタ2の値を代入します。

#### FUNC (for memory)

- 引数 : FUNC [OP](#op) [ADDRESS](#address)
- 効果 : レジスタ1に メモリのADDRWSS番地の値 OP レジスタ1の結果を格納します。
  
  また、その時の結果に応じて、状態フラグを変化させます。
- 例 : `FUNC 5 100` : レジスタ1にメモリの100番地の値とレジスタ1の値の排他的論理和の結果を返します。

#### JMP

- 引数 : JMP [CONDITION](#condition) [LABEL](#lable)
- 効果 : 条件を満たしたとき、LABELにジャンプします。

- 例 : `JMP 0 IF` : 無条件にIFと書かれてあるラベルにジャンプします。

#### CAL

- 引数 : CAL [CONDITION](#condition) [LABEL](#lable)
- 効果 : 条件を満たしたとき、LABELにジャンプします。

  ただし、[JMP](#jmp)命令とは異なり、[RET](#ret)によって復帰したときは、この命令の次に復帰します。

- 例 : `CAL 5 FUNCTION` : 状態レジスタのSignが正=0であるとき、FUNCTIONと書かれてあるラベルにジャンプします。また、RETが呼び出されたとき、この次の命令に復帰します。

#### RET

- 引数 : RET [CONDITION](#condition)
- 効果 : 条件を満たしたとき、直前に呼び出された[CAL](#cal)の次の命令に復帰します。

- 例 : `CAL 2` : 状態レジスタのZeroが1であるとき、直前に呼び出されたCALの次の命令に復帰します。

#### SET

- 引数 : SET [R](#r数字)
- 効果 : スタックポインタをRの値にセットします。

- 例 : `SET R1` :スタックポインタをレジスタ1の値にセットします。

#### IN

- 引数 : IN [R](#r数字) [DEVICE](#device)
- 効果 : デバイスDEVICEから入力を受け取り、レジスタRに代入します。
  
  初期状態では、DEVICE=0のとき、標準入力から入力を受け取ります。
- 例 : `IN R2 0` : デバイス0から入力を受け取り、その値をレジスタ2に代入します。

#### OUT

- 引数 : OUT [R](#r数字) [DEVICE](#device)
- 効果 : デバイスDEVICEにレジスタRの値を出力します。
  
  初期状態では、DEVICE=0のとき、標準出力から値を出力し、

  DEVICE=1のとき、標準エラー出力から値を出力します。
  
- 例 : `OUT R4 1` : デバイス1にレジスタ4の値を出力します。

#### HALT

- 引数 : HALT
- 効果 : プログラムを終了します。
  
- 注意 :  最後はこれが呼び出される必要があります。
