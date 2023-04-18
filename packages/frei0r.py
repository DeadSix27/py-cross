from packages.base_package import BasePackage


class Frei0rPackage(BasePackage):
    name = "frei0r"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        self.source_subfolder = "_build"

    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "https://files.dyne.org/frei0r/frei0r-plugins-1.8.0.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "45a28655caf057227b442b800ca3899e93490515c81e212d219fdf4a7613f5c4",
                    },
                ],
            },
            {
                "url": "https://cdn.netbsd.org/pub/pkgsrc/distfiles/frei0r-plugins-1.8.0.tar.gz",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "45a28655caf057227b442b800ca3899e93490515c81e212d219fdf4a7613f5c4",
                    },
                ],
            },
        ]
    
    @property
    def pkg_depends(self):
        return ("dlfcn-win32", )
    
    @property
    def pkg_config(self):
        return (
            "..",
            "--debug-find",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DWITHOUT_OPENCV=YES",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "AviSynth+ (Headers only)"}
