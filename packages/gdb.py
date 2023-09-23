
from packages.base_package import BasePackage


class gdb(BasePackage):
	name = "gdb"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

	@property
	def pkg_depends(self):
		return ["gmp", "mpfr"]

	@property
	def pkg_url(self) -> str:
		return "https://sourceware.org/git/binutils-gdb.git"

	@property
	def pkg_config(self):
		return (
				"--host={mingw_prefix}",
			   "--prefix={install_path}/mpv",
				"--disable-shared",
				"--enable-static",
				"--disable-werror",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install",]

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "twolame"}