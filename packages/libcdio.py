from packages.base_package import BasePackage

class libcdio(BasePackage):

	name = "libcdio"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make

		self.autogen_only_reconf = True

		# self.source_subfolder = "build/linux"
		self.autoconf_command = ["./configure"]
		
	def post_download_commands(self):
		self.compiler.runProcess(['touch', 'doc/version.texi'])
		self.compiler.runProcess(['touch', 'src/cd-info.1', 'src/cd-drive.1', 'src/iso-read.1', 'src/iso-info.1', 'src/cd-read.1'])

	@property
	def pkg_depends(self):
		return ( )

	@property
	def pkg_url(self):
		return 'https://git.savannah.gnu.org/git/libcdio.git'

	@property
	def pkg_config(self):
		return (
			'{autoconf_prefix_options}',
			'--build=x86_64-pc-linux-gnu',
			# '--cross-prefix={mingw_prefix_dash}',
			# '--disable-cddb',
			# '--enable-cpp-progs',
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install",)

	@property
	def pkg_info(self):
		return {
			"version": "git (master)",
			"fancy_name": "libcdio"
		}