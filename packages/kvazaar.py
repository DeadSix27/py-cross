from packages.base_package import BasePackage

class KVAZAAR(BasePackage): #todo fix by adding -DKVZ_STATIC_LIB to pkgconfig

    name = "kvazaar"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
        # self.runAutogenInSubSource = True
    
        # self.source_subfolder = "build/linux"
        self.autoconf_command = [ "./configure" ]
        self.make_command = [ "make", "V=1" ]

        # self.patches = [
            # { 'file': 'kvazaar/0001-mingw-workaround.patch' },
        # ]


        # self.regex_replace = {
        #     "post_patch": [
		# 		{
		# 			0: r"cygwin\*\|msys\*\|mingw\*",
		# 			1: r"cygwin*|msys*",
		# 			"in_file": "configure.ac",
		# 		},
        #         {
		# 			0: r'LDFLAGS=\"\$LDFLAGS -Wl,-z,noexecstack\"',
		# 			1: r'LDFLAGS="$LDFLAGS"',
		# 			"in_file": "configure.ac",
		# 		},
            # ],
        # }


    def pkg_post_regex_replace_cmd(self):
        self.compiler.runProcess(["./autogen.sh"])

    @property
    def pkg_depends(self):
        return ( )

    @property
    def pkg_url(self):
        return "https://github.com/ultravideo/kvazaar"
    
    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            '--enable-asm',
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
            "fancy_name": "kvazaar"
        }
