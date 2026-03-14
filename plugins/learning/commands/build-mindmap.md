---
description: Generate a mind map in Obsidian MarkMind Rich format from any topic, text, or file
argument-hint: <topic | "text to map" | path/to/file.md>
---

Generate a MarkMind mind map for: $ARGUMENTS

Execute immediately -- no plan mode. This command chains two skills:

1. **Generate mindmap outline** (skill: `learning:generate-mindmap`): brainstorm internally (do not show to user), identify the central theme (2-4 words), extract branches and sub-concepts scaled to complexity level, assign emoji and colors. Save the JSON outline to a temporary file.

2. **Render to MarkMind** (skill: `learning:markmind-mapper`): pipe the JSON outline to `plugins/learning/skills/markmind-mapper/scripts/generate_markmind.py` with `--output` flag to produce the `.md` file.

3. **Present the `.md` file** to the user, ready to drop into their Obsidian vault with the MarkMind plugin.

See `learning:generate-mindmap` for content principles, emoji semantic code, and color palette.
See `learning:markmind-mapper` for the renderer script usage and MarkMind Rich format details.
