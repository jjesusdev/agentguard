# AgentGuard v1.0 Professional Demo
Output docs/demo.gif
Output docs/demo.mp4

# Visual Settings
Set Theme "Catppuccin Frappe"
Set FontSize 18
Set Width 1200
Set Height 600
Set Margin 40
Set MarginFill "#1e1e2e"
Set BorderRadius 12
Set TypingSpeed 60ms
Set Framerate 30

# Setup hidden environment
Hide
Type "cd /home/champagnejesus/proyectos/agentguard"
Enter
Type "mkdir -p var/lib/agentguard/sessions"
Enter
Type "python3 generate_sample.py"
Enter
Type "mkdir -p ~/.opencode/agentguard"
Enter
Type "cp var/lib/agentguard/sessions/opencode-demo.raw.jsonl ~/.opencode/agentguard/opencode-demo.jsonl"
Enter
Type "clear"
Enter
Show

# Demo Sequence
Type "agentguard install-hooks --agent opencode"
Enter
Sleep 800ms

Type "agentguard run --session opencode-demo --agent opencode"
Enter
Sleep 2s

Type "agentguard verify opencode-demo"
Enter
Sleep 1s

Type "agentguard report opencode-demo --output docs/report.html"
Enter
Sleep 1s

Type "ls -lh docs/report.html"
Enter
Sleep 3s
