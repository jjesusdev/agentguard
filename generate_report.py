from pathlib import Path
import json

def generate_report(session_id: str, journal_dir: Path, output_path: Path):
    journal_path = journal_dir / f"{session_id}.jsonl"
    events = []
    if journal_path.exists():
        with journal_path.open() as f:
            for line in f:
                events.append(json.loads(line))
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>AgentGuard Report {session_id}</title></head>
<body>
<h1>AgentGuard Forensic Report</h1>
<p>Session: {session_id}</p>
<p>Events: {len(events)}</p>
<table border="1"><tr><th>seq</th><th>type</th><th>tool</th><th>path</th></tr>"""
    for e in events:
        html += f"<tr><td>{e.get('seq')}</td><td>{e.get('type')}</td><td>{e.get('tool_name')}</td><td>{e.get('path')}</td></tr>"
    html += "</table></body></html>"
    output_path.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    generate_report("opencode-demo", Path("var/lib/agentguard/sessions"), Path("report.html"))
    print("report.html generated")
