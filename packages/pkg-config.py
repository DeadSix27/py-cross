from packages.base_package import BasePackage


class pkgconfig(BasePackage):
    name = "pkg-config"

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

    @property
    def pkg_depends(self):
        return ()

    @property
    def pkg_env(self):
        return {
            "PKG_CONFIG_PATH": "{local_pkg_config_path}",
            "PATH": "{local_path}"
        }

    @property
    def pkg_mirrors(self):
        return (
            {
                "url": "https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591",
                    },
                ],
            },
            {
                "url": "https://fossies.org/linux/misc/pkg-config-0.29.2.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591",
                    },
                ],
            },
        )

    @property
    def pkg_config(self):
        return ("--prefix={toolchain_path_one}",
                "--disable-shared",
                "--enable-static",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "pkg-config"}
