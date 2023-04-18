from tkinter import OFF
from packages.base_package import BasePackage


class giflib(BasePackage):
    name = "giflib"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.patches = [
		    {"file": 'giflib/giflib-add-cmakelists.patch'}, # thanks to https://sourceforge.net/p/giflib/feature-requests/6/
        ]
    


    @property
    def pkg_depends(self):
        return []
    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "https://fossies.org/linux/misc/giflib-5.2.1.tar.bz2",
                "hashes": [
                    {
                        "type": "sha256",
                        "sum": "26cb5bdda7957f8c8fba45d1899936d81e0af04c0754bbba50fbe2ad6234bb01",
                    },
                ],
            },
        ]

    @property
    def pkg_config(self):
        return (
            "../patches/giflib/CMakeLists.txt",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_STATIC_LIBS=1",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]
