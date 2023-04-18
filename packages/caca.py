from packages.base_package import BasePackage

class CACA(BasePackage):

    name = "caca"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
    
        self.source_subfolder = "_build"

        self.autoconf_command = ["../configure"]

        self.regex_replace = {
            "post_patch": [
                {
                    0: r"SUBDIRS = . t",
                    1: r"SUBDIRS = .",
                    "in_file": "caca/Makefile.am", 
                },
                {
                    0: r"int vsnprintf",
                    1: r"int vnsprintf_disabled",
                    "in_file": "caca/string.c", 
                },
                {
                    0: r"int vsnprintf",
                    1: r"int vnsprintf_disabled",
                    "in_file": "caca/figfont.c", 
                },                
                {
                    0: r"__declspec\(dllexport\)",
                    1: r"",
                    "in_file": "cxx/caca++.h", 
                },
                
                {
                    0: r"__declspec\(dllexport\)",
                    1: r"",
                    "in_file": "caca/caca.h", 
                },
                
                {
                    0: r"__declspec\(dllexport\)",
                    1: r"",
                    "in_file": "caca/caca0.h", 
                },
                
                {
                    0: r"__declspec\(dllimport\)",
                    1: r"",
                    "in_file": "caca/caca.h", 
                },
                {
                    0: r"__declspec\(dllimport\)",
                    1: r"",
                    "in_file": "caca/caca0.h", 
                },
            ],
        }

    @property
    def pkg_depends(self):
        return ( )
    
    def pkg_post_regex_replace_cmd(self):
        self.compiler.runProcess(["autoreconf", "-fiv"])
    
    @property
    def pkg_url(self):
        return "https://github.com/cacalabs/libcaca.git"
    
    @property
    def pkg_config(self):
        return (
            '{autoconf_prefix_options}',
            '--build=x86_64-pc-linux-gnu',
            '--disable-cxx',
            '--disable-csharp',
            '--disable-java',
            '--disable-python',
            '--disable-ruby',
            '--disable-imlib2',
            '--disable-doc',
            '--disable-examples',
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
            "fancy_name": "caca"
        }



# {
# 	'repo_type' : 'git',
# 	'url' : 'https://github.com/cacalabs/libcaca.git',
# 	'branch': 'main',
# 	#'custom_cflag' : '-O3',
# 	'run_post_configure' : [
# 		'sed -i.bak "s/int vsnprintf/int vnsprintf_disabled/" "caca/string.c"',
# 		'sed -i.bak "s/int vsnprintf/int vnsprintf_disabled/" "caca/figfont.c"',
# 		'sed -i.bak "s/__declspec(dllexport)//g" cxx/caca++.h',
# 		'sed -i.bak "s/__declspec(dllexport)//g" caca/caca.h',
# 		'sed -i.bak "s/__declspec(dllexport)//g" caca/caca0.h',
# 		'sed -i.bak "s/__declspec(dllimport)//g" caca/caca.h',
# 		'sed -i.bak "s/__declspec(dllimport)//g" caca/caca0.h',
# 	],
# 	'run_post_install' : [
# 		"sed -i.bak 's/-lcaca *$/-lcaca -lz/' \"{pkg_config_path}/caca.pc\"",
# 	],
# 	'configure_options' : '{autoconf_prefix_options} --libdir={target_prefix}/lib --disable-cxx --disable-csharp --disable-java --disable-python --disable-ruby --disable-imlib2 --disable-doc --disable-examples',
# 	'_info' : { 'version' : None, 'fancy_name' : 'libcaca' },
# }