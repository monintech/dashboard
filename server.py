import http.server
import os
import json
import urllib.request
import urllib.parse
import gzip

PORT = int(os.environ.get("PORT", 8080))
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://itzgaxxfgbhxqthelxml.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0emdheHhmZ2JoeHF0aGVseG1sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzM2ODMwMSwiZXhwIjoyMDg4OTQ0MzAxfQ.48ybXcbQQOUQJB7__55VtwyHxjXGlHXyAB-E0YGwiic")

def fetch_table(table, query=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}{query}"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def build_context():
    try:
        influencers = fetch_table("influencers", "?order=followers.desc.nullslast&limit=50")
        playlists = fetch_table("playlists", "?limit=30")
        articles = fetch_table("articles_tracker", "?order=created_at.desc&limit=10")
        content = fetch_table("content_calendar", "?order=created_at.desc&limit=10")
        promo = fetch_table("promo_pages", "?limit=20")
        research = fetch_table("research_sources", "?order=created_at.desc&limit=20")
    except Exception as e:
        return f"Error fetching data: {e}"

    lines = []
    lines.append("# Music Manager Memory — Amina Monae")
    lines.append("\n## Artist")
    lines.append("- Name: Amina Monae (AI music artist, persona: Brittany)")
    lines.append("- Song: Trust Nobody — R&B/Soul pain anthem for women")
    lines.append("- Target: Women 18-35 — heartbreak, betrayal, toxic relationships")
    lines.append("- Release Date: April 1, 2026")
    lines.append("- Label: New Aura Empire INC (newauraempire@gmail.com)")
    lines.append("- Angle: AI artist with organic Selena Gomez co-sign")
    lines.append("- Social: TikTok @amina_monae | Instagram @amina.monae")

    lines.append(f"\n## Influencers ({len(influencers)} total)")
    for i in influencers[:20]:
        h = f"@{i['handle']}" if i.get('handle') else ""
        f_ = f"{int(i['followers']):,}" if i.get('followers') else "?"
        lines.append(f"- {i.get('name','?')} ({i.get('platform')}) {h} {f_} followers")

    lines.append(f"\n## Promo Pages ({len(promo)} total)")
    for p in promo:
        h = f"@{p['handle']}" if p.get('handle') else ""
        lines.append(f"- {p.get('name','?')} {h} — {p.get('niche','')}")

    lines.append(f"\n## Playlist Leads ({len(playlists)} total)")
    for pl in playlists[:15]:
        lines.append(f"- {(pl.get('name') or '')[:80]} ({pl.get('platform')}) status:{pl.get('status')}")

    lines.append(f"\n## Articles & Press ({len(articles)} total)")
    for a in articles[:10]:
        lines.append(f"- [{a.get('article_type')}] {(a.get('title') or '')[:80]} — {a.get('status')} — {a.get('publication','')}")

    lines.append(f"\n## Content Calendar ({len(content)} recent posts)")
    for c in content[:5]:
        lines.append(f"- {c.get('platform')} | {c.get('content_type')} | {c.get('goal')} | {c.get('status')}")

    lines.append(f"\n## Research Sources ({len(research)} recent)")
    for r in research[:10]:
        lines.append(f"- [{r.get('topic')}] {(r.get('title') or '')[:80]}")

    lines.append("\n## Infrastructure")
    lines.append("- Supabase: itzgaxxfgbhxqthelxml.supabase.co")
    lines.append("- Research Agent: Railway, daily 6am UTC")
    lines.append("- Music Manager: Railway, Mondays 6am UTC")
    lines.append("- Dashboard: monintech/dashboard on Railway")
    lines.append("- GitHub: monintech org")

    return "\n".join(lines)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/context" or self.path == "/memory":
            context = build_context()
            body = context.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass


print(f"Dashboard running on port {PORT}")
http.server.HTTPServer(("", PORT), Handler).serve_forever()
