---
name: file-organizer
description: Use when organizing messy folders (Downloads, Desktop, Documents), finding duplicate files, cleaning up old files, restructuring project directories, separating work from personal files, or automating file cleanup tasks. Triggers on cluttered folders, file chaos, storage cleanup, or directory restructuring needs.
---

# File Organizer

This skill acts as your personal organization assistant, helping you maintain a clean, logical file structure across your computer without the mental overhead of constant manual organization.

## When to Use This Skill

- Your Downloads folder is a chaotic mess
- You can't find files because they're scattered everywhere
- You have duplicate files taking up space
- Your folder structure doesn't make sense anymore
- You want to establish better organization habits
- You're starting a new project and need a good structure
- You're cleaning up before archiving old projects

## What This Skill Does

1. **Analyzes Current Structure**: Reviews your folders and files to understand what you have
2. **Finds Duplicates**: Identifies duplicate files across your system
3. **Suggests Organization**: Proposes logical folder structures based on your content
4. **Automates Cleanup**: Moves, renames, and organizes files with your approval
5. **Maintains Context**: Makes smart decisions based on file types, dates, and content
6. **Reduces Clutter**: Identifies old files you probably don't need anymore
7. **Detects Anti-Patterns**: Flags common organization mistakes and proposes fixes
8. **Recommends Maintenance**: Suggests a sustainable maintenance schedule

## How to Use

### From Your Home Directory

```
cd ~
```

Then run Claude Code and ask for help:

```
Help me organize my Downloads folder
```

```
Find duplicate files in my Documents folder
```

```
Review my project directories and suggest improvements
```

### Specific Organization Tasks

```
Organize these downloads into proper folders based on what they are
```

```
Find duplicate files and help me decide which to keep
```

```
Clean up old files I haven't touched in 6+ months
```

```
Create a better folder structure for my [work/projects/photos/etc]
```

## Instructions

When a user requests file organization help:

1. **Understand the Scope**

   Ask clarifying questions:
   - Which directory needs organization? (Downloads, Documents, entire home folder?)
   - What's the main problem? (Can't find things, duplicates, too messy, no structure?)
   - Any files or folders to avoid? (Current projects, sensitive data?)
   - How aggressively to organize? (Conservative vs. comprehensive cleanup)

   **Optional — Organization Philosophy**: If the user is setting up a top-level structure or reorganizing broadly, briefly propose an organization philosophy from the reference guide (PARA, Johnny Decimal, GTD, 7-Folder). Let the user choose — never force a philosophy. Skip this for simple, scoped tasks like cleaning Downloads.

2. **Analyze Current State**

   Review the target directory:
   ```bash
   # Get overview of current structure
   ls -la [target_directory]

   # Check file types and sizes
   find [target_directory] -type f -exec file {} \; | head -20

   # Identify largest files
   du -sh [target_directory]/* | sort -rh | head -20

   # Count file types
   find [target_directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
   ```

   Summarize findings:
   - Total files and folders
   - File type breakdown
   - Size distribution
   - Date ranges
   - Obvious organization issues

   **Anti-Pattern Detection**: While analyzing, flag any common anti-patterns found:
   - Desktop used as permanent archive (zero permanent files on Desktop is the goal)
   - Unnamed folders (`New Folder`, `New Folder (3)`)
   - Broken versioning (`document_FINAL_v2_DEFINITIVE_copy.docx`)
   - Downloads folder never cleaned (thousands of unsorted files)
   - Same file duplicated in multiple locations (use shortcuts instead)
   - Deeply nested paths approaching the 260-character Windows limit

3. **Identify Organization Patterns**

   Based on the files, determine logical groupings:

   **By Type**:
   - Documents (PDFs, DOCX, TXT)
   - Images (JPG, PNG, SVG)
   - Videos (MP4, MOV)
   - Archives (ZIP, TAR, DMG)
   - Code/Projects (directories with code)
   - Spreadsheets (XLSX, CSV)
   - Presentations (PPTX, KEY)

   **By Purpose**:
   - Work vs. Personal
   - Active vs. Archive
   - Project-specific
   - Reference materials
   - Temporary/scratch files

   **By Date**:
   - Current year/month
   - Previous years
   - Very old (archive candidates)

   **Context-Specific Structures** (use when content matches):
   - **Photos/Video**: `Year/YYYY-MM_event-location/` with RAW, Edited, Export subfolders
   - **Music**: `Artist/[Year] Album/NN - Track.ext`
   - **Work Projects**: Numbered prefixes (`01_Brief/`, `02_Research/`, `03_Assets/`, `04_Deliverables/`) with WIP/FINAL_APPROVED separation
   - **Finance/Personal Docs**: Include expiry dates in filenames (`passport_exp_2030.pdf`), organize by year then type
   - **Code**: Map local paths to remote URLs (`github.com/username/repo/`)

   See `references/organization-guide.md` for detailed templates.

4. **Find Duplicates**

   When requested, search for duplicates:
   ```bash
   # Find exact duplicates by hash
   find [directory] -type f -exec md5 {} \; | sort | uniq -d

   # Find files with same name
   find [directory] -type f -printf '%f\n' | sort | uniq -d

   # Find similar-sized files
   find [directory] -type f -printf '%s %p\n' | sort -n
   ```

   For each set of duplicates:
   - Show all file paths
   - Display sizes and modification dates
   - Recommend which to keep (usually newest or best-named)
   - **Important**: Always ask for confirmation before deleting
   - Suggest using shortcuts/aliases instead of keeping copies if the user needs access from multiple locations

5. **Propose Organization Plan**

   Present a clear plan before making changes:

   ```markdown
   # Organization Plan for [Directory]

   ## Current State
   - X files across Y folders
   - [Size] total
   - File types: [breakdown]
   - Issues: [list problems]
   - Anti-patterns found: [list any detected]

   ## Proposed Structure

   ```
   [Directory]/
   ├── Work/
   │   ├── Projects/
   │   ├── Documents/
   │   └── Archive/
   ├── Personal/
   │   ├── Photos/
   │   ├── Documents/
   │   └── Media/
   └── Downloads/
       ├── To-Sort/
       └── Archive/
   ```

   ## Changes I'll Make

   1. **Create new folders**: [list]
   2. **Move files**:
      - X PDFs → Work/Documents/
      - Y images → Personal/Photos/
      - Z old files → Archive/
   3. **Rename files**: [any renaming patterns]
   4. **Delete**: [duplicates or trash files]

   ## Files Needing Your Decision

   - [List any files you're unsure about]

   Ready to proceed? (yes/no/modify)
   ```

6. **Execute Organization**

   After approval, organize systematically:

   ```bash
   # Create folder structure
   mkdir -p "path/to/new/folders"

   # Move files with clear logging
   mv "old/path/file.pdf" "new/path/file.pdf"

   # Rename files with consistent patterns
   # Example: "YYYY-MM-DD_context_description_v01.ext"
   ```

   **Important Rules**:
   - Always confirm before deleting anything
   - Log all moves for potential undo
   - Preserve original modification dates
   - Handle filename conflicts gracefully
   - Stop and ask if you encounter unexpected situations

   **Optional — File Renaming**: When renaming files, offer to apply consistent naming conventions. Only rename when the user agrees — never auto-rename without consent:
   - ISO 8601 dates: `YYYY-MM-DD` (correct alphabetical sort across all OSes)
   - Formula: `[Date]_[Context]_[Description]_[Version].ext`
   - Zero-padded versioning: `v01`, `v02`, `v03` (minor: `v01.1`, `v01.2`)
   - Separators: `kebab-case` or `snake_case` (never spaces)
   - All lowercase for maximum cross-platform compatibility
   - Zero-padding for sequences: `001`, `002` (prevents `1, 10, 11, 2` sort)
   - Status prefixes when useful: `WIP_`, `DRAFT_`, `REVIEW_`, `APPROVED_`
   - Avoid: `< > : " / \ | ? *`, accents, emoji, leading dots, Windows reserved names (`CON`, `PRN`, `AUX`, `NUL`)
   - Keep filenames under 25-30 characters — let folder context provide the rest
   - Watch for full path length approaching Windows 260-character limit

7. **Provide Summary and Maintenance Tips**

   After organizing:

   ```markdown
   # Organization Complete!

   ## What Changed

   - Created [X] new folders
   - Organized [Y] files
   - Freed [Z] GB by removing duplicates
   - Archived [W] old files
   - Fixed [N] anti-patterns

   ## New Structure

   [Show the new folder tree]

   ## Maintenance Schedule

   To keep this organized:

   | Frequency | Time | Tasks |
   |-----------|------|-------|
   | Weekly | 15 min | Empty Downloads, process Inbox to zero, verify recent files are in place |
   | Monthly | 45 min | Scan for duplicates, verify backups, archive completed projects |
   | Quarterly | 2 hrs | Disk space audit, archive projects inactive 3+ months, test backup restore |
   | Yearly | Half day | Disaster recovery test, retention policy review, structure update |

   ## Quick Commands for You

   ```bash
   # Find files modified this week
   find . -type f -mtime -7

   # Sort downloads by type
   [custom command for their setup]

   # Find duplicates
   [custom command]
   ```

   Want to organize another folder?
   ```

## Examples

### Example 1: Organizing Downloads

**User**: "My Downloads folder is a mess with 500+ files. Help me organize it."

**Process**:
1. Analyzes Downloads folder
2. Finds patterns: work docs, personal photos, installers, random PDFs
3. Detects anti-patterns: broken versioning names, unnamed folders, duplicates
4. Proposes structure:
   - Downloads/
     - Work/
     - Personal/
     - Installers/ (DMG, PKG, EXE, MSI files)
     - Archive/
     - ToSort/ (things needing decisions)
5. Offers to rename files with consistent conventions (ISO dates, kebab-case)
6. Asks for confirmation
7. Moves and optionally renames files
8. Results: 500 files → 5 organized folders with clean names

### Example 2: Finding and Removing Duplicates

**User**: "Find duplicate files in my Documents and help me decide which to keep."

**Output**:
```markdown
# Found 23 Sets of Duplicates (156 MB total)

## Duplicate Set 1: "proposal.pdf"
- `/Documents/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Documents/old/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Desktop/proposal.pdf` (2.3 MB, modified: 2024-03-10)

**Recommendation**: Keep `/Documents/proposal.pdf` (most recent in correct location)
Create shortcut on Desktop if needed. Delete the other 2 copies?

[Continue for all duplicates...]
```

### Example 3: Restructuring Projects Folder

**User**: "Review my ~/Projects directory and suggest improvements."

**Output**:
```markdown
# Analysis of ~/Projects

## Current Structure Issues
- Mix of active and archived projects (3+ years old)
- No consistent naming convention
- Some projects at root, others in random subfolders
- Duplicate folders (project-name, project-name-old, project-name-v2)

## Anti-Patterns Detected
- 4 folders with `_FINAL_v2` naming → needs proper versioning
- `New Folder` and `New Folder (2)` → unnamed, unknown content
- Same README.md duplicated in 3 locations

## Proposed Structure

```
Projects/
├── Active/
│   ├── client-work/
│   ├── side-projects/
│   └── learning/
├── Archive/
│   ├── 2022/
│   ├── 2023/
│   └── 2024/
└── Templates/
```

## Specific Changes
1. Move 12 projects not touched since 2022 → Archive/
2. Consolidate 4 duplicate project folders
3. Rename projects to consistent format: "client-name-project-name"
4. Create Archive for old work

Want me to implement this?
```

### Example 4: Organizing Photos by Date

**User**: "Organize my photo folders by year and month."

**Output**: Creates structure like:
```
Photos/
├── 2023/
│   ├── 2023-01_january/
│   ├── 2023-02_february/
│   └── ...
├── 2024/
│   ├── 2024-01_january/
│   └── ...
└── Unsorted/
```

Then moves photos based on EXIF data or file modification dates. Optionally renames from camera defaults (`IMG_4523.jpg`) to `YYYY-MM-DD_event_NNN.jpg`.

### Example 5: Setting Up a New Top-Level Structure

**User**: "Help me reorganize my entire Documents folder from scratch."

**Process**:
1. Asks which organization philosophy appeals to the user:
   - **PARA**: Simple, 4 folders by actionability (Projects/Areas/Resources/Archives)
   - **Johnny Decimal**: Numeric IDs, max 2 levels, unambiguous references
   - **7-Folder**: Max 7 folders per level, max 3 levels, 343 total
   - **Custom**: Build a structure that fits their specific needs
2. Analyzes existing content to map files to the chosen structure
3. Proposes the migration plan
4. Executes with confirmation at each step

## Common Organization Tasks

### Downloads Cleanup
```
Organize my Downloads folder - move documents to Documents,
images to Pictures, keep installers separate, and archive files
older than 3 months.
```

### Project Organization
```
Review my Projects folder structure and help me separate active
projects from old ones I should archive.
```

### Duplicate Removal
```
Find all duplicate files in my Documents folder and help me
decide which ones to keep.
```

### Desktop Cleanup
```
My Desktop is covered in files. Help me organize everything into
my Documents folder properly.
```

### Photo Organization
```
Organize all photos in this folder by date (year/month) based
on when they were taken.
```

### Work/Personal Separation
```
Help me separate my work files from personal files across my
Documents folder.
```

## Pro Tips

1. **Start Small**: Begin with one messy folder (like Downloads) to build trust
2. **Regular Maintenance**: Run weekly cleanup on Downloads — 15 minutes saves 4 hours/week
3. **Consistent Naming**: Use `YYYY-MM-DD_context_description` format for important files
4. **Archive Aggressively**: Move old projects to Archive instead of deleting
5. **Keep Active Separate**: Maintain clear boundaries between active and archived work
6. **One File, One Place**: Never duplicate files — use shortcuts/aliases for multi-location access
7. **Inbox Zero for Files**: Use a single entry point folder, empty it weekly
8. **Trust the Process**: Let Claude handle the cognitive load of where things go

## Best Practices

### Folder Naming
- Use clear, descriptive names — all lowercase
- Avoid spaces (use hyphens or underscores)
- Be specific: `client-proposals` not `docs`
- Use prefixes for ordering: `01-current`, `02-archive`
- Max 3-4 levels deep for personal files, 5-7 for work environments
- Stay under ~500 items per level

### File Naming
- ISO dates: `2024-10-17_meeting-notes.md`
- Be descriptive: `q3-financial-report.xlsx`
- Use proper versioning: `v01`, `v02` instead of `_FINAL_v2`
- Remove download artifacts: `document-final-v2 (1).pdf` → `document.pdf`
- Include expiry dates for documents that expire: `passport_exp_2030.pdf`
- Status prefixes when useful: `DRAFT_`, `WIP_`, `APPROVED_`

### When to Archive
- Projects not touched in 6+ months
- Completed work that might be referenced later
- Old versions after migration to new systems
- Files you're hesitant to delete (archive first)
- Use compressed archives with README: `YYYY-MM_project-name_archive.7z`

## Related Use Cases

- Setting up organization for a new computer
- Preparing files for backup/archiving
- Cleaning up before storage cleanup
- Organizing shared team folders
- Structuring new project directories
