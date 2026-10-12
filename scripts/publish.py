"""Copy the approved public deck images from Drive into img/ and write manifest.json.

Only images that are already public (logos, certification and partner badges, illustrations, mockups of
approved named cases). Never portraits, photos of employees, NDA or anonymised cases, or Diger.

    python3 scripts/publish.py <path to digicode-decks plugin>
"""
import hashlib, json, os, shutil, sys

PLUGIN = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = "/Users/oleksiihaievyi/Library/CloudStorage/GoogleDrive-haievyio@mydigicode.com/My Drive/DC - Design/DigiCode - Branding/"
PUBLIC_KINDS = {"logo", "badge", "illustration"}
NEVER = ("product-diger", "client-")  # Diger is out of scope; client logos need the client's OK

def case_ok(slug):
    p = os.path.join(BRAND, "Claude/Presentation/cases", slug, "case.json")
    u = (json.load(open(p)).get("usage") or {}) if os.path.exists(p) else {}
    return u.get("status") == "approved" and u.get("client_named", True)

items = []
for e in json.load(open(os.path.join(PLUGIN, "assets/index.json")))["assets"]:
    k = e["kind"]
    if e["key"].startswith(NEVER):
        continue
    if not (k in PUBLIC_KINDS or (k == "case-image" and case_ok(e.get("case", "")))):
        continue
    name = e["key"].replace("/", "-")
    if k == "case-image":
        name = "case-" + name
    src = os.path.join(BRAND, e["drive"]["path"])
    shutil.copyfile(src, os.path.join(ROOT, "img", name))
    items.append({"key": e["key"], "file": "img/" + name, "kind": k, "alt": e.get("alt", ""),
                  "sha256": hashlib.sha256(open(src, "rb").read()).hexdigest(), "drive_id": e["drive"]["id"]})
json.dump({"images": items}, open(os.path.join(ROOT, "manifest.json"), "w"), indent=1)
print(len(items), "images")
