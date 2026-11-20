# エンティティマッチング

## ユースケースの概要
Recorded Future のエンティティ（企業、マルウェア、脅威アクターなど）を検索・解決し、セキュリティオペレーションセンター（SOC）のツールおよびワークフロー全体で一貫した参照を確保します。

Recorded Future エンティティの詳細については、[こちら](https://support.recordedfuture.com/hc/en-us/articles/115001359567-What-is-an-Entity)をクリックしてください。

## 課題
フリーテキストの名前は、ツールと Recorded Future の間で不一致を引き起こす可能性があります。脅威アクターのエンティティはユーザー名エンティティと同じ名前を持つ場合がありますが、それぞれのエンティティ ID は異なるため、混乱や誤った脅威インテリジェンスの関連付けが生じます。

## 解決策
[`banshee entity`](../../reference/commands.md#banshee-entity) コマンドを使用して、PS Banshee 内で直接エンティティを検索・解決します。

- エンティティ名やタイプがわかっており、対応するエンティティ ID を見つける必要がある場合は、[`banshee entity search`](../../reference/commands.md#banshee-entity-search) を使用します。

- エンティティ ID がわかっており、名前とタイプを取得する必要がある場合は、[`banshee entity lookup`](../../reference/commands.md#banshee-entity-lookup) を使用します。

- リンクされたエンティティを取得してエンリッチする場合は、[`banshee entity links`](../../reference/commands.md#banshee-entity-links) を使用します。

正しいエンティティ ID を取得したら、[`banshee list add`](../../reference/commands.md#banshee-list-add) などの後続の PS Banshee コマンドでそれを活用し、組織のウォッチリストにおける正確なエンティティ参照を確保します。