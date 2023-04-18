from packages.base_package import BasePackage

class OPENH264(BasePackage):

    name = "openh264"

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
					0: r"Libs: -L\${libdir} -lopenh264 -pthread -lm\n",
					1: r"Libs: -L${libdir} -lopenh264 -pthread -lm -lstdc++\n",
					"in_file": "{pkg_config_path}/openh264.pc",
				},
			]
		}

    @property
    def pkg_depends(self):
        return (  )
    
    @property
    def pkg_url(self):
        return "https://github.com/cisco/openh264"
    
    @property
    def pkg_config(self):
        return (
            '..',
            '--prefix={target_prefix}',
            '--cross-file={meson_env_file}',
            '--default-library=static',
            '-Dtests=disabled',
            )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ["install"]