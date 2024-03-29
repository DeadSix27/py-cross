from packages.base_package import BasePackage

class SPIRV_Headers(BasePackage):

    name = "spirv-headers"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "d4461bc88522f286acc8958415e0027e116bbe35"

    @property
    def pkg_depends(self):
        return ()
    
    @property
    def pkg_url(self):
        return "https://github.com/KhronosGroup/SPIRV-Headers"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DBUILD_TESTS=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]