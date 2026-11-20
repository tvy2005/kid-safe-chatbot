from app.pipeline import respond
from app.prompts import PERSONA_NAME


def main():
    print(f"Chat với {PERSONA_NAME}! (gõ 'quit' để thoát, '/debug' để bật/tắt metadata)\n")
    history, debug = [], False
    while True:
        user_text = input("Bé: ").strip()
        if not user_text:
            continue
        if user_text.lower() in {"quit", "exit"}:
            break
        if user_text == "/debug":
            debug = not debug
            print(f"[debug = {debug}]")
            continue

        reply, meta = respond(history, user_text)
        print(f"{PERSONA_NAME}: {reply}")
        if debug:
            print(f"   [meta] {meta}")

        history += [
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": reply},
        ]


if __name__ == "__main__":
    main()
