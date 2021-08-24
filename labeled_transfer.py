import os, sys, shutil
from codecs import open

def get_all_labeled_files(path="label_logs/"):
    log_files = [path+p for p in os.listdir(path)]
    labeled_paths = []
    for fp in log_files:
        log_str = open(fp, "r", "utf-8").read().strip().split("\n")
        for l in log_str:
            lpath = l.strip().split("|")[1]
            labeled_paths.append(lpath)
    return labeled_paths

def transfer(path="no_touch/"):
    paths = get_all_labeled_files()
    for i, p in enumerate(paths):
        sp = path+p
        if os.path.exists(p):
            shutil.move(p, sp)
            print(i, "move to", sp)


if __name__=="__main__":
    transfer()

