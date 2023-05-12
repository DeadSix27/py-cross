from packages.base_package import BasePackage


class pcre2(BasePackage):
	name = "pcre2"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Archive
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja

		self.patches = [
			{"file": "pcre2/0001-pcre2-iswild.patch" },
		]

		self.source_subfolder = "_build"
	@property
	def pkg_mirrors(self):
		return [
			{ 'url' : 'https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.42/pcre2-10.42.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8d36cd8cb6ea2a4c2bb358ff6411b0c788633a2a45dabbf1aeb4b701d1b5e840' }, ], },
			{ 'url' : 'https://fossies.org/linux/misc/pcre2-10.42.tar.bz2 ', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8d36cd8cb6ea2a4c2bb358ff6411b0c788633a2a45dabbf1aeb4b701d1b5e840' }, ], },
			]

	@property
	def pkg_config(self):
		return (
			"..",
			"{cmake_prefix_options}",
			"-DCMAKE_INSTALL_PREFIX={target_prefix}",
			"-DENABLE_STATIC_LIB=ON",
			"-DENABLE_SHARED_LIB=OFF",
			"-DENABLE_LIB_ONLY=ON",
			"-DPCRE2_BUILD_TESTS=OFF",
			"-DPCRE2_BUILD_PCRE2_8=ON",
			"-DPCRE2_BUILD_PCRE2_16=ON",
			"-DPCRE2_BUILD_PCRE2_32=ON",
			"-DPCRE2_NEWLINE=ANYCRLF",
			"-DPCRE2_SUPPORT_UNICODE=ON",
			"-DPCRE2_SUPPORT_JIT=ON",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]