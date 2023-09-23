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
        self.git_recursive = False

    @property
    def pkg_depends(self):
        return ( 'fast_float', 'glad', 'xxhash', 'lcms2', 'libdovi', 'libepoxy', 'spirv-tools', 'glslang', 'shaderc', 'vulkan-loader' )
    
    def pkg_post_download_commands(self):
        self.path.joinpath("3rdparty/fast_float").rmdir()
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("fast_float", True),
            self.path.joinpath("3rdparty/fast_float"),
        )
        self.path.joinpath("3rdparty/glad").rmdir()
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("glad", True),
            self.path.joinpath("3rdparty/glad"),
        )
        self.path.joinpath("3rdparty/Vulkan-Headers").rmdir()
        self.compiler.createSymlink(
            self.compiler.getPackagePathByName("vulkan-headers", True),
            self.path.joinpath("3rdparty/Vulkan-Headers"),
        )
    
    
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