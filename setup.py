#encoding:UTF-8

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()



setup(
    name = "redisScrapy",
    version = "0.1",
    packages = find_packages(),
    
    entry_points = {
        'console_scripts': [
            'redisScrapy = redisScrapy.main',
            'redisScrapy_main = redisScrapy.main',
        ],
        #'setuptools.installation': [
            #'eggsecutable = src.RedisScrapy.main',
        #]
    },
    
    install_requires=['jieba>=0.38', 
                      'selenium>=3.3.1'],
)