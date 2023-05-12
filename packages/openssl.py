from packages.base_package import BasePackage


class openssl(BasePackage):
	name = "openssl"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Autoconf
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make
		self.autoconf_command = [ "./Configure" ]
		self.make_install_command = ["make", "install_sw"]
		# self.git_tag = "v3.7.1"
		# self.regex_replace = {
		# 	"post_install": [
		# 		{
		# 			0: r"Libs.private:  -lws2_32 -lbcrypt\n",
		# 			1: r"Libs.private:  -lws2_32 -lbcrypt -ltls\n",
		# 			"in_file": "{pkg_config_path}/libcrypto.pc",
		# 		},
		# 	]
		# }

	@property
	def pkg_depends(self):
		return ()

	@property
	def pkg_url(self) -> str:
		return "https://github.com/openssl/openssl"

	@property
	def pkg_config(self):
		return (
			"mingw64",
            "--cross-compile-prefix={mingw_prefix_dash}",
			"-static",
            "--prefix={target_prefix}",
            "--openssldir={target_prefix}",
	        "--libdir=lib",
		)

	@property
	def pkg_build(self):
		return ()

	@property
	def pkg_install(self):
		return ("install",)

	@property
	def pkg_info(self):
		return {"version": "git (master)", "fancy_name": "openssl"}