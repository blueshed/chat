""" our dev tasks """
from invoke import task
import webbrowser


@task(help={'debug': 'run in hot-reload mode'})
def server(ctx, debug=False):
    """ run our python server """
    ctx.run(f'python -m chat.main --debug={debug}')


@task
def client(ctx):
    """ run our vite server """
    ctx.run('. nenv/bin/activate && cd client && npm run dev')


@task
def build(ctx):
    """ build our vue client """
    ctx.run('. nenv/bin/activate && cd client && npm run build')


@task
def lint(ctx):
    """ run axblack and pylint """
    ctx.run('black chat')
    ctx.run('pylint chat')


@task
def test(ctx):
    """ run our tests """
    ctx.run('pytest')


@task
def docs_build(ctx):
    """ build docs """
    ctx.run('cd docsrc && make github')
    ctx.run('touch ./docs/.nojekll')


@task
def docs_server(ctx, port='8081'):
    """ run a server for the documents """
    url = f'http://localhost:{port}'
    print(f'doc-server at: {url}')
    webbrowser.open(url)
    ctx.run(
        f'python3 -m http.server {port} --directory=./docsrc/_build/html/',
        pty=True,
    )


@task
def cheatsheet(_):
    """ open the github rst-cheatsheet """
    webbrowser.open(
        'https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst'
    )


@task(pre=[lint, build, test, docs_build])
def docker(ctx):
    """ build & run our docker server """
    ctx.run('docker-compose build')
    ctx.run('docker-compose up')
