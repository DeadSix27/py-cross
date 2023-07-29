from packages.base_package import BasePackage

class opencl_icd(BasePackage):

    name = "opencl_icd"

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
        return [ 'opencl_headers' ]
    
    @property
    def pkg_url(self):
        return "https://github.com/KhronosGroup/OpenCL-ICD-Loader.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DOPENCL_ICD_LOADER_HEADERS_DIR={target_prefix}/include',
            '-DBUILD_SHARED_LIBS=ON',
            '-DCMAKE_STATIC_LIBRARY_PREFIX=',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]