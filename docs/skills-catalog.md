<!-- このファイルは生成物です。手で編集しないでください。 -->
<!-- 更新: python3 .github/scripts/gen-skills-catalog.py -->

# Skill カタログ

[mattpocock/skills](https://github.com/mattpocock/skills) が提供する skill の一覧。
導入方法と使い方は [skills.md](./skills.md) を参照。

- 上流のリビジョン: `84fdeff`（2026-08-06）
- 収録数: 35 件。うち 20 件はユーザーが明示的に呼び出す skill

**このカタログは自動では更新されない。** 上流が変われば黙って古くなるため、
内容を信頼する前に上のリビジョンを確認すること。

凡例: (ユーザー呼び出し) はモデルが自動起動せず、スラッシュコマンドで明示的に呼ぶもの。

## engineering（18 件）

開発の流れそのものを扱う。このリポジトリの `docs/agents/` が前提にしているのはここ

### `/ask-matt` **(ユーザー呼び出し)**

Ask which skill or flow fits your situation. A router over the skills in this repo.

### `/code-review`

Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".

### `/codebase-design`

Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.

### `/diagnosing-bugs`

Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.

### `/domain-modeling`

Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.

### `/grill-with-docs` **(ユーザー呼び出し)**

A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.

### `/implement` **(ユーザー呼び出し)**

Implement a piece of work based on a spec or set of tickets.

### `/improve-codebase-architecture` **(ユーザー呼び出し)**

Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.

### `/prototype`

Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.

### `/research`

Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.

### `/resolving-merge-conflicts`

Use when you need to resolve an in-progress git merge/rebase conflict.

### `/setup-matt-pocock-skills` **(ユーザー呼び出し)**

Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.

### `/tdd`

Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.

### `/to-spec` **(ユーザー呼び出し)**

Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed.

### `/to-tickets` **(ユーザー呼び出し)**

Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blocking links on a real tracker.

### `/triage` **(ユーザー呼び出し)**

Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs.

### `/wayfinder` **(ユーザー呼び出し)**

Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.

### `/wizard`

Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.


## productivity（7 件）

考えを整理する、教わる、引き継ぐといった作業を扱う

### `/grill-me` **(ユーザー呼び出し)**

A relentless interview to sharpen a plan or design.

### `/grilling`

Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.

### `/handoff` **(ユーザー呼び出し)**

Compact the current conversation into a handoff document for another agent to pick up.

### `/teach` **(ユーザー呼び出し)**

Teach the user a new skill or concept, within this workspace.

### `/to-questionnaire` **(ユーザー呼び出し)**

Turn a decision you can't fully answer into a questionnaire for someone else to fill in.

### `/wait-what` **(ユーザー呼び出し)**

Stop. That last message did not land — re-pitch it.

### `/writing-for-agents`

Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.


## misc（4 件）

特定の場面向けの単発ツール

### `/git-guardrails-claude-code`

Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.

### `/migrate-to-shoehorn`

Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.

### `/scaffold-exercises`

Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.

### `/setup-pre-commit`

Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.


## in-progress（6 件）

上流で作りかけのもの。挙動が変わる前提で扱う

### `/claude-handoff` **(ユーザー呼び出し)**

Hand the current conversation off to a fresh background agent that picks up the work immediately.

### `/loop-me` **(ユーザー呼び出し)**

Grill me about specs for the workflows I want to build, within this workspace.

### `/setup-ts-deep-modules` **(ユーザー呼び出し)**

Wire dependency-cruiser into a TypeScript repo so each package is a deep module — implementation hidden in subfolders, reachable only through its entry-point files. User-invoked.

### `/writing-beats` **(ユーザー呼び出し)**

Writing, exploit — assemble raw material into a journey of beats, grounding each term before a beat leans on it.

### `/writing-fragments` **(ユーザー呼び出し)**

Writing, explore — mine raw fragments, no structure yet.

### `/writing-shape` **(ユーザー呼び出し)**

Writing, exploit — shape raw material into an article, paragraph by paragraph.
