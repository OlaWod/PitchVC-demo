#!/usr/bin/env python3

from jinja2 import FileSystemLoader, Environment

import os
from glob import glob

def gen_rows(gtype):
    ret = []

    pitchvc_paths = sorted(glob(f'data/{gtype}/pitchvc/*.wav'))

    for i, pitchvc in enumerate(pitchvc_paths):
        sovits = pitchvc.replace('pitchvc', 'sovits')
        knnvc = pitchvc.replace('pitchvc', 'knnvc')

        basename = os.path.basename(pitchvc).split('.')[0]
        tgt_basename, src_basename, tgt_basename = basename.split('-')
        srcpath = f'data/src/{gtype}/{src_basename}.wav'
        tgtpath = f'data/tgt/{tgt_basename}.wav'

        ret.append(
            (
                src_basename, tgt_basename, 
                srcpath, tgtpath, 
                pitchvc, sovits, knnvc
            )
        )

    return ret


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("base.html.jinja2")

    libri_rows = gen_rows("u2s")
    esd_en_rows = gen_rows("esd_en")
    esd_zh_rows = gen_rows("esd_zh")

    html = template.render(
        libri_rows=libri_rows,
        esd_en_rows=esd_en_rows,
        esd_zh_rows=esd_zh_rows
    )
    
    with open("index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()
