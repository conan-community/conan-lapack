import os
from conans import ConanFile, CMake, tools
from conans.tools import SystemPackageTool

# python 2 / 3 StringIO import
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class LapackConan(ConanFile):
    name = "lapack"
    version = "3.7.1"
    license = "BSD 3-Clause"
    homepage = "https://github.com/Reference-LAPACK/lapack"
    description = """LAPACK is a library of Fortran subroutines for solving the most commonly
occurring problems in numerical linear algebra"""
    url = "https://github.com/conan-community/conan-lapack"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "visual_studio": [True, False]}
    default_options = {"shared": False, "visual_studio": False, "fPIC": True}
    generators = "cmake"

    @property
    def source_subfolder(self):
        return "sources"

    def package_id(self):
        if self.options.visual_studio:
            self.info.settings.compiler = "Visual Studio"
            self.info.settings.compiler.version = "ANY"
            self.info.settings.compiler.runtime = "ANY"
            self.info.settings.compiler.toolset = "ANY"

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio" and not self.options.visual_studio:
            raise Exception("This library needs option 'visual_studio=True' to be consumed")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = ("%s/archive/v%s.zip" % (self.homepage, self.version))
        tools.get(source_url)
        os.rename("%s-%s" % (self.name, self.version), self.source_subfolder)
        tools.replace_in_file("sources/CMakeLists.txt", "project(LAPACK Fortran C)",
                              """project(LAPACK Fortran C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("mingw_installer/1.0@conan/stable")

    def system_requirements(self):
        installer = SystemPackageTool()
        if tools.os_info.is_linux:
            if (tools.os_info.linux_distro == "arch" or 
                    tools.os_info.linux_distro == "redhat" or 
                    tools.os_info.linux_distro == "fedora" or 
                    tools.os_info.linux_distro == "centos"):
                installer.install("gcc-fortran")
            else:
                installer.install("gfortran")
                versionfloat = float(str(self.settings.compiler.version))
                if self.settings.compiler == "gcc":
                    if versionfloat < 5.0:
                        installer.install("libgfortran-{}-dev".format(versionfloat))
                    else:
                        installer.install("libgfortran-{}-dev".format(int(versionfloat)))
        if tools.os_info.is_macos:
            try:
                installer.install("gcc", update=True, force=True)
            except Exception:
                self.output.warn("brew install gcc failed. Tying to fix it with 'brew link'")
                self.run("brew link --overwrite gcc")

    def build(self):
        if self.settings.compiler == "Visual Studio":
            raise Exception("This library cannot be built with Visual Studio. Please use MinGW to "
                            "build it and option 'visual_studio=True' to build and consume.")
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["CMAKE_GNUtoMS"] = self.options.visual_studio
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["LAPACKE"] = True
        cmake.definitions["CBLAS"] = True

        cmake.configure(source_folder=self.source_subfolder)
        cmake.build(target="blas")
        cmake.build(target="cblas")
        cmake.build(target="lapack")
        cmake.build(target="lapacke")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder, ignore_case=True,
                  keep_path=False)
        self.copy(pattern="*.h", dst="include", src="include", keep_path=False)
        self.copy(pattern="*blas*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*lapack*.dll", dst="bin", src="bin", keep_path=False)
        if self.options.visual_studio:
            self.copy(pattern="*blas*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*lapack*.lib", dst="lib", src="lib", keep_path=False)
        else:
            self.copy(pattern="*blas*.dll.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*lapack*.dll.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*blas*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*blas*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*blas.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.a", dst="lib", src="lib", keep_path=False)
        for bin_path in self.deps_cpp_info.bin_paths: # Copy MinGW dlls for Visual Studio consumers
            self.copy(pattern="*seh*.dll", dst="bin", src=bin_path, keep_path=False)
            self.copy(pattern="*sjlj*.dll", dst="bin", src=bin_path, keep_path=False)
            self.copy(pattern="*dwarf2*.dll", dst="bin", src=bin_path, keep_path=False)
            self.copy(pattern="*quadmath*.dll", dst="bin", src=bin_path, keep_path=False)
            self.copy(pattern="*winpthread*.dll", dst="bin", src=bin_path, keep_path=False)
            self.copy(pattern="*gfortran*.dll", dst="bin", src=bin_path, keep_path=False)


    def package_info(self):
        # the order is important for static builds
        self.cpp_info.libs = ["lapacke", "lapack", "blas", "cblas", "gfortran"]
        self.cpp_info.libdirs = ["lib"]
        if tools.os_info.is_macos:
            brewout = StringIO()
            try:
                self.run("gfortran --print-file-name libgfortran.dylib", output=brewout)
            except Exception as e:
                raise Exception("Failed to run command: {}. Output: {}".format(e, brewout.getvalue()))
            lib = os.path.dirname(os.path.normpath(brewout.getvalue().strip()))
            self.cpp_info.libdirs.append(lib)
