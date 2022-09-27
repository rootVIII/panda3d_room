from setuptools import setup

pkgs = ['components']

setup(
    name='panda3d_room',
    packages=pkgs,
    options={
        'build_apps': {
            'gui_apps': {
                'panda3d_room': 'main.py',
            },
            'log_filename': 'panda3d_room.log',
            'log_append': False,
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.bam',
            ],
            'plugins': [
                'pandagl',
            ],
            'platforms': ['win_amd64'],
            'include_modules': {'*': 'panda3d-gltf'},
        }
    }
)
