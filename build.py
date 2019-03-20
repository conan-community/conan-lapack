#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    if os.getenv("BUILD_VISUAL_STUDIO"):
        options = {"visual_studio": True, "shared": True}
        settings = {"compiler": "gcc", "compiler.version": "7", "os": "Windows", "arch": "x86_64"}
        for build_type in ["Release", "Debug"]:
            settings.update({"build_type": build_type})
            builder.add(settings, options, {}, {})
    else:
        builder.add_common_builds()
    builder.run()