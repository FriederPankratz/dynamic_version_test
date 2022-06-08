from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake, tools
from conans.tools import os_info
import os


class FooVirtualRunEnvGenerator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(FooVirtualRunEnvGenerator, self).__init__(conanfile)
        self.venv_name = "dynamic_version_test"

    def traact_env_items(self):
        lib_paths = []
        for dep in self.conanfile.deps_cpp_info.deps:
            if (dep.startswith('traact') and (dep != 'traact_core')):
                if self.settings.os == "Windows":
                    lib_paths.extend(self.conanfile.deps_cpp_info[dep].bin_paths)
                else:
                    lib_paths.extend(self.conanfile.deps_cpp_info[dep].lib_paths)

        return lib_paths

    def _add_traact_plugins(self):
        self.env['TRAACT_PLUGIN_PATHS'] = self.traact_env_items()
        return

    @property
    def content(self):
        self._add_traact_plugins()
        return super(FooVirtualRunEnvGenerator, self).content


class FooGeneratorPackage(ConanFile):
    name = "dynamic_version_test"    
    url = "https://github.com/traact/dynamric_version_test.git"
    license = "MIT"
    description = "conan virtual env generator for traact plugin dependencies"

    settings = "os", "compiler", "build_type", "arch"
    compiler = "cppstd"

    def build(self):
        pass

    def set_version(self):
        git = tools.Git(folder=self.recipe_folder)
        self.version = "%s_%s" % (git.get_branch(), git.get_revision())
        print(self.version)
        print("---------------------------")

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        self.cpp_info.srcdirs = []
