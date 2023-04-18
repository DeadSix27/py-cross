from packages.base_package import BasePackage


class theora(BasePackage):
	name = "theora"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

		self.patches = [
			{"file": 'theora/theora_remove_rint_1.2.0alpha1.patch' }
		]


	@property
	def pkg_depends(self):
		return ()

	@property
	def pkg_url(self) -> str:
		return "https://github.com/xiph/theora.git"

	@property
	def pkg_config(self):
		return (
			"{autoconf_prefix_options}",
			"--build=x86_64-pc-linux-gnu",
			"--disable-doc",
			"--disable-spec",
			"--disable-oggtest",
			"--disable-vorbistest",
			"--disable-examples",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install",)

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "theora"}