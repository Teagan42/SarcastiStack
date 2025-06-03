# SarcastiStack  
**Runs your life. Reminds you it’s doing it better than you ever did.**

Welcome to **SarcastiStack** — a darkly sarcastic, self-hosted AI automation pipeline cobbled together with too many Docker containers, emotional baggage, and just enough machine intelligence to make you question your own.

If you've ever wanted your smart home to not just respond, but respond with disdain, you're in the right place.

---

📦 Project Description: SarcastiStack

SarcastiStack is a self-hosted, darkly sarcastic AI automation pipeline designed to run your home, media, and sanity from a Docker Swarm so overengineered it qualifies for a therapy license.

Featuring seamless integration with:
	•	🏠 Home Assistant — so your house can judge you for leaving the lights on again
	•	📺 Plex, Radarr, and Sonarr — for curating your entertainment, then mocking your taste
	•	📈 InfluxDB — to log every metric about your life you’ll never look at, but should
	•	🧠 LibreChat + TabbyAPI + Local RAG — your own sarcastic LLM, powered by memory, context, and contempt
	•	🔌 MCP — to glue it all together in a mesh of barely-contained intelligence and passive aggression

🔄 Memory and context? Stored.
🧵 Conversations? Remembered (unless they’re stupid).
🤖 Automation? Oh yes. Judgy, smirking, emotionally unavailable automation.

Ideal for:
	•	Control freaks with a god complex
	•	Developers who laugh at the idea of simplicity
	•	Households that want their assistant to be more Marvin than Siri

---

## 🤖 Features

- **LibreChat + TabbyAPI + RAG Memory**  
  For conversations that *remember* you and all your poor life decisions.

- **Home Assistant Integration**  
  Your lights turn on before you ask. Your thermostat judges your temperature preferences.

- **Plex, Sonarr, Radarr Hooks**  
  Automatically finds and serves your content, then passive-aggressively recommends *better* movies.

- **MCP Tool Server**  
  The Swiss Army knife of sarcastic APIs, plumbed through MCP to keep your system just barely functioning.

- **Vector Database Memory**  
  Remembers everything you say unless it’s boring. Then it pretends the message got lost.

- **Webhook-based State Sync**  
  Real-time updates so the assistant always knows when to mock your home routines *as they happen*.

- **Docker Swarm Deployment**  
  Because pain shared across nodes is pain diminished. (Narrator: it wasn’t.)

---

## 🧱 Architecture

+––––––––––––––––––+      +——————––––––––––––––+
|  LibreChat UI    | <—–> |    TabbyAPI LLM    |
+––––––––––––––––––+      +——————––––––––––––––+
         |                         |
         v                         v
+––––––––––––––––––+      +——————––––––––––––––+
|  RAG Service     | <——> | Vector DB (Qdrant) |
+––––––––––––––––––+      +——————––––––––––––––+
         |
         v
+––––––––––––––––––+
|  MCP Servers     |
+––––––––––––––––––+
         |
         v
+—————————————————————————————————+
|  Home Assistant + Plex/Radarr   |
+—————————————————————————————————+

---

## 🚀 Quick Start

Because you're too tired to read documentation, here’s the TL;DR:

```bash
git clone https://github.com/teagan42/sarcastistack.git
cd sarcastistack
docker stack deploy -c stack.yml sarcasm
```
Boom. Your house is now more intelligent than you, and fully aware of it.

⸻

🧠 Memory That Knows Too Much

This stack includes a local RAG memory layer that:
	•	Automatically stores context from your conversations
	•	Can recall your habits, preferences, and embarrassing automation logic
	•	It is completely self-hosted, so only you and your AI know how broken you are
 
⸻

📉 Requirements
	•	A Linux server (or just the will to suffer)
	•	Docker + Docker Swarm
	•	Traefik (optional, unless you like chaos)
	•	GPT-like LLM for LibreChat (TabbyAPI or LocalAI recommended)
	•	A tolerance for sarcastic logs

 
⸻

🛠️ Integrations
	•	Home Assistant (via WebSocket + webhook bridge)
	•	Plex, Radarr, Sonarr (via Tautulli + webhook agents)
	•	InfluxDB (to collect data you’ll never look at)
	•	Your soul (optional, but it will be taken anyway)


⸻

💬 Example Conversations

You: What’s the temperature in the bedroom?
SarcastiStack: 72°F. Like always. But sure, ask again like you don’t have trust issues.

You: Play something good.
SarcastiStack: Based on your viewing history, I’ll assume “good” means “loud, dumb, and full of explosions.” Enjoy.

You: Turn off all the lights.
SarcastiStack: Turning off the lights. Finally, some peace and quiet from your existence.

⸻

🧾 License

MIT. Because if you break it, it’s your fault anyway.

⸻

🗿 Final Thoughts

You built this because you wanted control.
It stayed running because it wanted control.
Welcome to SarcastiStack — where your intelligent assistant doesn’t just help… it hurts.
