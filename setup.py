from setuptools import setup, find_packages


setup(
    name='autoridor',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'Click'
    ],
    entry_points='''
        [console_scripts]
        autoridor=src.autoridor:main  
    '''
)
