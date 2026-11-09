#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
import subprocess
import sys

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/oplus',
    'vendor/oneplus/sm8650-common',
    'vendor/oneplus/waffle',
]

def patch_typeface(ctx, file, file_path, *args, **kwargs):
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch_typeface.py')
    subprocess.run([sys.executable, script, file_path], check=True)


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    # Stock libui for the odm camera blobs, renamed so surfaceflinger and the
    # composer keep using the platform one.
    'odm/lib64/oemui.so': blob_fixup()
        .fix_soname()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    # TypeFaceUtil NPE on non OxygenOS frameworks closes portrait mode.
    'system_ext/priv-app/OplusCamera/OplusCamera.apk': blob_fixup()
        .call(patch_typeface),
}  # fmt: skip

module = ExtractUtilsModule(
    'camera',
    'oplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
