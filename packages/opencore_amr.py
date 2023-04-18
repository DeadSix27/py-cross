from packages.base_package import BasePackage


class OPENCORE_AMR(BasePackage):
    name = "opencore_amr"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

    @property
    def pkg_depends(self):
        return ()

    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.6.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "483eb4061088e2b34b358e47540b5d495a96cd468e361050fae615b1809dc4a1",
                    },
                ],
            },
        ]

    @property
    def pkg_config(self):
        return (
            "{autoconf_prefix_options}",
            "--build=x86_64-pc-linux-gnu",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "opencore_amr"}
