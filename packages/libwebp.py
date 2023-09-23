from packages.base_package import BasePackage

class LIBWEBP(BasePackage):

    name = "libwebp"

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
        return ( "zlib-ng", ) 
    
    @property
    def pkg_url(self):
        return "https://github.com/webmproject/libwebp.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
            '-DBUILD_SHARED_LIBS=OFF',
            '-DWEBP_LINK_STATIC=ON',
            '-DWEBP_BUILD_CWEBP=OFF',
            '-DWEBP_BUILD_DWEBP=OFF', 
            '-DWEBP_BUILD_GIF2WEBP=OFF', 
            '-DWEBP_BUILD_IMG2WEBP=OFF', 
            '-DWEBP_BUILD_VWEBP=OFF', 
            '-DWEBP_BUILD_WEBPINFO=OFF', 
            '-DWEBP_BUILD_WEBPMUX=OFF', 
            '-DWEBP_BUILD_EXTRAS=OFF', 
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]