# Learning Plugin

> Generate mind maps in Obsidian MarkMind Rich format from any content -- books, articles, topics, notes, or conversations.

## Skills

### `generate-mindmap`

Brainstorm and generate a structured mindmap JSON outline from any content. Handles content analysis, hierarchy design, emoji assignment, and color coding -- outputting a renderer-agnostic JSON structure.

| | |
|---|---|
| **Invoke** | Skill reference or via `/build-mindmap` |
| **Use for** | Content analysis, brainstorming, hierarchy extraction, concept mapping |

**Workflow:**
1. **Analyze** -- identify subject matter, key themes, and relationships
2. **Build outline** -- extract central theme, main branches (L2), sub-concepts (L3), leaf details (L4+)
3. **Output** -- JSON file with root, branches, children, colors, and emoji

### `markmind-mapper`

Render a mindmap JSON outline into Obsidian MarkMind Rich format. Takes a pre-built JSON structure and converts it into a `.md` file for the MarkMind plugin.

| | |
|---|---|
| **Invoke** | Skill reference or via `/build-mindmap` |
| **Use for** | Converting mindmap JSON to MarkMind Rich format for Obsidian |

**Workflow:**
1. **Locate** -- find the mindmap outline JSON (file, prior generate-mindmap output, or inline)
2. **Render** -- pipe JSON to `generate_markmind.py` script for coordinate calculation and formatting
3. **Output** -- ready-to-use `.md` file for Obsidian MarkMind plugin

**Includes:**
- `references/markmind-rich-spec.md` -- MarkMind Rich format specification
- `scripts/generate_markmind.py` -- JSON-to-MarkMind generator script

---

## Commands

### `/build-mindmap`

Generate a MarkMind mind map from any topic, text, or file. Chains `generate-mindmap` (brainstorming) and `markmind-mapper` (rendering).

```
/build-mindmap Python asyncio patterns
/build-mindmap "text to map"
/build-mindmap path/to/file.md
```

**Output:** `.md` file ready for Obsidian MarkMind plugin.
