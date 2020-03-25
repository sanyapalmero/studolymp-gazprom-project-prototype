from fabric import task


@task
def push_images(c):
    c.local("docker build . -f Dockerfile.backend -t registry.gitlab.com/sanyapalmero/studolymp/backend")
    c.local("docker push registry.gitlab.com/sanyapalmero/studolymp/backend")

    c.local("docker build . -f Dockerfile.frontend -t registry.gitlab.com/sanyapalmero/studolymp/frontend")
    c.local("docker push registry.gitlab.com/sanyapalmero/studolymp/frontend")


@task
def upgrade(c):
    push_images(c)

    with c.cd("~/studolymp"):
        # Pull updated images
        c.run("docker-compose pull")

        # Stop app containers
        c.run("docker-compose stop backend frontend")

        # Run the migrations
        c.run("docker-compose run --rm backend python manage.py migrate")

        # Remove the containers and temporary static files volume
        c.run("docker-compose rm -fv backend frontend")
        c.run("docker volume rm -f studolymp_static")

        # Recreate app containers
        c.run("docker-compose up -d")
