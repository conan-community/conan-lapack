#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from glob import glob
import os


class lapackConan(ConanFile):
    name = "lapack"
    version = "3.7.1"
    url = "https://github.com/Reference-LAPACK"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        source_url = ("%s/%s/archive/v%s.zip" % (self.url, self.name, self.version))
        tools.get(source_url)
        os.rename("%s-%s" % (self.name, self.version), "sources")
        tools.replace_in_file("sources/CMakeLists.txt", "project(LAPACK Fortran C)", """project(LAPACK Fortran C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["LAPACKE"] = True
        cmake.definitions["CBLAS"] = True
        cmake.configure(source_folder="sources")
        cmake.build(target="blas")
        cmake.build(target="cblas")
        cmake.build(target="lapack")
        cmake.build(target="lapacke")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src="sources", ignore_case=True, keep_path=False)
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
        self.cpp_info.libs = ["lapacke", "lapack", "cblas", "blas"]

    def package_id(self):
        self.info.settings.compiler = "ANY"
