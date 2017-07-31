# download-manifest.py

This is a simple script to download manifests from Docker hub. It is done via this v2 registry API call:

```
/v2/{repository}/manifests/{tag}
```

Sample usage:

```
$ ./download-manifest.py registry
{
  "schemaVersion": 1,
  "fsLayers": [
    {
      "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
    },
    {
      "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
    },
...
```

For more information check [this blog post](http://blog.tomecek.net/post/download-manifests-from-docker-hub/)

# Download manifests from Docker Hub
13 JUNE 2016
So we needed to fetch manifests of repositories from Docker Hub today. It’s not that hard. 30 lines of python can do it. But at the same time, you need to read docs with all the specs.

## Authentication
The biggest pain. pull seems to be a privileged operation which requires authentication. Luckily you only need to obtain a token:

```bash
repo = "library/fedora"
login_template = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
token = requests.get(login_template.format(repository=repo), json=True).json()["token"]
```
This is documented nicely [here](https://docs.docker.com/registry/spec/auth/token/).

API call for getting the manifest
That one is documented over [here](https://docs.docker.com/registry/spec/api/#manifest).

GET /v2/{repository}/manifests/{tag}
Nothing really to talk about: just fetch manifest of requested repository.

```python
get_manifest_template = "https://registry.hub.docker.com/v2/{repository}/manifests/{tag}"
manifest = requests.get(
    get_manifest_template.format(repository=repo, tag=tag),
    headers={"Authorization": "Bearer {}".format(token)},
    json=True
).json()
```

