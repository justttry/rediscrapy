#encoding:UTF-8

from setuptools import setup, find_packages

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
    }
)