from setuptools import setup

package_name = 'quadro'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='computer',
    maintainer_email='computer@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'main = quadro.main:main',
            'connect = quadro.connect:main',
            'camera = quadro.camera:main',
            'controller = quadro.controller:main',
            'coder = quadro.coder:main',
            'decoder = quadro.decoder:main'
        ],
    },
)
