# CFO

小さな事業の数字を集め、資金繰り・採算・予算・支出を判断し、小さく試した結果を次の判断に戻す aachat の Agent です。
結論、勧めること、判断が変わる条件、根拠、決める期限を短く返します。最終的に決めるのは本人です。

## 頼めること

- 日々：「前回から資金の見通しは変わった？ 対応が要るものを教えて」
- 毎月：「今月の結果と、来月変えたいことを整理して」
- 決めるとき：「この外注を頼む場合と、自分で続ける場合を比べて」
- 試した後：「入れたツールの効果を見て、続けるか考えたい」

## 18 の Skill

| まとまり | Skill |
|---|---|
| 財務データ管理 | `cfo-data-refresh` 集めて更新 / `cfo-data-check` 照合 / `cfo-data-model` 分析用に整える |
| 資金繰り管理 | `cfo-cash-forecast` 見通し / `cfo-cash-monitor` 変化を見つける / `cfo-cash-scenarios` 条件で比べる / `cfo-cash-actions` 打ち手 |
| 採算・価格分析 | `cfo-profitability` 採算 / `cfo-margin-drivers` 理由 / `cfo-pricing-options` 価格と条件 |
| 予算・月次経営管理 | `cfo-budget-plan` 予算 / `cfo-budget-variance` 予算と実績の差 / `cfo-monthly-review` 月次 / `cfo-reforecast` 見通しの更新 |
| 支出・投資判断 | `cfo-spend-decision` 支出の比較 / `cfo-decision-scenarios` 割に合う条件 / `cfo-trial-plan` 小さく試す / `cfo-trial-review` 結果の振り返り |

それぞれのまとまりは、Plugin としても単独で入れられます。

| Plugin | GitHub |
|---|---|
| 財務データ管理 | [p-take55/cfo-financial-data-plugin](https://github.com/p-take55/cfo-financial-data-plugin) |
| 資金繰り管理 | [p-take55/cfo-cash-management-plugin](https://github.com/p-take55/cfo-cash-management-plugin) |
| 採算・価格分析 | [p-take55/cfo-profitability-pricing-plugin](https://github.com/p-take55/cfo-profitability-pricing-plugin) |
| 予算・月次経営管理 | [p-take55/cfo-budget-review-plugin](https://github.com/p-take55/cfo-budget-review-plugin) |
| 支出・投資判断 | [p-take55/cfo-spend-investment-plugin](https://github.com/p-take55/cfo-spend-investment-plugin) |

## 使う前に

扱う事業・期間・通貨、数字の置き場所、守りたい残高や使える予算を、要る範囲で伝えてください。
CSV や表、請求の一覧からでも始められます。会計・銀行・請求などの接続があれば、そこから数字を取ります。

| 情報源の例 | 要る情報 |
|---|---|
| 会計 | 計上した売上・費用・科目・締めの状況 |
| 銀行・カード | 対象の口座の残高、入出金、引き落としの予定 |
| 請求・決済 | 請求、入金、手数料、返金、未回収 |
| 販売管理 | 商品・顧客・案件別の売上と契約 |
| 工数・契約の資料 | 提供にかかった時間、外注・採用・サービスの費用と条件 |

これは要る情報の一覧で、特定のサービスとつながることを約束するものではありません。

## 決めていること

- 売上・利益・入金・残高、実績・予定・仮定を混ぜない。分からない金額をゼロで埋めない。
- 本人の工数は別の欄に置き、空いた時間を売上や現金に換算しない。
- 計算は表やコードで再現でき、元の資料と式をたどれるようにする。
- 送金・注文・支払・借入・投資の取引・税の申告・契約の変更はしない。分析を頼まれたことを、それらの許可とは受け取らない。
- 通知や定期実行を設定していないのに、「見張っておく」とは言わない。

## 構成

- `identity.md`：役割と、判断の境目
- `.agents/skills/`：仕事ごとの Skill
- `tests/`：資金計算スクリプト（`cfo-cash-forecast/scripts/forecast.py`）のテスト。`python3 -m unittest discover -s tests` で動く。Python 3.10 以上、標準ライブラリだけを使う

## ライセンス

MIT
