from packages.base_package import BasePackage

class SPIRV_Tools(BasePackage):

    name = "spirv-tools"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "a525dccbe8058c42079a67a49e7aa9973d67de27"
        self.patches = [
            {"file": "https://github.com/DeadSix27/SPIRV-Tools/commit/6ef89a00fbccb833f6ba3c86c169845019ef36b0.patch"},
        ]

    @property
    def pkg_depends(self):
        return ("spirv-headers", )
    
    def pkg_post_download_commands(self):
        self.compiler.createSymlink(self.compiler.getPackagePathByName("spirv-headers", True), self.path.joinpath("external/spirv-headers"))
    
    @property
    def pkg_url(self):
        return "https://github.com/KhronosGroup/SPIRV-Tools"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DSPIRV_TOOLS_BUILD_STATIC=ON',
            '-DSPIRV_SKIP_EXECUTABLES=ON',
            '-DSPIRV_SKIP_TESTS=ON',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]