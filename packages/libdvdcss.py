
from packages.base_package import BasePackage


class libdvdcss(BasePackage):
	name = "libdvdcss"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

	@property
	def pkg_depends(self):
		return []

	@property
	def pkg_url(self) -> str:
		return "https://code.videolan.org/videolan/libdvdcss.git"

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
		return {"version": "git (master)", "fancy_name": "libdvdcss"}