---
description: Generate a mind map in Obsidian MarkMind Rich format from any topic, text, or file
argument-hint: <topic | "text to map" | path/to/file.md>
---

Generate a MarkMind mind map for: $ARGUMENTS

Execute immediately -- no plan mode. Follow the full `learning:markmind-mapper` skill workflow:

1. **Brainstorm internally** (do not show to user): identify the central theme (2-4 words), extract 5-7 L2 branches, 2-4 L3 sub-concepts per branch, 1-3 L4 leaf details per sub-concept. Assign emoji (semantic code from skill) and colors (coral, teal, lime, mint, peach, lavender, yellow, sky) to each L2 branch.

2. **Run the script**: pipe the JSON outline to `plugins/learning/skills/markmind-mapper/scripts/generate_markmind.py` with `--title` and `--output` flags.

3. **Present the `.md` file** to the user, ready to drop into their Obsidian vault with the MarkMind plugin.

See `learning:markmind-mapper` for the full content principles, emoji semantic code, color palette, and script usage.
