from packages.base_package import BasePackage


class zvbi(BasePackage):
    name = "zvbi"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        # self.autogen = False

        # self.source_subfolder = "build/generic"
        # self.autoconf_command = [ "./configure" ]
        self.patches = [
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0001-ssize_max.patch"},
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0002-ioctl.patch"},
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0003-fix-static-linking.patch"},
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0004-win32.patch"},
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0005-win32-undefined.patch"},
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0006-skip-directory.patch"},
            {"cmd": "git am --3way", "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/libzvbi-0007-fix-clang-compilation-on-i686.patch"},
        ]

    @property
    def pkg_env(self):
        return {
		    'LIBS' : '-lpng',
        }

    def pkg_post_download_commands(self):
        self.compiler.runProcess(
            ["mkdir", "-pv", "src"]
        )

    # def pkg_post_install_commands(self):
        # self.compiler.runProcess(
            # ["cp", "-rv", "zvbi-0.2.pc", "{target_prefix}/lib/pkgconfig/zvbi-0.2.pc"]
        # )

    @property
    def pkg_depends(self):
        return ["iconv", "dlfcn-win32", "libpng"]

    @property
    def pkg_url(self) -> str:
        return "https://github.com/zapping-vbi/zvbi.git"

    @property
    def pkg_config(self):
        return (
            "--host={mingw_prefix}",
            "--prefix={target_prefix}",
            '--build=x86_64-pc-linux-gnu',
            "--disable-shared",
            "--enable-static",
            "--disable-rpath",
            "--disable-dependency-tracking",
            "--disable-libtool-lock",
            "--disable-dvb",
            "--disable-bktr",
            "--disable-nls",
            "--disable-proxy",
            "--without-doxygen",
            "--without-x",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "zvbi"}
