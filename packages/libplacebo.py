from packages.base_package import BasePackage

class LIBPLACEBO(BasePackage): 

    name = "libplacebo"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"
        self.patches = [
            {"file": "https://github.com/haasn/libplacebo/compare/master...DeadSix27:libplacebo:patch-1.patch"},
            
        ]

    @property
    def pkg_depends(self):
        return ( 'lcms2', 'libdovi', 'libepoxy', 'spirv-tools', 'glslang', 'shaderc', 'vulkan-loader' )
    
    @property
    def pkg_url(self):
        return "https://code.videolan.org/videolan/libplacebo"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            '-Dvulkan=enabled',
            '-Dvulkan-registry={target_prefix}/share/vulkan/registry/vk.xml',
            '-Dglslang=enabled',
            '-Dshaderc=enabled',
            '-Dlcms=enabled',
            '-Ddovi=enabled',
            '-Dlibdovi=enabled',
            '-Ddemos=false',
            '-Dtests=false',
            '-Dbench=false',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]