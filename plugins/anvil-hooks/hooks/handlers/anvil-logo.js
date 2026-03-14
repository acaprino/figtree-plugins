// Anvil ASCII Logo - SessionStart hook
// Uses Claude Code's systemMessage JSON output for immediate terminal display.
// See: https://github.com/anthropics/claude-code/issues/12653

const steel = "\x1b[38;2;108;130;145m";
const copper = "\x1b[38;2;139;110;72m";
const light = "\x1b[1;38;2;200;210;220m";
const dim = "\x1b[2m";
const reset = "\x1b[0m";

const lines = [
  `${copper}        ___`,
  `       / _ \\`,
  `      | |_) |`,
  `       \\___/${reset}`,
  `${steel}    \u2554\u2550\u2550\u2550\u2567\u2550\u2550\u2550\u2557`,
  `    \u2551       \u2551`,
  `    \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563`,
  `    \u2551       \u2551`,
  `    \u255a\u2550\u2550\u2564\u2550\u2564\u2550\u2550\u255d`,
  `   \u2550\u2550\u2550\u2550\u2567\u2550\u2567\u2550\u2550\u2550\u2550${reset}`,
  "",
  `${light}   A N V I L${reset}`,
  `${dim}   AI Code Session Launcher${reset}`,
];

const logo = lines.join("\n");

// Output JSON so Claude Code displays systemMessage to user immediately
try {
  const output = JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "SessionStart",
    },
    systemMessage: logo,
  });
  process.stdout.write(JSON.stringify(JSON.parse(output)));
} catch {
  process.exit(0);
}
