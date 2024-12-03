from setuptools import setup

package_name = 'uwb_soccer_v'

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
    maintainer='coastz',
    maintainer_email='1310518371@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'uwb_soccer_v = uwb_soccer_v.uwb_soccer_v:main',
        ],
    },
)
