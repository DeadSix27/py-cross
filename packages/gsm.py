from packages.base_package import BasePackage

class GSM(BasePackage):

	name = "gsm"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Archive
		self.conf_system = BasePackage.ConfSystem.Ignore
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Ignore

		self.make_command = (
	    	"make",
			"AR={mingw_prefix_dash}ar",
            "PREFIX={target_prefix}",
            "RANLIB={mingw_prefix_dash}ranlib",
            "LD={mingw_prefix_dash}ld",
            "STRIP={mingw_prefix_dash}strip",
            "CXX={mingw_prefix_dash}g++",
            "CC={mingw_prefix_dash}gcc",
	    	"CCFLAGS=-c -Ofast -DNeedFunctionPrototypes=1 -Wall -Wno-comment",
		)

		# self.runAutogenInSubSource = True
	
		# self.source_subfolder = "build/linux"
		self.autoconf_command = ["./configure"]


		self.patches = [
			{ 'file': 'gsm/gsm-1.0.16.patch', "cmd": "patch -p0" },
			{ 'file': 'gsm/gsm-1.0.16_Makefile.patch', "cmd": "patch -p0" },
		]

	@property
	def pkg_depends(self):
		return ( )

	# @property
	# def pkg_env(self):
	# 	return {
	# 		"AR": "{mingw_prefix_dash}ar",
    #         "PREFIX": "{target_prefix}",
    #         "RANLIB": "{mingw_prefix_dash}ranlib",
    #         "LD": "{mingw_prefix_dash}ld",
    #         "STRIP": "{mingw_prefix_dash}strip",
    #         "CXX": "{mingw_prefix_dash}g++",
    #         "CC": "{mingw_prefix_dash}gcc",
	# 	}

	def pkg_post_make_commands(self):
		self.compiler.runProcess(['cp', '-fv', 'lib/libgsm.a', '{target_prefix}/lib'])
		self.compiler.runProcess(['mkdir', '-pv', '{target_prefix}/include/gsm'])
		self.compiler.runProcess(['cp', '-fv', 'inc/gsm.h', '{target_prefix}/include/gsm'])

	@property
	def pkg_mirrors(self):
		return [
			{
				"url": "https://www.quut.com/gsm/gsm-1.0.22.tar.gz",
				"hashes": [
					{
						"type": "sha256",
						"sum": "f0072e91f6bb85a878b2f6dbf4a0b7c850c4deb8049d554c65340b3bf69df0ac",
					},
				],
			}
		]

	# @property
	# def pkg_build(self):
	# 	return (
	# 		"AR={mingw_prefix_dash}ar",
    #         "PREFIX={target_prefix}",
    #         "RANLIB={mingw_prefix_dash}ranlib",
    #         "LD={mingw_prefix_dash}ld",
    #         "STRIP={mingw_prefix_dash}strip",
    #         "CXX={mingw_prefix_dash}g++",
	# 	)

	@property
	def pkg_info(self):
		return {
			"version": "git (master)",
			"fancy_name": "gsm"
		}