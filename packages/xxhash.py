from packages.base_package import BasePackage

class XXHASH(BasePackage):

	name = "xxhash"

	def __init__(self, compiler):
		super().__init__(compiler)

		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"

	@property
	def pkg_url(self):
		return "https://github.com/Cyan4973/xxHash.git"

	@property
	def pkg_config(self):
		return (
			'../cmake_unofficial',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DBUILD_STATIC=ON',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DXXHASH_BUILD_XXHSUM=OFF',
		)

	@property
	def pkg_build(self):
		return []

	@property
	def pkg_install(self):
		return ["install"]