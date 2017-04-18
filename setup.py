from setuptools import setup

setup(name='barbell',
      description='''
                    A tool for modeling environments and agents
                    for reinforcement learning simulations''',
      version='0.0.1',
      url='https://github.com/henriqdp/barbell',
      author='Henrique Lopes',
      author_email='hplopes@ainf.ufrgs.br',
      license='GPL',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3'
      ],
      packages=['barbell'],
      install_requires=[
          'PyYAML>=3.11',
          'gym'
      ]
)
