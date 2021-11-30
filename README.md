# simple-computer

1ward8bit,256wardによるアセンブリ言語の疑似実行環境

## スペック

- 1ワード8bit
- 256ワード構成
- データレジスタ:7個+標準出力
- 演算子:加算、減算、1増加、1減少、bitwiseOR,bitwiseAND,bitwiseXOR,Inverterの計8種類


## 命令一覧

### MOV

- 引数: MOV R_D , R_S　(R_D,R_S:レジスタ)
- 効果:R_DにR_Sの値を代入する

## FUNC

- 引数: FUNC OP R (OP:演算子を表す整数値、R:レジスタ)
- 効果:R0にR0 OP Rの結果を格納する
  
  また、その時のR0に応じて、状態フラグを変化させる

## LDI

- 引数: LDI R VALUE (R:レジスタ、VALUE:値)
- 効果:RにVALUEを代入する