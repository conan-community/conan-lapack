import platform
import re
from conan.packager import ConanMultiPackager


def get_value_from_recipe(search_string):
    with open("conanfile.py", "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result

def get_name_from_recipe():
    return get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''').groups()[0]

def get_version_from_recipe():
    return get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''').groups()[0]

if __name__ == "__main__":
    name = get_name_from_recipe()
    username = "conan"
    channel = "stable"
    version = get_version_from_recipe()
    login_username = "conanbot"
    reference = "{0}/{1}".format(name, version)
    upload_remote = "https://api.bintray.com/conan/conan-community/{0}".format(username)

    builder = ConanMultiPackager(
        stable_branch_pattern="stable/*",
        upload_only_when_stable=True,
        username=username,
        channel=channel,
        login_username=login_username,
        reference=reference,
        upload=upload_remote,
        remotes=upload_remote)

    builder.add_common_builds(pure_c=True)
    if platform.system() == "Windows":
        settings = {"arch": "x86",
                    "build_type": "Debug",
                    "compiler": "gcc",
                    "compiler.version": "4.9",
                    "compiler.threads": "posix",
                    "compiler.exception": "seh"}
        builder.add(settings=settings, options={"lapack:visual_studio": True}, env_vars={},
                    build_requires={})
        settings["arch"] = "x86_64"
        builder.add(settings=settings, options={"lapack:visual_studio": True}, env_vars={},
                    build_requires={})
        settings["arch"] = "x86"
        settings["build_type"] = "Release"
        builder.add(settings=settings, options={"lapack:visual_studio": True}, env_vars={},
                    build_requires={})
        settings["arch"] = "x86_64"
        builder.add(settings=settings, options={"lapack:visual_studio": True}, env_vars={},
                    build_requires={})
    builder.run()
