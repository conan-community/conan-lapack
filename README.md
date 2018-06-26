# conan-lapack

![conan-lapack image](/images/conan-lapack.png)

[![Download](https://api.bintray.com/packages/conan-community/conan/lapack%3Aconan/images/download.svg)](https://bintray.com/conan-community/conan/lapack%3Aconan/_latestVersion)
[![Build Status](https://travis-ci.org/conan-community/conan-lapack.svg?branch=stable%2F3.7.1)](https://travis-ci.org/conan-community/conan-lapack)
[![Build status](https://ci.appveyor.com/api/projects/status/jyeh443gn0l0f3bi/branch/stable/3.7.1?svg=true)](https://ci.appveyor.com/project/danimtb/conan-lapack/branch/stable/3.7.1)

[Conan.io](https://conan.io) package for [lapack](https://bitbucket.org/lapack/lapack) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/conan-community/conan/lapack%3Aconan).

## For Users: Use this package

### Basic setup

    $ conan install lapack/3.7.1@conan/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    lapack/3.7.1@conan/stable

    [generators]
    txt
    cmake

## License

[MIT License](LICENSE)
