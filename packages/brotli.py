from packages.base_package import BasePackage

class BROTLI(BasePackage):

    name = "brotli"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.CMake
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        self.regex_replace = {
			"post_download": [
				{
					0: r"#if defined\(BROTLI_SHARED_COMPILATION\)",
					1: r"#if defined(_MSVC)",
					"in_file": "c/include/brotli/port.h",
				},
			]
		}

    @property
    def pkg_depends(self):
        return ( )
    
    @property
    def pkg_url(self):
        return "https://github.com/google/brotli"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{cmake_prefix_options}',
            '-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DBROTLI_EMSCRIPTEN=OFF',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]