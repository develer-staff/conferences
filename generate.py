#!/usr/bin/env python3

import os
import glob

base = {
    "emergency-number": "112",
    "conf-chair": "Mena Marotta",
    "conf-staff-list": """
- Mena Marotta (she/her)
- Matteo Bertini (he/him)
- Aurélien Rainone (he/him)
- Federico Guerinoni (he/him)
- Pietro Lorefice (he/him)
""",
    "conf-year": "2026",
    "conf-location": "Bologna, Italy",
}

conf_data = {
    "golab": {
        "conf-name": "GoLab",
        "conf-hostname": "golab.io",
        "conf-lang": "Go",
        "conf-first-year": "2015",
        "conf-dates": "November 1-3",
        "cfp-open-close-date": "27 Feb 2026 12:00 am - 13 Apr 2026 11:59 pm (Italy local time)",
    },
    "rustlab": {
        "conf-name": "RustLab",
        "conf-hostname": "rustlab.it",
        "conf-lang": "Rust",
        "conf-first-year": "2019",
        "conf-dates": "November 1-3",
        "cfp-open-close-date": "27 Feb 2026 12:00 am - 13 Apr 2026 11:59 pm (Italy local time)",
    },
}

for conf in conf_data:
    conf_data[conf]["conf-slug"] = conf + "-" + base["conf-year"]

for this, other in [("golab", "rustlab"), ("rustlab", "golab")]:
    for key in list(conf_data[this]):
        if key.startswith("conf-"):
            conf_data[this]["other-" + key] = conf_data[other][key]


def generate(conf):
    os.makedirs(conf, exist_ok=True)
    for md in glob.glob("*.md"):
        oname = md

        # Look for conference-specific files
        splits = md.split(".")
        if len(splits) not in [2, 3]:
            print(f"does not support filenames with . such as {md}")
            sys.exit(1)

        if len(splits) == 3:
            if splits[0] != conf:
                print(f"skipping {md}")
                continue
            oname = ".".join(splits[1:])

        with open(md) as template:
            data = template.read()
            for key, value in (base | conf_data[conf]).items():
                data = data.replace("{{%s}}" % key, value)
        opath = os.path.join(conf, oname)
        with open(opath, "w+") as target:
            target.write(data)
            print(f"written {opath}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2 or sys.argv[1] not in ["golab", "rustlab"]:
        print("usage: generate.py golab|rustlab")
        sys.exit(1)
    generate(sys.argv[1])
