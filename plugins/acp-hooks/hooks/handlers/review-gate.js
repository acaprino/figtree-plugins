// Review Gate - PreToolUse hook (disablable)
// Blocks PR creation and merges to main/master until /code-review is run
// Toggle: set "reviewGate" to false in ~/.claude/acp-config.json to disable

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const homeDir = process.env.HOME || process.env.USERPROFILE;
const acpConfigPath = path.join(homeDir, ".claude", "acp-config.json");
const legacyConfigPath = path.join(homeDir, ".claude", "figs-config.json");
const configPath = fs.existsSync(acpConfigPath) ? acpConfigPath : legacyConfigPath;

// Check if review gate is enabled
let enabled = true;
try {
  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  if (config.reviewGate === false) {
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

    // Only check Bash commands
    if (toolName !== "Bash") {
      process.exit(0);
    }

    const command = (event.tool_input?.command || "").trim();

    // Bypass: --no-review escape hatch (match as discrete argument)
    if (command.split(/\s+/).includes("--no-review")) {
      process.exit(0);
    }

    let triggered = false;
    let reason = "";

    // Check for PR creation
    if (/\bgh\s+pr\s+create\b/.test(command)) {
      triggered = true;
      reason = "PR creation detected. Run /code-review before creating a PR, then retry this command.";
    }

    // Check for merge INTO main/master -- only block when on main/master
    if (!triggered && /\bgit\s+merge\b/.test(command)) {
      try {
        const currentBranch = execSync("git rev-parse --abbrev-ref HEAD", { encoding: "utf8", timeout: 5000 }).trim();
        if (/^(main|master)$/.test(currentBranch)) {
          triggered = true;
          reason = "Merge into main/master detected. Run /code-review before merging to main/master, then retry this command. Add --no-review to bypass.";
        }
      } catch {
        // If we can't determine branch, fall back to heuristic
        const mergeMatch = command.match(/\bgit\s+merge\s+(?:--[^\s]+\s+)*([^\s-][^\s]*)/);
        if (mergeMatch && !/^(main|master)$/.test(mergeMatch[1])) {
          triggered = true;
          reason = "Merge detected that may target main/master. Run /code-review before merging, then retry. Add --no-review to bypass.";
        }
      }
    }

    if (!triggered) {
      process.exit(0);
    }

    const output = {
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        decision: "block",
        reason: reason
      }
    };

    process.stdout.write(JSON.stringify(output));
  } catch {
    // If we can't parse input, allow the operation
    process.exit(0);
  }
});
