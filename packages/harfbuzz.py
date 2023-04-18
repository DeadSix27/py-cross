from packages.base_package import BasePackage

class HARFBUZZ(BasePackage): #todo: fix stdc++

    name = "harfbuzz"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Meson
        self.build_system = BasePackage.BuildSystem.Ninja
        self.install_system = BasePackage.BuildSystem.Ninja
        self.source_subfolder = "_build"

        self.regex_replace = {
			"post_install": [
				{
					0: r"Libs: -L\${libdir} -lharfbuzz -lm -lusp10 -lgdi32 -lrpcrt4\n",
					1: r"Libs: -L${libdir} -lharfbuzz -lm -lusp10 -lgdi32 -lrpcrt4 -lstdc++\n",
					"in_file": "{pkg_config_path}/harfbuzz.pc",
				},
			]
		}

    @property
    def pkg_depends(self):
        return ["brotli"]
    
    @property
    def pkg_url(self):
        return "https://github.com/harfbuzz/harfbuzz"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '{meson_prefix_options}',
            '--default-library=static',
            '-Dtests=disabled',
            '-Ddocs=disabled',
            '-Ddoc_tests=false',
            '-Dgdi=enabled',
            '-Dfreetype=disabled',
            '-Ddirectwrite=enabled',
            '-Dicu_builtin=false',
            '-Dutilities=disabled',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]