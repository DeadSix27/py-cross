from packages.base_package import BasePackage

class HIGHWAY(BasePackage):

    name = "highway"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.git_tag = "1.0.4"
        

    @property
    def pkg_depends(self):
        return ( )
    
    @property
    def pkg_url(self):
        return "https://github.com/google/highway"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DHWY_ENABLE_CONTRIB=OFF',
            '-DHWY_ENABLE_EXAMPLES=OFF',
            '-DHWY_ENABLE_TESTS=OFF',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DHWY_FORCE_STATIC_LIBS=ON',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]