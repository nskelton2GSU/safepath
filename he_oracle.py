"""
he_oracle.py — homomorphic encryption proof-of-concept.

The claim: a route can be SCORED by an untrusted server without the
server ever seeing the route.

How it works (Paillier, additively homomorphic):
  1. The user holds a secret key. Only they can decrypt.
  2. The user encrypts their route's feature vector (counts of unlit
     segments, steep segments, etc.) and sends ciphertext to the server.
  3. The server holds secret scoring weights. It multiplies each
     ciphertext by its weight (scalar mult), sums the results (homomorphic
     addition), and returns the encrypted total.
  4. Only the user can decrypt the result.

The server never sees: the route, the features, or the score.

Limitations (be honest about these on stage):
  - Paillier supports addition and scalar multiplication, NOT comparisons.
    Routing itself cannot happen on ciphertext. Only scoring.
  - This is a proof of concept. Paillier is slow; production would use
    a scheme with better performance characteristics.
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    from lightphe import LightPHE
    _HE_AVAILABLE = True
except ImportError:
    _HE_AVAILABLE = False


# ---- Feature names the server expects. Must be fixed, or the server ------
# ---- can't align weights with features. ----------------------------------
FEATURE_NAMES = ("unlit", "steep", "missing_ramp", "on_road")


@dataclass
class EncryptedScoreRequest:
    """What the user sends to the server. Opaque ciphertexts only."""
    encrypted_features: list  # list of ciphertext objects


@dataclass
class EncryptedScoreResponse:
    """What the server sends back. A single opaque ciphertext."""
    encrypted_score: object


class Server:
    """
    An untrusted scoring server. It holds secret weights but never
    sees the user's features. In a real deployment this would be a
    remote service; here it's a class to make the trust boundary
    visually obvious in the demo.
    """
    def __init__(self, weights: dict[str, int]):
        missing = set(FEATURE_NAMES) - set(weights.keys())
        if missing:
            raise ValueError(f"Server missing weights for: {missing}")
        self._weights = weights

    def score(self, request: EncryptedScoreRequest) -> EncryptedScoreResponse:
        """
        Compute sum(feature_i * weight_i) on ciphertext.
        Uses Paillier's homomorphic scalar multiplication and addition.
        """
        if len(request.encrypted_features) != len(FEATURE_NAMES):
            raise ValueError(
                f"expected {len(FEATURE_NAMES)} features, got "
                f"{len(request.encrypted_features)}"
            )

        weighted_terms = []
        for name, ciphertext in zip(FEATURE_NAMES, request.encrypted_features):
            weight = self._weights[name]
            if weight == 0:
                continue
            # Scalar multiplication: E(x)^weight = E(x * weight)
            weighted_terms.append(ciphertext * weight)

        if not weighted_terms:
            return EncryptedScoreResponse(encrypted_score=None)

        # Homomorphic addition: E(a) * E(b) = E(a + b)
        total = weighted_terms[0]
        for term in weighted_terms[1:]:
            total = total + term

        return EncryptedScoreResponse(encrypted_score=total)


class User:
    """
    Holds the secret key. Only the user can decrypt the final score.
    """
    def __init__(self):
        if not _HE_AVAILABLE:
            raise RuntimeError("lightphe not installed; run: pip install lightphe")
        self._scheme = LightPHE(algorithm_name="Paillier")

    def encrypt_features(self, features: dict[str, int]) -> EncryptedScoreRequest:
        missing = set(FEATURE_NAMES) - set(features.keys())
        if missing:
            raise ValueError(f"user missing features: {missing}")
        encrypted = [self._scheme.encrypt(features[name]) for name in FEATURE_NAMES]
        return EncryptedScoreRequest(encrypted_features=encrypted)

    def decrypt_score(self, response: EncryptedScoreResponse) -> int:
        if response.encrypted_score is None:
            return 0
        return self._scheme.decrypt(response.encrypted_score)