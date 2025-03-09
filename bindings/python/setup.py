# Python binding for Keystone engine. Nguyen Anh Quynh <aquynh@gmail.com>

import glob
import logging
import os
import shutil
import sys
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

log = logging.getLogger(__name__)

# are we building from the repository or from a source distribution?
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
LIBS_DIR = os.path.join(ROOT_DIR, 'keystone', 'lib')
SRC_DIR = os.path.join(ROOT_DIR, 'src')
BUILD_DIR = os.path.join(SRC_DIR, 'build')
# prebuilt libraries for Windows - for sdist
PATH_LIB64 = os.path.join(ROOT_DIR, 'prebuilt', 'win64')
PATH_LIB32 = os.path.join(ROOT_DIR, 'prebuilt', 'win32')

if sys.platform == 'darwin':
    LIBRARY_FILE = "libkeystone.dylib"
    MAC_LIBRARY_FILE = "libkeystone*.dylib"
elif sys.platform == 'win32':
    LIBRARY_FILE = "keystone.dll"
elif sys.platform == 'cygwin':
    LIBRARY_FILE = "cygkeystone-0.dll"
else:
    LIBRARY_FILE = "libkeystone.so"


def clean_bins():
    shutil.rmtree(LIBS_DIR, ignore_errors=True)


def copy_sources():
    """
    Copy the C sources into the source directory.
    This rearranges the source files under the python distribution
    directory.
    """
    shutil.rmtree(SRC_DIR, ignore_errors=True)
    os.mkdir(SRC_DIR)

    shutil.copytree(os.path.join(ROOT_DIR, '../../llvm'), os.path.join(SRC_DIR, 'llvm/'))
    shutil.copytree(os.path.join(ROOT_DIR, '../../include'), os.path.join(SRC_DIR, 'include/'))
    shutil.copytree(os.path.join(ROOT_DIR, '../../suite'), os.path.join(SRC_DIR, 'suite/'))

    src = []
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.h")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.cpp")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.inc")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.def")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../CMakeLists.txt")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../CMakeUninstall.in")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.txt")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.TXT")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../COPYING")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../LICENSE*")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../EXCEPTIONS-CLIENT")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../README.md")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../RELEASE_NOTES")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../ChangeLog")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../SPONSORS.TXT")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.cmake")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.sh")))
    src.extend(glob.glob(os.path.join(ROOT_DIR, "../../*.bat")))

    for filename in src:
        outpath = os.path.join(SRC_DIR, os.path.basename(filename))
        log.info("%s -> %s" % (filename, outpath))
        shutil.copy(filename, outpath)


def build_libraries():
    """
    Prepare the Keystone engine directory for a binary distribution or installation.
    Builds shared libraries and copies header files.
    """
    cwd = os.getcwd()
    clean_bins()
    os.mkdir(LIBS_DIR)

    # if Windows prebuilt library is available, then include it
    if sys.platform in ("win32", "cygwin"):
        if os.path.exists(os.path.join(PATH_LIB64, LIBRARY_FILE)):
            shutil.copy(os.path.join(PATH_LIB64, LIBRARY_FILE), LIBS_DIR)
            return
        elif os.path.exists(os.path.join(PATH_LIB32, LIBRARY_FILE)):
            shutil.copy(os.path.join(PATH_LIB32, LIBRARY_FILE), LIBS_DIR)
            return

    # otherwise, build
    if not os.path.isdir(SRC_DIR):
        copy_sources()
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)

    os.chdir(BUILD_DIR)
    conf = 'Debug' if int(os.getenv('DEBUG', 0)) else 'Release'
    cmake_args = ['cmake',
                  '-DBUILD_SHARED_LIBS=ON',
                  '-DKEYSTONE_BUILD_STATIC_RUNTIME=OFF',
                  '-DLLVM_BUILD_TESTS=OFF',
                  '-DBUILD_LIBS_ONLY=1',
                  '-DLLVM_TARGETS_TO_BUILD=all',
                  f"-DCMAKE_BUILD_TYPE={conf}"
                  ]
    cmake_build = ['cmake',
                   '--build',
                   '.'
                   ]

    if sys.platform == 'win32':
        cmake_args += ['-G "NMake Makefiles"']
        os.system(' '.join(cmake_args + ['..']))
        os.system(' '.join(cmake_build))
        winobj_dir = os.path.join(BUILD_DIR, 'llvm', 'bin')
        shutil.copy(os.path.join(winobj_dir, LIBRARY_FILE), LIBS_DIR)
    else:
        cmake_args += ['-G "Unix Makefiles"']
        cmake_build += ['-j', str(os.getenv("THREADS", "4"))]
        os.system(' '.join(cmake_args + ['..']))
        os.system(' '.join(cmake_build))
        obj_dir = os.path.join(BUILD_DIR, 'llvm', 'bin' if sys.platform == 'cygwin' else 'lib')
        obj64_dir = os.path.join(BUILD_DIR, 'llvm', 'lib64')
        if sys.platform == 'darwin':
            for file in glob.glob(os.path.join(obj_dir, MAC_LIBRARY_FILE)):
                try:
                    shutil.copy(file, LIBS_DIR, follow_symlinks=False)
                except:
                    shutil.copy(file, LIBS_DIR)
        else:
            try:
                shutil.copy(os.path.join(obj_dir, LIBRARY_FILE), LIBS_DIR)
            except:
                shutil.copy(os.path.join(obj64_dir, LIBRARY_FILE), LIBS_DIR)
    os.chdir(cwd)


class CustomSDist(sdist):
    def run(self):
        clean_bins()
        copy_sources()
        return super().run()


class CustomBuild(build_py):
    def run(self):
        log.info("Building C extensions")
        build_libraries()
        return super().run()


setup(
    cmdclass={'build_py': CustomBuild, 'sdist': CustomSDist},
    has_ext_modules=lambda: True,  # It's not a Pure Python wheel
)
