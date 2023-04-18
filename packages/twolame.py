
from packages.base_package import BasePackage


class twolame(BasePackage):
	name = "twolame"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

		
		self.autoconf_command = ["./autogen.sh"]
		
		self.autogen = False

		self.patches = [
			{"file": 'twolame/0001-twolame-mingw-workaround.patch'},
			{"file": "twolame/0002-only-build-lib.patch"}
		]

	@property
	def pkg_depends(self):
		return ()

	@property
	def pkg_url(self) -> str:
		return "https://github.com/njh/twolame/"

	@property
	def pkg_config(self):
		return (
			"{autoconf_prefix_options}",
			"--build=x86_64-pc-linux-gnu",
			"--disable-maintainer-mode",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install",)

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "twolame"}