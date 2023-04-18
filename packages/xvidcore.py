from packages.base_package import BasePackage


class xvidcore(BasePackage):
    name = "xvidcore"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.autogen = False
    
        self.source_subfolder = "build/generic"
        self.autoconf_command = [ "./configure" ]

    @property
    def pkg_depends(self):
        return ()

    def pkg_post_install_commands(self):
        self.compiler.runProcess(["rm", "-v", "{target_prefix}/lib/xvidcore.dll.a"])
        self.compiler.runProcess(
            [
                "mv",
                "-v",
                "{target_prefix}/lib/xvidcore.a",
                "{target_prefix}/lib/libxvidcore.a",
            ]
        )

    @property
    def pkg_mirrors(self):
        return (
            {
                "url": "https://downloads.xvid.com/downloads/xvidcore-1.3.7.tar.bz2",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "aeeaae952d4db395249839a3bd03841d6844843f5a4f84c271ff88f7aa1acff7",
                    },
                ],
            },
            {
                "url": "https://fossies.org/linux/misc/xvidcore-1.3.7.tar.bz2",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "aeeaae952d4db395249839a3bd03841d6844843f5a4f84c271ff88f7aa1acff7",
                    },
                ],
            },
        )

    @property
    def pkg_config(self):
        return ("{autoconf_prefix_options}",)

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "xvidcore"}
