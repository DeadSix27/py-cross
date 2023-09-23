from packages.base_package import BasePackage


class LIBPNG(BasePackage):
    name = "libpng"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        self.source_subfolder = "_build"
       
        self.patches = [
            { 'file': 'libpng/libpng-1.6.40-apng.patch' },
        ]


    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "https://download.sourceforge.net/libpng/libpng-1.6.40.tar.xz",
                "hashes": [
                    {
                        "type": "sha1",
                        "sum": "1c37609e3f0740ae52ca9e2a6adfc9743497b870",
                    },
                ],
            }
        ]
    
    @property
    def pkg_depends(self):
        return ["zlib-ng",]
    
    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DPNG_TESTS=OFF",
            "-DPNG_SHARED=OFF",
            "-DPNG_STATIC=ON",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "libpng"}
