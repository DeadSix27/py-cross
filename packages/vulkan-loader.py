from packages.base_package import BasePackage

class VULKAN_LOADER(BasePackage):

    name = "vulkan-loader"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        self.regex_replace = {
            'post_install': [
                {
                    0: r'(?:[^\r\n]+)?libdir=(?:[^\r\n]+)?',
                    'in_file': '{pkg_config_path}/vulkan.pc',
                    # 'out_file': '{pkg_config_path}/vulkan.pc'
                },
                {
                    0: r'exec_prefix=([^\r\n]+)',
                    1: r'exec_prefix=\1\nlibdir=${{exec_prefix}}/lib\n',
                    'in_file': '{pkg_config_path}/vulkan.pc',
                    # 'out_file': '{pkg_config_path}/vulkan.pc'
                },
                {
                    0: r'-lvulkan-1.dll$',
                    1: r'-l:libvulkan-1.dll.a',
                    'in_file': '{pkg_config_path}/vulkan.pc',
                    # 'out_file': '{pkg_config_path}/vulkan.pc'
                },
	    	]
        }

    @property
    def pkg_depends(self):
        return ("vulkan-headers", )
    
    @property
    def pkg_url(self):
        return "https://github.com/KhronosGroup/Vulkan-Loader.git"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
		    # '-DUPDATE_DEPS=ON',
            '-DBUILD_TESTS=OFF',
		    '-DUSE_MASM=OFF',
            '-DBUILD_STATIC_LOADER=ON',
            '-DENABLE_WERROR=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]