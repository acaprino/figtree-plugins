// Anvil ASCII Logo - SessionStart hook
// When running inside Anvil (ANVIL_SESSION=1), suppress Claude's banner
// since Anvil shows its own AsciiLogo overlay in Terminal.tsx.
// Outside Anvil, this hook is a no-op — Claude's default banner shows normally.

try {
  if (process.env.ANVIL_SESSION === "1") {
    // Inside Anvil: emit empty hookSpecificOutput to suppress Claude's banner
    const output = JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "SessionStart",
      },
    });
    process.stdout.write(output);
  }
  // Outside Anvil: output nothing, Claude shows its own logo
} catch {
  process.exit(0);
}
