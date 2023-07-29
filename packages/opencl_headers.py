from packages.base_package import BasePackage

class opencl_headers(BasePackage):

    name = "opencl_headers"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        # self.git_tag = "v1.3.0" #todo

    @property
    def pkg_depends(self):
        return []
    
    @property
    def pkg_url(self):
        return "https://github.com/KhronosGroup/OpenCL-Headers.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DOPENCL_HEADERS_BUILD_CXX_TESTS=OFF',
            '-DOPENCL_HEADERS_BUILD_TESTING=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]