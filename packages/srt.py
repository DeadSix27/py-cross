from packages.base_package import BasePackage

class srt(BasePackage):

	name = "srt"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.CMake
		self.build_system = BasePackage.BuildSystem.Ninja
		self.install_system = BasePackage.BuildSystem.Ninja
		self.source_subfolder = "_build"
		# self.git_tag = "v1.5.1" #todo

	@property
	def pkg_depends(self):
		return [
			"openssl",
			# "libressl"
	    ]

	@property
	def pkg_url(self) -> str:
		return  'https://github.com/Haivision/srt.git'

	@property
	def pkg_config(self):
		return (
			'..',
			'{cmake_prefix_options}',
			'-DCMAKE_INSTALL_PREFIX={target_prefix}',
			'-DBUILD_SHARED_LIBS=OFF',
			'-DENABLE_STATIC=ON',
			'-DUSE_STATIC_LIBSTDCXX=ON',
			# '-DUSE_ENCLIB=gnutls ',
			'-DUSE_ENCLIB=openssl ',
			'-DOPENSSL_USE_STATIC_LIBS=ON',
			'-DUSE_OPENSSL_PC=OFF',
			'-DENABLE_SHARED=OFF',
			'-DENABLE_APPS=OFF',
			)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ["install"]