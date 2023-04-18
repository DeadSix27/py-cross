from packages.base_package import BasePackage


class mujs(BasePackage):
    name = "mujs"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Git
        self.conf_system = BasePackage.ConfSystem.Ignore
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make
        self.regex_replace = {
            "post_download": [
                {
                    0: r"default\: build\/release\/mujs build\/release\/mujs\-pp",
                    1: r"default: build/release/mujs build/release/mujs-pp",
                    "in_file": "Makefile",
                },
                {
                    0: r"install \-m 755 build\/release\/mujs-pp \$\(DESTDIR\)\$\(bindir\)",
                    1: r"install -m 755 build/release/mujs-pp.exe $(DESTDIR)$(bindir) ",
                    "in_file": "Makefile",
                },
                {
                    0: r"install \-m 755 build\/release\/mujs \$\(DESTDIR\)\$\(bindir\)",
                    1: r"install -m 755 build/release/mujs.exe $(DESTDIR)$(bindir) ",
                    "in_file": "Makefile",
                },
                {
                    0: r"-DHAVE_READLINE -lreadline",
                    1: r"",
                    "in_file": "Makefile",
                },
            ],
            "post_install": [  # hardcode version because master builds use hashes and mpv checks for actual version, could probably edit the git describe command in the Makefile, but this will do.
                {
                    0: r"^Version:([\n\r\s]+)?[^\n]+$",
                    1: r"Version: 1.0.6",
                    "in_file": "{pkg_config_path}/mujs.pc",
                },
            ],
        }

    @property
    def pkg_depends(self):
        return ["readline"]

    @property
    def pkg_url(self):
        return "git://git.ghostscript.com/mujs.git"

    @property
    def pkg_config(self):
        return ["dlfcn-win32"]

    @property
    def pkg_build(self):
        return [
           "{make_prefix_options}",
           "prefix={target_prefix}",
           "HAVE_READLINE=no",
        ]

    @property
    def pkg_install(self):
        return [
            "install",
            "{make_prefix_options}",
            "prefix={target_prefix}",
            "HAVE_READLINE=no",
        ]

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "mujs"}
