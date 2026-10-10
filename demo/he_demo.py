"""
demo/he_demo.py

Stage demo: a route is scored by a server that never sees it.

Run:  python demo/he_demo.py

Designed to be readable from a projector. The point is the split
between what the USER knows and what the SERVER knows.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from he_oracle import User, Server, FEATURE_NAMES


def line(s=""):
    print(s)


def main() -> int:
    line("=" * 68)
    line(" SafePath — homomorphic scoring demo")
    line(" A server scores a route without ever seeing it.")
    line("=" * 68)
    line()

    # ---- Setup ---------------------------------------------------------
    line("[setup] User generates a keypair. The secret key never leaves the user.")
    user = User()

    # Server holds secret weights. The user never sees these either.
    server_weights = {"unlit": 5, "steep": 8, "missing_ramp": 10, "on_road": 3}
    server = Server(weights=server_weights)
    line("[setup] Server holds secret scoring weights (not shown).")
    line()

    # ---- User side -----------------------------------------------------
    user_features = {"unlit": 3, "steep": 2, "missing_ramp": 1, "on_road": 4}
    line(f"[user]  Route features (private to the user):")
    for name in FEATURE_NAMES:
        line(f"          {name}: {user_features[name]}")
    line()

    line("[user]  Encrypting features...")
    request = user.encrypt_features(user_features)

    # Show that the ciphertext is opaque
    sample = request.encrypted_features[0]
    sample_str = repr(sample)[:48] + "..."
    line(f"[user]  Sending to server. First ciphertext looks like:")
    line(f"          {sample_str}")
    line()

    # ---- Server side ---------------------------------------------------
    line("[server] Received ciphertexts. Cannot decrypt them.")
    line("[server] Computing weighted score homomorphically...")
    response = server.score(request)
    line("[server] Done. Returning encrypted score.")
    line()

    # ---- User decrypts -------------------------------------------------
    line("[user]  Decrypting score locally...")
    score = user.decrypt_score(response)

    # Compute expected for verification
    expected = sum(user_features[n] * server_weights[n] for n in FEATURE_NAMES)
    line(f"[user]  Decrypted score: {score}")
    line(f"[user]  Expected score:  {expected}")
    line()

    if score != expected:
        line("MISMATCH — something is wrong.")
        return 1

    line("=" * 68)
    line(" The server scored the route without ever seeing it.")
    line("=" * 68)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())