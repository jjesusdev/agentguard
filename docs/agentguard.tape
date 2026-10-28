# AgentGuard v1.0 Demo - Forensic Audit Multi-Agent
Output docs/demo.gif
Output docs/demo.mp4

Set Theme "Catppuccin Frappe"
Set FontSize 18
Set Width 1200
Set Height 600
Set Margin 40
Set MarginFill "#1e1e2e"
Set BorderRadius 12
Set TypingSpeed 40ms
Set Framerate 30

# Setup hidden
Hide
Type "cd /home/champagnejesus/proyectos/agentguard"
Enter
Type "mkdir -p var/lib/agentguard/sessions"
Enter
Type "python generate_sample.py"
Enter
Show

Type "uv run agentguard run --session opencode-demo --agent opencode"
Enter
Sleep 3s

Type "uv run agentguard verify opencode-demo"
Enter
Sleep 2s

Type "uv run agentguard report opencode-demo --output docs/report.html"
Enter
Sleep 2s

Type "ls -lh docs/report.html var/lib/agentguard/sessions/opencode-demo.jsonl"
Enter
Sleep 3s
