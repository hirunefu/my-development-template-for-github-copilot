# 対象サーフェスを Copilot CLI と VS Code Chat に限定し、指示ファイルの二重化を廃止する

`AGENTS.md` だけを指示ファイルの実体とし、`.github/copilot-instructions.md` と同期チェックの CI を削除する。

## 背景

[0001](./0001-duplicate-instruction-files.md) は、`AGENTS.md` が JetBrains / Visual Studio / Xcode / Eclipse の Chat で読まれないことを理由に、`.github/copilot-instructions.md` との二重化と CI での同期強制を決めた。

しかし読み込み対応を並べ直すと、`AGENTS.md` を読まないのは**その 4 つの IDE の Chat だけ**である。Copilot CLI、VS Code Chat、GitHub.com の cloud agent、code review はいずれも `AGENTS.md` を読む。

このテンプレートの対象を Copilot CLI と VS Code Chat に定めた結果、二重化が守っていた範囲は対象外になった。

## 決定

`AGENTS.md` を唯一の実体とする。`.github/copilot-instructions.md`、`.github/workflows/sync-instructions.yml`、ブランチ保護の `sync-instructions` チェックを削除する。

## 帰結

- **JetBrains / Visual Studio / Xcode / Eclipse の Chat では、このテンプレートの指示が読まれない。** 対象外と決めたうえでの帰結であり、見落としではない。これらの IDE を使うチームに配るなら 0001 の構成に戻す必要がある
- 二重化に伴う制約が消えたため、日英併記や `AGENTS.en.md` のような多言語構成が取れるようになった。byte-identical の強制がそれを禁じていた
- 維持すべきファイルが 1 つ減り、CI ジョブが 1 つ減った
