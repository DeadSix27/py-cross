from packages.base_package import BasePackage
import shlex


class luajit(BasePackage):
    name = "luajit"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
        self.git_branch = "v2.1-agentzh"
        self.patches = [
            {
                "file": "https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/luajit-0001-add-win32-utf-8-filesystem-functions.patch"
            }
        ]

    @property
    def pkg_url(self):
        return "https://github.com/openresty/luajit2"
    
    def pkg_post_install_commands(self):
        luajitPcFile = [
            "# Package information for LuaJIT to be used by pkg-config.",
            "majver=2",
            "minver=1",
            "relver=0",
            "version=${majver}.${minver}.${relver}-beta3",
            "abiver=5.1",

            F"prefix={self.compiler.crossPrefix}",
            "multilib=lib",
            "exec_prefix=${prefix}",
            "libdir=${exec_prefix}/${multilib}",
            "libname=luajit-${abiver}",
            "includedir=${prefix}/include/luajit-${majver}.${minver}",

            "INSTALL_LMOD=${prefix}/share/lua/${abiver}",
            "INSTALL_CMOD=${prefix}/${multilib}/lua/${abiver}",

            "Name: LuaJIT",
            "Description: Just-in-time compiler for Lua",
            "URL: http://luajit.org",
            "Version: ${version}",
            "Requires:",
            "Libs: -L${libdir} -l${libname}",
            "Libs.private: -lm -liconv",
            "Cflags: -I${includedir}",
            ]
        with open(self.compiler.pkgConfigPath.joinpath("luajit.pc"), "w") as pcfile:
            for l in luajitPcFile:
                pcfile.write(l + "\n")

    @property
    def pkg_config(self):
        return ["dlfcn-win32"]

    @property
    def pkg_build(self):
        return [
            "HOST_CC=gcc -m64",
            "CROSS={mingw_prefix_dash}",
            "TARGET_SYS=Windows",
            "BUILDMODE=static",
            "FILE_T=luajit.exe",
            "CFLAGS=-D_WIN32_WINNT=0x0602 -DUNICODE",
            "XCFLAGS=-DLUAJIT_ENABLE_LUA52COMPAT",
            "PREFIX={target_prefix}",
            "amalg",
        ]

        # return shlex.split('CROSS={mingw_prefix_dash} HOST_CC="gcc -m{bitness_num}" TARGET_SYS=Windows BUILDMODE="static amalg"')

    @property
    def pkg_install(self):
        return [
            "HOST_CC=gcc -m64",
            "CROSS={mingw_prefix_dash}",
            "TARGET_SYS=Windows",
            "BUILDMODE=static",
            "FILE_T=luajit.exe",
            "CFLAGS=-D_WIN32_WINNT=0x0602 -DUNICODE",
            "XCFLAGS=-DLUAJIT_ENABLE_LUA52COMPAT",
            "PREFIX={target_prefix}",
            "install",
        ]
        # return shlex.split(
        #     'install CROSS={mingw_prefix_dash} HOST_CC="gcc -m{bitness_num}" TARGET_SYS=Windows BUILDMODE=static FILE_T=luajit.exe PREFIX={target_prefix}'
        # )

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "luajit"}
