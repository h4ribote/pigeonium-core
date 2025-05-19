# Pigeonium について

## 概要
Pigeonium は、シンプルかつ効率的なブロックチェーンベースの通貨システムを提供するネットワークです。  
基軸通貨である **Pigeon** を中心に、トランザクションの管理やスマートコントラクトのデプロイを簡易的なコードで実現することを目指しています。  
開発者や利用者が簡単にアクセスできるように設計されており、柔軟性と拡張性を備えたプラットフォームです。

## 主な特徴

### 1. ネットワークと基軸通貨
- **ネットワーク名**: Pigeonium
- **基軸通貨**: Pigeon
  - 総供給量: 1,000,000.000000 Pigeon
  - トランザクション手数料やスマートコントラクトのデプロイ・実行コストに使用
- ネットワークは、MySQLデータベースを活用してトランザクション、残高、通貨、コントラクトのデータを管理

### 2. スマートコントラクト
Pigeonium では、簡易的なスマートコントラクトをデプロイおよび実行可能
- **スクリプト言語**: Python のサブセット（`asteval` を使用）
- **デプロイコスト**: スクリプトのバイト数 × 100 Pigeon
- **実行コスト**: スクリプトのバイト数 × 10 Pigeon
- **機能例**:
  - トークンの送金（`transferFromContract`）
  - 通貨の作成（`createCurrency`）
  - 残高確認（`getBalance`）
  - 変数の保存・取得（`setVariable`, `getVariable`）

### 3. トランザクション
- トランザクションは、ウォレットの署名と管理者署名を必要とする設計
- 主なフィールド:
  - 送信元（`source`）と受信先（`dest`）
  - 通貨ID（`currencyId`）
  - 金額（`amount`）と手数料（`feeAmount`）
  - 入力データ（`inputData`）によるコントラクトとの連携
- データベース（`transaction` テーブル）に記録され、透明性と追跡可能性を確保

### 4. ウォレット
- ECDSA（NIST256p）を使用した暗号化ウォレット
- 機能:
  - ウォレットの生成（`Wallet.generate`）
  - 秘密鍵または公開鍵からのウォレット作成
  - データ署名（`sign`）と署名検証（`verifySignature`）
- アドレスは公開鍵のハッシュ（SHA256 + MD5）で生成

### 5. API とサーバー
- **FastAPI** を使用した RESTful API
- 現在のエンドポイント:
  - `GET /`: ネットワーク情報（名前、ID、コスト設定、管理者公開鍵）を返却
- 今後の拡張予定:
  - ウォレット管理、トランザクション送信、コントラクトデプロイ用のエンドポイント

### 6. データベース構造
Pigeonium は MySQL データベースを使用してデータを管理  
主なテーブル:
- `balance`: アドレスごとの通貨残高
- `currency`: 通貨情報（ID、名前、シンボル、発行者、供給量）
- `contract`: コントラクトのスクリプトとアドレス
- `transaction`: トランザクションの詳細
- `variable`: コントラクトの状態変数

## サンプルユースケース
Pigeonium のスマートコントラクトを使用したデポジットシステムの例:

```python
from funcHint import *

# 通貨デポジットシステム
if not getSelfCurrency():
    createCurrency("TestCurrency", "TC", 1000_000000)

depo_amount = getVariable(selfAddress, transaction.source)
depo_time = getVariable(selfAddress, md5(transaction.source))
if depo_amount and depo_time:
    depoTime = int.from_bytes(depo_time, 'big')
    depoAmount = int.from_bytes(depo_amount, 'big')
    depoPeriod = transaction.timestamp - depoTime
    if depoPeriod < 60*60*24:
        transferFromContract(transaction.source, getSelfCurrency().currencyId, depo_amount)
    else:
        interestRate = 1 + depoPeriod/(60*60*24) * 0.01
        transferFromContract(transaction.source, getSelfCurrency().currencyId, int(depo_amount*(interestRate)))

if transaction.currencyId == getSelfCurrency().currencyId:
    setVariable(transaction.source, transaction.amount.to_bytes(8, 'big'))
    setVariable(md5(transaction.source), transaction.timestamp.to_bytes(8, 'big'))
else:
    transferFromContract(transaction.source, transaction.currencyId, transaction.amount)
```

このスクリプトは、ユーザーが通貨をデポジットし、一定期間後に利息付きで引き出す機能を提供します。

## 利用シーン
- **開発者向け**: 簡単なコードでトークンやコントラクトを作成・デプロイ可能
- **小規模コミュニティ向け**: カスタム通貨や自動化されたトランザクション処理の実装

## 今後の展望
- **クライアントライブラリ**: 簡易操作を可能にするライブラリの提供
- **API 拡張**: ウォレット管理、トランザクション送信、コントラクト操作用のエンドポイント追加
- **開発ツール**: コントラクトのテンプレートやローカルテスト環境の整備
