from setuptools import setup

setup(
    name='tag_counter',
    version='0.1',
    packages=['', 'tk', 'event', 'model', 'console', 'resources'],
    package_dir={'': 'tagcounter'},
    url='https://github.com/theconst/tag_counter',
    license='MIT',
    author='kko',
    install_requires=[
        'pyaml>3.13',
        'sqlalchemy>1.2',
        'matplotlib==2.2.3',
        'validators>0.12',
    ],
    author_email='theconst@users.noreply.github.com',
    description='Simple application demo of tag_counting'
)
