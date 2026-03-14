---
name: generate-mindmap
description: "Brainstorm and generate a structured mindmap JSON outline from any content (books, articles, topics, notes, conversations). Use this skill whenever the user asks to create a mind map, mappa mentale, mappa concettuale, concept map, or visual summary. Also trigger when the user says 'mindmap', 'mind map', 'mappa', or asks to visualize/map/schematize any content. The skill handles content analysis, hierarchy design, emoji assignment, and color coding -- outputting a JSON structure that can be rendered by markmind-exporter or any other renderer."
---

# Generate Mindmap

Analyze content and produce a structured mindmap JSON outline. This skill focuses on the intellectual work: extracting themes, building hierarchy, assigning visual attributes. The output is a renderer-agnostic JSON structure.

## Parameters

The user can specify these parameters when requesting a mind map. If not specified, use **normal** complexity and the default max depth for that complexity.

### Complexity

| Level        | L2 branches | L3 per branch | L4 per L3 | Default max depth | Description                       |
| ------------ | ----------- | ------------- | --------- | ----------------- | --------------------------------- |
| **essential** | 3-4         | 1-2           | 0         | 2                 | Minimal overview, few nodes       |
| **normal**    | 5-7         | 2-4           | 1-3       | 4                 | Balanced coverage (default)       |
| **detailed**  | 7-10        | 3-5           | 2-4       | 5                 | Deep, comprehensive exploration   |

### Max depth

Maximum number of hierarchy levels below root (L2 = depth 1, L3 = depth 2, etc.). Overrides the complexity default if specified. Range: 1-6.

## Workflow

### Step 1: Analyze content

Identify the subject matter, key themes, and relationships. For file inputs, read the file first.

### Step 2: Build outline

1. **Identify the central theme** in 2-4 words
2. **Extract main branches** (L2) -- count varies by complexity level
3. **For each branch, extract sub-concepts** (L3) -- count varies by complexity level. Each is a keyword or micro-phrase (2-4 words max)
4. **For deeper levels (L4+)** -- only if max depth allows. Single keyword or keyword pair
5. **Assign emoji** to every L2 and L3 node using the semantic code below
6. **Assign colors** to each L2 branch from the palette
7. **Verify depth** -- no node exceeds the max depth limit

Do NOT skip this phase. The quality of the map depends entirely on the brainstorming outline.

### Step 3: Output

Write the mindmap in the requested format. Default is **JSON** unless the user explicitly asks for markdown.

#### JSON format (default)

```json
{
  "root": "Central Theme",
  "branches": [
    {
      "text": "Branch One",
      "color": "#ff6b6b",
      "children": [
        {
          "text": "Sub-concept A",
          "children": [
            { "text": "Detail 1" },
            { "text": "Detail 2" }
          ]
        }
      ]
    }
  ]
}
```

Save to a file (e.g., `/tmp/mindmap-outline.json` or next to the target output) so downstream renderers (markmind-exporter, forcegraph-exporter) can consume it.

#### Markdown format

When the user requests markdown output, produce a nested bullet list:

```markdown
# Central Theme

- Branch One
  - Sub-concept A
    - Detail 1
    - Detail 2
- Branch Two
  - Sub-concept B
```

Rules for markdown output:
- Root becomes an H1 heading
- L2 branches are top-level bullets
- Each deeper level adds one indent (2 spaces)
- Preserve emoji prefixes on all nodes
- Colors are omitted (markdown has no color support)
- Save as `.md` file

## Content Principles

Follow the E-Myth model: **complete coverage, balanced branches, equal weight across all L2 rami**. No Pareto filtering. The goal is a comprehensive visual reference, not a highlight reel.

- Every node = **keyword or micro-phrase**, never a full sentence
- Prefer nouns and action verbs; strip articles and prepositions
- Causal/sequential relations: use arrows in node text
- Opposites/tensions: use contrasting symbols
- Never use the em dash character

### Emoji Semantic Code

| Function                     | Emoji |
| ---------------------------- | ----- |
| Central concept / nucleus    | 🎯    |
| Definition / "what is it"    | 📌    |
| Process / sequence           | ⚙️    |
| Risk / warning               | ⚠️    |
| Advantage / strength         | ✅    |
| Disadvantage / limit         | ❌    |
| Concrete example             | 💡    |
| Cross-branch link            | 🔗    |
| Open question / explore      | ❓    |
| Numeric data / metric        | 📊    |
| Person / role                | 👤    |
| Time / phase                 | ⏳    |

Add domain-specific emoji where useful (🧠 psychology, 💻 tech, 💰 finance, 📖 book, etc.). Emoji always goes **before** the keyword.

### Color Palette (L2 branches)

| Branch # | Hex       | Name       |
| -------- | --------- | ---------- |
| 1        | #ff6b6b   | Coral      |
| 2        | #4ecdc4   | Teal       |
| 3        | #95e77e   | Lime       |
| 4        | #a8e6cf   | Mint       |
| 5        | #ffd3b6   | Peach      |
| 6        | #d4a5f5   | Lavender   |
| 7        | #f7dc6f   | Yellow     |
| 8        | #85c1e9   | Sky        |

## JSON Schema

### Root level

| Field      | Type   | Required | Description                |
| ---------- | ------ | -------- | -------------------------- |
| root       | string | yes      | Central theme text (2-4 words, with emoji) |
| branches   | array  | yes      | List of L2 branch objects  |

### Branch / child node

| Field      | Type   | Required | Description                |
| ---------- | ------ | -------- | -------------------------- |
| text       | string | yes      | Node label (keyword/micro-phrase with emoji for L2/L3) |
| color      | string | L2 only  | Hex color from palette (only on L2 branches) |
| children   | array  | no       | Nested child nodes         |
