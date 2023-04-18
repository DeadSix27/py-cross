
from packages.base_package import BasePackage


class libdvdread(BasePackage):
	name = "libdvdread"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

		self.regex_replace = {
            "post_install": [
                {
                    0: r"Libs: -L\${libdir} -ldvdread\n",
                    1: r"Libs: -L${libdir} -ldvdread -ldvdcss\n",
                    "in_file": "{pkg_config_path}/dvdread.pc",
                },
            ]
        }

	@property
	def pkg_depends(self):
		return ["libdvdcss"]

	@property
	def pkg_url(self) -> str:
		return "https://code.videolan.org/videolan/libdvdread.git"

	@property
	def pkg_config(self):
		return [
			"{autoconf_prefix_options}",
			"--build=x86_64-pc-linux-gnu",
			"--disable-doc",
		]

	@property
	def pkg_build(self):
		return []
	
	@property
	def pkg_install(self):
		return ["install"]

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "libdvdread"}