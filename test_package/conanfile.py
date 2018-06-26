#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*lapack*.dll", dst="bin", src="bin")
        self.copy("*blas*.dll", dst="bin", src="bin")
        self.copy("*gfortran*.dll", dst="bin", src="bin")
        self.copy("*gcc_*.dll", dst="bin", src="bin")
        self.copy("*quadmath*.dll*", dst="bin", src="bin")
        self.copy("*winpthread*.dll*", dst="bin", src="bin")
        self.copy("*lapack*.dylib*", dst="bin", src="lib")
        self.copy("*blas*.dylib*", dst="bin", src="lib")
        self.copy("*gfortran*.dylib*", dst="bin", src="bin")
        self.copy("*gcc_*.dylib*", dst="bin", src="bin")
        self.copy("*quadmath*.dylib*", dst="bin", src="bin")
        self.copy("*winpthread*.dylib*", dst="bin", src="bin")

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "test_package")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))
