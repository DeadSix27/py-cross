

from packages.base_package import BasePackage


class libdvdnav(BasePackage):
	name = "libdvdnav"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

		# self.regex_replace = {
        #     "post_install": [
        #         {
        #             0: r"-ldvdread -ldvdcss",
        #             1: r"if(NOT APPLE)",
        #             "in_file": "",
        #         },
        #     ]
        # }

	@property
	def pkg_depends(self):
		return ["libdvdread"]

	@property
	def pkg_url(self) -> str:
		return "https://code.videolan.org/videolan/libdvdnav.git"

	@property
	def pkg_config(self):
		return [
			"{autoconf_prefix_options}",
			"--build=x86_64-pc-linux-gnu",
			"--with-libdvdcss",
		]

	@property
	def pkg_build(self):
		return []
	
	@property
	def pkg_install(self):
		return ["install"]

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "libdvdnav"}