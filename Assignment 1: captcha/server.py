import os, time, json, hmac, hashlib, base64, secrets, random
from flask import Flask, request, jsonify, send_file, make_response

app = Flask(__name__)
SECRET = os.environ.get("CAPTCHA_SECRET", "change-me-in-prod").encode()

ICONS = ["🍎","🍌","🍇","🍊","🍓","🍉","🥑","🥕","🥐","🍞","🧀","🍩","🍪","🍕","🍔","🍟","🌮","🍣","🍤","🍫"]

CHALLENGE_TTL = 120
PASS_TTL = 300
MAX_VERIFY_ATTEMPTS = 3

# Demo storage (for assignment). Use Redis in real apps.
CHALLENGES = {}          # challenge_id -> record
USED_CHALLENGES = set()  # anti-replay
PASS_TOKENS = {}         # pass_id -> payload
USED_PASS = set()        # anti-reuse

def now() -> int:
    return int(time.time())

def b64u_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

def b64u_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "===")

def canonical_json(payload: dict) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()

def hmac_sign(payload: dict) -> str:
    sig = hmac.new(SECRET, canonical_json(payload), hashlib.sha256).digest()
    return b64u_encode(sig)

def hmac_verify(payload: dict, sig: str) -> bool:
    return hmac.compare_digest(hmac_sign(payload), sig)

def get_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr) or "0.0.0.0"

def get_or_set_session_id(resp=None) -> str:
    sid = request.cookies.get("sid")
    if not sid:
        sid = secrets.token_urlsafe(18)
        if resp is not None:
            resp.set_cookie("sid", sid, httponly=True, samesite="Lax")
    return sid

def build_grid(side: int):
    grid_n = side * side
    target = random.choice(ICONS)

    # easy demo: 3x3 always
    k = random.randint(1, 3)
    distractor_pool = [x for x in ICONS if x != target]
    choices = [target] * k + random.choices(distractor_pool, k=grid_n - k)
    random.shuffle(choices)

    correct = sorted([i for i, x in enumerate(choices) if x == target])
    return target, choices, correct

def issue_pass_token(sid: str, ip: str) -> dict:
    pass_id = secrets.token_urlsafe(16)
    payload = {
        "pass_id": pass_id,
        "exp": now() + PASS_TTL,
        "sid": sid,
        "ip_hash": hashlib.sha256((ip + "|pepper").encode()).hexdigest()[:16],
    }
    sig = hmac_sign(payload)
    PASS_TOKENS[pass_id] = payload
    return {"pass_token": b64u_encode(canonical_json(payload)), "pass_sig": sig, "expires_in": PASS_TTL}

def verify_pass_token(pass_token: str, pass_sig: str, sid: str, ip: str) -> tuple[bool, str]:
    try:
        payload = json.loads(b64u_decode(pass_token).decode())
    except Exception:
        return False, "bad_pass_token"

    if not hmac_verify(payload, pass_sig):
        return False, "bad_pass_signature"

    if now() > int(payload.get("exp", 0)):
        return False, "pass_expired"

    if payload.get("sid") != sid:
        return False, "wrong_session"

    pass_id = payload.get("pass_id")
    if not pass_id or pass_id not in PASS_TOKENS:
        return False, "unknown_pass"

    if pass_id in USED_PASS:
        return False, "pass_reused"

    ip_hash = hashlib.sha256((ip + "|pepper").encode()).hexdigest()[:16]
    if payload.get("ip_hash") != ip_hash:
        return False, "ip_mismatch"

    USED_PASS.add(pass_id)
    return True, "ok"

@app.get("/")
def home():
    here = os.path.dirname(os.path.abspath(__file__))
    return send_file(os.path.join(here, "demo.html"))

@app.get("/captcha/new")
def captcha_new():
    resp = make_response()
    sid = get_or_set_session_id(resp)
    ip = get_ip()

    # Always show captcha (easy testing)
    side = 3  # 3x3
    target, choices, correct = build_grid(side)

    challenge_id = secrets.token_urlsafe(16)
    exp = now() + CHALLENGE_TTL

    CHALLENGES[challenge_id] = {
        "exp": exp,
        "correct": correct,
        "attempts": 0,
        "sid": sid,
        "ip": ip,
        "side": side,
        "target": target,
    }

    public_payload = {"challenge_id": challenge_id, "exp": exp, "sid": sid}
    sig = hmac_sign(public_payload)

    resp.set_data(json.dumps({
        "ok": True,
        "prompt": f"Click all {target}",
        "side": side,
        "choices": choices,
        "challenge": public_payload,
        "sig": sig,
        "expires_in": CHALLENGE_TTL,
        "attempts_left": MAX_VERIFY_ATTEMPTS
    }))
    resp.mimetype = "application/json"
    return resp

@app.post("/captcha/verify")
def captcha_verify():
    ip = get_ip()
    data = request.get_json(force=True) or {}
    picked = data.get("picked", [])
    challenge = data.get("challenge", {})
    sig = data.get("sig", "")

    sid = request.cookies.get("sid") or ""
    if not sid:
        return jsonify({"ok": False, "reason": "missing_session"}), 400

    if not isinstance(challenge, dict) or not hmac_verify(challenge, sig):
        return jsonify({"ok": False, "reason": "bad_signature"}), 400

    if challenge.get("sid") != sid:
        return jsonify({"ok": False, "reason": "wrong_session"}), 400

    challenge_id = challenge.get("challenge_id", "")
    exp = int(challenge.get("exp", 0))

    if now() > exp:
        return jsonify({"ok": False, "reason": "expired"}), 400

    if not challenge_id or challenge_id not in CHALLENGES:
        return jsonify({"ok": False, "reason": "unknown_challenge"}), 400

    if challenge_id in USED_CHALLENGES:
        return jsonify({"ok": False, "reason": "replay"}), 400

    rec = CHALLENGES[challenge_id]

    # bind to session & ip
    if rec["sid"] != sid:
        return jsonify({"ok": False, "reason": "challenge_context_mismatch"}), 400
    if rec["ip"] != ip:
        return jsonify({"ok": False, "reason": "ip_mismatch"}), 400

    # attempts
    rec["attempts"] += 1
    attempts_left = MAX_VERIFY_ATTEMPTS - rec["attempts"]

    if rec["attempts"] > MAX_VERIFY_ATTEMPTS:
        USED_CHALLENGES.add(challenge_id)
        return jsonify({
            "ok": False,
            "reason": "blocked",
            "message": "This doesn’t look like human behaviour. Please try a new challenge."
        }), 403

    # normalize picks
    try:
        picked_norm = sorted({int(i) for i in picked})
    except Exception:
        return jsonify({"ok": False, "reason": "bad_picks", "attempts_left": attempts_left}), 400

    if picked_norm == rec["correct"]:
        USED_CHALLENGES.add(challenge_id)
        pass_pack = issue_pass_token(sid, ip)
        return jsonify({"ok": True, "message": "Human verified ✅", "attempts_left": attempts_left, **pass_pack})

    # wrong
    if attempts_left <= 0:
        USED_CHALLENGES.add(challenge_id)
        return jsonify({
            "ok": False,
            "reason": "blocked",
            "message": "This doesn’t look like human behaviour. Please try a new challenge."
        }), 403

    return jsonify({
        "ok": False,
        "reason": "wrong",
        "attempts_left": attempts_left,
        "message": "Wrong selection. Try again."
    }), 403

if __name__ == "__main__":
    app.run(debug=True)