from packages.base_package import BasePackage

class mpfr(BasePackage):

	name = "mpfr"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Archive
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make
		# self.source_subfolder = "_build"
		# self.autoconf_command = ["./autogen.sh"]
		
		# self.autogen = False

	@property
	def pkg_depends(self):
		return ()

	@property
	def pkg_mirrors(self):
		return [
			{
				"url": "https://www.mpfr.org/mpfr-current/mpfr-4.2.1.tar.xz",
				"hashes": [
					{
						"type": "sha256",
						"sum": "SKIP",
					},
				],
			},
		]

	@property
	def pkg_config(self):
		return (
				"--host={mingw_prefix}",
				"--prefix={target_prefix}",
				"--disable-shared",
				"--enable-static",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]