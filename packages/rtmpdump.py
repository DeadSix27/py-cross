from packages.base_package import BasePackage


class rtmpdump(BasePackage):
    name = "rtmpdump"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.make_command = (
            "make",
            "SYS=mingw",
            "CRYPTO=OPENSSL",
            "LIB_OPENSSL=!CMD(pkg-config --libs --static openssl)CMD! -lz",
            "OPT=-O3",
            "CROSS_COMPILE={mingw_prefix_dash}",
            "SHARED=no",
            "prefix={target_prefix}",
        )

        self.make_install_command = (
            "make",
            "install",
            "SYS=mingw",
            "CRYPTO=OPENSSL",
            "LIB_OPENSSL=!CMD(pkg-config --libs --static openssl)CMD! -lz",
            "OPT=-O3",
            "CROSS_COMPILE={mingw_prefix_dash}",
            "SHARED=no",
            "prefix={target_prefix}",
        )
        self.patches = [{"file": "rtmpdump/0001-Add-support-for-LibreSSL.patch"}]

    @property
    def pkg_depends(self):
        return [
            # "libressl",
            "openssl",
            "zlib"
        ]

    @property
    def pkg_url(self):
        return "https://git.ffmpeg.org/rtmpdump.git"

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "rtmpdumb"}
