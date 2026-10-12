"""Copy the deck images from Drive into img/ and write manifest.json.

Everything the decks use is public (Oleksii, 2026-10-12): logos, badges, icons, illustrations (the deck
set and the SVG library), office photos, leadership portraits and case mockups. Still never: Diger (out
of scope) and NDA or anonymised cases (their screens can show the client's name).

    python3 scripts/publish.py <path to digicode-decks plugin>

Existing files are overwritten in place; nothing is deleted.
"""
import hashlib, json, os, shutil, sys

PLUGIN = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = "/Users/oleksiihaievyi/Library/CloudStorage/GoogleDrive-haievyio@mydigicode.com/My Drive/DC - Design/DigiCode - Branding/"
CASES = os.path.join(BRAND, "Claude/Presentation/cases")
NEVER = ("product-diger",)
items = []


def case_ok(slug):
    p = os.path.join(CASES, slug, "case.json")
    u = (json.load(open(p)).get("usage") or {}) if os.path.exists(p) else {}
    return u.get("status") == "approved" and u.get("client_named", True)


def copy(src, rel, item):
    dst = os.path.join(ROOT, "img", rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    item.update(file="img/" + rel, sha256=hashlib.sha256(open(src, "rb").read()).hexdigest())
    items.append(item)


for e in json.load(open(os.path.join(PLUGIN, "assets/index.json")))["assets"]:
    if e["key"].startswith(NEVER) or (e["kind"] == "case-image" and not case_ok(e.get("case", ""))):
        continue
    rel = ("case-" if e["kind"] == "case-image" else "") + e["key"].replace("/", "-")
    copy(os.path.join(BRAND, e["drive"]["path"]), rel,
         {"key": e["key"], "kind": e["kind"], "slot": e.get("slot"), "alt": e.get("alt") or "",
          "good_for": e.get("good_for", ""), "theme": e.get("theme"), "drive_id": e["drive"]["id"]})

for e in json.load(open(os.path.join(PLUGIN, "assets/library.json")))["assets"]:
    copy(os.path.join(BRAND, e["drive"]["path"]), e["key"],
         {"key": e["key"], "kind": "library", "slot": "illustration", "alt": e.get("alt") or "",
          "good_for": e.get("good_for", "") or ", ".join(e.get("tags") or []), "theme": e.get("theme"),
          "drive_id": e["drive"]["id"]})

for slug in sorted(os.listdir(CASES)):
    mj = os.path.join(CASES, slug, "mockups", "mockups.json")
    if slug.startswith("_") or not os.path.exists(mj) or not case_ok(slug):
        continue
    title = json.load(open(os.path.join(CASES, slug, "case.json"))).get("title") or slug
    for m in json.load(open(mj)).get("items", []):
        src = os.path.join(CASES, slug, "mockups", m["file"])
        if not os.path.exists(src):
            continue
        bg = m.get("background") or ""
        copy(src, f"cases/{slug}/{m['file']}",
             {"key": f"{slug}/{m['file']}", "kind": "case-mockup", "slot": "case", "case": slug,
              "alt": f"{title}: {m.get('format', '')} mockup".strip(),
              "good_for": {"light": "light slides", "navy": "navy (dark) slides", "dark": "navy (dark) slides"}.get(bg, ""),
              "theme": bg or None, "drive_id": m.get("drive_id")})

json.dump({"images": items}, open(os.path.join(ROOT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
print(len(items), "images")
