from setuptools import setup
import pip
import os
import sys

try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements

def load_requirements(fname):
    requirements = parse_requirements(os.path.join(os.path.dirname(__file__), fname), session=PipSession())
    return [str(requirement.requirement) for requirement in requirements]

if __name__ == '__main__':
    setup(name='SemanticQuantities',
          version='0.1.0',
          description="""
          A package that provides classes and utilities dealing with physical quantities, their units, uncertainty and bounds.
          """,
          url='git@github.com:andreacortis/SemanticQuantities.git',
          author='Andrea Cortis',
          author_email='andrea.cortis@gmail.com',
          license='MIT',
          packages=['quantities'],
          include_package_data=True,
          zip_safe=False,
          install_requires=load_requirements('requirements.txt')
          )


