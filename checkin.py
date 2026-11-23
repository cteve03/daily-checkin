import json, os, sys, urllib.request

BASE = "https://aiker.top/api"
CID = os.environ.get("CHECKIN_COURSE_ID", "12a0c344-9471-4014-8d7f-2081dce96f39")
USER = os.environ.get("CHECKIN_USER", "")
PASS = os.environ.get("CHECKIN_PASS", "")


def call(path, data=None, tok=None):
    h = {"Content-Type": "application/json", "X-Device-Id": "a1b2c3d4e5f6a7b8",
         "Accept": "application/json", "User-Agent": "Mozilla/5.0 (Linux; Android 14)"}
    if tok:
        h["Authorization"] = "Bearer " + tok
    req = urllib.request.Request(BASE + path,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers=h)
    body = urllib.request.urlopen(req, timeout=30).read()
    return json.loads(body) if body and body.strip() else None


def main():
    if not USER or not PASS:
        print("missing secrets")
        return 1
    tok = call("/auth/login", {"username": USER, "password": PASS})["token"]
    st = call(f"/experience/check-in-status?courseId={CID}", tok=tok) or {}
    if st.get("hasCheckedIn"):
        print("already checked in, days:", st.get("consecutiveDays"))
        return 0
    r = call(f"/experience/daily-check-in?courseId={CID}", {}, tok=tok) or {}
    if r.get("success"):
        print("checked in, points:", r.get("pointsGained"), "days:", r.get("consecutiveDays"))
        return 0
    print("failed:", r.get("message"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
