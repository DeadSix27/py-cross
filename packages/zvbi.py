from packages.base_package import BasePackage


class zvbi(BasePackage):
    name = "zvbi"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        # self.autogen = False

        # self.source_subfolder = "build/generic"
        # self.autoconf_command = [ "./configure" ]
        self.patches = [
            {"file": "zvbi/0001-zvbi-0.2.35_win32.patch"},
            {"file": "zvbi/0002-zvbi-0.2.35_ioctl.patch"},
            {"file": "zvbi/0003-build-only-src.patch"},
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
    def pkg_mirrors(self):
        return (
            {
                "url": "https://sourceforge.net/projects/zapping/files/zvbi/0.2.35/zvbi-0.2.35.tar.bz2",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "fc883c34111a487c4a783f91b1b2bb5610d8d8e58dcba80c7ab31e67e4765318",
                    },
                ],
            },
            {
                "url": "https://download.videolan.org/contrib/zvbi/zvbi-0.2.35.tar.bz2",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "fc883c34111a487c4a783f91b1b2bb5610d8d8e58dcba80c7ab31e67e4765318",
                    },
                ],
            },
        )

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
