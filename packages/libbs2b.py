from packages.base_package import BasePackage


class LIBBS2B(BasePackage):
    name = "libbs2b"

    def __init__(self, compiler):
        self.compiler = compiler
        self.type = BasePackage.PackageType.Dependecy
        self.source_type = BasePackage.SourceType.Archive
        self.conf_system = BasePackage.ConfSystem.Autoconf
        self.build_system = BasePackage.BuildSystem.Make
        self.install_system = BasePackage.BuildSystem.Make

        self.source_subfolder = "_build"

        self.autoconf_command = ["../configure"]

        self.regex_replace = {
            "post_patch": [
                {
                    0: r" dist-lzma",
                    1: r" dist-xz",
                    "in_file": "configure.ac",  # configure.ac:7: error: support for lzma-compressed distribution archives has been removed
                },
                {
                    0: r"\t-lsndfile",
                    "in_file": "src/Makefile.am"},
                {
                    0: r"bs2bconvert_LDFLAGS = \\",
                    1: r"bs2bconvert_LDFLAGS = !CMD(pkg-config --static sndfile --libs-only-l)CMD!\n",
                    "in_file": "src/Makefile.am",
                },
            ],
        }

    @property
    def pkg_env(self):
        return {
            "ac_cv_func_malloc_0_nonnull": "yes",
            "CFLAGS" : "-DFLAC__NO_DLL",
            }

    def pkg_post_regex_replace_cmd(self):
        self.compiler.runProcess(["autoreconf", "-fiv"])

    @property
    def pkg_depends(self):
        return ("libsndfile",)

    @property
    def pkg_mirrors(self):
        return [
            {
                "url": "https://sourceforge.net/projects/bs2b/files/libbs2b/3.1.0/libbs2b-3.1.0.tar.bz2",
                "hashes": [
                    {
                        "type": "sha1",
                        "sum": "353180e0f260b074508c6ddb34259b0d08a12dd7",
                    },
                ],
            },
        ]

    @property
    def pkg_config(self):
        return (
            "{autoconf_prefix_options}",
            "--build=x86_64-pc-linux-gnu",
        )

    @property
    def pkg_build(self):
        return ()

    @property
    def pkg_install(self):
        return ("install",)

    @property
    def pkg_info(self):
        return {"version": "git (master)", "fancy_name": "libass"}
