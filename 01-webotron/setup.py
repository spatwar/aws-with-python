from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author='Sameer P',
    author_email='s_patwardhan@yahoo.com',
    description='setup tool for buckets and static website',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/spatwar/aws-with-python',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:click
        '''
)
