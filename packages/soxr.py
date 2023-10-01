from packages.base_package import BasePackage

class soxr(BasePackage):

	name = "soxr"

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
		return ()

	@property
	def pkg_mirrors(self):
		return [
			{
				"url": "https://download.videolan.org/contrib/soxr/soxr-0.1.3-Source.tar.xz",
				"hashes": [
					{
						"type": "sha256",
						"sum": "b111c15fdc8c029989330ff559184198c161100a59312f5dc19ddeb9b5a15889",
					},
				],
			},
		]

	@property
	def pkg_config(self):
		return (
			'..',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DWITH_LSR_BINDINGS=OFF',
			'-DBUILD_LSR_TESTS=OFF',
			'-DBUILD_EXAMPLES=OFF',
			'-DBUILD_TESTS=OFF',
			'-DCMAKE_AR={toolchain_bin_path_one}/{mingw_prefix_dash}ar',
			)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]