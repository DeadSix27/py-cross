from packages.base_package import BasePackage

class OPENMPT(BasePackage):

	name = "openmpt"

	def __init__(self, compiler):
		self.compiler = compiler
		self.type = BasePackage.PackageType.Dependecy
		self.source_type = BasePackage.SourceType.Git
		self.conf_system = BasePackage.ConfSystem.Ignore
		self.build_system = BasePackage.BuildSystem.Make
		self.install_system = BasePackage.BuildSystem.Make
		self.git_tag = "libopenmpt-0.6.10"

		self.make_command = (
			"make",
			"AR={mingw_prefix_dash}ar",
			"PREFIX={target_prefix}",
			"RANLIB={mingw_prefix_dash}ranlib",
			"LD={mingw_prefix_dash}ld",
			"STRIP={mingw_prefix_dash}strip",
			"CXX={mingw_prefix_dash}g++",
			"CC={mingw_prefix_dash}gcc",
			"CONFIG=mingw-w64",
			"OPTIMIZE=vectorize",
			"OPENMPT123=0",
			"VERBOSE=1",
			"TEST=0",
			"SHARED_LIB=0",
			"SHARED_SONAME=0",
			"DYNLINK=0",
			"STATIC_LIB=1",
			"EXAMPLES=0",
			"MODERN=1",
		)
		
		self.make_install_command = (
            "make",
	    	"install",
            "AR={mingw_prefix_dash}ar",
            "PREFIX={target_prefix}",
            "RANLIB={mingw_prefix_dash}ranlib",
            "LD={mingw_prefix_dash}ld",
            "STRIP={mingw_prefix_dash}strip",
            "CXX={mingw_prefix_dash}g++",
            "CC={mingw_prefix_dash}gcc",
            "CONFIG=mingw-w64",
            "OPTIMIZE=vectorize",
            "OPENMPT123=0",
            "VERBOSE=1",
            "TEST=0",
            "SHARED_LIB=0",
            "SHARED_SONAME=0",
            "DYNLINK=0",
            "STATIC_LIB=1",
            "EXAMPLES=0",
            "MODERN=1",
        )
		# self.runAutogenInSubSource = True
	
		# self.source_subfolder = "build/linux"
		self.autoconf_command = ["./configure"]


	@property
	def pkg_depends(self):
		return ( )

	# @property
	# def pkg_env(self):
	# 	return {
	# 		"AR": "{mingw_prefix_dash}ar",
	#		 "PREFIX": "{target_prefix}",
	#		 "RANLIB": "{mingw_prefix_dash}ranlib",
	#		 "LD": "{mingw_prefix_dash}ld",
	#		 "STRIP": "{mingw_prefix_dash}strip",
	#		 "CXX": "{mingw_prefix_dash}g++",
	#		 "CC": "{mingw_prefix_dash}gcc",
	# 	}

	@property
	def pkg_url(self):
		return "https://github.com/OpenMPT/openmpt.git"

	# @property
	# def pkg_build(self):
	# 	return (
	# 		"AR={mingw_prefix_dash}ar",
	#		 "PREFIX={target_prefix}",
	#		 "RANLIB={mingw_prefix_dash}ranlib",
	#		 "LD={mingw_prefix_dash}ld",
	#		 "STRIP={mingw_prefix_dash}strip",
	#		 "CXX={mingw_prefix_dash}g++",
	# 	)

	@property
	def pkg_info(self):
		return {
			"version": "git (master)",
			"fancy_name": "openmpt"
		}

	@property
	def pkg_install(self):
		return ["install"]