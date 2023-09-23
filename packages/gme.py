from packages.base_package import BasePackage

class GME(BasePackage):
    name = "gme"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        self.source_subfolder = "_build"

        self.regex_replace = {
            'post_patch': [
                {
                    0: r'add_subdirectory\(player EXCLUDE_FROM_ALL\)',
                    'in_file': 'CMakeLists.txt'
                },
                {
                    0: r'add_subdirectory\(demo EXCLUDE_FROM_ALL\)',
                    'in_file': 'CMakeLists.txt'
                }
                
            ],
        }

    @property
    def url(self):
        return "https://bitbucket.org/mpyne/game-music-emu.git"
    
    @property
    def pkg_depends(self):
        return ["zlib-ng"]
    
    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DENABLE_UBSAN=OFF",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "gme"}
