import shutil
from packages.base_package import BasePackage

class ICU4C(BasePackage):

    name = "icu4c"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
    
        self.runAutogenInSubSource = True
        self.source_subfolder = "icu4c/source"

        self.regex_replace = {
			"post_install": [
				{
					0: r"Libs: -L\${libdir} -licuuc -licudt\n",
					1: r"Libs: -L${libdir} -licuuc -licudt -lstdc++\n",
					"in_file": "{pkg_config_path}/icu-uc.pc",
				},
			]
		}
       
        # self.patches = [
        #     { 'file': 'icu.patch' },
        # ]

    @property
    def pkg_depends(self):
        return ["icu4c_local"]
    
    
    def pkg_post_download_sub_commands(self):
        with open("../../icu4c/source/config/Makefile.inc.in_new", "w") as fnew:
            with open("../../icu4c/source/config/Makefile.inc.in", "r") as f:
                for line in f:
                    if "STATIC_PREFIX = s" in line:
                        line = line.replace("STATIC_PREFIX = s", "STATIC_PREFIX = ")
                    fnew.write(line)
        shutil.move("../../icu4c/source/config/Makefile.inc.in_new", "../../icu4c/source/config/Makefile.inc.in")


        with open("../../icu4c/source/icudefs.mk.in_new", "w") as fnew:
            with open("../../icu4c/source/icudefs.mk.in", "r") as f:
                for line in f:
                    if "STATIC_PREFIX = s" in line:
                        line = line.replace("STATIC_PREFIX = s", "STATIC_PREFIX = ")
                    fnew.write(line)
        shutil.move("../../icu4c/source/icudefs.mk.in_new", "../../icu4c/source/icudefs.mk.in")


        with open("../../icu4c/source/icudefs.mk.in_new", "w") as fnew:
            with open("../../icu4c/source/icudefs.mk.in", "r") as f:
                for line in f:
                    if "STATIC_PREFIX_WHEN_USED = s" in line:
                        line = line.replace("STATIC_PREFIX_WHEN_USED = s", "STATIC_PREFIX_WHEN_USED = ")
                    fnew.write(line)
        shutil.move("../../icu4c/source/icudefs.mk.in_new", "../../icu4c/source/icudefs.mk.in")



    
    @property
    def pkg_env(self):
        return {
            'STATIC_PREFIX_WHEN_USED': "",
            'STATIC_PREFIX': "",
        }

    @property
    def pkg_url(self):
        return "https://github.com/unicode-org/icu"

    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            # '--disable-tools',
            '--disable-tests',
            '--disable-samples',
            '--build=x86_64-pc-linux-gnu',
            '--with-cross-build=' + str(self.compiler.getPackagePathByName("icu4c_local")),
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
            "fancy_name": "icu4c"
        }