from conan.packager import ConanMultiPackager
import os, re, platform


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
    command = "sudo apt-get install gfortran" if os.getenv("CONAN_GCC_VERSIONS") else None

    builder = ConanMultiPackager(
        username=username,
        channel=channel,
        login_username=login_username,
        reference=reference,
        upload=upload_remote,
        remotes=upload_remote,
        docker_entry_script=command)

    builder.add_common_builds(shared_option_name="lapack:shared", pure_c=True)
    builder.run()
