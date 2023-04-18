from packages.base_package import BasePackage

class SPIRV_CROSS(BasePackage):

    name = "spirv-cross"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.patches = [
            {"file": 'https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/spirv-cross-0001-static-linking-hacks.patch'}
        ]

    @property
    def pkg_depends(self):
        return ()
    
    @property
    def pkg_url(self):
        return "https://github.com/KhronosGroup/SPIRV-Cross.git"
    
    def pkg_post_install_commands(self):
        self.compiler.runProcess(["cp", "-rv", "{target_prefix}/lib/pkgconfig/spirv-cross-c-shared.pc", "{target_prefix}/lib/pkgconfig/spirv-cross.pc"])
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DSPIRV_CROSS_SHARED=ON',
            '-DSPIRV_CROSS_CLI=OFF',
            '-DSPIRV_CROSS_ENABLE_TESTS=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]