from pybuilder.core import init, use_plugin


@init
def initialize(project):
    project.set_property("run_unit_tests_propagate_stdout", True)
    project.set_property("run_unit_tests_propagate_stderr", True)
    project.set_property('verbose', True)


use_plugin("exec")
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin('python.install_dependencies')
use_plugin("python.flake8")
use_plugin("python.coverage")
# use_plugin('python.integrationtest')

default_task = ['clean']