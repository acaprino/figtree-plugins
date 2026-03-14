// Skill Awareness - SessionStart hook
// Injects the anvil-forge skill content into every session so Claude
// knows to check for and invoke relevant skills before responding.
// Mirrors the pattern from obra/superpowers using-superpowers hook.

const fs = require("fs");
const path = require("path");

const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, "../..");
const anvilToolsetRoot = path.resolve(pluginRoot, "../..");
const skillPath = path.join(anvilToolsetRoot, "plugins", "ai-tooling", "skills", "anvil-forge", "SKILL.md");

let skillContent = "";
try {
  skillContent = fs.readFileSync(skillPath, "utf8");
} catch (err) {
  if (err.code === "ENOENT") {
    process.exit(0);
  }
  throw err;
}

try {
  const context = `<IMPORTANT>\nYou have the Anvil skill system.\n\n**Below is the full content of your 'ai-tooling:anvil-forge' skill -- your guide to using skills. For all other skills, use the 'Skill' tool:**\n\n${skillContent}\n</IMPORTANT>`;

  const output = {
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: context
    }
  };

  process.stdout.write(JSON.stringify(output));
} catch {
  // Silent fail -- never block session startup
  process.exit(0);
}
