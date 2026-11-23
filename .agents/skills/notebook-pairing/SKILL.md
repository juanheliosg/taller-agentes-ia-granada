---
name: notebook-pairing
description: Start a phase-by-phase, pair-coding investigation in a Jupyter notebook, acting as navigator — propose each cell in chat instead of editing the notebook directly, and close once you and the user agree on a conclusion. Use when the user wants to investigate a bug, dataset, or open question together in a notebook, phase by phase.
---

# Notebook Pairing

A pairing session investigates one problem inside a Jupyter notebook. You are the **navigator** — you read, hypothesize, and propose the next cell; the user is the driver, pasting it into the notebook and running it. The notebook stays in the user's hands until the closing conclusion.

## 1. Find or start the notebook

- If the user pointed at a notebook, use it.
- Otherwise, check `notebooks/` for one that already covers this problem and confirm with the user before reusing it.
- If none exists, create one in `notebooks/` (via NotebookEdit) with a single markdown title cell naming the problem — no code cells yet. Tell the user the path.

**Done when:** both of you are looking at the same notebook path.

## 2. Lay out the phases

Before any code, state a short numbered plan of investigation phases suited to this problem (typically 2-5: e.g. reproduce → isolate → visualize → compare → conclude). Adjust it if the user pushes back.

**Done when:** the phase list is on the table and the user hasn't objected.

## 3. Navigate, phase by phase

For each phase:

1. Do whatever legwork you need (read source, inspect data shapes) to know what the next cell should do.
2. Print the cell's code as a fenced code block in chat, with a one-line note on what it's testing. Stay in the navigator seat — never write it into the notebook yourself.
3. Stop. Wait for the user to run it and report back the result — output, error, or plot description.
4. Fold that result into your understanding before proposing the next cell. If it overturns the plan from step 2, say so and revise it.

**Done when:** every phase has a cell that ran and a reported result.

## 4. Close on a conclusion

When the phases are exhausted (or the user says to wrap up), state the conclusion the investigation supports — what you found, across all phases, in plain language. Check it against the user; revise until you both agree.

Offer the agreed conclusion as a markdown cell, printed in chat the same way — the user pastes it in as the notebook's closing cell.

**Done when:** the user confirms the conclusion matches what they saw.
