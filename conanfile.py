import os
from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class LapackConan(ConanFile):
    name = "lapack"
    version = "3.7.1"
    description = """LAPACK is a library of Fortran subroutines for solving the most commonly
occurring problems in numerical linear algebra"""
    url = "https://github.com/conan-community/conan-lapack"
    homepage = "https://github.com/Reference-LAPACK/lapack"
    settings = "os", "arch", "compiler", "build_type"
    options = {"CMAKE_GNUtoMS": [True, False]}
    default_options = "CMAKE_GNUtoMS=False"
    generators = "cmake"

    def package_id(self):
        if self.options.CMAKE_GNUtoMS:
            self.info.settings.compiler = "Visual Studio"
            self.info.settings.compiler.version = "ANY"
            self.info.settings.compiler.runtime = "ANY"
            self.info.settings.compiler.toolset = "ANY"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = ("%s/archive/v%s.zip" % (self.homepage, self.version))
        tools.get(source_url)
        os.rename("%s-%s" % (self.name, self.version), "sources")
        tools.replace_in_file("sources/CMakeLists.txt", "project(LAPACK Fortran C)",
                              """project(LAPACK Fortran C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("mingw_installer/1.0@conan/stable")

    def system_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            installer.install("gfortran")
        if os_info.is_macos:
            installer = SystemPackageTool()
            installer.install("gcc", update=True, force=True)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = True
        cmake.definitions["CMAKE_GNUtoMS"] = self.options.CMAKE_GNUtoMS
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["LAPACKE"] = True
        cmake.definitions["CBLAS"] = True
        cmake.configure(source_folder="sources")
        cmake.build(target="blas")
        cmake.build(target="cblas")
        cmake.build(target="lapack")
        cmake.build(target="lapacke")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src="sources", ignore_case=True,
                  keep_path=False)
        self.copy(pattern="*.h", dst="include", src="sources", keep_path=False)
        self.copy(pattern="*blas*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*lapack*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*blas*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*blas*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*blas*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*blas*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*lapack*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*blas*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*lapack*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if "objects" in self.cpp_info.libs:
            self.cpp_info.libs.remove("objects")
