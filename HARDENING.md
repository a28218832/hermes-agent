# local/hardening 分支與本地修改紀錄（E5）

本分支保存對 Hermes core 的本地修改，避免 `hermes update` 的 autostash 再次吞掉功能
（2026-11-16 事故：423 行 patch 進 stash、credit dashboard ~217 行修改遺失）。

## 現況（2026-11-19 建立）

- 分支：`local/hardening`（基底：main，v0.23.1+8063）
- fork remote：`git@github.com:a28218832/hermes-agent.git`
- 首次 commit 內容：`gateway/delivery.py`、`gateway/run_notifications.py`、
  `plugins/platforms/discord/adapter.py`（Discord 通知靜音／@silent 相關，080 session 產物）
- autostash 紀錄：`stash@{0} = hermes-update-autostash-20261116-113120`（423 行 core patch）。
  078 已決定移植為 plugin；移植完成前**保留在 stash，不要 pop 到 live tree**。
- credit dashboard 修改（~217 行＋discord_tool.py 8 行）已被 11-16 update 吞掉：
  待從 stash 或輕備份 repo（a28218832/hermes-light-backup）找回，目標移植為 plugin。

## 更新流程（E5 紀律：取代直接 `hermes update`）

1. `git status --porcelain` 必須為空；有修改先 commit 到本分支。
2. `git fetch origin && git rebase origin/main`（衝突解完後跑 `hermes doctor`）。
3. `git push fork local/hardening`。
4. 任何 core 修改（如 E8 guard 訊息、E2 Hermes 端 pkill 攔截）一律在本分支 commit＋push，
   不留在工作區。
