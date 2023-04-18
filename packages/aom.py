from packages.base_package import BasePackage

class AOM(BasePackage):

    name = "aom"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
    
        self.source_subfolder = "_build"

    @property
    def pkg_depends(self):
        return ("libxml2", )

    @property
    def pkg_url(self):
        return "https://aomedia.googlesource.com/aom"

    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=0',
            '-DENABLE_DOCS=0',
            '-DENABLE_TESTS=0',
            '-DENABLE_TOOLS=0',
            '-DENABLE_CCACHE=1',
            '-DCONFIG_LPF_MASK=1',
            '-DENABLE_EXAMPLES=0',
            '-DENABLE_TESTDATA=0',
            '-DCONFIG_AV1_DECODER=1',
            '-DCONFIG_AV1_ENCODER=1',
            '-DCONFIG_PIC=1',
            '-DCONFIG_SPATIAL_RESAMPLING=1',
            '-DENABLE_NASM=off',
            '-DCONFIG_STATIC=1',
            '-DCONFIG_SHARED=0',
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {
            "version": "git (master)",
            "fancy_name": "AOM"
        }