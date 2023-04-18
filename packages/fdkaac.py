from packages.base_package import BasePackage

class FDKAAC(BasePackage):
    name = "fdkaac"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja

        self.source_subfolder = "_build"

    @property
    def url(self):
        return "https://github.com/mstorsjo/fdk-aac"
    
    @property
    def pkg_depends(self):
        return ()
    
    @property
    def pkg_config(self):
        return (
            "..",
            "{cmake_prefix_options}",
            "-DCMAKE_INSTALL_PREFIX={target_prefix}",
            "-DBUILD_SHARED_LIBS=OFF",
            "-DBUILD_PROGRAMS=OFF",
            "-DFDK_AAC_INSTALL_CMAKE_CONFIG_MODULE=OFF",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "fdk-aac"}
