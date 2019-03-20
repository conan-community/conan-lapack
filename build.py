#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import copy
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    if os.getenv("BUILD_VISUAL_STUDIO"):
        options = {"lapack:visual_studio": True, "lapack:shared": True}
        settings = {"compiler": "gcc", "compiler.version": "7", "os": "Windows", "arch": "x86_64"}
        for build_type in ["Release", "Debug"]:
            settings.update({"build_type": build_type})
            builder.add(copy.copy(settings), options, {}, {})
    else:
        builder.add_common_builds()
    builder.run()