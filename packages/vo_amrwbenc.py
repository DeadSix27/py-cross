from packages.base_package import BasePackage


class vo_amrwbenc(BasePackage):
    name = "vo_amrwbenc"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.source_subfolder = "_build"

        self.autoconf_command = [ "../configure" ]

    @property
    def pkg_mirrors(self):
        return [
            { 'url' : 'https://sourceforge.net/projects/opencore-amr/files/vo-amrwbenc/vo-amrwbenc-0.1.3.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5652b391e0f0e296417b841b02987d3fd33e6c0af342c69542cbb016a71d9d4e' }, ], },
        ]

    @property
    def pkg_depends(self):
        return ()

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
        return {"version": "git (master)", "fancy_name": "vo_amrwbenc"}
