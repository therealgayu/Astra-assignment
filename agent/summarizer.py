import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


def generate_summary(target_url, users_found, techniques_used):
    """
    Calls a local Ollama model to turn raw findings into a human-readable summary.
    """
    if not users_found:
        prompt = (
            f"You are generating one short security report paragraph. "
            f"Do not offer options, do not ask questions, do not add headers — "
            f"output only the final paragraph, nothing else.\n\n"
            f"A WordPress user enumeration tool scanned {target_url} using "
            f"techniques: {', '.join(techniques_used)}. No usernames were found. "
            f"Write exactly 2-3 sentences summarizing this result and its implication."
        )
    else:
        usernames = ", ".join(u["username"] for u in users_found)
        prompt = (
            f"You are generating one short security report paragraph. "
            f"Do not offer options, do not ask questions, do not add headers — "
            f"output only the final paragraph, nothing else.\n\n"
            f"A WordPress user enumeration tool scanned {target_url} using "
            f"techniques: {', '.join(techniques_used)}. "
            f"It discovered these usernames: {usernames}. "
            f"Write exactly 2-3 sentences summarizing what was found, how it was found, "
            f"and the security risk this poses."
        )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        raw = response.json().get("response", "").strip()
        # Safety net: if model still adds a preamble/options, take first paragraph only
        cleaned = raw.split("\n\n")[0].strip()
        return cleaned
    except requests.exceptions.RequestException as e:
        return f"[!] Could not generate AI summary: {e}"


if __name__ == "__main__":
    fake_users = [{"username": "testadmin", "evidence": "rest_api"}]
    summary = generate_summary("http://localhost:8080", fake_users, ["rest_api"])
    print("[AI Agent] Summary:")
    print(summary)