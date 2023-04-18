from packages.base_package import BasePackage


class lzo(BasePackage):
	name = "lzo"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Archive
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"

	@property
	def pkg_depends(self):
		return []

	@property
	def pkg_mirrors(self):
		return [
			{ 'url' : 'http://www.oberhumer.com/opensource/lzo/download/lzo-2.10.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'c0f892943208266f9b6543b3ae308fab6284c5c90e627931446fb49b4221a072' }, ], },
		]

	@property
	def pkg_config(self):
		return (
			"..",
			"{cmake_prefix_options}",
			"-DCMAKE_INSTALL_PREFIX={target_prefix}",
			"-DBUILD_SHARED_LIBS=OFF",
			"-DENABLE_SHARED=OFF",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]

