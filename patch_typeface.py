#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
# OplusCamera TypeFaceUtil reads OplusBaseConfiguration.mOplusExtraConfiguration
# through OplusTypeCastingHelper and hits an uncaught NPE on non OxygenOS
# frameworks (portrait mode closes the activity). Make the method that does it
# return Typeface.DEFAULT. The class name is obfuscated and changes between
# builds, so look it up by its source file and by what the method does.

import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

TOP = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
SMALI_DIR = os.path.join(TOP, 'prebuilts/extract-tools/common/smali')
BAKSMALI = os.path.join(SMALI_DIR, 'baksmali.jar')
SMALI = os.path.join(SMALI_DIR, 'smali.jar')

SIG = '(Landroid/content/Context;)Landroid/graphics/Typeface;'
BODY = """    .registers 1

    sget-object p0, Landroid/graphics/Typeface;->DEFAULT:Landroid/graphics/Typeface;

    return-object p0
"""


def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('failed: %s\n%s%s' % (' '.join(cmd), r.stdout, r.stderr))


def patch_smali(path):
    text = open(path).read()
    if '.source "TypeFaceUtil.java"' not in text:
        return False
    out, done = [], False
    for m in re.finditer(r'(\.method public static (\w+)' + re.escape(SIG) + r'\n)(.*?)(\.end method)', text, re.S):
        body = m.group(3)
        if 'mOplusExtraConfiguration' in body:
            text = text[:m.start(3)] + BODY + text[m.end(3):]
            done = True
            break
    if done:
        open(path, 'w').write(text)
    return done


def main(apk):
    work = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(apk) as z:
            dexes = sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex', n))
            z.extractall(work, dexes)
        for dex in dexes:
            out = os.path.join(work, dex + '.d')
            run('java', '-jar', BAKSMALI, 'disassemble', '-o', out, os.path.join(work, dex))
            hit = None
            for root, _, files in os.walk(out):
                for f in files:
                    if f.endswith('.smali') and patch_smali(os.path.join(root, f)):
                        hit = f
            if hit:
                newdex = os.path.join(work, 'new.dex')
                run('java', '-jar', SMALI, 'assemble', '--api', '34', '-o', newdex, out)
                tmp = apk + '.tmp'
                with zipfile.ZipFile(apk) as zin, zipfile.ZipFile(tmp, 'w') as zout:
                    for item in zin.infolist():
                        data = open(newdex, 'rb').read() if item.filename == dex else zin.read(item.filename)
                        zout.writestr(item, data)
                os.replace(tmp, apk)
                print('patched TypeFaceUtil in %s (%s)' % (dex, hit))
                return
        sys.exit('TypeFaceUtil method not found')
    finally:
        shutil.rmtree(work)


if __name__ == '__main__':
    main(sys.argv[1])
