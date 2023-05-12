from packages.base_package import BasePackage
import shutil

class ICU4CLOCAL(BasePackage):

    name = "icu4c_local"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
        self.runAutogenInSubSource = True
        self.git_tag = "release-73-rc"
        
        self.source_subfolder = "icu4c/source"
       
        # self.patches = [
        #     { 'file': 'icu.patch' },
        # ]

    @property
    def pkg_depends(self):
        return ( )

    @property
    def pkg_url(self):
        return "https://github.com/unicode-org/icu"
    
    @property
    def pkg_env(self):
        return {
            'STATIC_PREFIX_WHEN_USED': "",
            'STATIC_PREFIX': "",
        }
    
    
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
    def pkg_config(self):
        return (
            '--disable-shared',
            '--enable-static',
            # '--disable-tools',
            '--disable-tests',
            '--disable-samples',
            '--prefix=' + str(self.path),
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
            "fancy_name": "icu4c_local"
        }