#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import hashlib
import importlib
import importlib.util
import io
import logging

# try:
#     import msvcrt  # For Windows systems #type: ignore
# except ImportError:
#     import getch  # For Unix-like systems #type: ignore
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from collections import defaultdict
from pprint import pprint as pp
from typing import Any, List, Optional, Tuple, Union, final
from urllib.parse import urlparse

import progressbar
import requests

from packages.base_package import BasePackage
from pathlibex import Path

from ansimarkup import ansistring


class Colors:
    """ANSI color codes"""

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


class MyLogFormatter(logging.Formatter):
    def __init__(self, l, ld):
        MyLogFormatter.log_format = l
        MyLogFormatter.log_date_format = ld
        # MyLogFormatter.inf_fmt = (
        #     Colors.LIGHTCYAN_EX + MyLogFormatter.log_format + Colors.RESET
        # )
        # MyLogFormatter.err_fmt = (
        #     Colors.LIGHTRED_EX + MyLogFormatter.log_format + Colors.RESET
        # )
        # MyLogFormatter.dbg_fmt = (
        #     Colors.LIGHTYELLOW_EX + MyLogFormatter.log_format + Colors.RESET
        # )
        # MyLogFormatter.war_fmt = (
        #     Colors.YELLOW + MyLogFormatter.log_format + Colors.RESET
        # )*
        super().__init__(
            fmt="%(levelno)d: %(msg)s",
            datefmt=MyLogFormatter.log_date_format,
            style="%",
        )

    def format(self, record):
        if not hasattr(record, "type"):
            record.type = ""
        else:
            record.type = "[" + record.type.upper() + "]"  # type: ignore
            # record.type = ansistring(record.type)

        if record.levelno == logging.DEBUG:
            record.msg = f"<grey>{record.msg}</grey>"
        elif record.levelno == logging.INFO:
            record.msg = f"<cyan>{record.msg}</cyan>"
        elif record.levelno == logging.ERROR:
            record.msg = f"<light-red>{record.msg}</light-red>"
        elif record.levelno == logging.WARNING:
            record.msg = f"<light-yellow>{record.msg}</light-yellow>"

        # record.msg = ansistring(record.msg)

        self._style._fmt = MyLogFormatter.log_format
        # # format_orig = self._style._fmt
        result = logging.Formatter.format(self, record)

        result = ansistring(result)
        # self._style._fmt = format_orig
        return result


# class MyLogFormatter(logging.Formatter):
#     def __init__(self, l, ld):
#         MyLogFormatter.log_format = l
#         MyLogFormatter.log_date_format = ld
#         # MyLogFormatter.inf_fmt = (
#         #     Colors.LIGHTCYAN_EX + MyLogFormatter.log_format + Colors.RESET
#         # )
#         # MyLogFormatter.err_fmt = (
#         #     Colors.LIGHTRED_EX + MyLogFormatter.log_format + Colors.RESET
#         # )
#         # MyLogFormatter.dbg_fmt = (
#         #     Colors.LIGHTYELLOW_EX + MyLogFormatter.log_format + Colors.RESET
#         # )
#         # MyLogFormatter.war_fmt = (
#         #     Colors.YELLOW + MyLogFormatter.log_format + Colors.RESET
#         # )
#         super().__init__(
#             fmt="%(levelno)d: %(msg)s",
#             datefmt=MyLogFormatter.log_date_format,
#             style="%",
#         )

#     def format(self, record):
#         if not hasattr(record, "type"):
#             record.type = ""
#         else:
#             record.type = "[" + record.type.upper() + "]"  # type: ignore

#         format_orig = self._style._fmt
#         # if record.levelno == logging.DEBUG:
#         #     self._style._fmt = MyLogFormatter.dbg_fmt
#         # elif record.levelno == logging.INFO:
#         #     self._style._fmt = MyLogFormatter.inf_fmt
#         # elif record.levelno == logging.ERROR:
#         #     self._style._fmt = MyLogFormatter.err_fmt
#         # elif record.levelno == logging.WARNING:
#         #     self._style._fmt = MyLogFormatter.war_fmt
#         result = logging.Formatter.format(self, record)
#         self._style._fmt = format_orig
#         return result


class WarnDefaultDict(defaultdict):
    def __init__(self, default, logger):
        super().__init__(default)
        self.logger = logger

    def __missing__(self, key):
        self.logger.warning(f"Unknown variable {key}, ignoring")
        return f"{{{key}}}"


class TimeFilter(logging.Filter):
    def filter(self, record):
        record.created = datetime.datetime.now().timestamp()
        return True


class CrossCompiler:
    def __init__(self):
        hdlr = logging.StreamHandler(sys.stdout)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(hdlr)
        self.logger.addFilter(TimeFilter())
        self.logger.setLevel(logging.INFO)
        fmt = MyLogFormatter(
            "<light-cyan>[%(asctime)s][%(levelname)s]</light-cyan>%(type)s %(message)s",
            "%H:%M:%S",
        )
        hdlr.setFormatter(fmt)

        self.packages: dict[str, BasePackage] = {}

        self.packagesBuilt: dict[str, bool] = {}

        self.originalEnv = dict(os.environ)

        self.projectRoot = Path(os.getcwd())
        self.fullPatchDir = self.projectRoot.joinpath("patches")

        self.workPath = Path(os.getcwd()).joinpath("work")
        self.installDir = Path(os.getcwd()).joinpath("install")

        self.xArchPrefixStr = f"x86_64"
        self.mingwPrefixStr = f"{self.xArchPrefixStr}-w64-mingw32"
        self.mingwPrefixStrDash = f"{self.xArchPrefixStr}-w64-mingw32-"
        self.toolchainRootPath = self.workPath.joinpath("toolchain")
        self.toolchainPathOne = self.toolchainRootPath.joinpath(
            self.mingwPrefixStr
        )
        self.toolchainBinPathOne = self.toolchainPathOne.joinpath("bin")
        self.toolchainPathTwo = self.toolchainPathOne.joinpath(
            self.mingwPrefixStr
        )
        self.pkgConfigPath = self.toolchainPathTwo.joinpath("lib/pkgconfig")
        self.toolchainBinPathTwo = self.toolchainPathTwo.joinpath("bin")
        self.crossPrefix = self.toolchainPathTwo
        self.packagesRoot = self.workPath.joinpath("sources")
        self.rustTargetStr = "x86_64-pc-windows-gnu"

        self.runProcessDebug = False

        self.originalPATH = os.environ["PATH"]

        self.localPkgConfigPath = self.aquireLocalPkgConfigPath()

        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"

        self.bitnessStr = "x86_64"
        self.bitnessStrWin = "win64"
        self.bitnessStrNum = "64"

        self.cmakeToolchainFile = self.workPath.joinpath(
            "mingw_toolchain.cmake"
        )
        self.cargoHomePath = self.workPath.joinpath("cargohome")
        self.mesonEnvFile = self.workPath.joinpath("meson_environment.ini")
        self.mesonNativeFile = self.workPath.joinpath("meson_native.ini")

        self.makePrefixOptions = (
            f"CC={self.mingwPrefixStrDash}gcc",
            f"AR={self.mingwPrefixStrDash}ar",
            f"PREFIX={self.crossPrefix}",
            f"RANLIB={self.mingwPrefixStrDash}ranlib",
            f"LD={self.mingwPrefixStrDash}ld",
            f"STRIP={self.mingwPrefixStrDash}strip",
            f"CXX={self.mingwPrefixStrDash}g++",
        )

        # self.formatDict = WarnDefaultDict(lambda: "", self.logger)
        self.formatDict = {
            "bitness": self.bitnessStr,
            "bitness_win": self.bitnessStrWin,
            "bitness_num": self.bitnessStrNum,
            "toolchain_path_one": str(self.toolchainPathOne),
            "arch_string": self.xArchPrefixStr,
            "target_prefix": str(self.crossPrefix),
            "target_prefix_sed_escaped": str(self.crossPrefix).replace(
                "/", "\\/"
            ),
            "toolchain_bin_path_one": str(self.toolchainBinPathOne),
            "mingw_prefix": str(self.mingwPrefixStr),
            "mingw_prefix_dash": str(self.mingwPrefixStrDash),
            "cmake_prefix_options": (
                f"-DCMAKE_TOOLCHAIN_FILE={self.cmakeToolchainFile}",
                "-GNinja",
                "-DCMAKE_BUILD_TYPE=Release",
            ),
            "autoconf_prefix_options": (
                "--host={mingw_prefix}",
                "--prefix={target_prefix}",
                "--disable-shared",
                "--enable-static",
            ),
            "meson_prefix_options": (
                "--prefix={target_prefix}",
                "--cross-file={meson_env_file}",
                "--native-file=" + str(self.mesonNativeFile),
            ),
            "meson_options": (
                "--cross-file={meson_env_file}",
                "--native-file=" + str(self.mesonNativeFile),
            ),
            "meson_env_file": str(self.mesonEnvFile),
            "meson_native_file": str(self.mesonNativeFile),
            "make_prefix_options": self.makePrefixOptions,
            "rust_target": self.rustTargetStr,
            "pkg_config_path": str(self.pkgConfigPath),
            "local_pkg_config_path": self.localPkgConfigPath,
            "local_path": self.originalPATH,
            "install_path": str(self.installDir),
        }

        os.makedirs("work/sources", exist_ok=True)

        self.loadPackages()
        self.sanityCheckPackages()

        self.buildMinGWToolchain()
        self.createCmakeToolchainFile()
        self.createMesonEnvFile()
        self.createCargoHome()
        self.setDefaultEnv()

        self.buildPackages(self.packages[sys.argv[1]])
        exit()

        for pkg_name, pkg in self.packages.items():
            print(pkg_name, end="\n" * 4 + str(pkg.depends) + "\n" * 4)
            self.buildPackages(pkg)

    def aquireLocalPkgConfigPath(self):
        possiblePathsStr = (
            subprocess.check_output(
                "pkg-config --variable pc_path pkg-config",
                shell=True,
                stderr=subprocess.STDOUT,
            )
            .decode("utf-8")
            .strip()
        )

        if possiblePathsStr == "":
            raise Exception(
                "Unable to determine local pkg-config path(s), pkg-config output is empty"
            )

        possiblePaths = [Path(x.strip()) for x in possiblePathsStr.split(":")]

        for p in possiblePaths:
            if not p.exists():
                possiblePaths.remove(p)

        if not len(possiblePaths):
            raise Exception(
                f"Unable to determine local pkg-config path(s), pkg-config output is: {possiblePathsStr}"
            )

        return ":".join(str(x) for x in possiblePaths)

    def buildPackages(self, pkg):
        print(f"Building {pkg.name}")
        if pkg.name in self.packagesBuilt:
            if self.packagesBuilt[pkg.name]:
                print(f"{pkg.name} already built")
                return
            else:
                raise Exception(
                    f"Error building {pkg.name}: circular dependency detected."
                )
        self.packagesBuilt[pkg.name] = False

        if len(pkg.depends) > 0:
            print(f"{pkg.name} depends on {pkg.depends}")
            for pkg_name in pkg.depends:
                if pkg_name not in self.packages:
                    raise Exception(
                        f"{pkg_name} is not an available package, requested by: {pkg.name}"
                    )
                dependency_pkg = self.packages[pkg_name]
                self.buildPackages(dependency_pkg)

        try:
            self.buildPackage(pkg)
            self.packagesBuilt[pkg.name] = True
            print(f"{pkg.name} built successfully")
        except:
            self.packagesBuilt[pkg.name] = False
            raise

    def setDefaultEnv(self):
        os.environ[
            "PATH"
        ] = f"{self.toolchainBinPathOne}:{self.originalEnv['PATH']}"
        os.environ["CARGO_HOME"] = str(self.cargoHomePath)

        os.environ["PKG_CONFIG_LIBDIR"] = ""
        os.environ["PKG_CONFIG_PATH"] = str(self.pkgConfigPath)
        os.environ["COLOR"] = "ON"  # Force coloring on (for CMake primarily)
        os.environ["CLICOLOR_FORCE"] = "ON"  # Force coloring on (for CMake primarily)
        os.environ["CFLAGS"] = "-Ofast -march=znver3 -mtune=znver3"  # Force coloring on (for CMake primarily)
        # os.environ["CMAKE_SYSTEM_IGNORE_PATH"] = "/;/usr;/usr/local"

        # os.environ["MESON_CMAKE_TOOLCHAIN_FILE"] = str(self.cmakeToolchainFile)

        # os.environ["CC"]        = f"{self.mingwPrefixStrDash}gcc"
        # os.environ["AR"]        = f"{self.mingwPrefixStrDash}ar"
        # os.environ["PREFIX"]    = f"{self.crossPrefix}"
        # os.environ["RANLIB"]    = f"{self.mingwPrefixStrDash}ranlib"
        # os.environ["LD"]        = f"{self.mingwPrefixStrDash}ld"
        # os.environ["STRIP"]     = f"{self.mingwPrefixStrDash}strip"
        # os.environ["CXX"]       = f"{self.mingwPrefixStrDash}g++"

        # pp(os.environ)

    def createSymlink(self, sourcePath: Path, targetLinkPath: Path):
        if not sourcePath.exists():
            raise ValueError(f"{sourcePath} does not exist")

        if targetLinkPath.exists():
            return

        if sourcePath.is_file():
            link_type = "file"
        elif sourcePath.is_dir():
            link_type = "dir"
        else:
            raise ValueError(f"{sourcePath} is not a file or directory")

        try:
            os.symlink(
                str(sourcePath),
                str(targetLinkPath),
                target_is_directory=(link_type == "dir"),
            )
        except OSError as e:
            raise OSError(f"Failed to create symlink: {e}")

    def getPackagePathByName(self, name, root=False):
        pkg: BasePackage = self.packages[name]
        pkgPath = pkg.path
        if pkg.get_source_subfolder and not root:
            pkgPath = pkgPath.joinpath(pkg.get_source_subfolder)
        return pkgPath

    def handleRegexReplace(self, rp, packageName):
        cwd = Path(os.getcwd())
        if "in_file" not in rp:
            print(
                f"The regex_replace command in the package {packageName}:\n{rp}\nMisses the in_file parameter."
            )
            exit(1)
        if 0 not in rp:
            print(
                f'A regex_replace command in the package {packageName}\nrequires at least the "0" key to be a RegExpression, if 1 is not defined matching lines will be removed.'
            )
            exit(1)

        in_files = rp["in_file"]
        if isinstance(in_files, (list, tuple)):
            in_files = (
                cwd.joinpath(self.format_variable_str(x)) for x in in_files
            )
        else:
            in_files = (cwd.joinpath(self.format_variable_str(in_files)),)

        repls = [
            self.format_variable_str(rp[0]),
        ]
        if 1 in rp:
            repls.append(self.format_variable_str(rp[1]))

        self.logger.info(
            f"Running regex replace commands on package: '{packageName}' [{os.getcwd()}]"
        )

        for _current_infile in in_files:
            if "out_file" not in rp:
                out_files = (_current_infile,)
                shutil.copy(
                    _current_infile,
                    _current_infile.parent.joinpath(
                        _current_infile.name + ".backup"
                    ),
                )
            else:
                if isinstance(rp["out_file"], (list, tuple)):
                    out_files = (
                        cwd.joinpath(self.format_variable_str(x))
                        for x in rp["out_file"]
                    )
                else:
                    out_files = (
                        cwd.joinpath(self.format_variable_str(rp["out_file"])),
                    )

            for _current_outfile in out_files:
                if not _current_infile.exists():
                    self.logger.warning(
                        f"[Regex-Command] In-File '{_current_infile}' does not exist in '{os.getcwd()}'"
                    )

                if _current_outfile == _current_infile:
                    _backup = _current_infile.parent.joinpath(
                        _current_infile.name + ".backup"
                    )
                    if not _backup.parent.exists():
                        self.logger.warning(
                            f"[Regex-Command] Out-File parent '{_backup.parent}' does not exist."
                        )
                    shutil.copy(_current_infile, _backup)
                    _tmp_file = _current_infile.parent.joinpath(
                        _current_infile.name + ".tmp"
                    )
                    shutil.move(_current_infile, _tmp_file)
                    _current_infile = _tmp_file
                self.logger.info(
                    f"[{packageName}] Running regex command on '{_current_outfile}'"
                )

                with open(_current_infile, "r") as f:
                    # input_file_content = f.read()
                    # print("Input file content:", input_file_content)

                    f.seek(
                        0
                    )  # reset the file pointer to the beginning of the file
                    with open(_current_outfile, "w") as nf:
                        for line in f:
                            if re.search(repls[0], line) and len(repls) > 1:
                                self.logger.info(f"RegEx replacing line")
                                self.logger.info(
                                    f"in {_current_outfile}\n{line}\nwith:"
                                )
                                line = re.sub(repls[0], repls[1], line)
                                self.logger.info(f"\n{line}")
                                nf.write(line)
                            elif re.search(repls[0], line):
                                self.logger.info(
                                    f"RegEx removing line\n{line}:"
                                )
                            else:
                                # print(repls[0])
                                nf.write(line)

    def runProcess(
        self, args, ignore_errors=False, exit_on_error=True, inputFile=None
    ) -> int:
        if not isinstance(args, tuple) and not isinstance(args, list):
            raise ValueError("only tuple/list accepted")

        args = self.format_variable_list(args)

        stdin_arg = subprocess.PIPE if inputFile is not None else None

        if self.runProcessDebug:
            self.logger.info(f"Running process: {' '.join(args)}")
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=stdin_arg,
        )

        if inputFile is not None and process.stdin is not None:
            with open(inputFile, "rb") as f:
                input_data = f.read()
            process.stdin.write(input_data)
            process.stdin.close()

        if process.stderr is None and process.stdout is None:
            raise Exception("meh")

        while process.stdout is not None:
            nextline = process.stdout.readline()
            if nextline == b"" and process.poll() is not None:
                break
            line_str = nextline.decode("utf-8", "ignore")
            print(line_str, end="")

        if process.stdout:
            process.stdout.close()

        return_code = process.wait()

        if return_code != 0:
            if not ignore_errors:
                self.logger.error(
                    f"Error [{return_code}] running process: '{' '.join(str(x) for x in args)}' in '{os.getcwd()}'"
                )
                if exit_on_error:
                    exit(1)

        return return_code

    def svnHasNewCommits(self, pkg: BasePackage):
        # Get local revision using svn info command
        local_info = os.popen("svn info").read().strip()
        local_rev_match = re.search(
            r"^Revision:\s*(\d+)", local_info, re.MULTILINE
        )
        local_rev = local_rev_match.group(1) if local_rev_match else ""

        # Get remote revision using svn info command with package URL
        remote_info = os.popen(f"svn info {pkg.url}").read().strip()
        remote_rev_match = re.search(
            r"^Revision:\s*(\d+)", remote_info, re.MULTILINE
        )
        remote_rev = remote_rev_match.group(1) if remote_rev_match else ""
        return local_rev != remote_rev

    def svnCheckout(self, package: BasePackage):
        checkoutUrl = package.url
        if package.path.exists():
            _olddir = os.getcwd()
            os.chdir(package.path)
            if self.svnHasNewCommits(package):
                self.runProcess(["svn", "update"])
                os.chdir(_olddir)
                return True
            else:
                self.logger.info(f"SVN repo for {package.name} is up to date")
            os.chdir(_olddir)
            return False
        self.logger.info(f"Checking out {package.name} from '{checkoutUrl}'")
        self.runProcess(["svn", "checkout", checkoutUrl, str(package.path)])
        return True

    def gitHasNewCommits(self):
        localCommit = os.popen("git rev-parse HEAD").read().strip()
        remoteCommit = (
            os.popen("git ls-remote -q . HEAD")
            .read()
            .strip()
            .split("\n")[0]
            .split("\t")[0]
        )
        return not localCommit == remoteCommit

    def gitClone(self, package: BasePackage):
        cloneUrl = package.url
        if package.path.exists():
            _olddir = os.getcwd()
            os.chdir(package.path)
            if self.gitHasNewCommits():
                self.runProcess(("git", "pull"))
                os.chdir(_olddir)
                return True
            else:
                self.logger.info(f"Git repo for {package.name} is up to date")
            os.chdir(_olddir)
            return False

        cloneCmd = ["git", "clone", "--progress", "-v"]
        if package.git_depth:
            cloneCmd.append(f"--depth={package.git_depth}")
        if package.git_recursive:
            cloneCmd.append("--recursive")
        if package.git_shallow_submodules:
            cloneCmd.append("--shallow-submodules")
        if package.git_branch:
            cloneCmd.append(f"--branch={package.git_branch}")

        cloneCmd.append(cloneUrl)
        cloneCmd.append(str(package.path))

        self.logger.info(
            f"Cloning {package.name} with '{shlex.join(cloneCmd)}'"
        )
        self.runProcess(cloneCmd)
        return True

    def hgHasNewCommits(self):
        localRevision = (
            os.popen("hg identify --debug").read().strip().split()[0]
        )
        remoteRevision = (
            os.popen("hg identify -r default --debug").read().strip().split()[0]
        )
        return not localRevision == remoteRevision

    def hgClone(self, package: BasePackage):
        cloneUrl = package.url
        if package.path.exists():
            _olddir = os.getcwd()
            os.chdir(package.path)
            if self.hgHasNewCommits():
                self.runProcess(("hg", "pull"))
                os.chdir(_olddir)
                return True
            else:
                self.logger.info(
                    f"Mercurial repo for {package.name} is up to date"
                )
            os.chdir(_olddir)
            return False
        cmd = ["hg", "clone", "-v", cloneUrl, str(package.path)]
        self.logger.info(f"Cloning {package.name} with '{shlex.join(cmd)}'")
        self.runProcess(cmd)
        return True

    def hashFile(self, fname, type="sha256"):
        if type == "sha256":
            hash_obj = hashlib.sha256()
        elif type == "sha512":
            hash_obj = hashlib.sha512()
        elif type == "sha1":
            hash_obj = hashlib.sha1()
        elif type == "md5":
            hash_obj = hashlib.md5()
        elif type == "blake2b":
            hash_obj = hashlib.blake2b()
        else:
            raise ValueError(f"Unsupported hash type: {type}")
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def verifyHash(self, file, hash):
        newHash = self.hashFile(file, hash["type"])
        if hash["sum"] == newHash:
            return (True, hash["sum"], newHash)
        return (False, hash["sum"], newHash)

    def extractFile(self, filename, outputPath):
        def on_progress(filename, position, total_size, pb):
            pass

        def get_file_progress_file_object_class(on_progress, pb):
            class FileProgressFileObject(tarfile.ExFileObject):
                def read(self, size, *args):
                    on_progress(
                        self.name, self.position, self.size, pb
                    )  # type:ignore
                    return tarfile.ExFileObject.read(self, size, *args)

            return FileProgressFileObject

        class ProgressFileObject(io.FileIO):
            def __init__(self, path, pb, *args, **kwargs):
                self.pb = pb
                self._total_size = os.path.getsize(path)
                io.FileIO.__init__(self, path, *args, **kwargs)

            def read(self, size):
                self.pb.update(self.tell())
                return io.FileIO.read(self, size)

        #:
        terms = shutil.get_terminal_size((100, 100))
        # filler = 0
        # if terms[0] > 100:
        # 	filler = int(terms[0]/4)
        widgets = [
            progressbar.FormatCustomText(
                "Extracting : {:25.25}".format(os.path.basename(filename))
            ),
            " ",
            progressbar.Percentage(),
            " ",
            progressbar.Bar(
                fill=chr(9617), marker=chr(9608), left="[", right="]"
            ),
            " ",
            progressbar.DataSize(),
            "/",
            progressbar.DataSize(variable="max_value"),
            # " "*filler,
        ]
        pbar = progressbar.ProgressBar(
            widgets=widgets, maxval=os.path.getsize(filename)
        )
        pbar.start()
        tarfile.TarFile.fileobject = get_file_progress_file_object_class(
            on_progress, pbar
        )
        tar = tarfile.open(
            fileobj=ProgressFileObject(filename, pbar), mode="r:*"
        )
        # outputPath = os.path.commonprefix(tar.getnames())
        if os.path.isfile(outputPath):
            tar.close()
            pbar.finish()
            return outputPath
        else:
            members = tar.getmembers()
            if len(members) == 1 and members[0].name != Path(
                filename
            ).stem.rstrip(".tar"):
                base_path = members[0].name
            else:
                base_path = Path(filename).stem.rstrip(".tar")
            for i in range(len(members)):
                np = Path(members[i].name)
                members[i].name = str(Path(*np.parts[1:]))
                if base_path != Path(filename).stem.rstrip(".tar"):
                    members[i].name = str(Path(base_path) / Path(*np.parts))
            tar.extractall(path=outputPath, members=members)
            tar.close()
            pbar.finish()
            return outputPath

    #:

    def downloadArchive(self, package: BasePackage, path=None):
        if package.path.exists():
            return (True, package.path)
        for mirror in package.mirrors:
            url = mirror["url"]
            self.logger.info(f"Downloading {package.name} from '{url}'")
            try:
                f = self.downloadFile(url, outputPath=path)
                hashes = mirror["hashes"]
                for h in hashes:  # type:ignore
                    self.logger.info("Comparing hashes..")
                    hashReturn = self.verifyHash(f, h)
                    if hashReturn[0] is True:
                        self.logger.info(
                            "Hashes matched: {0}...{1} (local) == {2}...{3} (remote)".format(
                                hashReturn[1][0:5],
                                hashReturn[1][-5:],
                                hashReturn[2][0:5],
                                hashReturn[2][-5:],
                            )
                        )
                        return (False, f)
                    else:
                        self.logger.error(
                            "File hashes didn't match: %s(local) != %s(remote)"
                            % (hashReturn[1], hashReturn[2])
                        )
                        raise Exception("File download error: Hash mismatch")
                        exit(1)
            except Exception as e:
                print(e)
                continue
        return None

    def format_variable_str(self, in_str: str):
        if not isinstance(in_str, str):
            raise ValueError(f"The input is not a string: {in_str}")
        matches = re.findall(r"\{([^{}]+)\}|\!CMD\(([^)]+)\)CMD\!", in_str)
        modified_str = (
            in_str  # create a new variable to store the modified string
        )
        for var, cmd in matches:
            if var:
                if var in self.formatDict:
                    modified_var = self.formatDict[var]
                    if isinstance(modified_var, list) or isinstance(
                        modified_var, tuple
                    ):
                        modified_var = self.format_variable_list(modified_var)
                        if isinstance(modified_var, list) or isinstance(
                            modified_var, tuple
                        ):
                            return modified_var
                    elif not isinstance(modified_var, str):
                        raise ValueError(
                            f"The variable {var} contains a non str or list value: {modified_var}"
                        )

                    modified_str = re.sub(
                        r"\{" + re.escape(var) + r"\}",
                        modified_var,
                        modified_str,
                    )
            elif cmd:
                cmd_output = (
                    subprocess.check_output(cmd, shell=True).decode().strip()
                )
                modified_str = re.sub(
                    r"\!CMD\(" + re.escape(cmd) + r"\)CMD\!",
                    cmd_output,
                    modified_str,
                )
        return modified_str  # return the modified string

    def format_variable_list(
        self, str_obj: Union[List[str], Tuple[str]]
    ) -> Union[List[str], Tuple[str]]:
        if isinstance(str_obj, list):
            formatted_lst = []
            for in_str in str_obj:
                if isinstance(in_str, str):
                    new = self.format_variable_str(in_str)
                    if isinstance(new, list) or isinstance(new, tuple):
                        formatted_lst.extend(new)
                    else:
                        formatted_lst.append(new)
                else:
                    raise TypeError(
                        f"Input must be a list or a tuple of strings, not {type(in_str)} [{in_str}]"
                    )
            return list(formatted_lst)

        elif isinstance(str_obj, tuple):
            formatted_tpl = []
            for in_obj in str_obj:
                if isinstance(in_obj, str):
                    new = self.format_variable_str(in_obj)
                    if isinstance(new, list) or isinstance(new, tuple):
                        formatted_tpl.extend(new)
                    else:
                        formatted_tpl.append(new)

                    # formatted_tpl.append(self.format_variable_str(in_obj))
                else:
                    raise TypeError(
                        f"Input must be a list or a tuple of string, not {type(in_obj)} [{in_obj}]"
                    )
            return tuple(formatted_tpl)

        else:
            raise TypeError(
                f"Input must be a list or a tuple of strings, not {type(str_obj)} [{str_obj}]"
            )

    def formatVariableStr(
        self, strLst: Union[List[str], Tuple[str]]
    ) -> Tuple[str]:
        if not strLst:
            return tuple(strLst)

        formattedStrings = []

        if not isinstance(strLst, tuple) and not isinstance(strLst, list):
            strLst = (strLst,)

        for s in strLst:
            s: str
            matches = re.findall(
                r"(\{([a-zA-Z0-9_\-]+)\})|(\!CMD\(([^\)]+)\)CMD\!)", s
            )
            if matches:
                for match in matches:
                    if match[0]:
                        replaceVar = self.formatDict[match[1]]
                        if isinstance(replaceVar, tuple):
                            group1 = self.formatVariableStr(replaceVar)
                            formattedStrings.extend(group1)
                        else:
                            s = re.sub(r"\{[a-zA-Z0-9_\-]+\}", replaceVar, s)
                            formattedStrings.append(s)
                    elif match[2]:
                        cmd_output = (
                            subprocess.check_output(match[3], shell=True)
                            .decode()
                            .strip()
                        )
                        print()
                        print()
                        print()
                        print(cmd_output)
                        print()
                        print()
                        print()

                        s = re.sub(r"\!CMD\(([^\)]+)\)CMD\!", cmd_output, s)
                        formattedStrings.append(s)
            else:
                formattedStrings.append(s)

        return tuple(formattedStrings)

    def formatVariableStrO2(
        self, strLst: Union[List[str], Tuple[str]]
    ) -> Tuple[str]:
        if not strLst:
            return tuple(strLst)

        formattedStrings = []

        if not isinstance(strLst, tuple) and not isinstance(strLst, list):
            strLst = (strLst,)

        for s in strLst:
            s: str
            matches = re.findall(r"(\{([a-zA-Z0-9_\-]+)\})", s)
            if matches:
                for match in matches:
                    replaceVar = self.formatDict[match[1]]
                    if isinstance(replaceVar, tuple):
                        group1 = self.formatVariableStr(replaceVar)
                        formattedStrings.extend(group1)
                    else:
                        s = re.sub(r"\{[a-zA-Z0-9_\-]+\}", replaceVar, s)
                        formattedStrings.append(s)
            else:
                formattedStrings.append(s)

        return tuple(formattedStrings)

    def formatVariableStrO(self, strLst: Union[List, Tuple]):
        if not strLst:
            return tuple(strLst)
        formattedStrings = []

        if not isinstance(strLst, tuple) and not isinstance(strLst, list):
            strLst = (strLst,)

        for s in strLst:
            s: str
            matches = re.findall(r"(\{([a-zA-Z0-9_\-]+)\})", s)
            if matches:
                for match in matches:
                    replaceVar = self.formatDict[match[1]]
                    if isinstance(replaceVar, tuple):
                        group1 = []
                        for x in replaceVar:
                            group1.append(x)
                        formattedStrings.extend(group1)
                    else:
                        formattedStrings.append(
                            re.sub(r"\{[a-zA-Z0-9_\-]+\}", replaceVar, s)
                        )
            else:
                formattedStrings.append(s)
        return tuple(formattedStrings)

    def autogenConfigure(self, pkg: BasePackage):
        if pkg.autogen:
            if pkg.autogen_only_reconf:
                self.runProcess(["autoreconf", "-vi"])
                self.logger.info(
                    f"Running only autoreconf for {pkg.name} in {os.getcwd()}"
                )
            else:
                if pkg.path.joinpath("autogen.sh").exists():
                    self.logger.info(
                        f"Running autogen for {pkg.name} in {os.getcwd()}"
                    )
                    self.runProcess(["./autogen.sh"])
                else:
                    self.logger.info(
                        f"Running autoreconf for {pkg.name} in {os.getcwd()}"
                    )
                    self.runProcess(["autoreconf", "-vi"])

    # def display_message(self, message):
    #     return
    #     """Display message in console and wait for any key to be pressed"""
    #     sys.stdout.write(message)
    #     sys.stdout.flush()
    #     # Wait for a single key press
    #     try:
    #         if sys.platform.startswith("win"):
    #             # For Windows systems, use msvcrt.getch()
    #             msvcrt.getch()
    #         else:
    #             # For Unix-like systems, use getch.getch()
    #             getch.getch()
    #     except KeyboardInterrupt:
    #         # Handle the user pressing Ctrl-C by exiting the function
    #         pass

    def aquirePackage(self, package: BasePackage):
        packageDir = package.path
        if package.source_type == BasePackage.SourceType.Git:
            if not self.gitClone(package):
                self.packagesBuilt[package.name] = True
                return False
            else:
                return True

        elif package.source_type == BasePackage.SourceType.Archive:
            archive = self.downloadArchive(package, self.packagesRoot)
            if archive is None:
                raise Exception("error downloading")
            elif archive[0] is False:
                self.extractFile(archive[1], packageDir)
                os.unlink(archive[1])
                return True
            else:
                self.logger.info(
                    f"Archive from {package.name} already downloaded and extracted"
                )
                self.packagesBuilt[package.name] = True
                return False

        elif package.source_type == BasePackage.SourceType.Mercurial:
            if not self.hgClone(package):
                self.packagesBuilt[package.name] = True
                return False
            else:
                return True
        elif package.source_type == BasePackage.SourceType.SVN:
            if not self.svnCheckout(package):
                self.packagesBuilt[package.name] = True
                return False
            else:
                return True
        if packageDir == None:
            raise Exception("Package type not implemented")

        return False

    def patchPackage(self, package):
        if package.has_patches:
            for patch in package.patches:
                self.applyPatchv2(patch)

    def buildPackage(self, package: BasePackage):
        if package.name in self.packagesBuilt:
            if self.packagesBuilt[package.name]:
                return

        originalPath = os.getcwd()

        originalEnv = {}

        if package.env:
            for envVar in package.env.keys():
                self.logger.info(
                    f"Backing up env var {envVar} = {'None' if envVar not in os.environ else os.environ[envVar]}"
                )
                originalEnv[envVar] = (
                    None if envVar not in os.environ else os.environ[envVar]
                )

        packageDir = package.path

        sourceUpdated = self.aquirePackage(package)

        self.logger.info(f"Moving into package folder: {packageDir}")
        os.chdir(packageDir)

        self.display_message("Continue with patch?")

        if sourceUpdated:
            self.patchPackage(package)
            if len(package.regex_replace):
                _pos = "post_patch"
                if _pos in package.regex_replace:
                    for r in package.regex_replace[_pos]:
                        try:
                            self.handleRegexReplace(r, package.name)
                        except re.error as e:
                            print("errormeh", e)
                            exit(1)
                _pos = "post_download"
                if _pos in package.regex_replace:
                    for r in package.regex_replace[_pos]:
                        try:
                            self.handleRegexReplace(r, package.name)
                        except re.error as e:
                            print("errormeh", e)
                            exit(1)
            package.post_regex_replace_cmd()
            package.post_download_commands()

            if (
                not package.path.joinpath("_already_conf").exists()
                and not package.runAutogenInSubSource
            ):
                if package.conf_system == BasePackage.ConfSystem.Autoconf:
                    if (
                        not packageDir.joinpath("Configure").exists()
                        and not packageDir.joinpath("configure").exists()
                    ):
                        self.autogenConfigure(package)

        if package.get_source_subfolder is not None:
            self.logger.info(
                f"Moving into package build folder: {package.get_source_subfolder}"
            )
            if not package.get_source_subfolder.exists():
                package.get_source_subfolder.mkdir()
            os.chdir(package.get_source_subfolder)  # type: ignore

        package.post_download_sub_commands()

        if sourceUpdated:
            if (
                not package.path.joinpath("_already_conf").exists()
                and package.runAutogenInSubSource
            ):
                if package.conf_system == BasePackage.ConfSystem.Autoconf:
                    if (
                        not package.get_source_subfolder_combined.joinpath(
                            "Configure"
                        ).exists()
                        and not package.get_source_subfolder_combined.joinpath(
                            "configure"
                        ).exists()
                    ):
                        print(
                            package.get_source_subfolder_combined.joinpath(
                                "configure"
                            )
                        )
                        self.autogenConfigure(package)

            self.display_message("Continue with conf?")

        if package.env:
            for envVar in package.env.keys():
                envVarFormatted = self.format_variable_str(package.env[envVar])
                self.logger.info(
                    f"Setting env var {envVar} to {envVarFormatted}"
                )
                os.environ[envVar] = envVarFormatted

        # print("### Environment variables:  ###")
        # for tk in os.environ:
        #     print("\t" + tk + " : " + os.environ[tk])
        # print("##############################")

        if not package.path.joinpath("_already_conf").exists():
            if package.conf_system == BasePackage.ConfSystem.CMake:
                self.cmakePackage(package)
            elif package.conf_system == BasePackage.ConfSystem.Autoconf:
                self.autoconfPackage(package)
            elif package.conf_system == BasePackage.ConfSystem.Meson:
                self.mesonPackage(package)
            elif package.conf_system == BasePackage.ConfSystem.Cargo:
                pass
            package.path.joinpath("_already_conf").touch()

            self.display_message("Continue with build?")

        if not package.path.joinpath("_already_build").exists():
            if package.build_system == BasePackage.BuildSystem.Ninja:
                self.ninjaMakePackage(package)
            elif package.build_system == BasePackage.BuildSystem.Make:
                self.autoconfMakePackage(package)
            elif package.build_system == BasePackage.BuildSystem.Cargo:
                self.cargoBuildPackage(package)

            package.post_make_commands()

            package.path.joinpath("_already_build").touch()

            package.post_build_commands()

            self.display_message("Continue with install?")

        if not package.path.joinpath("_already_install").exists():
            if package.install_system == BasePackage.BuildSystem.Ninja:
                self.ninjaInstallPackage(package)
            elif package.install_system == BasePackage.BuildSystem.Make:
                self.autoconfInstallPackage(package)
            elif package.install_system == BasePackage.BuildSystem.Cargo:
                pass
            package.path.joinpath("_already_install").touch()

            package.post_install_commands()

            if len(package.regex_replace):
                _pos = "post_install"
                if _pos in package.regex_replace:
                    for r in package.regex_replace[_pos]:
                        try:
                            self.handleRegexReplace(r, package.name)
                        except re.error as e:
                            print("errormeh", e)
                            exit(1)

        if package.env:
            for envVar in package.env.keys():
                if envVar in os.environ:
                    if originalEnv[envVar] is None:
                        self.logger.info(f"Deleting env var {envVar}")
                        del os.environ[envVar]
                    elif originalEnv[envVar]:
                        self.logger.info(
                            f"Restoring env var {envVar} to {originalEnv[envVar]}"
                        )
                        os.environ[envVar] = originalEnv[envVar]

        self.packagesBuilt[package.name] = True

        # os.environ.clear()
        # os.environ.update(backEnv)

    def mesonPackage(self, package: BasePackage):
        conf = package.config
        self.logger.info(f"Mesoning {package.name} with '{' '.join(conf)}'")
        self.runProcess(list(package.meson_command) + list(package.config))

    def autoconfPackage(self, package: BasePackage):
        conf = package.config
        self.logger.info(f"Autoconfing {package.name} with '{' '.join(conf)}'")

        cmd = list(package.autoconf_command)
        mainCmd = cmd[0]
        if not package.path.joinpath(mainCmd).executeable():
            cmd = ["sh"] + cmd
            self.logger.warning(
                "configure command is not executeable, using SH"
            )

        self.runProcess(cmd + list(package.config))

    def cmakePackage(self, package: BasePackage):
        pp(list(package.cmake_command))
        pp(list(package.config))
        pp(list(package.cmake_command) + list(package.config))

        conf = package.config
        self.logger.info(f"C-Making {package.name} with '{' '.join(conf)}'")

        self.runProcess(list(package.cmake_command) + list(package.config))

    def cargoBuildPackage(self, package):
        bconf = package.build
        self.logger.info(
            f"Cargo C-Building {package.name} with '{' '.join(bconf)}'"
        )
        result = subprocess.run(list(package.cargo_command) + list(bconf))
        if result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            exit(1)

    def autoconfMakePackage(self, package):
        bconf = package.build
        cmd = list(package.make_command) + list(bconf)
        self.logger.info(
            f"Autoconf Building {package.name} with '{shlex.join(cmd)}'"
        )
        self.runProcess(cmd)

    def autoconfInstallPackage(self, package):
        iconf = package.install
        self.logger.info(
            f"Autoconf Installing {package.name} with '{' '.join(iconf)}'"
        )
        self.runProcess(list(package.make_install_command) + list(iconf))

    def ninjaMakePackage(self, package):
        bconf = package.build
        self.logger.info(
            f"Ninja Building {package.name} with '{' '.join(bconf)}'"
        )
        self.runProcess(list(package.ninja_command) + list(bconf))

    def ninjaInstallPackage(self, package):
        iconf = package.install
        self.logger.info(
            f"Ninja Installing {package.name} with '{' '.join(iconf)}'"
        )
        self.runProcess(list(package.ninja_command) + list(iconf))

    def applyPatchv2(self, patchData):
        url = patchData["file"]

        originalFolder = os.getcwd()
        if "dir" in patchData and patchData["dir"] is not None:
            os.chdir(patchData["dir"])
            self.logger.debug("Moving to patch folder: {0}".format(os.getcwd()))

        self.logger.debug(
            "Applying patch '{0}' in '{1}'".format(url, os.getcwd())
        )

        patchTouchName = "patch_%s.done" % (self.md5(url))

        if os.path.isfile(patchTouchName):
            self.logger.debug("Patch '{0}' already applied".format(url))
            os.chdir(originalFolder)
            return

        pUrl = urlparse(url)
        if pUrl.scheme != "":
            fileName = os.path.basename(pUrl.path)
            self.logger.info(
                "Downloading patch '{0}' to: {1}".format(url, fileName)
            )
            self.downloadFile(url, fileName)
        else:
            local_patch_path = os.path.join(self.fullPatchDir, url)
            fileName = os.path.basename(Path(local_patch_path).name)
            if os.path.isfile(local_patch_path):
                copyPath = os.path.join(os.getcwd(), fileName)
                self.logger.info(
                    "Copying patch from '{0}' to '{1}'".format(
                        local_patch_path, copyPath
                    )
                )
                shutil.copyfile(local_patch_path, copyPath)
            else:
                fileName = os.path.basename(urlparse(url).path)
                url = (
                    "https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches"
                    + url
                )
                self.downloadFile(url, fileName)

        cmd = "patch -p1"
        if "cmd" in patchData and patchData["cmd"] is not None:
            cmd = patchData["cmd"]

        self.logger.info("Patching source using: '{0}'".format(fileName))
        self.runProcess(shlex.split(cmd), inputFile=fileName)
        self.touch(patchTouchName)

        if "dir" in patchData and patchData["dir"] is not None:
            os.chdir(originalFolder)

    def touch(self, f):
        Path(f).touch()

    def downloadFile(
        self, url=None, outputFileName=None, outputPath=None, bytesMode=False
    ):
        def fmt_size(num, suffix="B"):
            for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num, unit, suffix)
                num /= 1024.0
            return "%.1f%s%s" % (num, "Yi", suffix)

        #:
        if not url:
            raise Exception("No URL specified.")

        if outputPath is None:  # Default to current dir.
            outputPath = os.getcwd()
        else:
            if not os.path.isdir(outputPath):
                raise Exception(
                    'Specified path "{0}" does not exist'.format(outputPath)
                )

        fileName = os.path.basename(url)  # Get URL filename
        userAgent = self.userAgent

        if "sourceforge.net" in url.lower():
            userAgent = "wget/1.18"  # sourceforce <3 wget

        if url.lower().startswith("ftp://"):
            self.logger.info("Requesting : {0}".format(url))
            if outputFileName is not None:
                fileName = outputFileName
            fullOutputPath = os.path.join(outputPath, fileName)
            urllib.request.urlretrieve(url, fullOutputPath)
            return fullOutputPath

        if url.lower().startswith("file://"):
            url = url.replace("file://", "")
            self.logger.info("Copying : {0}".format(url))
            if outputFileName is not None:
                fileName = outputFileName
            fullOutputPath = os.path.join(outputPath, fileName)
            try:
                shutil.copyfile(url, fullOutputPath)
            except Exception as e:
                print(e)
                exit(1)
            return fullOutputPath

        req = requests.get(url, stream=True, headers={"User-Agent": userAgent})

        if req.status_code != 200:
            req.raise_for_status()

        if "content-disposition" in req.headers:
            reSponse = re.findall(
                "filename=(.+)", req.headers["content-disposition"]
            )
            if reSponse is None:
                fileName = os.path.basename(url)
            else:
                fileName = reSponse[0]

        size = None
        compressed = False
        if "Content-Length" in req.headers:
            size = int(req.headers["Content-Length"])

        if "Content-Encoding" in req.headers:
            if req.headers["Content-Encoding"] == "gzip":
                compressed = True

        self.logger.info(
            "Requesting : {0} - {1}".format(
                url, fmt_size(size) if size is not None else "?"
            )
        )

        # terms = shutil.get_terminal_size((100,100))
        # filler = 0
        # if terms[0] > 100:
        # 	filler = int(terms[0]/4)

        widgetsNoSize = [
            progressbar.FormatCustomText(
                "Downloading: {:25.25}".format(os.path.basename(fileName))
            ),
            " ",
            progressbar.AnimatedMarker(markers="|/-\\"),
            " ",
            progressbar.DataSize()
            # " "*filler
        ]
        widgets = [
            progressbar.FormatCustomText(
                "Downloading: {:25.25}".format(os.path.basename(fileName))
            ),
            " ",
            progressbar.Percentage(),
            " ",
            progressbar.Bar(
                fill=chr(9617), marker=chr(9608), left="[", right="]"
            ),
            " ",
            progressbar.DataSize(),
            "/",
            progressbar.DataSize(variable="max_value"),
            " |",
            progressbar.AdaptiveTransferSpeed(),
            " | ",
            progressbar.ETA(),
            # " "*filler
        ]
        pbar = None
        if size is None:
            pbar = progressbar.ProgressBar(
                widgets=widgetsNoSize, maxval=progressbar.UnknownLength
            )
        else:
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=size)

        if outputFileName is not None:
            fileName = outputFileName
        fullOutputPath = os.path.join(outputPath, fileName)

        updateSize = 0

        if isinstance(pbar.max_value, int):
            updateSize = pbar.max_value if pbar.max_value < 1024 else 1024

        if bytesMode is True:
            output = b""
            bytesrecv = 0
            pbar.start()
            for buffer in req.iter_content(chunk_size=1024):
                if buffer:
                    output += buffer
                if compressed:
                    pbar.update(updateSize)
                else:
                    pbar.update(bytesrecv)
                bytesrecv += len(buffer)
            pbar.finish()
            return output
        else:
            with open(fullOutputPath, "wb") as file:
                bytesrecv = 0
                pbar.start()
                for buffer in req.iter_content(chunk_size=1024):
                    if buffer:
                        file.write(buffer)
                        file.flush()
                    if compressed:
                        pbar.update(updateSize)
                    else:
                        pbar.update(bytesrecv)
                    bytesrecv += len(buffer)
                pbar.finish()

                return fullOutputPath

    #:

    def sanityCheckPackages(self):
        pkg: BasePackage
        for pkg_name, pkg in self.packages.items():
            if pkg_name in pkg.depends:
                self.logger.error(
                    f"Package {pkg_name} depends on itself, which is not valid."
                )
                exit(1)
            if len(pkg.depends):
                for pkg_depend in pkg.depends:
                    if pkg_depend not in self.packages.keys():
                        self.logger.error(
                            f"The dependency <u>{pkg_depend}</u> for <u>{pkg_name}</u> does not exist."
                        )
                        exit(1)

    def loadPackages(self):
        pkg_dir = "packages"
        print("Loading Packages")

        # Add the main directory to the system path^

        for file_name in os.listdir(pkg_dir):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]
                module_path = os.path.join(pkg_dir, file_name)
                spec = importlib.util.spec_from_file_location(
                    module_name, module_path
                )
                if spec is not None:
                    module = importlib.util.module_from_spec(spec)
                    if spec.loader is not None:
                        spec.loader.exec_module(module)
                    for name in dir(module):
                        obj = getattr(module, name)
                        try:
                            if (
                                issubclass(obj, BasePackage)
                                and obj is not BasePackage
                            ):
                                self.packages[obj.name] = obj(self)
                        except TypeError as e:
                            # print(traceback.format_exc())
                            pass

    def createCargoHome(self):
        if not os.path.isdir(self.cargoHomePath):
            os.environ["CARGO_HOME"] = str(self.cargoHomePath)
            self.logger.info("Creating Cargo Home: '%s'" % (self.cargoHomePath))

            cargoConfigPath = self.cargoHomePath.joinpath("config.toml")

            self.cargoHomePath.mkdir(parents=True)
            tcFile = [
                f"[target.{self.rustTargetStr}]",
                f'linker = "{self.mingwPrefixStrDash}gcc"',
                f'ar = "{self.mingwPrefixStrDash}ar"',
            ]
            with open(cargoConfigPath, "w") as f:
                f.write("\n".join(tcFile))
            self.logger.info(
                "Wrote Cargo Home config.toml in '%s'" % (self.cargoHomePath)
            )

            self.logger.info(
                "Setting up cargo toolchain in '%s'" % (self.cargoHomePath)
            )

            result = subprocess.run(["cargo", "install", "cargo-c"])
            if result.returncode != 0:
                print(f"Command failed with return code {result.returncode}")
                exit(1)

    def createCmakeToolchainFile(self):
        if not os.path.isfile(self.cmakeToolchainFile):
            self.logger.info(
                "Creating CMake Toolchain file at: '%s'"
                % (self.cmakeToolchainFile)
            )
            tcFile = [
                f"set(CMAKE_SYSTEM_NAME Windows)",
                f"set(CMAKE_SYSTEM_PROCESSOR {self.bitnessStr})",
                # F'set(CMAKE_SYSROOT {self.targetSubPrefix})',
                # F'set(CMAKE_STAGING_PREFIX /home/devel/stage)',
                f"set(CMAKE_RANLIB {self.mingwPrefixStrDash}ranlib)",
                f"set(CMAKE_C_COMPILER {self.mingwPrefixStrDash}gcc)",
                f"set(CMAKE_CXX_COMPILER {self.mingwPrefixStrDash}g++)",
                f"set(CMAKE_RC_COMPILER {self.mingwPrefixStrDash}windres)",
                f"set(CMAKE_ASM_COMPILER {self.mingwPrefixStrDash}as)",
                f"set(CMAKE_FIND_ROOT_PATH {self.toolchainRootPath}/)",
                f"set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM BOTH)",
                f"set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)",
                f"set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)",
                f"set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)",
                # for shaderc
                f"set(MINGW_COMPILER_PREFIX {self.mingwPrefixStrDash})",
                # F'set(MINGW_SYSROOT {self.targetSubPrefix})'
            ]
            with open(self.cmakeToolchainFile, "w") as f:
                f.write("\n".join(tcFile))

    def createMesonEnvFile(self):
        if not os.path.isfile(self.mesonEnvFile):
            self.logger.info(
                "Creating Meson Environment file at: '%s'" % (self.mesonEnvFile)
            )
            meFile = (
                "[binaries]\n",
                f"c = '{self.mingwPrefixStrDash}gcc'",
                f"cpp = '{self.mingwPrefixStrDash}g++'",
                f"ld = 'bfd'",  # See: https://github.com/mesonbuild/meson/issues/6431#issuecomment-572544268, no clue either why we can't just define full "ld" path, but whatever.
                # F"ld = '{self.mingwPrefixStrDash}ld'",
                f"ar = '{self.mingwPrefixStrDash}ar'",
                f"strip = '{self.mingwPrefixStrDash}strip'",
                f"windres = '{self.mingwPrefixStrDash}windres'",
                f"ranlib = '{self.mingwPrefixStrDash}ranlib'",
                "pkgconfig = 'pkg-config'",
                f"dlltool = '{self.mingwPrefixStrDash}dlltool'",
                f"gendef = '{self.toolchainBinPathOne}/gendef'",
                "cmake = 'cmake'",
                "#needs_exe_wrapper = false",
                "#exe_wrapper = 'wine' # A command used to run generated executables.",
                "",
                "[host_machine]",
                "system = 'windows'",
                f"cpu_family = '{self.bitnessStr}'",
                f"cpu = '{self.bitnessStr}'",
                "endian = 'little'",
                "",
                "[target_machine]",
                "system = 'windows'",
                f"cpu_family = '{self.bitnessStr}'",
                f"cpu = '{self.bitnessStr}'",
                "endian = 'little'",
                "",
                "[properties]",
                f"cmake_toolchain_file = '{str(self.cmakeToolchainFile)}'",
                # "c_link_args = ['-static', '-static-libgcc']",
                # "# sys_root = Directory that contains 'bin', 'lib', etc for the toolchain and system libraries",
                # F"sys_root = '{self.targetSubPrefix}'"
            )
            with open(self.mesonEnvFile, "w") as f:
                f.write("\n".join(meFile))

        if not os.path.isfile(self.mesonNativeFile):
            meNaFile = (
                "[properties]",
                "c_args = ['', '-nostdinc']",
                "cpp_args = ['', '-nostdinc']",
                "link_args = ['', '-nostdlib']",
            )
            with open(self.mesonNativeFile, "w") as f:
                f.write("\n".join(meNaFile))

    def sanitizeFilename(self, f):
        return re.sub(r'[/\\:*?"<>|]', "", f)

    def md5(self, *args):
        msg = "".join(args).encode("utf-8")
        m = hashlib.md5()
        m.update(msg)
        return m.hexdigest()

    def buildMinGWToolchain(self):
        gccBin = f"{self.toolchainBinPathOne}/{self.mingwPrefixStrDash}gcc"
        if os.path.isfile(gccBin):
            gccOutput = subprocess.check_output(
                gccBin + " -v", shell=True, stderr=subprocess.STDOUT
            ).decode("utf-8")
            workingGcc = re.compile(
                "^Target: .*-w64-mingw32$", re.MULTILINE
            ).findall(gccOutput)
            if len(workingGcc) > 0:
                self.logger.info("MinGW-w64 install is working!")
                return
            else:
                raise Exception(
                    "GCC is not working properly, target is not mingw32."
                )
                exit(1)

        def toolchainBuildStatus(logMessage):
            self.logger.info(logMessage)

        mod = importlib.import_module(
            "mingw_toolchain_script.mingw_toolchain_script"
        )

        # from mingw_toolchain_script.mingw_toolchain_script import MinGW64ToolChainBuilder

        toolchainBuilder = mod.MinGW64ToolChainBuilder()

        toolchainBuilder.setMinGWcheckout("")
        toolchainBuilder.onStatusUpdate += toolchainBuildStatus
        toolchainBuilder.build()

        self.buildPackages(self.packages["pkg-config"])


if __name__ == "__main__":
    compiler = CrossCompiler()
