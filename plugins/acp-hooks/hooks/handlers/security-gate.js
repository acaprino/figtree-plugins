// Security Gate - PreToolUse hook (disablable)
// Blocks Write/Edit operations that would persist hardcoded secrets to disk.
// This runs BEFORE the write executes, so a detected secret never touches the
// filesystem. (Previously ran as PostToolUse -- kept for reference: on
// PostToolUse, exit 1 surfaces an error but the write already happened.)
//
// Toggle: set "securityGate" to false in ~/.claude/acp-config.json to disable.

const fs = require("fs");
const path = require("path");

const homeDir = process.env.HOME || process.env.USERPROFILE;
const acpConfigPath = path.join(homeDir, ".claude", "acp-config.json");
const legacyConfigPath = path.join(homeDir, ".claude", "figs-config.json");
const configPath = fs.existsSync(acpConfigPath) ? acpConfigPath : legacyConfigPath;

// Check if security gate is enabled
let enabled = true;
try {
  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  if (config.securityGate === false) {
    enabled = false;
  }
} catch {
  // No config file = enabled by default
}

if (!enabled) {
  process.exit(0);
}

// Get the tool event from stdin
let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => { input += chunk; });
process.stdin.on("end", () => {
  try {
    const event = JSON.parse(input);
    const toolName = event.tool_name || "";

    // Only check Write and Edit operations
    if (toolName !== "Write" && toolName !== "Edit") {
      process.exit(0);
    }

    const filePath = event.tool_input?.file_path || "";
    const ext = path.extname(filePath).toLowerCase();

    // Skip files unlikely to contain hardcoded secrets
    const skipExts = [".md", ".lock", ".csv", ".svg", ".png", ".jpg", ".gif", ".ico"];
    const skipFiles = ["package-lock.json", "tsconfig.json", "tslint.json", "eslintrc.json", ".prettierrc.json"];
    const skipPatterns = ["migration"];

    if (skipExts.includes(ext)) {
      process.exit(0);
    }

    const fileName = path.basename(filePath).toLowerCase();
    if (skipFiles.some(f => fileName === f)) {
      process.exit(0);
    }

    if (skipPatterns.some(p => filePath.toLowerCase().includes(p))) {
      process.exit(0);
    }

    // Check content for potential secrets
    const content = event.tool_input?.content || event.tool_input?.new_string || "";

    // Common secret patterns
    const secretPatterns = [
      /(?:api[_-]?key|apikey)\s*[:=]\s*["'][a-zA-Z0-9_\-]{20,}["']/i,
      /(?:secret|password|passwd|pwd)\s*[:=]\s*["'][^"']{8,}["']/i,
      /(?:token)\s*[:=]\s*["'][a-zA-Z0-9_\-]{20,}["']/i,
      /(?:sk|pk)[-_](?:live|test)[-_][a-zA-Z0-9]{20,}/,
      /(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}/,
      /xox[bpors]-[a-zA-Z0-9\-]{10,}/,
      /eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}/,
      /AKIA[0-9A-Z]{16}/,
      /-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----/,
    ];

    for (const pattern of secretPatterns) {
      if (pattern.test(content)) {
        // PreToolUse: exit 1 blocks the Write/Edit before it executes.
        // Emit a PreToolUse-shaped JSON decision so Claude sees the reason.
        const decision = {
          hookSpecificOutput: {
            hookEventName: "PreToolUse",
            permissionDecision: "deny",
            permissionDecisionReason:
              `[Security Gate] Potential hardcoded secret detected in ${path.basename(filePath)}. ` +
              `Pattern matched: ${pattern.source.substring(0, 40)}... ` +
              `Move secrets to .env or a secure vault, then retry.`,
          },
        };
        process.stdout.write(JSON.stringify(decision));
        process.exit(0);
      }
    }

    process.exit(0);
  } catch {
    // Fail closed -- don't allow unchecked operations
    const decision = {
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "[Security Gate] Failed to parse hook input, blocking as precaution.",
      },
    };
    process.stdout.write(JSON.stringify(decision));
    process.exit(0);
  }
});
