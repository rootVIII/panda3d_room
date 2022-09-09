from setuptools import setup

setup(
    name='panda3d_room',
    options={
        'build_apps': {
            'gui_apps': {
                'panda3d_test': 'main.py',
            },
            'log_filename': 'panda3d_test.log',
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