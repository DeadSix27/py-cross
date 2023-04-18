from packages.base_package import BasePackage


class LAME(BasePackage):
    name = "lame"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.source_subfolder = "_build"

        self.autoconf_command = ["../configure"]

    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "https://sourceforge.net/projects/lame/files/lame/3.100/lame-3.100.tar.gz",
                "hashes": [
                    {
                        "type": "sha1",
                        "sum": "64c53b1a4d493237cef5e74944912cd9f98e618d",
                    },
                ],
            }
        ]

    @property
    def pkg_depends(self):
        return ()

    @property
    def pkg_config(self):
        return (
            "{autoconf_prefix_options}",
            "--build=x86_64-pc-linux-gnu",
            "--disable-examples",
            "--disable-silent-rules",
            "--disable-frontend",
            "--enable-nasm",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "lame"}
