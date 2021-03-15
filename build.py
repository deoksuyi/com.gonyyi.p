#!/usr/bin/python3

conf = {}
index_template = "index-template.html"
doc_directory = "docs"


# {
#     "lastUpdate": "3/15/2021 12:12:12pm",
#     "portfolios": [
#         "random": [
#             {
#                 "date": "3/15/2021",
#                 "name": "DSYiM Maker",
#                 "desc": "DSYiM custom maker",
#                 "used": [
#                     "javascript", "css", "html"
#                 ]
#                 "url": ""
#             }
#         ],
#         "library": [
#             {
#                 "date": "3/15/2021",
#                 "name": "Alog",
#                 "desc": "Logger for Golang",
#                 "used": [
#                     "golang"
#                 ]
#                 "url": ""
#             }
#         ],
#         "media": [
#         ]
#     ]
# }

def getConf(filename):
    import json
    global conf
    conf = json.loads(open(filename, "r").read())
    fo = open(filename, "w")
    fo.write(json.dumps(conf, indent=3, sort_keys=True))
    fo.close()


def clean(dst, excludes):
    import os
    files = os.listdir(dst)
    for fname in files:
        if fname.endswith(".html") and fname not in excludes:
            print("Delete: " + dst + "/" + fname)
            os.remove(dst + "/" + fname)


def create(link, name, to, time):
    if link == "" or name == "" or to == "" or time == "":
        print("Not created: "+name)
        return
    templ = open(index_template, "r")
    fo = open(doc_directory + "/" + link + ".html", "w")
    
    s = templ.read()
    s = s.replace("{{LINK:NAME}}", str(name))
    s = s.replace("{{LINK:TO}}", str(to))
    s = s.replace("{{LINK:TO_SHORT}}", str(shorter_url(to)))
    s = s.replace("{{LINK:TIME}}", str(time))
    
    fo.write(s)
    fo.close()

    print("Created: "+name)

def update_version(msg):
    from datetime import datetime

    fo = open(doc_directory + "/VERSION", "w")
    ver = conf.get("version", "")
    time = datetime.now()

    fo.write("--- gonyyi.a ---\n")
    fo.write("Version: " + ver+"\n")
    fo.write("Updated: " + str(time)+"\n")
    if msg != "":
        fo.write("\n--- Change(s) --- \n" +msg+ "\n")

    fo.close()


def main():
    import sys

    getConf("conf.json")

    clean(conf.get("directory", ""),
          conf.get("link", {}).get("excludes", []))

    if len(sys.argv) > 1:
        update_version(" ".join(sys.argv[1:]))
        # ${{ github.event.head_commit.message }}
    else:
        update_version("")

    for link in conf.get("link", {}).get("links", []):
        create(link.get("link", ""), link.get("name", ""), link.get("to", ""), link.get("sec", ""))


if __name__ == "__main__":
    main()
