import os.path
from glob import glob


def postBuild(site):
    root = os.path.join(site.paths['build'], 'static/js/')
    os.chdir(root)

    # Delete all existing source maps
    for source_map in glob('*.map'):
        os.unlink(source_map)

    # Compile coffeescript, with source maps
    os.system("coffee --compile --map *.coffee")

    # Minify everything, with source maps
    sources = [js for js in glob('*.js') if not js.endswith('.min.js')]
    for source in sources:
        name, ext = os.path.splitext(source)
        map_path = '%s.map' % name
        command = 'uglifyjs --compress drop_debugger=false --mangle --source-map {map} --screw-ie8 {input} -o {output}'.format(
            map=map_path,
            input=source,
            output='%s.min.js' % name,
        )
        if os.path.exists(map_path):
            command += ' --in-source-map %s' % map_path
        os.system(command)
